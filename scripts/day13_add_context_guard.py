"""Add the test-only missing-context guard to the existing Day 13 chat copy."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
from datetime import datetime, timezone

TARGET = "Neptune-Day13-Recovery-Chat"
MARKER = "Day13 Version Marker"
CHECK = "Day13 Context Check"
NOTICE = "Day13 Missing Context"
MESSAGE = ("I do not have your claim reference in this new conversation. "
           "Please provide it again when asked, or request a Claims representative.")


def aws(service, operation, *args):
    r = subprocess.run(["aws", service, operation, *args, "--region", "us-west-2",
                        "--output", "json", "--no-cli-pager"],
                       capture_output=True, text=True,
                       env={**os.environ, "AWS_PAGER": "", "AWS_CLI_AUTO_PROMPT": "off"})
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout) if r.stdout.strip() else {}


def patch(source):
    data = copy.deepcopy(source)
    actions = data["Actions"]
    by_id = {a["Identifier"]: a for a in actions}
    if len(by_id) != len(actions) or data["StartAction"] != MARKER:
        raise RuntimeError("Expected a valid flow starting at the A marker.")
    marker = by_id[MARKER]
    if marker["Type"] != "MessageParticipant" or marker["Parameters"].get("Text") != "Neptune Day 13 recovery drill — version A.":
        raise RuntimeError("Expected the published version A marker.")
    if CHECK in by_id or NOTICE in by_id:
        raise RuntimeError("A context block already exists. Stopped to avoid duplicating it.")
    entry = marker["Transitions"]["NextAction"]
    if entry not in by_id or entry == MARKER:
        raise RuntimeError("Marker must lead to the original journey.")
    check = {
        "Identifier": CHECK, "Type": "Compare",
        "Parameters": {"ComparisonValue": "$.Attributes.day13ClaimReference"},
        "Transitions": {
            "NextAction": NOTICE,
            "Conditions": [{"NextAction": entry,
                            "Condition": {"Operator": "Equals", "Operands": ["CLM-1001"]}}],
            "Errors": [{"NextAction": NOTICE, "ErrorType": "NoMatchingCondition"}],
        },
    }
    notice = {
        "Identifier": NOTICE, "Type": "MessageParticipant",
        "Parameters": {"Text": MESSAGE},
        "Transitions": {"NextAction": entry,
                        "Errors": [{"NextAction": entry, "ErrorType": "NoMatchingError"}]},
    }
    marker["Transitions"]["NextAction"] = CHECK
    actions.extend([check, notice])
    metadata = data.setdefault("Metadata", {})
    positions = metadata.setdefault("ActionMetadata", {})
    pos = positions.get(MARKER, {}).get("position", {"x": 0, "y": 300})
    for key, value in positions.items():
        if key != MARKER and isinstance(value.get("position"), dict):
            value["position"]["x"] += 600
    positions[CHECK] = {
        "position": {"x": pos["x"] + 250, "y": pos["y"]}, "isFriendlyName": True,
        "conditions": [], "conditionMetadata": [{
            "id": str(uuid.uuid4()),
            "operator": {"name": "Equals", "value": "Equals", "shortDisplay": "="},
            "value": "CLM-1001",
        }],
    }
    positions[NOTICE] = {"position": {"x": pos["x"] + 500, "y": pos["y"] + 180},
                         "isFriendlyName": True}
    metadata.update({"name": TARGET, "status": "PUBLISHED"})
    metadata.pop("hash", None)
    ids = {a["Identifier"] for a in actions}

    def validate(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "NextAction" and item not in ids:
                    raise RuntimeError("A connection target is missing.")
                validate(item)
        elif isinstance(value, list):
            for item in value:
                validate(item)
    validate(actions)
    return data


def main():
    os.umask(0o077)
    root = Path.home() / "Neptune-Day13-Backups"
    backups = sorted(root.glob("*/recovery-flow-after.json"))
    if not backups:
        raise RuntimeError("The earlier version A backup was not found.")
    saved = json.loads(backups[-1].read_text())
    original_saved = json.loads((backups[-1].parent / "original-flow-before.json").read_text())
    if saved["Name"] != TARGET or original_saved["Name"] != "Neptune-Inbound-Chat":
        raise RuntimeError("Backup flow names do not match the intended resources.")
    arn = saved["Arn"]
    iid = arn.split(":instance/", 1)[1].split("/")[0]
    target_id = arn.split("/contact-flow/", 1)[1].split(":")[0]
    original_id = original_saved["Arn"].split("/contact-flow/", 1)[1].split(":")[0]
    if target_id == original_id or aws("sts", "get-caller-identity")["Account"] != arn.split(":")[4]:
        raise RuntimeError("Account or flow identity mismatch.")

    def describe(fid):
        return aws("connect", "describe-contact-flow", "--instance-id", iid,
                   "--contact-flow-id", fid)["ContactFlow"]
    original = describe(original_id)
    before = describe(target_id)
    if before["Name"] != TARGET or before.get("Status") != "PUBLISHED":
        raise RuntimeError("Expected the published recovery copy.")
    try:
        draft = describe(arn + ":$SAVED")
    except RuntimeError as error:
        if "ResourceNotFoundException" not in str(error):
            raise
        draft = before
    previous_draft = json.loads((backups[-1].parent / "recovery-draft-before.json").read_text())
    draft_actions = json.loads(draft["Content"])["Actions"]
    if (draft_actions != json.loads(before["Content"])["Actions"]
            and draft_actions != json.loads(previous_draft["Content"])["Actions"]):
        raise RuntimeError("An unfamiliar unpublished action change exists; review it first.")
    folder = root / ("context-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    folder.mkdir(parents=True, exist_ok=False)

    def save(name, data):
        path = folder / name
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return path
    save("original-before.json", original)
    save("recovery-before.json", before)
    save("recovery-draft-before.json", draft)
    print("Backups saved:", folder, flush=True)
    updated = patch(json.loads(before["Content"]))
    path = save("recovery-A-with-context.json", updated)
    aws("connect", "update-contact-flow-content", "--instance-id", iid,
        "--contact-flow-id", target_id, "--content", "file://" + str(path))
    after = describe(target_id)
    save("recovery-after.json", after)
    if after.get("Status") != "PUBLISHED" or json.loads(after["Content"])["Actions"] != updated["Actions"]:
        raise RuntimeError("Published content was not confirmed by read-back.")
    if json.loads(describe(original_id)["Content"]) != json.loads(original["Content"]):
        raise RuntimeError("Original content changed during the run; inspect before continuing.")
    print("PASS: context check and recovery message are PUBLISHED.")
    print("PASS: original Neptune-Inbound-Chat content is unchanged.")
    print("Next: test once with empty attributes, then with the synthetic reference.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError, OSError) as error:
        print("STOP:", error, file=sys.stderr)
        sys.exit(1)
