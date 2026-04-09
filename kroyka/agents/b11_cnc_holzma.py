"""B11 - CNC Postprocessor Holzma HPL format"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState
import os as _os

OUTDIR = '/tmp/kroyka_cnc'

def run(state: PipelineState) -> PipelineState:
    if not state.plan: return state
    _os.makedirs(OUTDIR, exist_ok=True)
    lines = ['% HOLZMA HPL', f'% Sheets: {state.plan.sheets_used}', f'% Efficiency: {state.plan.efficiency*100:.1f}%', '']
    for p in state.plan.placements:
        lines.append(f'PART "{p.part_name}" X={p.x:.1f} Y={p.y:.1f} W={p.w:.1f} H={p.h:.1f} SHEET={p.sheet_idx}')
    path = f'{OUTDIR}/holzma.hpl'
    with open(path, 'w') as f: f.write('\n'.join(lines))
    new_plan = state.plan.model_copy(update={'cnc_paths': state.plan.cnc_paths + [path]})
    return state.model_copy(update={'plan': new_plan})
