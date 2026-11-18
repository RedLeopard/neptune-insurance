#!/usr/bin/env python3
"""Deploy the fictional Neptune Insurance static site to its own AWS subdomain.

Requires: AWS CLI v2, configured AWS credentials, Python 3.8+, Route 53
public hosted zone for hireedwardthornton.click in the selected AWS account.
Uses us-east-1 for S3 and ACM, an OAC-protected S3 origin, and CloudFront.
Does not modify the existing portfolio distribution or bucket.
"""
from __future__ import annotations
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

DOMAIN = "neptune.hireedwardthornton.click"
PARENT = "hireedwardthornton.click"
REGION = "us-east-1"
CF_HOSTED_ZONE = "Z2FDTNDATAQYW2"
CACHE_POLICY = "658327ea-f89d-4fab-a63d-7e88639e58f6"  # AWS managed CachingOptimized
ROOT = Path(__file__).resolve().parent
SITE = ROOT / "neptune-insurance"

class AwsError(Exception):
    pass


def run_aws(*args, json_output=True, check=True):
    cmd = ["aws", *map(str, args), "--no-cli-pager", "--output", "json" if json_output else "text"]
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        if check:
            raise AwsError("Command failed: aws " + " ".join(map(str, args[:4])) + "\n" + completed.stderr.strip())
        return None
    if not json_output:
        return completed.stdout.strip()
    try:
        return json.loads(completed.stdout) if completed.stdout.strip() else {}
    except json.JSONDecodeError as e:
        raise AwsError("Unexpected AWS CLI response: " + str(e)) from e


def change_records(zone_id, changes):
    return run_aws("route53", "change-resource-record-sets", "--hosted-zone-id", zone_id,
                   "--change-batch", json.dumps({"Changes": changes}, separators=(",", ":")))


def upsert_record(name, value, rtype="CNAME", ttl=300):
    return {"Action": "UPSERT", "ResourceRecordSet": {
        "Name": name, "Type": rtype, "TTL": ttl,
        "ResourceRecords": [{"Value": value}]}}


def get_record_sets(zone_id):
    return run_aws("route53", "list-resource-record-sets", "--hosted-zone-id", zone_id)["ResourceRecordSets"]


def matching_record(records, name, rtype):
    return next((r for r in records if r["Name"].rstrip(".").lower() == name.lower()
                 and r["Type"] == rtype), None)


