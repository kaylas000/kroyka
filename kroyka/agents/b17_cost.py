"""B17 - Cost Calculator: считает стоимость материалов"""
import sys,os;sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..'));from kroyka.models import PipelineState
def run(s):
    if not s.plan:return s
    total=0.0
    for sheet in s.sheets:
        used=len({p.sheet_idx for p in s.plan.placements})
        total+=sheet.cost_per_sheet*used
    warnings=list(s.warnings)
    warnings.append(f'B17: Material cost estimate: {total:.2f} RUB ({s.plan.sheets_used} sheets)')
    return s.model_copy(update={'warnings':warnings})
