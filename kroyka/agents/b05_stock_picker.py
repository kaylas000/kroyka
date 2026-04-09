"""B05 - Stock Picker: подбирает листы из стока для каждого материала"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState, Sheet
from typing import List

# Сток по умолчанию — стандартные листы 2800x2070
DEFAULT_SHEETS = {
    'ЛДСП': Sheet(material='ЛДСП', w=2800.0, h=2070.0, qty=999),
    'МДФ': Sheet(material='МДФ', w=2800.0, h=2070.0, qty=999),
    'ФСФ': Sheet(material='ФСФ', w=2440.0, h=1220.0, qty=999),
}

def run(state: PipelineState) -> PipelineState:
    if state.sheets:
        return state  # уже заданы
    materials = {p.material for p in state.raw_parts}
    sheets: List[Sheet] = []
    warnings = list(state.warnings)
    for mat in sorted(materials):
        if mat in DEFAULT_SHEETS:
            sheets.append(DEFAULT_SHEETS[mat])
        else:
            # универсальный лист
            sheets.append(Sheet(material=mat, w=2800.0, h=2070.0, qty=999))
            warnings.append(f'B05: unknown material {mat!r}, using default 2800x2070')
    return state.model_copy(update={'sheets': sheets, 'warnings': warnings})
