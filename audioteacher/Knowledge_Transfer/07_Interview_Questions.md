# ❓ 07. Technical Interview Questions & Spoken Response Bank

### Q1: How do you handle many-to-many revenue attribution between accounts and managers?
- **30-Second Pitch**: We use a Bridge Table with allocation weights connecting customer dimensions to business manager dimensions.
- **Spoken Response**: "In our Enterprise Sales Data Warehouse, a corporate customer can be managed by multiple sales reps. To handle this without duplicating order lines in our atomic fact table, we implement `BRIDGE_CUSTOMER_MANAGER_ASSIGNMENT`. The bridge stores fractional allocation weights, allowing BI reports to join facts through the bridge and attribute revenue proportionally across sales managers."
