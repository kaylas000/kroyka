"""B09 - SVG Generator: генерирует SVG карты раскроя (чистый Python, без svgwrite)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState
from typing import List
import os as _os

OUTPUT_DIR = '/tmp/kroyka_svg'

COLORS = ['#AED6F1','#A9DFBF','#F9E79F','#F1948A','#D2B4DE',
          '#AEB6BF','#FAD7A0','#A3E4D7','#F8C471','#85C1E9']

def run(state: PipelineState) -> PipelineState:
    if not state.plan:
        return state
    _os.makedirs(OUTPUT_DIR, exist_ok=True)
    plan = state.plan
    sheets_data = {}
    for p in plan.placements:
        sheets_data.setdefault(p.sheet_idx, []).append(p)

    svg_paths = []
    for sheet_idx, parts in sorted(sheets_data.items()):
        sheet = state.sheets[0] if state.sheets else None
        sw = sheet.w if sheet else 2800
        sh = sheet.h if sheet else 2070
        scale = 0.2
        W = int(sw * scale)
        H = int(sh * scale)
        lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
        lines.append(f'<rect width="{W}" height="{H}" fill="#FDFEFE" stroke="#333" stroke-width="1"/>')
        for i, pp in enumerate(parts):
            color = COLORS[i % len(COLORS)]
            x = pp.x * scale
            y = pp.y * scale
            w = pp.w * scale
            h = pp.h * scale
            lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{color}" stroke="#555" stroke-width="0.5" opacity="0.85"/>')
            cx, cy = x + w/2, y + h/2
            label = pp.label or pp.part_name[:8]
            lines.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="6" text-anchor="middle" dominant-baseline="middle" fill="#1A1A1A">{label}</text>')
        lines.append('</svg>')
        path = f'{OUTPUT_DIR}/sheet_{sheet_idx:03d}.svg'
        with open(path, 'w') as f:
            f.write('\n'.join(lines))
        svg_paths.append(path)
    new_plan = plan.model_copy(update={'svg_paths': svg_paths})
    return state.model_copy(update={'plan': new_plan})
