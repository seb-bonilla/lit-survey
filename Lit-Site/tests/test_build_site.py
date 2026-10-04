import importlib.util
from pathlib import Path
import tempfile
import unittest
import json

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("site_export", ROOT / "build_site.py")
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class SiteExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.book = self.root / "private.xlsx"

    def save(self, rows):
        wb = Workbook()
        wb.active.title = "Main"
        for row in rows:
            wb.active.append(row)
        wb.create_sheet("Papers").append(["Private paper metadata"])
        wb.save(self.book)
        wb.close()

    def test_narrative_order_and_private_workbook_preserved(self):
        self.save([["Survey"], ["Section"], [None, "Intro"], ["Subsection", "First"], [None, "Second"], ["Next section"]])
        before = self.book.read_bytes()
        output = site.export(self.book, docs_dir=self.root / "docs")
        content = output.read_text()
        self.assertIn("# Survey", content)
        self.assertIn("## Section", content)
        self.assertIn("### Subsection", content)
        self.assertLess(content.index("Intro"), content.index("First"))
        self.assertLess(content.index("First"), content.index("Second"))
        self.assertNotIn("Private paper", content)
        self.assertEqual(before, self.book.read_bytes())

    def test_missing_figure_does_not_overwrite_existing_page(self):
        self.save([["Survey"], ["Section", None, "Figure 1"]])
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("Keep this")
        with self.assertRaises(ValueError):
            site.export(self.book, docs_dir=docs)
        self.assertEqual((docs / "index.md").read_text(), "Keep this")

    def test_explicit_omission_and_relative_asset_copy(self):
        self.save([["Survey"], ["Section"], [None, "Text", "Figure 1"], [None, None, "Figure 2"]])
        content = site.export(self.book, docs_dir=self.root / "plain", skip_figures=True).read_text()
        self.assertIn("Figure 2 omitted", content)
        (self.root / "plot.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        (self.root / "plot.html").write_text("<html>plot</html>")
        mapping = self.root / "figures.json"
        mapping.write_text(json.dumps({"Figure 1": {"file": "plot.svg", "caption": "Comparison"}, "Figure 2": {"file": "plot.html", "caption": "Interactive"}}))
        docs = self.root / "docs"
        content = site.export(self.book, docs_dir=docs, mapping=mapping).read_text()
        self.assertIn("assets/figures/figure1.svg", content)
        self.assertIn("<iframe", content)
        self.assertTrue((docs / "assets/figures/figure2.html").is_file())

    def test_formula_and_missing_main_fail_explicitly(self):
        self.save([["Survey"], [None, "=1+2"]])
        with self.assertRaisesRegex(ValueError, "formula"):
            site.export(self.book, docs_dir=self.root / "docs")
        with self.assertRaisesRegex(ValueError, "not found"):
            site.export(self.book, sheet="Absent", docs_dir=self.root / "docs")


if __name__ == "__main__":
    unittest.main()
