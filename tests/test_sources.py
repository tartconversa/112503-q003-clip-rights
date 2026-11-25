"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'assets.csv': ['asset', 'kind', 'duration', 'copyright_case'], 'edges.csv': ['parent', 'layer', 'source', 'source_from', 'source_to', 'target_from', 'target_to'], 'rights.csv': ['grant', 'case', 'market', 'channel', 'start', 'stop', 'segment_from', 'segment_to', 'parties', 'shares', 'rev'], 'placements.csv': ['placement', 'asset', 'channel', 'market', 'live_from', 'live_until', 'state'], 'plays.csv': ['event', 'placement', 'platform_key', 'start', 'end', 'valid_count'], 'inflows.csv': ['receipt', 'play_group', 'cents', 'date', 'refunds', 'market'], 'paid.csv': ['payment', 'month', 'receipt', 'party', 'cents', 'rights_rev'], 'layer_weights.csv': ['market', 'channel', 'layer', 'share_bp', 'from_day', 'to_day']}
REFERENCES = [('edges.csv', 'parent', 'assets.csv', 'asset'), ('edges.csv', 'source', 'assets.csv', 'asset'), ('rights.csv', 'case', 'assets.csv', 'copyright_case'), ('placements.csv', 'asset', 'assets.csv', 'asset'), ('plays.csv', 'placement', 'placements.csv', 'placement'), ('inflows.csv', 'play_group', 'plays.csv', 'event'), ('paid.csv', 'receipt', 'inflows.csv', 'receipt')]
OBSERVED_VALUES = [('rights.csv', 'grant', 'G1', 2), ('plays.csv', 'platform_key', 'key-1', 2), ('inflows.csv', 'play_group', 'V2', 2)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
