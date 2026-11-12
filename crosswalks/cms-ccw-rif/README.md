# CMS-to-CDL crosswalk (CCW RIF)

Maps CMS Medicare fee-for-service Research Identifiable Files (CCW RIF, distributed through ResDAC) to APCD-CDL v4.0.1.

## Version

Version 1.0, October 2026, imported from the final mapping workbook. Built against these reference versions:

| Reference file | Code book | Record layout |
|---|---|---|
| APCD-CDL | Version 4.0.1, 2/2025 | |
| Medical claims | Version L, 8/2026, Version 1.17 | Version 2, 7/2026 |
| Eligibility (beneficiary file) | Version 2, 5/2026, Version 1.2 | Version 2, 3/2025 |
| Part D Event | 10/2025, Version 1.9 | 7/2025 |

## Contents

- `source/` the crosswalk, one CSV per CDL file: `me-member-eligibility.csv`, `mc-medical-claims.csv`, `pc-pharmacy-claims.csv`

## Reading the tables

- In the CDL, Medical Claims is one row per service line whatever the claim type. The RIF splits Medicare claims into separate files by claim type (inpatient, outpatient, SNF, hospice, home health, carrier, DME), and the same CDL element can come from a different variable in each. So ME and PC have one row per CDL element, and MC has one row per CDL element per RIF source file. The MC key is `element_id` + `rif_file` + `rif_file_part`.
- `rif_file_part` (Base, Revenue, Line) and `rif_short_sas_name` apply to MC only. In `rif_file`, `hop` is the outpatient file.
- In MC, a `rif_file` value can stand for a group of claim files. `All` means all seven claim-type files use the same variable, so the element has one row instead of seven. `All other` means the five facility files (inpatient, outpatient, SNF, hospice, home health), which are not listed one by one. Carrier and DME have their own rows for those elements. It is used for Line Counter (CDLMC006) and ICD Version Indicator (CDLMC036), and appears as both `All other` and `All Other` in this version.
- `MBSF`, `bene_name crosswalk`, `bene_ssn crosswalk`, and `bene_mbi crosswalk` name single CMS files, the ones of those names on the release workbook's Required CMS Files tab. Their casing differs between the ME, MC, and PC tables in this version (see Status).
- `N/A` means no RIF source. `notes` then says how to populate the element, for example "Report as null" or a hard-coded value.
- Each file carries the spec's Un-assigned row (`CDLMEXXX`, `CDLMCXXX`, `CDLPCXXX`). In v4.0.1 it marks element numbers reserved for future use, between the last assigned element and the 899 Record Type. It is not a joinable element id.
- `element_id` is the join key. `element_name` is carried for readability. The spec's element tables are in [source/files/](../../source/files/).

## CMS files and Part D variables used

The mapping draws on these CCW RIF files. In `rif_file` they appear as `MBSF`, `inpatient`, `hop`, `snf`, `hospice`, `hha`, `carrier`, `dme`, the Part D event file, and the `bene_*` crosswalk files.

- Enrollment: Master Beneficiary Summary File A/B/C/D (MBSF)
- Medicare claims: Inpatient (CCW-IP), Outpatient (CCWOP), SNF (CCWSNF), Hospice (CCWHS), Home Health (CCWHHA), Carrier (CCWCAR), DMERC (CCWDME)
- Part D: Part D Event (PDE), Part D Drug Characteristics (PDECF)
- Crosswalks (state segment only): BENE ID to SSN (CCWSSX), BENE ID to Name (XWALK0), BENE ID to MBI (CCWMBX)

Part D Event variables used:

- Patient Date of Birth (DOB)
- Patient Sex
- RX Service Date
- Quantity Dispensed
- Product/Service Identifier
- Days Supply
- Patient Pay Amount
- Gross Drug Cost (sum of Ingredient Cost Paid, Dispensing Fee Paid, Total Amount Attributed to Sales Tax)
- Drug Coverage Status Code
- The Brand-Generic Code reported by submitting plan
- Compound Code
- Dispense as Written/Product Selection Code
- Fill Number
- Other True Out-of-Pocket (TrOOP) Amount
- Low-Income Cost-Sharing Subsidy Amount (LICS)
- Patient Liability Reduction due to Other Payer Amount (PLRO)
- Covered D Plan Paid Amount (CPP)
- Paid Date

The release workbook carries the same lists, highlighted, on its Required CMS Files and Required PDE Variables tabs.

## Approach

Freedman HealthCare, Onpoint Health Data, and Human Services Research Institute (HSRI) each mapped the RIF to the CDL independently. The three mappings were reconciled into one selection, and the Arkansas Center for Health Improvement (ACHI) reviewed the draft and provided feedback. This folder carries only the final selection.

## Scope

In scope: CMS Medicare FFS RIF variables mapped to the CDL Member Eligibility, Medical Claims, and Pharmacy Claims files.
Out of scope: Dental and Provider files (no Medicare mapping), MA encounter data, and any redesign of the CDL.

## Maintenance

Maintained by NAHDO as a living technical resource, outside the CDL's formal maintenance and change process. It is revised as the RIF layouts or the CDL change. Each change is a commit whose message states what changed and why.

## Copyright

CMS Medicare Research Identifiable Files (RIF) Mapping to the APCD Common Data Layout, Version 1.0. Copyright 2026 by NAHDO. All rights reserved.

This crosswalk reproduces element numbers and names from the APCD-CDL™. APCD-CDL™ is copyright 2018-2025 by APCD Council, NAHDO, The University of New Hampshire, and is licensed by the National Association of Health Data Organizations (NAHDO) and the University of New Hampshire. Commercial uses of APCD-CDL™ must receive written approval.

Reuse of this crosswalk follows the [APCD Council Attribution Policy](https://www.apcdcouncil.org/attribution-policy).

## Status

Version 1.0. The CSVs in `source/` are canonical and match the v1.0 workbook, which is attached to the crosswalk's GitHub Release.

The `rif_file` and `rif_file_part` values keep the casing used in the v1.0 workbook. Normalizing them is deferred to the next crosswalk version.
