"""B15 - Generic G-code postprocessor"""
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState;OUTDIR='/tmp/kroyka_cnc'
def run(s):
    if not s.plan:return s
    os.makedirs(OUTDIR,exist_ok=True)
    lines=['G21','G90','G17','']
    for i,p in enumerate(s.plan.placements):
        lines+=[f'; Part: {p.part_name} Sheet:{p.sheet_idx}',f'G0 X{p.x:.2f} Y{p.y:.2f}',f'G1 X{p.x+p.w:.2f} Y{p.y:.2f} F3000',f'G1 X{p.x+p.w:.2f} Y{p.y+p.h:.2f}',f'G1 X{p.x:.2f} Y{p.y+p.h:.2f}',f'G1 X{p.x:.2f} Y{p.y:.2f}','']
    lines+=['M30']
    path=f'{OUTDIR}/cut.gcode';open(path,'w').write('\n'.join(lines))
    return s.model_copy(update={'plan':s.plan.model_copy(update={'cnc_paths':s.plan.cnc_paths+[path]})})
