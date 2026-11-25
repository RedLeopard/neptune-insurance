# Neptune Insurance | Build journal

## 2026-11-24 (America/Chicago) — Day 10 complete (10/14); Day 11 next

**Checkpoint: Day 10 complete (10/14), explicitly confirmed by the owner. Next: Day 11 — security, resilience and observability.** Channel delivery is verified through the owner's reported observations and supplied terminal/transcript evidence. Cross-contact continuity has not been demonstrated. The portfolio update changes progress content in the existing layout.

- Web chat: Neptune-Claims and Neptune-Training saved Chat capacity 1 and existing business-queue eligibility. Jordin remains outside Auto Claims. Neptune-Inbound-Chat uses the existing NeptuneInsurance Production alias, Default/idle/error messages, five dynamic handoff mappings and customerIntent department checks.
- Billing and confirmed new-claim app paths now escalate with Billing and AutoClaims respectively. The generic human handoff export still returns NeedsTriage; it is not silently treated as a Claims request. Application deployment was reported.
- Owner-reported live chat tests: Claims reached Elena; Billing reached Jordin, with agent acceptance/reply. The Neptune-WebChat homepage snippet was committed and the owner published it via scripts/publish_site.sh. Supplied website transcript shows the Neptune greeting and Billing response.
- SMS: existing originator Active with SMS capability; CSD-Neptune-Insurance-TollFree-SMS Complete and its associated phone resource matched. Existing $50 approval and sandbox exit retained. Dedicated delivery role permits connect:SendChatIntegrationEvent with source-account-restricted SMS service trust. Number imported into Connect and associated with Neptune-Inbound-Chat. Owner confirmed inbound response, Billing acceptance by Jordin and delivery of Jordin's reply back to the same phone.
- Messaging subtype: Segment attributes / Subtype = connect:SMS sets entryChannel = SMS; no match uses the WebChat label. Both enter the same app and department routing.
- Asynchronous eligibility: Claims Voice/Chat/Task/Email enabled at capacity 1, no other channels. One Auto Claims queue row holds all four channels at priority 1/delay 0. The proposed separate priority 2 row could not save because the console required queue-name uniqueness; priority 2 was not deployed.
- Neptune-Claim-Followup published and read back successfully. Neptune-To-AutoClaims destination and published Default queue transfer were inspected; terminal output confirms attachment to Auto Claims. Owner confirmed Elena accepted/completed the synthetic manual task and ACW. This verifies manual assignment, not automatic after-hours creation.
- Email setup: existing SES approval retained, Connect email service role created and hireedwardthornton.click added as Verified. Email messages and attachments associated to existing private S3 storage with the existing Connect KMS key. Public-access blocks are all true and bucket policy status is nonpublic; bucket default is AES256 while Connect's associations specify KMS. Attachment CORS added for GET/PUT from the existing Neptune workspace origin, without a public origin wildcard.
- Neptune-Inbound-Email published and its content verified; claims@hireedwardthornton.click created with that flow and saved as Auto Claims' default reply address. Owner explicitly confirmed Elena's inbound acceptance and receipt of her reply in the same test inbox. Email contact closure/ACW were included in the accepted test instructions.
- After-hours: both queues use the verified shared hours resource. Python backed up the messaging flow, preserved working branches, added explicit Claims/Billing hours checks, task-success/failure messages and safe claim-reference/summary mappings. The draft was read back; editor-only metadata differences were separated from behavioral differences. The owner enabled Link to contact in the designer and reported publication. Task creation/automatic delivery is not claimed as observed.
- DevOps: Python subprocess orchestrated AWS CLI, not direct Boto3. Scripts used account checks where present, actual resource discovery, backups, draft isolation, JSON generation, connection checks and read-back verification. IAM troubleshooting included inline-policy size limits, scoped managed policies, simulation and actual-operation verification. A simulation result was not treated as successful deployment.
- Export provenance: the last supplied Neptune-Inbound-Chat (4).json was the earlier published version without after-hours blocks. Later draft terminal output and reported publication establish the new configuration; no final linked-task export was supplied. Do not label the older attachment as the final flow.

