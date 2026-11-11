# APCD-CDL

Structured source for the APCD Common Data Layout (APCD-CDL), maintained by the APCD Council. This repository holds APCD-CDL version 4.0.1 and the CMS-to-CDL crosswalk.

- `source/files/` one CSV of elements for each file in the layout (HD, TR, ME, MC, PC, DC, PV, AP, PR, CF), with the file's introductory text beside it as Markdown
- `source/codesets/` code sets referenced by elements: insurance type/product (Appendix J) and market category (Appendix K)
- `source/reference/` external code sources (Appendix L)
- `source/frontmatter/` the title page, copyright notice, acknowledgments, introduction, purpose, and technical specifications
- `source/manifest.csv` the published structure, one row per section, with its heading, table title, and reference column header
- `crosswalks/cms-ccw-rif/` the CMS-to-CDL crosswalk
- `scripts/check_integrity.py` checks that element ids are well formed and that every crosswalk `element_id` exists in the spec. Run it from the repository root with `python3 scripts/check_integrity.py`.

There is no build step. Files are read here on GitHub, CSVs as tables and prose as Markdown. Every element is keyed by its `element_id`, for example CDLMC121.

## Reading the CSVs in source/files/

There is one CSV for each CDL file and one row for each data element. The columns mirror the columns of the published tables.

- `element_id` is Element #.
- `element_name` is Element Name.
- `type` is Type.
- `max_length` is Max Length.
- `description` is the published description column, headed "Description/ Codes/ Sources" or "Description/ Valid Values".
- `source_reference` is the X12 or NCPDP reference column. It is present in ME, MC, PC, and DC only. Its published header is in `source/manifest.csv`.

The CSVs carry no columns beyond the published ones. References to code sets (Appendices J and K) and to external code sources (Appendix L) stay in the description text, as published.

## Versions

Each published version is a git tag, and its GitHub Release carries the published PDF. `CHANGELOG.md` says what changed in each version and why. The APCD Council website remains the main download for the published layout.

The content is the layout as published, including known errors. Corrections go through the APCD-CDL maintenance process and appear in a later version.

## Copyright and use

APCD-CDL™ is licensed by the National Association of Health Data Organizations (NAHDO) and the University of New Hampshire. Commercial use of APCD-CDL™ requires written approval. Questions about commercial use go to info@nahdo.org. See `NOTICE`.

For citation and attribution, see the [APCD Council Attribution Policy](https://www.apcdcouncil.org/attribution-policy).
