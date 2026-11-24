#!/usr/bin/env python3
"""Run synthetic Neptune Insurance lookup checks via AWS CLI."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
FUNCTION = "NeptuneInsuranceLookup"
REGION = "us-west-2"
FIELDS = {"resultCode", "reference", "status", "product", "requestId"}
CASES = [
    ("claim-owned", "OK", "CLM-1001", "IN_REVIEW"),
    ("voice-claim-owned", "OK", "CLM-1001", "IN_REVIEW"),
    ("voice-claim-unauthorized", "UNAUTHORIZED", "", ""),
    ("policy-owned", "OK", "POL-1001", "ACTIVE"),
    ("claim-not-found", "NOT_FOUND", "", ""),
    ("claim-unauthorized", "UNAUTHORIZED", "", ""),
    ("malformed-reference", "MALFORMED", "", ""),
    ("unexpected-identity", "MALFORMED", "", ""),
]


def run_case(name, expected_code, expected_reference, expected_status, directory):
    fixture = PROJECT / "events" / (name + ".json")
    output = directory / (name + "-response.json")
    if not fixture.is_file():
        raise ValueError("Missing fixture: " + str(fixture))

    invocation = subprocess.run(
        [
            "aws", "lambda", "invoke",
            "--function-name", FUNCTION,
            "--region", REGION,
            "--invocation-type", "RequestResponse",
            "--payload", "fileb://" + str(fixture),
            "--output", "json",
            "--no-cli-pager",
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    if invocation.returncode:
        raise ValueError(invocation.stderr.strip() or "AWS CLI invocation failed")

    metadata = json.loads(invocation.stdout)
    response = json.loads(output.read_text())
    if metadata.get("StatusCode") != 200 or metadata.get("FunctionError"):
        error_type = response.get("errorType", "unknown runtime error")
        raise ValueError("Lambda execution failed: " + error_type)
    if not isinstance(response, dict) or set(response) != FIELDS:
        raise ValueError("Response must contain exactly the five approved fields")
    if not all(isinstance(value, str) for value in response.values()):
        raise ValueError("All response values must be Strings")
    if not response["requestId"].strip():
        raise ValueError("Missing invocation requestId")

    expected = {
        "resultCode": expected_code,
        "reference": expected_reference,
        "status": expected_status,
        "product": "AUTO" if expected_code == "OK" else "",
    }
    for field, value in expected.items():
        if response[field] != value:
            raise ValueError(
                field + ": expected " + repr(value)
                + ", received " + repr(response[field])
            )

    print(
        "PASS " + name + ": " + response["resultCode"]
        + " | requestId=" + response["requestId"],
        flush=True,
    )


def main():
    print("Checking " + FUNCTION + " in " + REGION, flush=True)
    with tempfile.TemporaryDirectory(prefix="neptune-insurance-") as temporary:
        directory = Path(temporary)
        for case in CASES:
            try:
                run_case(*case, directory)
            except (OSError, ValueError, TypeError) as error:
                print("FAIL " + case[0] + ": " + str(error), file=sys.stderr)
                return 1
    print(str(len(CASES)) + "/" + str(len(CASES)) + " lookup checks passed.")
    print("Direct Lambda checks do not verify a live Connect conversation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
