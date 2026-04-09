"""B14 - SCM CUT format"""
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState;OUTDIR='/tmp/kroyka_cnc'
def run(s):
    if not s.plan:return s
    os.makedirs(OUTDIR,exist_ok=True);lines=['[SCM_PROGRAM]','']
    for p in s.plan.placements:lines.append(f'PIECE "{p.part_name}" {p.x:.0f} {p.y:.0f} {p.w:.0f} {p.h:.0f} {p.sheet_idx}')
    path=f'{OUTDIR}/scm.cut';open(path,'w').write('\n'.join(lines))
    return s.model_copy(update={'plan':s.plan.model_copy(update={'cnc_paths':s.plan.cnc_paths+[path]})})
