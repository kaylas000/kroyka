"""
B08 - Guillotine Packer
Чистый Python гильотинный алгоритм без внешних зависимостей
Размещает детали на листах, учитывая направление волокна.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState, PlacedPart, CutPlan, GrainDir
from typing import List, Tuple, Optional

class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

def guillotine_pack(sheet_w, sheet_h, items):
    """
    items: list of (id, w, h, grain, can_rotate)
    returns: list of (id, x, y, w, h, rotated), unplaced ids
    """
    free = [Rect(0, 0, sheet_w, sheet_h)]
    placed = []
    unplaced = []

    def best_fit(w, h):
        best = None
        best_area = float('inf')
        best_idx = -1
        for i, r in enumerate(free):
            if r.w >= w and r.h >= h:
                waste = r.w * r.h - w * h
                if waste < best_area:
                    best_area = waste
                    best = r
                    best_idx = i
        return best_idx, best

    def split(r, w, h):
        # Горизонтальный разрез
        r1 = Rect(r.x + w, r.y, r.w - w, h)       # прав
        r2 = Rect(r.x, r.y + h, r.w, r.h - h)     # низ
        result = []
        if r1.w > 0 and r1.h > 0:
            result.append(r1)
        if r2.w > 0 and r2.h > 0:
            result.append(r2)
        return result

    for (pid, pw, ph, grain, can_rotate) in items:
        placed_flag = False
        candidates = [(pw, ph, False)]
        if can_rotate and grain == GrainDir.ANY:
            candidates.append((ph, pw, True))

        for (tw, th, rotated) in candidates:
            idx, r = best_fit(tw, th)
            if r is not None:
                placed.append((pid, r.x, r.y, tw, th, rotated))
                new_rects = split(r, tw, th)
                free.pop(idx)
                free.extend(new_rects)
                placed_flag = True
                break

        if not placed_flag:
            unplaced.append(pid)

    return placed, unplaced


def run(state: PipelineState) -> PipelineState:
    if not state.sheets:
        return state.model_copy(update={'errors': state.errors + ['B08: no sheets defined']})

    all_placements: List[PlacedPart] = []
    all_unplaced: List[str] = []
    total_area_used = 0.0
    total_sheet_area = 0.0
    sheet_counter = 0

    # Группируем детали по материалу
    mat_parts = {}
    for p in state.raw_parts:
        mat_parts.setdefault(p.material, []).append(p)

    for sheet in state.sheets:
        parts = mat_parts.get(sheet.material, [])
        # Разворачиваем qty
        items = []
        for p in parts:
            for i in range(p.qty):
                items.append((f'{p.name}#{i}', p.w, p.h, p.grain, True))

        while items:
            sw, sh = sheet.w, sheet.h
            total_sheet_area += sw * sh
            placed, items = guillotine_pack(sw, sh, items)
            for (pid, x, y, w, h, rotated) in placed:
                base_name = pid.rsplit('#', 1)[0]
                all_placements.append(PlacedPart(
                    part_name=base_name,
                    sheet_idx=sheet_counter,
                    x=x, y=y, w=w, h=h,
                    rotated=rotated,
                ))
                total_area_used += w * h
            sheet_counter += 1
            if not placed:  # нет прогресса
                all_unplaced.extend(pid for (pid, *_) in items)
                break

    eff = (total_area_used / total_sheet_area) if total_sheet_area > 0 else 0.0
    plan = CutPlan(
        sheets_used=sheet_counter,
        efficiency=round(eff, 4),
        placements=all_placements,
        unplaced=all_unplaced,
    )
    return state.model_copy(update={'plan': plan})
