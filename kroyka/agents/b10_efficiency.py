"""B10 - Efficiency Calculator: считает % использования листа и отходы"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    if not state.plan or not state.sheets:
        return state
    plan = state.plan
    total_parts_area = sum(p.w * p.h for p in plan.placements)
    total_sheet_area = 0.0
    for s in state.sheets:
        # учитываем кол-во использованных листов для данного материала
        used_sheets = len({p.sheet_idx for p in plan.placements})
        total_sheet_area += s.w * s.h * used_sheets
        break  # упрощение: один тип листа
    eff = total_parts_area / total_sheet_area if total_sheet_area > 0 else 0.0
    waste_pct = round((1 - eff) * 100, 2)
    warnings = list(state.warnings)
    if eff < 0.7:
        warnings.append(f'B10: LOW efficiency {eff*100:.1f}% (waste {waste_pct}%)')
    new_plan = plan.model_copy(update={'efficiency': round(eff, 4)})
    return state.model_copy(update={'plan': new_plan, 'warnings': warnings})
