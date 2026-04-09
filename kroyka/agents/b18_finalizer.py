"""B18 - Finalizer: проверяет полноту плана и выставляет финальный статус"""
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState
def run(s):
    warnings=list(s.warnings)
    errors=list(s.errors)
    if s.plan and s.plan.unplaced:
        errors.append(f'B18: {len(s.plan.unplaced)} parts could not be placed: {s.plan.unplaced[:5]}')
    if s.plan:
        warnings.append(f'B18 DONE: {s.plan.sheets_used} sheets, efficiency={s.plan.efficiency*100:.1f}%, svg={len(s.plan.svg_paths)}, cnc={len(s.plan.cnc_paths)}')
    else:
        errors.append('B18: No cut plan generated!')
    return s.model_copy(update={'warnings':warnings,'errors':errors})