**Scope decisions:** workload-type concurrency remains deferred, retaining working channel-level Task/Email capacity. The owner removed isolated closed-hours testing and voice callback build/test from current project scope; these are excluded, not incomplete deliverables. The test-copy script stopped at denied ListHoursOfOperations before creating its test hours or test flow. A test-hours permission addition succeeded; no cleanup of those IAM permissions is claimed.

**Resume:** Day 11 — security, resilience and observability. Day 10 is closed per the owner's completion decision. Existing limits on evidence remain: identity/ownership checks must be re-established on new contacts; Customer Profiles, automatic history retrieval, persistent chat and end-to-end cross-contact continuity are not claimed deployed or verified. Excluded optional work is not an incomplete Day 10 requirement. Do not repeat passed channel tests.

## 2026-11-24 (America/Chicago) — CLM-1001 fix verified; carryover testing DONE

**Status: carried-over lookup troubleshooting and testing DONE. Day 9 remains complete (9/14); the main Day 10 work is not marked complete.** Portfolio/page updates are deferred until Day 10 is finished.

- Supplied AWS CLI configuration: active NeptuneInsuranceLookup, handler neptune_insurance_lookup.lambda_handler, successful update, 3-second timeout.
- Supplied regression output: 8/8 checks passed, including canonical/spoken owned claims, denied owner access, policy, missing record, malformed input and injected identity.
- Fresh live diagnostics identified reference_format rejection of the captured synthetic text "Just calling one thousand and one." The handler correctly rejected that unsupported wording before a database read; the broader parser was not loosened.
- The next controlled phone call used "one zero zero one": CloudWatch returned OK at 2026-11-24T21:32:31Z; the owner confirmed hearing IN_REVIEW. This verifies the live voice-to-backend lookup rather than only a mock.
- Updated the claim-reference User choice prompt to request four digits individually.
- Added a separate follow-up User choice using attached continueChoice / custom NeptuneContinueChoice. The intended Yes path redirects to NeptuneWelcome, No ends via Exit application, and No match redirects to NeptuneRecovery. The latest supplied export has all three destinations connected; custom value IDs require the matching slot resource.
- Reviewed and archived the supplied NeptuneClaimStatus.flow (7).json as connect/agentic/NeptuneClaimStatus.flow.json. The owner subsequently confirmed "problem fixed" and requested testing marked done. This is owner-reported acceptance; no separate transcript for each continuation branch was supplied.
- Temporary bounded validation diagnostics from commit 727cdaef remain in the Lambda source; lookup permissions, validation and the five-field output contract are unchanged.

**Next:** continue the actual Day 10 syllabus. Do not replay the completed lookup tests. Earlier agent handoff/context, quick-connect evidence, module/slot export packaging and unexecuted live failure-branch checks remain separate from this completed fix.

## 2026-11-23 (America/Chicago) — Day 9 complete; live-call verification carried into Day 10

**Checkpoint: Day 9 complete (9/14), per the owner's completion decision.** Remaining live-call tests and troubleshooting are explicitly carried into the start of Day 10. The owner stopped testing for the evening. Do not replay resource creation or the completed direct timeout drill.

