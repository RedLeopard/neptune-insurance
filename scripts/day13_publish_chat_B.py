"""Back up the tested A+guard flow, then publish only its B marker change."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

TARGET = "Neptune-Day13-Recovery-Chat"
MARKER = "Day13 Version Marker"
A = "Neptune Day 13 recovery drill — version A."
B = "Neptune Day 13 recovery drill — version B."


def aws(service, operation, *args):
    r = subprocess.run(["aws", service, operation, *args, "--region", "us-west-2",
                        "--output", "json", "--no-cli-pager"],
                       capture_output=True, text=True,
                       env={**os.environ, "AWS_PAGER": "", "AWS_CLI_AUTO_PROMPT": "off"})
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout) if r.stdout.strip() else {}


def make_b(content):
    updated = copy.deepcopy(content)
    actions = {a["Identifier"]: a for a in updated["Actions"]}
    if len(actions) != len(updated["Actions"]) or updated["StartAction"] != MARKER:
        raise RuntimeError("Unexpected flow entry or duplicate action IDs.")
    marker = actions[MARKER]
    check = actions["Day13 Context Check"]
    notice = actions["Day13 Missing Context"]
    if marker["Type"] != "MessageParticipant" or marker["Parameters"].get("Text") != A:
        raise RuntimeError("Expected version A. Stopped without replacing a backup.")
    if (marker["Transitions"]["NextAction"] != check["Identifier"]
            or check["Type"] != "Compare"
            or check["Parameters"].get("ComparisonValue") != "$.Attributes.day13ClaimReference"
            or notice["Type"] != "MessageParticipant"):
        raise RuntimeError("The expected context guard was not found.")
    marker["Parameters"]["Text"] = B
    updated.setdefault("Metadata", {}).pop("hash", None)
    return updated


def main():
    os.umask(0o077)
    root = Path.home() / "Neptune-Day13-Backups"
    snapshots = sorted(root.glob("context-*/recovery-after.json"))
    if not snapshots:
        raise RuntimeError("Published context-guard backup not found.")
    saved = json.loads(snapshots[-1].read_text())
    original_saved = json.loads((snapshots[-1].parent / "original-before.json").read_text())
    if saved["Name"] != TARGET or original_saved["Name"] != "Neptune-Inbound-Chat":
        raise RuntimeError("Backup names do not match the intended flows.")
    arn = saved["Arn"]
    iid = arn.split(":instance/", 1)[1].split("/")[0]
    fid = arn.split("/contact-flow/", 1)[1].split(":")[0]
    original_id = original_saved["Arn"].split("/contact-flow/", 1)[1].split(":")[0]
    if fid == original_id or aws("sts", "get-caller-identity")["Account"] != arn.split(":")[4]:
        raise RuntimeError("Account or flow identity mismatch.")

    def describe(flow_id):
        return aws("connect", "describe-contact-flow", "--instance-id", iid,
                   "--contact-flow-id", flow_id)["ContactFlow"]

    original = describe(original_id)
    before = describe(fid)
    if before["Name"] != TARGET or before.get("Status") != "PUBLISHED":
        raise RuntimeError("Expected the published recovery copy.")
    content_a = json.loads(before["Content"])
    content_b = make_b(content_a)
    folder = root / ("rollback-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    folder.mkdir(parents=True, exist_ok=False)

    def save(name, data):
        p = folder / name
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return p

    save("A-flow-response.json", before)
    save("A-content.json", content_a)
    save("original-before.json", original)
    path = save("B-content.json", content_b)
    print("Known-good A + guard saved:", folder, flush=True)
    aws("connect", "update-contact-flow-content", "--instance-id", iid,
        "--contact-flow-id", fid, "--content", "file://" + str(path))
    after = describe(fid)
    save("B-flow-response.json", after)
    if after.get("Status") != "PUBLISHED" or json.loads(after["Content"])["Actions"] != content_b["Actions"]:
        raise RuntimeError("Published B was not confirmed by read-back.")
    if json.loads(describe(original_id)["Content"]) != json.loads(original["Content"]):
        raise RuntimeError("Original flow changed during the run; inspect before continuing.")
    print("PASS: version B is PUBLISHED; context guard retained.")
    print("PASS: original Neptune-Inbound-Chat content is unchanged.")
    print("Next: start a fresh Test chat with {} and observe B, notice, welcome.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError, OSError) as error:
        print("STOP:", error, file=sys.stderr)
        sys.exit(1)
