import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch, Mock

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('converter', REPO / 'Py-tools' / 'convert_pdfs.py')
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)

class ConversionFallbackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.page_count = patch.object(converter, 'pdf_page_count', return_value=1)
        self.page_count.start()
        self.addCleanup(self.page_count.stop)

    def papers(self, *names):
        for name in names:
            (self.folder / (name + '.pdf')).write_bytes(b'fixture')

    def run_batch(self):
        return converter.convert_folder(self.folder, dry_run=False, overwrite=False)

    def test_anydoc_success_never_loads_docling(self):
        self.papers('paper')
        with patch.object(converter, 'load_anydoc', return_value=types.SimpleNamespace(to_markdown=lambda _: '# Evidence')), patch.object(converter, 'load_docling_converter') as loader:
            self.assertEqual(self.run_batch(), 0)
            loader.assert_not_called()
        self.assertEqual((self.folder / 'markdown' / 'paper.md').read_text(), '# Evidence')

    def test_failed_and_empty_anydoc_use_one_lazy_fallback(self):
        self.papers('a', 'b')
        anydoc = types.SimpleNamespace(to_markdown=Mock(side_effect=[RuntimeError('OCR required'), '  ']))
        with patch.object(converter, 'load_anydoc', return_value=anydoc), patch.object(converter, 'load_docling_converter', return_value=object()) as loader, patch.object(converter, 'convert_with_docling', return_value='# OCR evidence') as fallback:
            self.assertEqual(self.run_batch(), 0)
            loader.assert_called_once()
            self.assertEqual(fallback.call_count, 2)
        self.assertEqual(len(list((self.folder / 'markdown').glob('*.md'))), 2)

    def test_missing_models_do_not_block_later_anydoc_success(self):
        self.papers('a', 'b', 'c')
        anydoc = types.SimpleNamespace(to_markdown=Mock(side_effect=[RuntimeError('scan'), RuntimeError('scan'), 'Text evidence']))
        with patch.object(converter, 'load_anydoc', return_value=anydoc), patch.object(converter, 'load_docling_converter', side_effect=RuntimeError('models missing')) as loader:
            self.assertEqual(self.run_batch(), 1)
            loader.assert_called_once()
        self.assertFalse((self.folder / 'markdown' / 'a.md').exists())
        self.assertEqual((self.folder / 'markdown' / 'c.md').read_text(), 'Text evidence')

    def test_save_failure_does_not_trigger_ocr(self):
        self.papers('paper')
        with patch.object(converter, 'load_anydoc', return_value=types.SimpleNamespace(to_markdown=lambda _: 'Text')), patch.object(converter, 'write_markdown_atomic', side_effect=OSError('disk full')), patch.object(converter, 'load_docling_converter') as loader:
            self.assertEqual(self.run_batch(), 1)
            loader.assert_not_called()

    def test_existing_markdown_preserved_without_loading_converters(self):
        self.papers('paper')
        (self.folder / 'markdown').mkdir()
        output = self.folder / 'markdown' / 'paper.md'
        output.write_text('Checked evidence')
        with patch.object(converter, 'load_anydoc') as loader:
            self.assertEqual(self.run_batch(), 0)
            loader.assert_not_called()
        self.assertEqual(output.read_text(), 'Checked evidence')

if __name__ == '__main__':
    unittest.main()

