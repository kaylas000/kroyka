"""
B01 - Order Parser
Читает CSV заказа и возвращает список RawPart
Формат CSV: name,qty,w,h,material,grain,edge_t,edge_b,edge_l,edge_r
"""
import csv, io, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import RawPart, GrainDir, PipelineState
from typing import List

GRAIN_MAP = {'along': GrainDir.ALONG, 'across': GrainDir.ACROSS,
             'any': GrainDir.ANY, '': GrainDir.ANY,
             'вдоль': GrainDir.ALONG, 'поперек': GrainDir.ACROSS}

def run(state: PipelineState) -> PipelineState:
    """Парсит order_csv -> raw_parts"""
    parts: List[RawPart] = []
    errors = list(state.errors)
    try:
        reader = csv.DictReader(io.StringIO(state.order_csv))
        for i, row in enumerate(reader, start=2):
            try:
                grain_raw = row.get('grain', 'any').strip().lower()
                grain = GRAIN_MAP.get(grain_raw, GrainDir.ANY)
                part = RawPart(
                    name=row['name'].strip(),
                    qty=int(row['qty']),
                    w=float(row['w']),
                    h=float(row['h']),
                    material=row['material'].strip(),
                    grain=grain,
                    edge_top=float(row.get('edge_t', 0) or 0),
                    edge_bottom=float(row.get('edge_b', 0) or 0),
                    edge_left=float(row.get('edge_l', 0) or 0),
                    edge_right=float(row.get('edge_r', 0) or 0),
                    label=row.get('label', '').strip(),
                )
                parts.append(part)
            except Exception as e:
                errors.append(f'B01 row {i}: {e}')
    except Exception as e:
        errors.append(f'B01 CSV parse error: {e}')
    new = state.model_copy(update={'raw_parts': parts, 'errors': errors})
    return new