def main():
    if shutil.which("aws") is None:
        raise AwsError("AWS CLI not found. Install it, then run: aws configure")
    if shutil.which("python3") is None:
        raise AwsError("Python 3 not found.")
    if not (SITE / "index.html").is_file():
        raise AwsError("Website assets missing. Run this script in the extracted Neptune package.")

    identity = run_aws("sts", "get-caller-identity")
    account = identity["Account"]
    bucket = f"neptune-insurance-{account}-{REGION}"
    print("\nNEPTUNE INSURANCE — SUBDOMAIN DEPLOYMENT")
    print("AWS account:", account)
    print("Domain:", DOMAIN)
    print("Private S3 bucket:", bucket)
    print("Region:", REGION, "(certificate and website)")
    print("This creates or updates billable AWS resources; it does not alter your main portfolio.")
    if input("Type DEPLOY to continue: ").strip() != "DEPLOY":
        print("No changes made.")
        return

    zones = run_aws("route53", "list-hosted-zones-by-name", "--dns-name", PARENT)["HostedZones"]
    zone = next((z for z in zones if z["Name"].rstrip(".") == PARENT
                 and not z.get("Config", {}).get("PrivateZone", False)), None)
    if not zone:
        raise AwsError("No public Route 53 hosted zone for " + PARENT +
                       " in this AWS account. Check the profile/account and your domain's DNS provider.")
    zone_id = zone["Id"].split("/")[-1]
    records = get_record_sets(zone_id)
    for rtype in ("A", "AAAA", "CNAME"):
        record = matching_record(records, DOMAIN, rtype)
        if record:
            if rtype == "CNAME":
                raise AwsError("Existing Neptune CNAME detected. Refusing to replace it: " + str(record))
            alias = record.get("AliasTarget", {}).get("DNSName", "").rstrip(".")
            # The known distribution is validated later before its alias is reused.
            if not alias.endswith(".cloudfront.net"):
                raise AwsError("Existing Neptune DNS record is not a CloudFront alias. Refusing to change: " + str(record))

    # Reuse an issued exact/wildcard certificate if present; otherwise request the exact name.
    certs = run_aws("acm", "list-certificates", "--region", REGION,
                    "--certificate-statuses", "ISSUED", "PENDING_VALIDATION").get("CertificateSummaryList", [])
    def matches_cert(c):
        names = c.get("SubjectAlternativeNames") or [c.get("DomainName", "")]
        return DOMAIN in names or f"*.{PARENT}" in names
    candidates = [c for c in certs if matches_cert(c)]
    candidates.sort(key=lambda c: (c.get("Status") != "ISSUED", c.get("DomainName") != DOMAIN))
    if candidates:
        arn = candidates[0]["CertificateArn"]
        print("Using ACM certificate:", arn)
    else:
        result = run_aws("acm", "request-certificate", "--region", REGION,
                         "--domain-name", DOMAIN, "--validation-method", "DNS",
                         "--idempotency-token", "neptuneportfolio2026")
        arn = result["CertificateArn"]
        print("Requested certificate:", arn)

    details = run_aws("acm", "describe-certificate", "--region", REGION,
                      "--certificate-arn", arn)["Certificate"]
    if details["Status"] != "ISSUED":
        options = details.get("DomainValidationOptions", [])
        resource = next((v.get("ResourceRecord") for v in options if v.get("ResourceRecord")), None)
        if resource:
            current = matching_record(records, resource["Name"], "CNAME")
            if current:
                existing_values = [x["Value"].rstrip(".") for x in current.get("ResourceRecords", [])]
                if resource["Value"].rstrip(".") not in existing_values:
                    raise AwsError("Conflicting certificate validation CNAME; refusing to overwrite: " + str(current))
            change_records(zone_id, [upsert_record(resource["Name"], resource["Value"])])
            print("Created/verified Route 53 certificate validation record.")
        else:
            print("ACM hasn't returned a DNS validation record yet.")
        print("\nCertificate status:", details["Status"])
        print("DNS validation must complete before CloudFront can use this name.")
        print("When the certificate shows ISSUED, rerun: python3 deploy_neptune_subdomain.py")
        print("No customer website or existing portfolio resources were modified.")
        return

    dists = run_aws("cloudfront", "list-distributions").get("DistributionList", {}).get("Items", [])
    dist = next((d for d in dists if DOMAIN in d.get("Aliases", {}).get("Items", [])), None)
    if dist:
        origins = [o.get("DomainName", "") for o in dist["Origins"]["Items"]]
        if f"{bucket}.s3.{REGION}.amazonaws.com" not in origins:
            raise AwsError("An existing CloudFront distribution owns this subdomain but uses a different origin."
                           " Stop and review it before proceeding.")
        dist_id, dist_domain = dist["Id"], dist["DomainName"]
        print("Reusing existing distribution:", dist_id)
    else:
        # Existing DNS aliases are not silently reassigned to a new distribution.
        for rtype in ("A", "AAAA"):
            if matching_record(records, DOMAIN, rtype):
                raise AwsError("Existing Neptune CloudFront DNS alias found, but no matching distribution in this AWS account."
                               " No overwrite attempted. Check the account before continuing.")

    print("Preparing private S3 website bucket...")
    if run_aws("s3api", "head-bucket", "--bucket", bucket, check=False) is None:
        run_aws("s3api", "create-bucket", "--bucket", bucket, "--region", REGION)
    run_aws("s3api", "put-public-access-block", "--bucket", bucket,
            "--public-access-block-configuration",
            "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true")
    run_aws("s3api", "put-bucket-versioning", "--bucket", bucket,
            "--versioning-configuration", "Status=Enabled")
    run_aws("s3", "sync", str(SITE), f"s3://{bucket}/", "--region", REGION, "--exclude", ".DS_Store",
            json_output=False)

    if not dist:
        print("Configuring private CloudFront origin access...")
        oac_name = f"neptune-insurance-{account}"
        oacs = run_aws("cloudfront", "list-origin-access-controls").get("OriginAccessControlList", {}).get("Items", [])
        oac = next((o for o in oacs if o.get("Name") == oac_name), None)
        if oac:
            oac_id = oac["Id"]
        else:
            oac_config = {"Name": oac_name, "Description": "Private access for Neptune portfolio demonstration",
                          "SigningProtocol": "sigv4", "SigningBehavior": "always", "OriginAccessControlOriginType": "s3"}
            created = run_aws("cloudfront", "create-origin-access-control",
                              "--origin-access-control-config", json.dumps(oac_config))
            oac_id = created["OriginAccessControl"]["Id"]
        origin_id = "neptune-s3"
        dist_config = {
            "CallerReference": f"neptune-{account}-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "Aliases": {"Quantity": 1, "Items": [DOMAIN]},
            "DefaultRootObject": "index.html",
            "Origins": {"Quantity": 1, "Items": [{"Id": origin_id,
                "DomainName": f"{bucket}.s3.{REGION}.amazonaws.com",
                "S3OriginConfig": {"OriginAccessIdentity": ""},
                "OriginAccessControlId": oac_id}]},
            "DefaultCacheBehavior": {
                "TargetOriginId": origin_id, "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"],
                                   "CachedMethods": {"Quantity": 2, "Items": ["GET", "HEAD"]}},
                "Compress": True, "CachePolicyId": CACHE_POLICY},
            "Comment": "Neptune Insurance fictional portfolio demo — independent site",
            "Enabled": True, "PriceClass": "PriceClass_100",
            "ViewerCertificate": {"ACMCertificateArn": arn, "SSLSupportMethod": "sni-only",
                                  "MinimumProtocolVersion": "TLSv1.2_2021"},
            "Restrictions": {"GeoRestriction": {"RestrictionType": "none", "Quantity": 0}},
            "HttpVersion": "http2", "IsIPV6Enabled": True,
        }
        created = run_aws("cloudfront", "create-distribution", "--distribution-config", json.dumps(dist_config))
        dist_id, dist_domain = created["Distribution"]["Id"], created["Distribution"]["DomainName"]
        print("Created CloudFront distribution:", dist_id)

    policy = {"Version": "2012-10-17", "Statement": [{
        "Sid": "AllowCloudFrontReadOnly", "Effect": "Allow",
        "Principal": {"Service": "cloudfront.amazonaws.com"}, "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket}/*",
        "Condition": {"StringEquals": {"AWS:SourceArn":
            f"arn:aws:cloudfront::{account}:distribution/{dist_id}"}}
    }]}
    run_aws("s3api", "put-bucket-policy", "--bucket", bucket, "--policy", json.dumps(policy))

    alias = {"HostedZoneId": CF_HOSTED_ZONE, "DNSName": dist_domain,
             "EvaluateTargetHealth": False}
    changes = [{"Action": "UPSERT", "ResourceRecordSet": {
        "Name": DOMAIN, "Type": rtype, "AliasTarget": alias}} for rtype in ("A", "AAAA")]
    change_records(zone_id, changes)
    run_aws("cloudfront", "create-invalidation", "--distribution-id", dist_id,
            "--paths", "/*")
    print("\nDEPLOYMENT CONFIGURED")
    print("Domain: https://" + DOMAIN)
    print("CloudFront ID:", dist_id)
    print("CloudFront hostname:", dist_domain)
    print("Bucket:", bucket)
    print("DNS and CloudFront changes may need time to propagate before the URL responds.")
    print("No Amazon Connect voice, SMS or chat integration is implied by this deployment.")


if __name__ == "__main__":
    try:
        main()
    except (AwsError, FileNotFoundError) as e:
        print("\nDEPLOYMENT STOPPED:", str(e), file=sys.stderr)
        print("Review the error before rerunning. Existing portfolio files were not changed.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopped by user. AWS changes already completed, if any, are not automatically undone.")
        sys.exit(130)
