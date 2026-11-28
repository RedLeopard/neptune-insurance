# Portfolio source snapshots

`index.html` is the current Hire Edward portfolio homepage snapshot, including Neptune first, AncestorIQ second, and Dialogflow third. Neptune uses the same single case-study link pattern as the other cards.

The matching case study lives at the repository root, `neptune-insurance.html`. The existing format, hero, images, styles, scripts, links and homepage are retained. Progress now shows all 14 core days complete, accepted November 28, 2026. The Day 14 capstone, architecture defense and operational handoff are reflected in the existing milestone format; the SDK stack now explicitly names Boto3 and links the Lambda source. Working SMS/email/manual Task evidence is retained. Next are the separate S3 recording, Nova 2 Sonic and cleanup bonus missions. The associated artwork remains `assets/neptune-share.png`.

These are the canonical copies of the portfolio files updated with this Neptune milestone. This progress update changes the case study only; the homepage, project order, other cards and all artwork are retained. This folder is not a standalone website: the homepage still references the existing portfolio's other pages and assets. Keep those in the existing `~/hireedward` folder.

## Sync the existing laptop portfolio

After pulling this repository, run:

```bash
bash ~/NeptuneInsurance/scripts/sync_portfolio.sh
```

The script copies only the homepage, Neptune case study, and preview artwork into the existing `~/hireedward` folder. You can supply a different existing portfolio directory as its first argument. It does not run Git commands, upload to AWS, or invalidate CloudFront. Website publication remains a separate operation.

For routine updates to these files, use this copy script. `install_neptune.py` is the earlier card/bootstrap installer and can rewrite the homepage card placement.


## Publish the updated case study with the existing Hire Edward bash

The source repository is `~/NeptuneInsurance`; the existing portfolio is `~/hireedward`. For this case-study-only update, copy the one changed HTML file so unrelated local homepage edits are retained:

```bash
cd ~/NeptuneInsurance &&
git pull --ff-only origin main &&
cp neptune-insurance.html ~/hireedward/neptune-insurance.html &&
cd ~ &&
bash ./deploy-hireedward.sh
```

The owner's existing `~/deploy-hireedward.sh` publishes the Hire Edward portfolio. It is separate from `scripts/publish_site.sh`, which publishes the Neptune customer demo. The GitHub/source closeout does not itself execute that laptop script or claim a new public deployment.