- Created the on-demand `NeptuneInsuranceLab` DynamoDB table with a String partition key and three synthetic policy/claim records.
- Created `NeptuneInsuranceLookupRole`: Lambda service trust, GetItem on the lab table, and basic execution logging. Deployed `NeptuneInsuranceLookup` with Python 3.13, a 3-second timeout and read-only behavior.
- Verified canonical claim and policy success, not-found, unauthorized, malformed-reference and unexpected-identity responses through supplied terminal output. The five-field response excludes owner IDs and internal notes, including the synthetic injection-test note.
- Verified a controlled direct Lambda timeout, restoration of the original timeout/environment and a successful recovery lookup.
- Added the scoped Connect invocation permission, resolved the operator's Lambda-association permission, and confirmed the function association in the instance.
- Built input/output contracts and synchronous Lambda mappings in a flow module. Saving as a tool produced/selected `NeptuneInsuranceLookupModule-Copy`; the original module's tool flag remained false. The Data request points to the tool copy, not the original.
- Saved the `NeptuneInsuranceLookup` Data request and inserted it after claim-reference capture in `NeptuneClaimStatus`. Success routes to a Split; non-OK results, Failure and Timeout route to `NeptuneRecovery`; the approved result path reaches the existing Basic response and Exit application.
- Observed the canvas mock returning OK / CLM-1001 / IN_REVIEW. After correcting the Split selection and the response variable, the pasted test transcript displayed IN_REVIEW. This was a mock, not a DynamoDB call.
- The owner reported deploying the application. Real calls entered through keypad option 3 and reached the AI and Lambda; CloudWatch showed MALFORMED. A temporary diagnostic revealed a full spoken sentence where the handler expected a canonical reference.
- Added bounded spoken-reference normalization in commit `87f0e94`. Seven offline test groups passed, including the actual spoken phrase, authorization and malformed/ambiguous input cases. Added an eight-case AWS CLI regression runner. The owner reported running the deployment commands, but its regression transcript was not supplied.
- The owner reported that the subsequent phone test still failed. No post-fix result code or successful live claim-status response has been supplied. The cause of this latest failure remains unresolved.
- The normalizer release removes the temporary diagnostic from source. Confirm the active deployed code and recent logs when resuming; do not assume an older log describes the current build.
- Portfolio update is limited to progress text and the Day 9 milestone. Existing hero image, styling, scripts and project ordering are retained; live publication is separate.

**Start Day 10:** obtain fresh logs from the latest failed call and confirm the deployed handler/package. Inspect the actual reference, the tool-copy input mapping and the deployed application environment. Confirm a real OK lookup and returned status to close the carried-over live verification. Then capture final corrected flow/tool exports and remaining controlled failure-path evidence. See [lookup verification and remaining work](terraform/LOOKUP_VERIFICATION.md).

**Still open from earlier sessions:** phone-to-agent acceptance and received handoff context; the full quick-connect retest. Terraform adoption stays last, after the functional lookup works.

## 2026-11-22 (America/Chicago) — Day 8 AI controls and handoff configuration

- Saved `NeptuneHumanHandoff` and `NeptuneSupervisorHandoff` with Start → Escalate, fixed customer messages, and five Set state modifications on each path.
- Created `handoffReason`, `handoffSummary`, `handoffClaimReference`, `customerIntent` as String context variables and `supervisorRequested` as Boolean. The schema generator was given unquoted `false` to produce the Boolean type.
- Saved `NeptuneHumanRequests` (Input): supervisor/manager keywords route to the supervisor flow; human/representative keywords route to the general flow. The second rule required a nonempty enforcement message and was saved using Override → Static plus the Route to field.
- Saved `NeptuneInsuranceOutput` (Output), with the `NoInsuranceDecisions` LLM-judge rule and a fixed Override → Static response. Its intended scope is unsupported case-specific coverage, liability, fraud and payment decisions; effectiveness is not certified by saving the rule.
- Attached both guardrails and both handoff flows to `NeptuneInsurance`. A new build and deployment were reported; its version/build identifier was not captured. Existing Welcome, Fallback, Unknown and Incomprehension defaults were retained.
- Observed supervisor test transcript: the correct supervisor-request message, then **Application exited via Escalation**. General-human test success was learner-reported; no full transcript was supplied.
- Connected the existing claims-context check to `Neptune Agentic CX`; its Escalation path reads all five returned Agentic CX context values into Current contact / User defined attributes, then selects and transfers to Auto Claims. Error goes to the existing claims acknowledgement/queue path; Idle chat timeout goes to technical fallback; Default disconnects.
- Added `Neptune AI Voice` near the entry. Reviewed supplied export `(27)`: 26 blocks reachable from Entry, no empty targets or missing graph references, correct dynamic handoff mappings, and connected routing/error paths. The supplied file contains `TextToSpeechVoice: Joanna` but no explicit language attribute.
- After that review, the learner reported enabling the English (United States) language attribute and publishing. No updated export or live phone-call result followed. This final correction/publication is recorded as reported, not inferred into the archived JSON.
- Updated GitHub documentation, the sanitized latest supplied flow snapshot, and the portfolio case study. The live customer website and live personal portfolio were not deployed by this source update.

