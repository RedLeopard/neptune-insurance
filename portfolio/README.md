# Portfolio source snapshots

`index.html` is the current Hire Edward portfolio homepage snapshot, including Neptune first, AncestorIQ second, and Dialogflow third. Neptune uses the same single case-study link pattern as the other cards.

The matching case study lives at the repository root, `neptune-insurance.html`. The existing format, hero, images, styles, scripts, links and homepage are retained. Progress now shows Day 12 complete with twelve of fourteen days complete. Supervisor, historical voice/channel and agent reports were saved; controlled Billing-to-Claims transfer and Claims abandonment tests completed; reporting windows and linked contact records were reviewed. A qualitative executive scorecard, data dictionary, report inventory and test/progress CSVs were created. Resume at Day 13 — reliability drills and omnichannel runbooks. The associated artwork remains `assets/neptune-share.png`.

These are the canonical copies of the portfolio files updated with this Neptune milestone. This progress update changes the case study only; the homepage, project order, other cards and all artwork are retained. This folder is not a standalone website: the homepage still references the existing portfolio's other pages and assets. Keep those in the existing `~/hireedward` folder.

## Sync the existing laptop portfolio

After pulling this repository, run:

```bash
bash ~/NeptuneInsurance/scripts/sync_portfolio.sh
```

The script copies only the homepage, Neptune case study, and preview artwork into the existing `~/hireedward` folder. You can supply a different existing portfolio directory as its first argument. It does not run Git commands, upload to AWS, or invalidate CloudFront. Website publication remains a separate operation.

For routine updates to these files, use this copy script. `install_neptune.py` is the earlier card/bootstrap installer and can rewrite the homepage card placement.

