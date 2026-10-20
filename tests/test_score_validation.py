"""Boundary and saved-response validation checks using synthetic data only."""
import contextlib
import csv
import importlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
score = importlib.import_module('score')


class ValidationTests(unittest.TestCase):
    def test_inclusive_boundaries(self):
        self.assertEqual(score.decide(.62, .41, True), 'REPRODUCED')
        self.assertEqual(score.decide(.82, .61, True), 'REPRODUCED')
        self.assertEqual(score.decide(.619999, .41, True), 'NOT REPRODUCED')
        self.assertEqual(score.decide(.82, .610001, True), 'NOT REPRODUCED')

    def run_case(self, mode):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'reference').mkdir()
            run = root / 'runs' / 'synthetic'
            run.mkdir(parents=True)
            with (root / 'reference/labels.csv').open('w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['case_id', 'label'])
                w.writerows([(str(i), 'Task' if i % 2 else 'Obvious') for i in range(1, 6)])
            for i in range(1, 6):
                item = {'case_id': str(i), 'predicted_label': 'Task' if i % 2 else 'Obvious',
                        'context_sufficient': True, 'reason': 'Synthetic test.'}
                items = [item]
                if i == 1:
                    if mode == 'unexpected':
                        items.append(dict(item, case_id='unknown'))
                    elif mode == 'missing':
                        items = []
                    elif mode == 'duplicate':
                        items.append(item.copy())
                    elif mode == 'invalid_label':
                        item['predicted_label'] = 'unknown'
                    elif mode == 'wrong_type':
                        item['context_sufficient'] = 'true'
                path = run / f'batch_{i:02d}.txt'
                path.write_text(json.dumps(items), encoding='utf-8')
            if mode == 'missing_file':
                (run / 'batch_01.txt').unlink()
            elif mode == 'malformed':
                (run / 'batch_01.txt').write_text('not JSON', encoding='utf-8')
            with patch.object(score, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                score.main(run)
            out = root / 'results/synthetic'
            result = json.loads((out / 'metrics.json').read_text())
            if mode == 'valid':
                self.assertEqual(result['accuracy'], 1)
                self.assertEqual(result['mcc'], 1)
                self.assertTrue((out / 'repair_candidates.csv').exists())
            else:
                self.assertEqual(result['decision'], 'INCONCLUSIVE')

    def test_valid_saved_run(self):
        self.run_case('valid')

    def test_bad_saved_runs(self):
        for mode in ['unexpected', 'missing', 'duplicate', 'invalid_label',
                     'wrong_type', 'missing_file', 'malformed']:
            with self.subTest(mode=mode):
                self.run_case(mode)
