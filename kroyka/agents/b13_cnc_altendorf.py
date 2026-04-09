"""B13 - Altendorf WA format"""
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState;OUTDIR='/tmp/kroyka_cnc'
def run(s):
    if not s.plan:return s
    os.makedirs(OUTDIR,exist_ok=True);lines=['WA_PROGRAM','VERSION=3','']
    for p in s.plan.placements:lines.append(f'CUT X={p.x:.0f} Y={p.y:.0f} LX={p.w:.0f} LY={p.h:.0f} T=1 B=0 D={p.part_name}')
    path=f'{OUTDIR}/altendorf.wa';open(path,'w').write('\n'.join(lines))
    return s.model_copy(update={'plan':s.plan.model_copy(update={'cnc_paths':s.plan.cnc_paths+[path]})})
