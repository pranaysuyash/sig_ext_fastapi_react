# Tools

Reusable helpers for local exploration and validation.

## PDF fixtures

- `generate_native_form_fixture.py`: generates a reusable AcroForm benchmark PDF with text, checkbox, dropdown, and radio widgets.
- `generate_parser_benchmark_corpus.py`: generates the broader parser benchmark corpus.
- `compare_parser_baselines.py`: prints the current parser comparison matrix.

Usage:

```bash
./.venv/bin/python tools/generate_native_form_fixture.py
./.venv/bin/python tools/generate_parser_benchmark_corpus.py
./.venv/bin/python tools/compare_parser_baselines.py
```
