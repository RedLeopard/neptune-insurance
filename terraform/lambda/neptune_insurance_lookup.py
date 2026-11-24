"""Neptune Insurance: read-only lookup of synthetic policy and claim records.

The demonstration customer ID is server-controlled configuration, not real
customer authentication. Replace it with a trusted authenticated identity before
using this handler with actual customer records.
"""

import json
import os
import re
import time

import boto3
from botocore.config import Config


TABLE = boto3.resource(
    "dynamodb",
    config=Config(
        connect_timeout=1,
        read_timeout=1,
        retries={"max_attempts": 0},
    ),
).Table(os.environ.get("TABLE_NAME", "NeptuneInsuranceLab"))

PREFIXES = {"policy": "POL", "claim": "CLM"}
ALLOWED_STATUSES = {
    "policy": {"ACTIVE", "LAPSED"},
    "claim": {"RECEIVED", "IN_REVIEW", "CLOSED"},
}

SMALL_NUMBERS = dict(zip(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(),
    range(20),
))
TENS = dict(zip("twenty thirty forty fifty sixty seventy eighty ninety".split(),
                range(20, 100, 10)))


def _under_hundred(words):
    if len(words) == 1:
        return SMALL_NUMBERS.get(words[0], TENS.get(words[0]))
    if (len(words) == 2 and words[0] in TENS
            and 1 <= SMALL_NUMBERS.get(words[1], -1) <= 9):
        return TENS[words[0]] + SMALL_NUMBERS[words[1]]
    return None


def _under_thousand(words):
    if not words:
        return 0
    if len(words) >= 2 and words[1] == "hundred":
        hundreds = SMALL_NUMBERS.get(words[0], -1)
        if not 1 <= hundreds <= 9:
            return None
        rest = words[2:]
        if rest[:1] == ["and"]:
            rest = rest[1:]
            if not rest:
                return None
        remainder = _under_hundred(rest) if rest else 0
        return None if remainder is None else hundreds * 100 + remainder
    return _under_hundred(words)


def normalize_reference(record_type, reference):
    """Accept one bounded spoken reference; never infer or search for an ID.

    Unrecognized/ambiguous text is returned unchanged for strict validation.
    No customer identity or database lookup is involved in normalization.
    """
    if not isinstance(reference, str) or len(reference) > 160:
        return reference
    prefix = PREFIXES[record_type]
    if re.fullmatch(prefix + r"-[0-9]{4}", reference):
        return reference

    text = reference.strip().lower().replace("\u2019", "'")
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].strip()
    text = re.sub(r"[.!?]$", "", text).strip()
    text = re.sub(r"^(?:it's|it is)\s+", "", text)
    label = "claim" if record_type == "claim" else "policy"
    spoken_prefix = r"\s*".join(prefix.lower())
    match = re.fullmatch(
        r"(?:(?:my|the)\s+)?(?:" + label
        + r"(?:\s+(?:number|reference))?|" + spoken_prefix
        + r")(?:\s+is)?\s*(?:(?:-|dash|hyphen)\s*)?(.+)", text
    )
    if match:
        text = match[1].strip()
    if re.fullmatch(r"[0-9]{4}", text):
        return prefix + "-" + text

    words = text.replace("-", " ").split()
    digits = {word: str(number) for word, number in SMALL_NUMBERS.items()
              if number < 10}
    digits["oh"] = "0"
    if len(words) == 4 and all(word in digits for word in words):
        return prefix + "-" + "".join(digits[word] for word in words)

    if len(words) >= 2 and words[1] == "thousand":
        thousands = SMALL_NUMBERS.get(words[0], -1)
        rest = words[2:]
        if rest[:1] == ["and"]:
            rest = rest[1:]
            if not rest:
                return reference
        remainder = _under_thousand(rest)
        if 1 <= thousands <= 9 and remainder is not None:
            return prefix + "-" + str(thousands * 1000 + remainder)
    return reference


def lambda_handler(event, context):
    """Validate a Connect request and return a flat, sanitized String map."""
    request_id = context.aws_request_id

    def respond(code, reference="", status="", product=""):
        print(json.dumps({"requestId": request_id, "resultCode": code}))
        return {
            "resultCode": code,
            "reference": reference,
            "status": status,
            "product": product,
            "requestId": request_id,
        }

    def malformed(reason, **diagnostic):
        # Temporary diagnostics for synthetic lab calls; never log the full event.
        print(json.dumps({
            "requestId": request_id, "validationFailure": reason, **diagnostic,
        }))
        return respond("MALFORMED")

    if not isinstance(event, dict):
        return malformed("event_not_object")

    details = event.get("Details")
    if not isinstance(details, dict):
        return malformed("details_not_object")

    parameters = details.get("Parameters")
    if not isinstance(parameters, dict):
        return malformed("parameters_not_object")

    if set(parameters) != {"recordType", "reference"}:
        return malformed("parameter_keys", parameterKeys=sorted(str(k)[:80] for k in parameters)[:10])

    record_type = parameters["recordType"]
    reference = parameters["reference"]
    if not isinstance(record_type, str) or record_type not in PREFIXES:
        return malformed("record_type", valueType=type(record_type).__name__, recordType=record_type[:80] if isinstance(record_type, str) else None)

    raw_reference = reference
    reference = normalize_reference(record_type, reference)
    if not isinstance(reference, str) or not re.fullmatch(
        PREFIXES[record_type] + r"-[0-9]{4}", reference
    ):
        return malformed(
            "reference_format", recordType=record_type,
            valueType=type(raw_reference).__name__,
            syntheticReference=raw_reference[:160] if isinstance(raw_reference, str) else None,
        )

    # Only administrator configuration can introduce the bounded test delay.
    try:
        delay = float(os.environ.get("LOOKUP_DELAY_SECONDS", "0"))
        if not 0 <= delay <= 3:
            return respond("UNAVAILABLE")
    except ValueError:
        return respond("UNAVAILABLE")
    time.sleep(delay)

    # A fixed synthetic principal makes ownership behavior testable.
    # Never accept a customer identity chosen by the conversation or model.
    customer_id = os.environ.get("DEMO_CUSTOMER_ID", "")
    if customer_id != "DEMO-1001":
        return respond("UNAUTHORIZED")

    try:
        item = TABLE.get_item(
            Key={"pk": record_type.upper() + "#" + reference},
            ConsistentRead=True,
        ).get("Item")
    except Exception as error:
        print(json.dumps({
            "requestId": request_id,
            "backendErrorType": type(error).__name__,
        }))
        return respond("UNAVAILABLE")

    if not item:
        return respond("NOT_FOUND")

    if item.get("ownerId") != customer_id:
        return respond("UNAUTHORIZED")

    # Validate stored values as well as request inputs.
    status = item.get("status")
    if (
        not isinstance(status, str)
        or status not in ALLOWED_STATUSES[record_type]
        or item.get("product") != "AUTO"
    ):
        return respond("UNAVAILABLE")

    # Build an explicit response; internalNotes and ownerId stay in the backend.
    return respond("OK", reference, status, item["product"])

