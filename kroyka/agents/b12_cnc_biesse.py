"""B12 - CNC Postprocessor Biesse BPP format"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState
OUTDIR='/tmp/kroyka_cnc'
def run(state):
    if not state.plan: return state
    os.makedirs(OUTDIR,exist_ok=True)
    lines=['[BIESSE BPP]',f'SHEETS={state.plan.sheets_used}','']
    for p in state.plan.placements:
        lines.append(f'REC X={p.x:.1f};Y={p.y:.1f};W={p.w:.1f};H={p.h:.1f};ID="{p.part_name}";SH={p.sheet_idx}')
    path=f'{OUTDIR}/biesse.bpp'
    open(path,'w').write('\n'.join(lines))
    return state.model_copy(update={'plan':state.plan.model_copy(update={'cnc_paths':state.plan.cnc_paths+[path]})})
