"""
Тесты пайплайна раскроя kroyka
for Python unittest (without pytest)
"""
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from kroyka.models import PipelineState, RawPart, GrainDir, Sheet
from kroyka.agents import b01_order_parser, b02_dim_validator, b03_dedup
from kroyka.agents import b04_sorter, b05_stock_picker, b06_kerf, b07_labeler
from kroyka.agents import b08_packer, b10_efficiency, b18_finalizer

CSV_PATH = os.path.join(os.path.dirname(__file__), 'test_order.csv')

class TestModels(unittest.TestCase):
    def test_raw_part_creation(self):
        p = RawPart(name='Тест', qty=2, w=600, h=400, material='ЛДСП')
        self.assertEqual(p.name, 'Тест')
        self.assertEqual(p.qty, 2)

    def test_pipeline_state(self):
        s = PipelineState()
        self.assertEqual(s.errors, [])
        self.assertEqual(s.raw_parts, [])

class TestB01Parser(unittest.TestCase):
    def test_parse_csv(self):
        csv = 'name,qty,w,h,material,grain\nПолка,3,500,300,ЛДСП,any'
        s = PipelineState(order_csv=csv)
        s2 = b01_order_parser.run(s)
        self.assertEqual(len(s2.raw_parts), 1)
        self.assertEqual(s2.raw_parts[0].name, 'Полка')
        self.assertEqual(s2.raw_parts[0].qty, 3)

    def test_empty_csv(self):
        s = PipelineState(order_csv='name,qty,w,h,material\n')
        s2 = b01_order_parser.run(s)
        self.assertEqual(len(s2.raw_parts), 0)

class TestB02Validator(unittest.TestCase):
    def test_negative_dim(self):
        p = RawPart(name='x', qty=1, w=-10, h=100, material='ЛДСП')
        s = PipelineState(raw_parts=[p])
        s2 = b02_dim_validator.run(s)
        self.assertTrue(any('B02' in e for e in s2.errors))

    def test_valid_part(self):
        p = RawPart(name='x', qty=1, w=600, h=400, material='ЛДСП')
        s = PipelineState(raw_parts=[p])
        s2 = b02_dim_validator.run(s)
        self.assertEqual(s2.errors, [])

class TestB08Packer(unittest.TestCase):
    def test_basic_packing(self):
        parts = [RawPart(name=f'p{i}', qty=1, w=500, h=400, material='ЛДСП') for i in range(4)]
        sheet = Sheet(material='ЛДСП', w=2800, h=2070, qty=10)
        s = PipelineState(raw_parts=parts, sheets=[sheet])
        s2 = b08_packer.run(s)
        self.assertIsNotNone(s2.plan)
        self.assertGreater(len(s2.plan.placements), 0)
        self.assertEqual(len(s2.plan.unplaced), 0)

    def test_efficiency_above_50pct(self):
        parts = [RawPart(name=f'big{i}', qty=1, w=1200, h=1000, material='ЛДСП') for i in range(4)]
        sheet = Sheet(material='ЛДСП', w=2800, h=2070, qty=10)
        s = PipelineState(raw_parts=parts, sheets=[sheet])
        s2 = b08_packer.run(s)
        s3 = b10_efficiency.run(s2)
        self.assertGreater(s3.plan.efficiency, 0.5)

class TestFullPipeline(unittest.TestCase):
    def test_full_run(self):
        from kroyka.orchestrator import run_pipeline
        result = run_pipeline(CSV_PATH, verbose=False)
        self.assertIsNotNone(result.plan)
        self.assertGreater(result.plan.sheets_used, 0)
        self.assertGreater(len(result.plan.placements), 0)
        self.assertEqual(result.errors, [])

    def test_efficiency_reasonable(self):
        from kroyka.orchestrator import run_pipeline
        result = run_pipeline(CSV_PATH, verbose=False)
        self.assertGreater(result.plan.efficiency, 0.3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
