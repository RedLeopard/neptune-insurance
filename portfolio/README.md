# Portfolio source snapshots

`index.html` is the current Hire Edward portfolio homepage snapshot, including Neptune first, AncestorIQ second, and Dialogflow third. Neptune uses the same single case-study link pattern as the other cards.

The matching case study lives at the repository root, `neptune-insurance.html`. Its preview picture opens the live Neptune website, its voice number links to the demo line, and its progress reflects Day 7 completion, including the separately deployed conversational application. The associated artwork is `assets/neptune-share.png`.

These are the canonical copies of the portfolio files updated with this Neptune milestone. This folder is not a standalone website: the homepage still references the existing portfolio's other pages and assets. Keep those in the existing `~/hireedward` folder.

## Sync the existing laptop portfolio

After pulling this repository, run:

```bash
bash ~/NeptuneInsurance/scripts/sync_portfolio.sh
```

The script copies only the homepage, Neptune case study, and preview artwork into the existing `~/hireedward` folder. You can supply a different existing portfolio directory as its first argument. It does not run Git commands, upload to AWS, or invalidate CloudFront. Website publication remains a separate operation.

For routine updates to these files, use this copy script. `install_neptune.py` is the earlier card/bootstrap installer and can rewrite the homepage card placement.
