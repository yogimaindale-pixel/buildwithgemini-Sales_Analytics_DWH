import datetime

def get_raw_dates():
    start_date = datetime.date(2024, 1, 1)
    dates = []
    for i in range(365 * 3): # 3 years: 2024, 2025, 2026
        current = start_date + datetime.timedelta(days=i)
        dates.append({
            "date_key": int(current.strftime("%Y%m%d")),
            "full_date": current.strftime("%Y-%m-%d"),
            "year": current.year,
            "quarter": (current.month - 1) // 3 + 1,
            "month": current.month,
            "month_name": current.strftime("%B"),
            "day_of_month": current.day,
            "day_of_week": current.isoweekday(),
            "day_name": current.strftime("%A"),
            "year_month": current.strftime("%Y-%m"),
            "is_weekend": current.isoweekday() in (6, 7)
        })
    return dates

def get_raw_locations():
    return [
        {"location_id": "LOC-001", "location_name": "New York Headquarters", "location_type": "Sales Office", "region": "North", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"location_id": "LOC-002", "location_name": "New Jersey Central Warehouse", "location_type": "Warehouse", "region": "North", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"location_id": "LOC-003", "location_name": "Chicago Regional Hub", "location_type": "Sales Office", "region": "West", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"location_id": "LOC-004", "location_name": "Illinois Assembly Facility", "location_type": "Manufacturing", "region": "West", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"location_id": "LOC-005", "location_name": "Atlanta Distribution Center", "location_type": "Warehouse", "region": "South", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"location_id": "LOC-006", "location_name": "Texas Manufacturing Plant", "location_type": "Manufacturing", "region": "South", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1}
    ]

def get_raw_customers():
    return [
        {"customer_id": "CUST-101", "customer_name": "Acme Dynamics Corp", "customer_type": "Enterprise", "status": "Active", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"customer_id": "CUST-102", "customer_name": "Global Tech Solutions", "customer_type": "Enterprise", "status": "Active", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"customer_id": "CUST-103", "customer_name": "Apex Retail Systems", "customer_type": "SMB", "status": "Active", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"customer_id": "CUST-104", "customer_name": "Federal Defense Logistics", "customer_type": "Government", "status": "Active", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1}
    ]

def get_raw_managers():
    return [
        {"manager_id": "MGR-201", "manager_name": "Sarah Connor", "division": "Electronics", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"manager_id": "MGR-202", "manager_name": "Marcus Vance", "division": "Industrial", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"manager_id": "MGR-203", "manager_name": "Elena Rostova", "division": "Consumer", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1}
    ]

def get_raw_products():
    return [
        {"product_id": "PROD-501", "product_name": "UltraBook Pro 15", "category": "Laptops", "unit_price": 1500.00, "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"product_id": "PROD-502", "product_name": "Enterprise AI Server Node", "category": "Servers", "unit_price": 8500.00, "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"product_id": "PROD-503", "product_name": "4K Ultra-Wide Monitor", "category": "Accessories", "unit_price": 650.00, "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1},
        {"product_id": "PROD-504", "product_name": "Industrial Sensor Controller", "category": "Industrial", "unit_price": 3200.00, "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True, "version_number": 1}
    ]

def get_raw_assignments():
    return [
        {"customer_id": "CUST-101", "manager_id": "MGR-201", "division": "Electronics", "location_id": "LOC-001", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True},
        {"customer_id": "CUST-102", "manager_id": "MGR-202", "division": "Industrial", "location_id": "LOC-003", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True},
        {"customer_id": "CUST-103", "manager_id": "MGR-203", "division": "Consumer", "location_id": "LOC-005", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True},
        {"customer_id": "CUST-104", "manager_id": "MGR-201", "division": "Electronics", "location_id": "LOC-001", "effective_start_date": "2024-01-01", "effective_end_date": "9999-12-31", "is_current": True}
    ]

def get_raw_visits():
    return [
        {"customer_id": "CUST-101", "division_visited": "Electronics", "visit_date": "2024-03-15", "assisting_manager_id": "MGR-201", "visit_count": 1},
        {"customer_id": "CUST-102", "division_visited": "Industrial", "visit_date": "2024-04-10", "assisting_manager_id": "MGR-202", "visit_count": 1},
        {"customer_id": "CUST-103", "division_visited": "Consumer", "visit_date": "2024-05-20", "assisting_manager_id": "MGR-203", "visit_count": 2},
        {"customer_id": "CUST-104", "division_visited": "Electronics", "visit_date": "2024-06-05", "assisting_manager_id": "MGR-201", "visit_count": 1}
    ]

def get_raw_order_lines():
    # Multi-product orders with valid and test-invalid fulfillment locations
    return [
        # Order 1 (Valid fulfillment from Warehouse LOC-002)
        {"order_number": "ORD-2024-001", "line_number": 1, "order_date": "2024-01-15", "order_location_id": "LOC-001", "fulfillment_location_id": "LOC-002", "customer_id": "CUST-101", "product_id": "PROD-501", "manager_id": "MGR-201", "quantity": 10, "unit_price": 1500.00, "discount_amount": 500.00},
        {"order_number": "ORD-2024-001", "line_number": 2, "order_date": "2024-01-15", "order_location_id": "LOC-001", "fulfillment_location_id": "LOC-002", "customer_id": "CUST-101", "product_id": "PROD-503", "manager_id": "MGR-201", "quantity": 10, "unit_price": 650.00, "discount_amount": 200.00},
        
        # Order 2 (Valid fulfillment from Manufacturing LOC-004)
        {"order_number": "ORD-2024-002", "line_number": 1, "order_date": "2024-02-10", "order_location_id": "LOC-003", "fulfillment_location_id": "LOC-004", "customer_id": "CUST-102", "product_id": "PROD-502", "manager_id": "MGR-202", "quantity": 4, "unit_price": 8500.00, "discount_amount": 1000.00},
        
        # Order 3 (Valid fulfillment from Warehouse LOC-005)
        {"order_number": "ORD-2024-003", "line_number": 1, "order_date": "2024-03-05", "order_location_id": "LOC-001", "fulfillment_location_id": "LOC-005", "customer_id": "CUST-103", "product_id": "PROD-503", "manager_id": "MGR-203", "quantity": 25, "unit_price": 650.00, "discount_amount": 450.00},
        {"order_number": "ORD-2024-003", "line_number": 2, "order_date": "2024-03-05", "order_location_id": "LOC-001", "fulfillment_location_id": "LOC-005", "customer_id": "CUST-103", "product_id": "PROD-504", "manager_id": "MGR-203", "quantity": 5, "unit_price": 3200.00, "discount_amount": 500.00},
        
        # Order 4 (Valid fulfillment from Manufacturing LOC-006)
        {"order_number": "ORD-2024-004", "line_number": 1, "order_date": "2024-04-18", "order_location_id": "LOC-003", "fulfillment_location_id": "LOC-006", "customer_id": "CUST-104", "product_id": "PROD-502", "manager_id": "MGR-201", "quantity": 2, "unit_price": 8500.00, "discount_amount": 0.00},
        
        # Order 5 (INVALID fulfillment attempt from LOC-001 Sales Office - MUST BE QUARANTINED)
        {"order_number": "ORD-2024-005", "line_number": 1, "order_date": "2024-05-12", "order_location_id": "LOC-001", "fulfillment_location_id": "LOC-001", "customer_id": "CUST-101", "product_id": "PROD-501", "manager_id": "MGR-201", "quantity": 5, "unit_price": 1500.00, "discount_amount": 100.00}
    ]
