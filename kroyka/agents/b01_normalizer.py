from kroyka.models import PipelineState, RawPart

def run(state: PipelineState) -> PipelineState:
    normalized = []
    for part in (state.raw_parts or []):
        p = part.dict() if hasattr(part, 'dict') else dict(part)
        # Round w/h to int mm
        if 'length' in p and 'w' not in p:
            p['w'] = int(round(float(p.pop('length', 0))))
        else:
            p['w'] = int(round(float(p.get('w', 0) or 0)))
        if 'width' in p and 'h' not in p:
            p['h'] = int(round(float(p.pop('width', 0))))
        else:
            p['h'] = int(round(float(p.get('h', 0) or 0)))
        p.setdefault('qty', 1)
        p.setdefault('material', 'default')
        normalized.append(RawPart(**{k: v for k, v in p.items() if k in RawPart.__fields__}))
    state.raw_parts = normalized
    return state

if __name__ == '__main__':
    s = PipelineState(raw_parts=[{
        'name': 'Part1', 'w': 1220, 'h': 2440,
        'qty': 1, 'material': 'LDSP'
    }])
    print('b01 ok:', run(s).raw_parts)
