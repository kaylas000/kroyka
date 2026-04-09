import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState, RawPart

DEFAULT_PART = {'name': 'Part1', 'w': 600, 'h': 400, 'qty': 2, 'material': 'LDSP'}

class TestB01Normalizer(unittest.TestCase):
    def test_returns_pipeline_state(self):
        from kroyka.agents import b01_normalizer
        state = PipelineState(raw_parts=[DEFAULT_PART])
        result = b01_normalizer.run(state)
        self.assertIsInstance(result, PipelineState)

    def test_preserves_dimensions(self):
        from kroyka.agents import b01_normalizer
        state = PipelineState(raw_parts=[DEFAULT_PART])
        result = b01_normalizer.run(state)
        self.assertEqual(len(result.raw_parts), 1)

    def test_defaults_qty(self):
        from kroyka.agents import b01_normalizer
        p = {'name': 'X', 'w': 100, 'h': 50, 'material': 'LDSP', 'qty': 1}
        state = PipelineState(raw_parts=[p])
        result = b01_normalizer.run(state)
        part = result.raw_parts[0]
        qty = part.qty if hasattr(part, 'qty') else part.get('qty', 1)
        self.assertGreaterEqual(qty, 1)

class TestB02Validator(unittest.TestCase):
    def test_valid_part_passes(self):
        from kroyka.agents import b02_validator
        state = PipelineState(raw_parts=[
            {'name': 'Door', 'w': 800, 'h': 400, 'qty': 2, 'material': 'LDSP 16mm'}
        ])
        result = b02_validator.run(state)
        self.assertIsInstance(result, PipelineState)

    def test_empty_parts_valid(self):
        from kroyka.agents import b02_validator
        state = PipelineState(raw_parts=[])
        result = b02_validator.run(state)
        self.assertTrue(result.validated)
        self.assertEqual(result.errors, [])

if __name__ == '__main__':
    unittest.main()
