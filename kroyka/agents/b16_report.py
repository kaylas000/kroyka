"""B16 - JSON Report Generator"""
import sys,os,json;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState;OUTDIR='/tmp/kroyka_cnc'
def run(s):
    if not s.plan:return s
    os.makedirs(OUTDIR,exist_ok=True)
    report={'sheets_used':s.plan.sheets_used,'efficiency_pct':round(s.plan.efficiency*100,2),'parts_placed':len(s.plan.placements),'parts_unplaced':len(s.plan.unplaced),'warnings':s.warnings,'errors':s.errors,'svg':s.plan.svg_paths,'cnc':s.plan.cnc_paths}
    path=f'{OUTDIR}/report.json';open(path,'w').write(json.dumps(report,ensure_ascii=False,indent=2))
    print(f'B16 Report: {path}');return s
