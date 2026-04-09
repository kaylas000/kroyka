"""
orthestrator.py - Главный пайплайн мультиагентной системы раскроя
B01 -> B02 -> B03 -> B04 -> B05 -> B06 -> B07 -> B08 -> B09 -> B10
     -> B11 -> B12 -> B13 -> B14 -> B15 -> B16 -> B17 -> B18
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kroyka.models import PipelineState
from kroyka.agents import (
    b01_order_parser, b02_dim_validator, b03_dedup,
    b04_sorter, b05_stock_picker, b06_kerf, b07_labeler,
    b08_packer, b09_svg_gen, b10_efficiency,
    b11_cnc_holzma, b12_cnc_biesse, b13_cnc_altendorf,
    b14_cnc_scm, b15_cnc_gcode, b16_report, b17_cost, b18_finalizer
)

PIPELINE = [
    ('B01 OrderParser',   b01_order_parser.run),
    ('B02 DimValidator',  b02_dim_validator.run),
    ('B03 Dedup',         b03_dedup.run),
    ('B04 Sorter',        b04_sorter.run),
    ('B05 StockPicker',   b05_stock_picker.run),
    ('B06 Kerf',          b06_kerf.run),
    ('B07 Labeler',       b07_labeler.run),
    ('B08 Packer',        b08_packer.run),
    ('B09 SVGGen',        b09_svg_gen.run),
    ('B10 Efficiency',    b10_efficiency.run),
    ('B11 Holzma',        b11_cnc_holzma.run),
    ('B12 Biesse',        b12_cnc_biesse.run),
    ('B13 Altendorf',     b13_cnc_altendorf.run),
    ('B14 SCM',           b14_cnc_scm.run),
    ('B15 GCode',         b15_cnc_gcode.run),
    ('B16 Report',        b16_report.run),
    ('B17 Cost',          b17_cost.run),
    ('B18 Finalizer',     b18_finalizer.run),
]

def run_pipeline(csv_path: str, kerf: float = 4.0, verbose: bool = True) -> PipelineState:
    csv_content = open(csv_path, 'r', encoding='utf-8').read()
    state = PipelineState(order_csv=csv_content)
    for name, agent_fn in PIPELINE:
        try:
            state = agent_fn(state)
            if verbose:
                errs = len(state.errors)
                print(f'  [{name}] OK | errors={errs}')
            if state.errors:
                # останавливаемся только на критических ошибках
                if name in ('B01 OrderParser', 'B02 DimValidator'):
                    if verbose:
                        print(f'  CRITICAL errors in {name}, stopping: {state.errors}')
                    break
        except Exception as e:
            state.errors.append(f'{name} EXCEPTION: {e}')
            if verbose:
                print(f'  [{name}] EXCEPTION: {e}')
    return state

if __name__ == '__main__':
    import json
    csv = sys.argv[1] if len(sys.argv) > 1 else 'kroyka/tests/test_order.csv'
    print(f'Running pipeline for: {csv}')
    result = run_pipeline(csv)
    if result.plan:
        print(f'\nResult: {result.plan.sheets_used} sheets, efficiency={result.plan.efficiency*100:.1f}%')
        print(f'Placements: {len(result.plan.placements)}, Unplaced: {len(result.plan.unplaced)}')
        print(f'SVG: {result.plan.svg_paths}')
        print(f'CNC: {result.plan.cnc_paths}')
    print(f'Warnings ({len(result.warnings)}): {result.warnings[-3:]}')
    print(f'Errors ({len(result.errors)}): {result.errors}')
