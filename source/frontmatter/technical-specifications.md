# Technical Specifications

## File Content

Each file contains individual data elements, data types, field lengths, and field description/code assignments for collecting claims-based and non-claims payment data from healthcare payers. The submission of the medical, pharmacy, and dental claim is based upon the adjudication date within a given reporting period. All files shall be submitted as separate pipe-delimited files with variable field lengths. Elements with no data should be reported as two pipes together, with no spaces or tab characters padding the field.

Variations from any file layout can cause data processing delays and errors, requiring additional resources to bring non-compliant submissions into the APCD. Therefore, exceptions should only be granted when data submitter compliance is unfeasible. Programs typically only give exceptions for the shortest time possible.

This guidance is intentionally silent on establishing 1) definitions for “primary care” and “behavioral health” and 2) data quality thresholds to allow APCD programs flexibility during testing and implementation. Both will vary across state-designated agencies due to policy and technical capability differences. Care definitions and data quality can also vary by data supplier within a state. For this reason, APCD programs typically set data quality thresholds based on submission testing, expectations setting with data suppliers, and in consultation with other state agencies collecting these data. Exceptions to data quality thresholds might be negotiated and adjusted over time to improve data quality in compliance with submission requirements.

### Consistent Identifiers

Providing consistent member, provider, and plan identifiers across all files is critical. A data submitter and any contracted entity acting on their behalf shall ensure that member identifiers for the same individuals are unique and consistent across member eligibility and payment files.

### Financial Amounts

Financial amount data elements assume the following:

- The amount paid for each payment record is mutually exclusive.
- The sum of all claim lines for a given claim will equal the total dollar amount of the claim.
- For claims-based payment records (i.e., medical, pharmacy, and dental claims), use an implied decimal when reporting dollar amounts (e.g., $1,000.25 = 100025).
- For non-claims payment records (i.e., annual, pharmacy rebates, and capitation), round or truncate to the nearest dollar and report as an integer (e.g., $1,000.25 = 1000).
