# Module 12: Known Issues, FAQ, and Glossary

## Frequently Asked Questions

### Q1: Why are fulfillment locations restricted?
**A**: Business policy requires orders to ship from physical inventory locations (`Warehouse` or `Manufacturing`). Orders assigned to sales offices represent data entry errors or drop-ship attempts that require manual review.

### Q2: What is the difference between Gross Revenue and Net Revenue?
**A**: Gross Revenue is `Quantity * Unit Price`. Net Revenue subtracts any line-item discounts (`Gross Revenue - Discount Amount`).

---

## Technical Glossary
- **SCD (Slowly Changing Dimension)**: Technique for storing historical dimension attribute changes.
- **SCD Type 1**: Overwrite old attribute value with new attribute value (no history kept).
- **SCD Type 2**: Track history by creating a new dimension row with `effective_start_date` and `effective_end_date`.
- **Bridge Table**: Table used to represent many-to-many or complex temporal relationships (e.g., Customer to Manager assignments).
- **Grain**: The atomic level of detail represented by a single row in a fact table.
