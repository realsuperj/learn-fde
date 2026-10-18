#!/usr/bin/env python3
"""Merge an actual Promptfoo report; cannot turn failed evals into passed state."""
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--root',default=str(Path(__file__).resolve().parents[1]));a=p.parse_args();out=Path(a.root)/'artifacts/w01'
r=json.loads((out/'promptfoo-results.json').read_text());stats=r['results']['stats'];cases=r['results']['results']
ok=stats['successes']>=3 and stats['failures']==0 and stats.get('errors',0)==0 and len(cases)>=3 and all(c['success'] and json.loads(c['response']['output']).get('model_mode')=='live' for c in cases)
env=json.loads((out/'environment_check.json').read_text());env['checks']['evaluation']={'status':'pass' if ok else 'fail','code':'PROMPTFOO_REPORT_VERIFIED' if ok else 'PROMPTFOO_FAILED'};(out/'environment_check.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n');print(env['checks']['evaluation']);raise SystemExit(0 if ok else 1)
