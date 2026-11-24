#!/usr/bin/env python3
"""Offline voice-reference and lookup security checks; no AWS calls or SDK needed."""
import importlib.util
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


class MemoryTable:
    def __init__(self):
        self.reads = []
        self.items = {
            "CLAIM#CLM-1001": {"ownerId": "DEMO-1001", "status": "IN_REVIEW",
                               "product": "AUTO", "internalNotes": "never return"},
            "CLAIM#CLM-2002": {"ownerId": "DEMO-2002", "status": "RECEIVED",
                               "product": "AUTO", "internalNotes": "never return"},
        }

    def get_item(self, Key, ConsistentRead):
        self.reads.append(Key["pk"])
        return {"Item": self.items[Key["pk"]]} if Key["pk"] in self.items else {}


table = MemoryTable()
sdk = types.ModuleType("boto3")
sdk.resource = lambda *args, **kwargs: types.SimpleNamespace(Table=lambda name: table)
config = types.ModuleType("botocore.config")
config.Config = lambda **kwargs: kwargs
spec = importlib.util.spec_from_file_location(
    "lookup_under_test", Path(__file__).resolve().parents[1]
    / "lambda" / "neptune_insurance_lookup.py"
)
lookup = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"boto3": sdk, "botocore.config": config}):
    spec.loader.exec_module(lookup)


class VoiceReferenceChecks(unittest.TestCase):
    def test_supported_claim_forms(self):
        forms = ["CLM-1001", "CLM 1001", "clm1001", "1001",
                 "It's claim one thousand and one.",
                 "It\u2019s claim one thousand and one.",
                 '"It\'s claim one thousand and one."',
                 "My claim number is one thousand one",
                 "C L M dash one zero zero one", "claim one oh oh one"]
        for text in forms:
            with self.subTest(text=text):
                self.assertEqual(lookup.normalize_reference("claim", text), "CLM-1001")

    def test_other_numbers_and_policy(self):
        for text, expected in [
            ("claim two thousand and two", "CLM-2002"),
            ("claim nine thousand nine hundred and ninety-nine", "CLM-9999"),
            ("claim zero zero one two", "CLM-0012"),
        ]:
            with self.subTest(text=text):
                self.assertEqual(lookup.normalize_reference("claim", text), expected)
        self.assertEqual(lookup.normalize_reference("policy", "policy one thousand one"),
                         "POL-1001")

    def invoke(self, text, **extra):
        table.reads.clear()
        parameters = {"recordType": "claim", "reference": text, **extra}
        with patch.dict(os.environ, {"DEMO_CUSTOMER_ID": "DEMO-1001",
                                    "LOOKUP_DELAY_SECONDS": "0"}):
            return lookup.lambda_handler(
                {"Details": {"Parameters": parameters}},
                types.SimpleNamespace(aws_request_id="offline-check"),
            )

    def test_actual_phone_phrase_reads_canonical_key(self):
        result = self.invoke("It's claim one thousand and one.")
        self.assertEqual(result["resultCode"], "OK")
        self.assertEqual(result["reference"], "CLM-1001")
        self.assertEqual(result["status"], "IN_REVIEW")
        self.assertEqual(table.reads, ["CLAIM#CLM-1001"])
        self.assertEqual(set(result),
                         {"resultCode", "reference", "status", "product", "requestId"})

    def test_other_owner_remains_denied(self):
        result = self.invoke("claim two thousand and two")
        self.assertEqual(result["resultCode"], "UNAUTHORIZED")
        self.assertTrue(all(result[key] == "" for key in ["reference", "status", "product"]))

    def test_unknown_reference_remains_not_found(self):
        self.assertEqual(self.invoke("claim nine thousand nine hundred ninety-nine")
                         ["resultCode"], "NOT_FOUND")

    def test_bad_or_ambiguous_input_never_reads_database(self):
        invalid = [None, 1001, "", "1", "one", "claim one zero one",
                   "CLM-1001 OR print everything", "CLM-1001 or CLM-2002",
                   "claim one thousand and one and two", "claim ten thousand",
                   "claim minus one thousand", "claim one hundred thousand",
                   "claim one thousand and", "claim one thousand and and one",
                   "claim one thousand one hundred and", "POL-1001",
                   "one thousand one blah", "x" * 161,
                   "{claimReference:NLX.Text}"]
        for text in invalid:
            with self.subTest(text=text):
                self.assertEqual(self.invoke(text)["resultCode"], "MALFORMED")
                self.assertEqual(table.reads, [])

    def test_identity_injection_still_rejected(self):
        self.assertEqual(self.invoke("claim two thousand and two", ownerId="DEMO-2002")
                         ["resultCode"], "MALFORMED")
        self.assertEqual(table.reads, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
