"""Jetta QA stage dispatch: qa_mode controls obligations, profile controls executor."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, 'C:/Scripts/Jetta Harness/scripts')
from flow import prepare

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ledger',required=True);p.add_argument('--packet',required=True)
    a=p.parse_args()
    try:
        packet=json.loads(Path(a.packet).read_text(encoding='utf-8-sig'))
        if packet.get('qa_mode') not in ('Quick','Standard','Deep'):raise ValueError('qa_mode required independently of model_profile')
        if not packet.get('verification'):raise ValueError('QA dispatch requires verification allocation')
        print(json.dumps(prepare(packet,a.ledger),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,TypeError) as error:
        print(str(error),file=sys.stderr);sys.exit(2)