**Resume:** confirm the published flow and lab number association, sign an eligible Auto Claims test agent into the workspace and set Available, then make one controlled synthetic call: press 3, ask for a representative, confirm agent acceptance/audio and inspect the returned handoff attributes. Record the real result; obtain a final post-language-fix export. Day 6 quick-connect retest and unexecuted negative/failure checks remain pending.

## 2026-11-21 (America/Chicago) — Day 7 conversational application

- Saved `NeptuneInsurance` in `Neptune Insurance Lab`; deployment v0.1.0 displayed successful and Live.
- Built Welcome, Recovery, Billing, New Auto Claim, and Claim Status flows; added typed slots, recap placeholders, confirmation endings, and connected No match recovery paths.
- Reviewed the supplied 11-node claim-flow export for graph connectivity and matching placeholder types.
- Observed pasted test evidence: billing recognized `NeptuneBilling` and exited via Default; an unsupported pizza request reached recovery and exited via Default. Additional intake tests were reported successful by the learner, without full transcripts.
- The app collects synthetic information only. It does not file a claim, determine coverage, or retrieve live status. Phone/web invocation and human handoff remain future work.
- Updated the portfolio case study to Day 7, with 7/14 progress and the next Day 8 milestone. Publication to the personal portfolio is separate.

## 2026-11-20 (America/Chicago) — Day 6 routing configuration

- Worked through Billing and Auto Claims queues, routing-profile eligibility, agent state, and channel capacity.
- Console reported `Neptune-To-AutoClaims` saved: Queue type, Auto Claims destination, Default queue transfer flow.
- Learner requested a full quick-connect retest on return. Keep this open; AI application tests do not verify a queue transfer or agent delivery.

## 2026-11-19 (America/Chicago) — Voice entry source and public demo links

- Confirmed the existing voice demo number, `1-800-810-5374`, is associated with `Neptune-Inbound-Voice` in the supplied Connect configuration.
- Added clickable phone links to all eight website footers and to the Home, Support, Claims and My Neptune content. Replaced the pending-number card; clarified voice versus planned messaging and the separate browser-only claims form.
- Added the supplied 21-block flow as a sanitized public template under `connect/flows/`, with consistent placeholder account, instance, hours and queue identifiers. Included binding instructions and the current menu behavior.
- Configuration evidence: the supplied export reports `PUBLISHED` and includes logging, voice-channel and hours checks, one retry, Auto Claims queue selection/transfer, and connected failure paths.
- Static validation checks phone destinations, internal links, unique HTML IDs, graph references, the retry bound and identifier replacement. These checks do not execute a phone call.
- Pending: deploy these website source changes to S3/CloudFront and execute T01–T04. No live-call results or successful agent delivery are claimed.

## 2026-11-17 (America/Chicago) — Static website goes live

- Created fictional Neptune Insurance customer website with responsive coverage, claims, portal, support, and information pages.
- Requested and DNS-validated an ACM certificate for `neptune.hireedwardthornton.click`; verified `ISSUED`.
- Deployed private S3 origin behind CloudFront; distribution `E3GSYLGJJFG7RR` (`d24fdjlm9el2lj.cloudfront.net`).
- Created Route 53 A/AAAA aliases. DNS was initially cached negatively; later authoritative and public DNS resolved.
- Confirmed custom domain HTTPS and CloudFront `HTTP/2 200` with content length 19,835 for `index.html`.
- No live voice, chat, SMS, or email integration was demonstrated by these web tests.

## Next checkpoint — Portfolio + GitHub baseline

- [ ] Relocate Neptune source folder from Mac Downloads to home projects directory.
- [ ] Review case-study page and add portfolio carousel card.
- [x] Dedicated source repository: https://github.com/RedLeopard/neptune-insurance (established before this update).
- [ ] Verify public portfolio link.
- [ ] Capture architecture screenshots for an interview-ready walkthrough.

## Note for future entries

Use format: date, change made, service/component, proof/test, architectural decision, next action.

