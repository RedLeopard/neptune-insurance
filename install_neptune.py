#!/usr/bin/env python3
"""Install/update ONLY Neptune case study and carousel card into existing portfolio."""
from __future__ import annotations
import argparse, datetime, pathlib, re, shutil, sys
ROOT=pathlib.Path(__file__).resolve().parent
START='<!-- NEPTUNE_PROJECT_CARD_START -->'
END='<!-- NEPTUNE_PROJECT_CARD_END -->'
CARD="""
                <!-- NEPTUNE_PROJECT_CARD_START -->
                <article class="mission"><a class="mission-visual project-cover-card" href="neptune-insurance.html"
                    aria-label="Explore Neptune Insurance: live web demonstration and staged Amazon Connect architecture">
                    <img class="platform-project-cover" src="assets/neptune-project-cover.svg"
                    alt="Neptune Insurance: enterprise cloud customer experience portfolio project" width="1734" height="907" loading="lazy" decoding="async"><span class="visual-arrow">↗</span></a>
                  <div class="mission-body"><div class="mission-type">AWS / OMNICHANNEL CUSTOMER EXPERIENCE</div>
                    <h3><a href="neptune-insurance.html">Neptune Insurance</a></h3>
                    <p>An AWS-hosted insurance demo with claims, a sample policy portal, and an evolving Amazon Connect omnichannel architecture.</p>
                    <div class="tags"><span>CloudFront</span><span>Amazon Connect</span><span>Agentic AI</span><span>Architecture</span></div>
                    <a class="text-link" href="neptune-insurance.html">View Neptune project <span>↗</span></a>
                  </div></article>
                <!-- NEPTUNE_PROJECT_CARD_END -->
"""
def main():
 p=argparse.ArgumentParser(description='Safely add Neptune project to existing portfolio')
 p.add_argument('portfolio_dir',help='Existing portfolio folder with index.html and assets/, e.g. ~/hireedward')
 p.add_argument('--dry-run',action='store_true',help='Report what would change without writing')
 args=p.parse_args(); dest=pathlib.Path(args.portfolio_dir).expanduser().resolve(); idx=dest/'index.html'
 if not idx.is_file() or not (dest/'assets').is_dir():
  sys.exit(f'ERROR: Not a recognized portfolio folder: {dest} (needs index.html and assets/)')
 raw=idx.read_text(encoding='utf-8')
 if 'id="projects-track"' not in raw or 'class="reel-footer"' not in raw:
  sys.exit('ERROR: Expected project carousel not found; stopping without edits.')
 updated=raw
 if START in raw:
  if END not in raw: sys.exit('ERROR: Incomplete Neptune project marker. Stopping without edits.')
  updated=raw[:raw.index(START)]+CARD.strip()+raw[raw.index(END)+len(END):]
 else:
  a=raw.index('id="projects-track"'); b=raw.find('<div class="reel-footer">',a)
  if b<0: sys.exit('ERROR: Project carousel footer missing')
  closing=raw.rfind('</div>',a,b)
  if closing<0: sys.exit('ERROR: Project carousel closing tag missing')
  updated=raw[:closing]+CARD+raw[closing:]
 updated=re.sub(r'(\b)FIVE MISSIONS\.',r'\g<1>SIX MISSIONS.',updated)
 # Only adjust static initial counter. Carousel JS computes actual number dynamically.
 updated=updated.replace('id="projects-range">1–3 / 5','id="projects-range">1–3 / 6')
 output=[idx,dest/'neptune-insurance.html',dest/'assets/neptune-project-cover.svg']
 print('Portfolio:',dest)
 print('Files to update:',*[str(x.relative_to(dest)) for x in output],sep='\n  - ')
 print('Other project pages and resources will not be changed.')
 if args.dry_run:
  print('DRY RUN: No changes written.');return
 stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
 backup=dest/f'index.html.before-neptune-{stamp}.bak'
 shutil.copy2(idx,backup)
 shutil.copy2(ROOT/'neptune-insurance.html',output[1]);shutil.copy2(ROOT/'assets/neptune-project-cover.svg',output[2])
 idx.write_text(updated,encoding='utf-8')
 print('Installed Neptune portfolio page. Backup:',backup)
 print('Open local neptune-insurance.html or deploy using your existing portfolio workflow.')
if __name__=='__main__':main()
