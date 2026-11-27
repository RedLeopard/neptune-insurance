"""Publish the Day 13 A marker on the existing isolated chat copy only."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

REGION = "us-west-2"
INSTANCE = "neptune-insurance-lab"
TARGET = "Neptune-Day13-Recovery-Chat"
ORIGINAL = "Neptune-Inbound-Chat"
MARKER = "Day13 Version Marker"
MESSAGE = "Neptune Day 13 recovery drill — version A."
BACKUP_ROOT = Path.home() / "Neptune-Day13-Backups"


def aws(service, operation, *args):
    result = subprocess.run(
        ["aws", service, operation, *args, "--region", REGION,
         "--output", "json", "--no-cli-pager"],
        capture_output=True, text=True,
        env={**os.environ, "AWS_PAGER": "", "AWS_CLI_AUTO_PROMPT": "off"},
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "AWS CLI failed")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def unique(items, key, value):
    matches = [item for item in items if item.get(key) == value]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {value}; found {len(matches)}. Stopped.")
    return matches[0]


def patch(content):
    result = copy.deepcopy(content)
    actions = result["Actions"]
    ids = [a["Identifier"] for a in actions]
    if len(ids) != len(set(ids)) or result["StartAction"] not in ids:
        raise RuntimeError("The existing graph has invalid action identifiers.")
    existing = [a for a in actions if a["Identifier"] == MARKER]
    if existing:
        marker = existing[0]
        if marker["Type"] != "MessageParticipant" or result["StartAction"] != MARKER:
            raise RuntimeError("An unexpected marker configuration exists. Stopped.")
        if marker.get("Parameters", {}).get("Text") != MESSAGE:
            raise RuntimeError("The marker already has different content. Stopped.")
        return result
    entry = result["StartAction"]
    actions.insert(0, {
        "Identifier": MARKER,
        "Type": "MessageParticipant",
        "Parameters": {"Text": MESSAGE},
        "Transitions": {
            "NextAction": entry,
            "Errors": [{"NextAction": entry, "ErrorType": "NoMatchingError"}],
        },
    })
    result["StartAction"] = MARKER
    metadata = result.setdefault("Metadata", {})
    positions = metadata.setdefault("ActionMetadata", {})
    position = positions.get(entry, {}).get("position", {"x": 300, "y": 300})
    positions[MARKER] = {
        "position": {"x": position["x"] - 250, "y": position["y"]},
        "isFriendlyName": True,
    }
    metadata["entryPointPosition"] = {
        "x": position["x"] - 450, "y": position["y"]}
    metadata["name"] = TARGET
    metadata["status"] = "PUBLISHED"
    metadata.pop("hash", None)
    return result


def main():
    if not shutil.which("aws"):
        raise RuntimeError("AWS CLI is not installed in this terminal.")
    os.umask(0o077)
    identity = aws("sts", "get-caller-identity")
    instance = unique(aws("connect", "list-instances")["InstanceSummaryList"],
                      "InstanceAlias", INSTANCE)
    if instance["Arn"].split(":")[4] != identity["Account"]:
        raise RuntimeError("Account mismatch. Stopped.")
    iid = instance["Id"]
    flows = aws("connect", "list-contact-flows", "--instance-id", iid)["ContactFlowSummaryList"]
    target = unique(flows, "Name", TARGET)
    original = unique(flows, "Name", ORIGINAL)
    if target["Id"] == original["Id"] or target.get("ContactFlowType") != "CONTACT_FLOW":
        raise RuntimeError("Target must be a separate inbound test flow. Stopped.")

    def describe(flow_id):
        return aws("connect", "describe-contact-flow", "--instance-id", iid,
                   "--contact-flow-id", flow_id)["ContactFlow"]

    live = describe(original["Id"])
    before = describe(target["Id"])
    try:
        draft = describe(target["Arn"] + ":$SAVED")
    except RuntimeError as error:
        if "ResourceNotFoundException" not in str(error):
            raise
        draft = before
    if before["Name"] != TARGET or draft["Name"] != TARGET:
        raise RuntimeError("Described target name mismatch. Stopped.")
    folder = BACKUP_ROOT / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder.mkdir(parents=True, exist_ok=False)

    def write(name, data):
        path = folder / name
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        return path

    write("original-flow-before.json", live)
    write("recovery-flow-before.json", before)
    write("recovery-draft-before.json", draft)
    print("Backups saved:", folder, flush=True)
    updated = patch(json.loads(draft["Content"]))
    path = write("Neptune-Day13-Recovery-Chat-version-A.json", updated)
    print("Publishing version A on", TARGET, flush=True)
    aws("connect", "update-contact-flow-content", "--instance-id", iid,
        "--contact-flow-id", target["Id"], "--content", "file://" + str(path))
    after = describe(target["Id"])
    write("recovery-flow-after.json", after)
    actual = json.loads(after["Content"])
    if after.get("Status") != "PUBLISHED":
        raise RuntimeError("Content was sent but PUBLISHED status was not confirmed.")
    if actual["StartAction"] != MARKER or actual["Actions"] != updated["Actions"]:
        raise RuntimeError("Read-back did not match the requested graph. Inspect the backup folder.")
    if json.loads(describe(original["Id"])["Content"]) != json.loads(live["Content"]):
        raise RuntimeError("Original content changed during this run; inspect before continuing.")
    print("PASS: version A is PUBLISHED and its action graph matches.")
    print("PASS: original Neptune-Inbound-Chat content is unchanged.")
    print("Next: start a fresh Test chat and verify the A message.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError, OSError) as error:
        print("STOP:", error, file=sys.stderr)
        sys.exit(1)
