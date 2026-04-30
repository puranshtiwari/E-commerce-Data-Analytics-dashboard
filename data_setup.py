"""
Data Setup Script - Generates realistic e-commerce data and stores it in SQLite.
Run this ONCE before starting the dashboard.
"""

import sqlite3
import random
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")

# --- Seed for reproducibility ---
random.seed(42)

# --- Realistic data pools ---
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Arun", "Priya", "Rahul", "Ananya", "Vikram", "Sneha", "Amit", "Pooja",
    "Rajesh", "Kavita", "Suresh", "Meera", "Deepak", "Nisha", "Sanjay", "Ritu",
    "Wei", "Yuki", "Hiroshi", "Sakura", "Chen", "Mei", "Akira", "Hana",
    "Carlos", "Sofia", "Diego", "Valentina", "Luis", "Camila", "Pedro", "Isabella",
    "Liam", "Emma", "Noah", "Olivia", "Ethan", "Ava", "Lucas", "Mia",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Sharma", "Patel", "Verma", "Gupta", "Singh", "Kumar", "Joshi", "Reddy",
    "Tanaka", "Yamamoto", "Nakamura", "Watanabe", "Suzuki", "Wang", "Li", "Zhang",
    "Kim", "Park", "Choi", "Mueller", "Schmidt", "Fischer", "Dubois", "Moreau",
]

CITIES_STATES_COUNTRIES = [
    ("New York", "New York", "United States"),
    ("Los Angeles", "California", "United States"),
    ("Chicago", "Illinois", "United States"),
    ("Houston", "Texas", "United States"),
    ("Phoenix", "Arizona", "United States"),
    ("San Francisco", "California", "United States"),
    ("Seattle", "Washington", "United States"),
    ("Miami", "Florida", "United States"),
    ("Denver", "Colorado", "United States"),
    ("Austin", "Texas", "United States"),
    ("Boston", "Massachusetts", "United States"),
    ("Atlanta", "Georgia", "United States"),
    ("Portland", "Oregon", "United States"),
    ("Nashville", "Tennessee", "United States"),
    ("London", "England", "United Kingdom"),
    ("Manchester", "England", "United Kingdom"),
    ("Birmingham", "England", "United Kingdom"),
    ("Toronto", "Ontario", "Canada"),
    ("Vancouver", "British Columbia", "Canada"),
    ("Montreal", "Quebec", "Canada"),
    ("Mumbai", "Maharashtra", "India"),
    ("Delhi", "Delhi", "India"),
    ("Bangalore", "Karnataka", "India"),
    ("Hyderabad", "Telangana", "India"),
    ("Chennai", "Tamil Nadu", "India"),
    ("Sydney", "NSW", "Australia"),
    ("Melbourne", "Victoria", "Australia"),
    ("Berlin", "Berlin", "Germany"),
    ("Munich", "Bavaria", "Germany"),
    ("Paris", "Île-de-France", "France"),
    ("Tokyo", "Tokyo", "Japan"),
    ("Singapore", "Singapore", "Singapore"),
    ("Dubai", "Dubai", "UAE"),
    ("São Paulo", "São Paulo", "Brazil"),
    ("Mexico City", "CDMX", "Mexico"),
]

SEGMENTS = ["Enterprise", "SMB", "Consumer", "Premium", "Startup"]

PRODUCT_CATALOG = [
    # (name, category, price, cost)
    ("CloudSync Pro", "Software", 299.99, 45.00),
    ("DataVault Enterprise", "Software", 599.99, 90.00),
    ("SecureShield Antivirus", "Software", 79.99, 12.00),
    ("CodeEditor Ultimate", "Software", 149.99, 22.00),
    ("AnalyticsDash Suite", "Software", 449.99, 67.00),
    ("ProjectFlow Manager", "Software", 199.99, 30.00),
    ("DesignStudio Pro", "Software", 349.99, 52.00),
    ("ChatBot Builder", "Software", 129.99, 19.50),
    ("API Gateway Plus", "Software", 249.99, 37.50),
    ("ML Pipeline Toolkit", "Software", 699.99, 105.00),
    ("ThinkPad X1 Carbon", "Hardware", 1499.99, 980.00),
    ("ProDisplay 4K Monitor", "Hardware", 799.99, 520.00),
    ("MechKey Pro Keyboard", "Hardware", 179.99, 85.00),
    ("ErgoMouse Wireless", "Hardware", 89.99, 35.00),
    ("NanoServer Rack Unit", "Hardware", 2999.99, 1950.00),
    ("SmartDock Station", "Hardware", 249.99, 130.00),
    ("PowerHub UPS 1500VA", "Hardware", 399.99, 210.00),
    ("NetSwitch 48-Port", "Hardware", 649.99, 380.00),
    ("WiFi 6E Access Point", "Hardware", 199.99, 95.00),
    ("SSD NVMe 2TB", "Hardware", 179.99, 90.00),
    ("Cloud Hosting Basic", "Services", 49.99, 15.00),
    ("Cloud Hosting Pro", "Services", 149.99, 45.00),
    ("Cloud Hosting Enterprise", "Services", 499.99, 150.00),
    ("Managed Database", "Services", 199.99, 60.00),
    ("CDN Global", "Services", 99.99, 30.00),
    ("24/7 Support Plan", "Services", 299.99, 120.00),
    ("Security Audit", "Services", 999.99, 400.00),
    ("Data Migration Service", "Services", 599.99, 240.00),
    ("DevOps Consulting", "Services", 1499.99, 750.00),
    ("Training Workshop", "Services", 349.99, 140.00),
    ("Tech Fundamentals Course", "Training", 199.99, 30.00),
    ("Advanced Python Bootcamp", "Training", 399.99, 60.00),
    ("Cloud Architecture Cert", "Training", 499.99, 75.00),
    ("Data Science Masterclass", "Training", 599.99, 90.00),
    ("Cybersecurity Essentials", "Training", 349.99, 52.50),
]

ORDER_STATUSES = ["Completed", "Completed", "Completed", "Completed", "Completed",
                  "Completed", "Completed", "Shipped", "Shipped", "Processing",
                  "Refunded", "Cancelled"]

PAYMENT_METHODS = ["Credit Card", "Credit Card", "Credit Card", "PayPal", "PayPal",
                   "Bank Transfer", "Crypto", "Wire Transfer"]


def create_tables(conn):
    """Create the database schema."""
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT,
            state TEXT,
            country TEXT,
            segment TEXT,
            signup_date DATE,
            lifetime_value REAL DEFAULT 0
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            margin REAL GENERATED ALWAYS AS (price - cost) STORED
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT NOT NULL,
            payment_method TEXT,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE INDEX idx_orders_date ON orders(order_date);
        CREATE INDEX idx_orders_customer ON orders(customer_id);
        CREATE INDEX idx_order_items_order ON order_items(order_id);
        CREATE INDEX idx_order_items_product ON order_items(product_id);
        CREATE INDEX idx_customers_country ON customers(country);
        CREATE INDEX idx_customers_segment ON customers(segment);
    """)
    conn.commit()


def generate_customers(conn, count=1200):
    """Generate realistic customer data."""
    cursor = conn.cursor()
    emails_used = set()
    customers = []

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2026, 4, 28)
    date_range = (end_date - start_date).days

    for i in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        # Generate unique email
        email_base = f"{first.lower()}.{last.lower()}"
        email = f"{email_base}@example.com"
        suffix = 1
        while email in emails_used:
            email = f"{email_base}{suffix}@example.com"
            suffix += 1
        emails_used.add(email)

        city, state, country = random.choice(CITIES_STATES_COUNTRIES)
        segment = random.choice(SEGMENTS)

        # Bias signup dates: more recent = more signups (growth pattern)
        days_offset = int(random.betavariate(2, 5) * date_range)
        signup_date = start_date + datetime.timedelta(days=days_offset)

        customers.append((first, last, email, city, state, country, segment,
                          signup_date.isoformat()))

    cursor.executemany("""
        INSERT INTO customers (first_name, last_name, email, city, state, country,
                               segment, signup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, customers)
    conn.commit()
    print(f"  ✓ Generated {count} customers")


def generate_products(conn):
    """Insert the product catalog."""
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO products (name, category, price, cost)
        VALUES (?, ?, ?, ?)
    """, PRODUCT_CATALOG)
    conn.commit()
    print(f"  ✓ Generated {len(PRODUCT_CATALOG)} products")


def generate_orders(conn, count=8500):
    """Generate realistic orders with seasonal patterns and growth trends."""
    cursor = conn.cursor()

    # Get all customer ids and their signup dates
    cursor.execute("SELECT id, signup_date FROM customers")
    customers = cursor.fetchall()

    # Get all product ids
    cursor.execute("SELECT id, price FROM products")
    products = cursor.fetchall()

    start_date = datetime.date(2023, 1, 15)
    end_date = datetime.date(2026, 4, 28)
    date_range = (end_date - start_date).days

    orders = []
    all_items = []

    for i in range(count):
        # Growth trend: more orders in recent months
        raw_offset = random.betavariate(2.2, 3) * date_range
        order_date = start_date + datetime.timedelta(days=int(raw_offset))

        # Seasonal boost: more orders in Nov-Dec (holiday season) and Q1
        month = order_date.month
        if month in [11, 12]:
            if random.random() < 0.3:  # 30% chance to push to holiday season
                order_date = order_date.replace(month=random.choice([11, 12]),
                                                day=random.randint(1, 28))
        elif month in [1, 2]:
            if random.random() < 0.15:  # New year sales
                order_date = order_date.replace(month=random.choice([1, 2]),
                                                day=random.randint(1, 28))

        # Pick a customer who signed up before the order date
        eligible = [c for c in customers if c[1] <= order_date.isoformat()]
        if not eligible:
            continue

        customer_id = random.choice(eligible)[0]
        status = random.choice(ORDER_STATUSES)
        payment = random.choice(PAYMENT_METHODS)

        # Generate 1-5 items per order (weighted toward fewer)
        num_items = random.choices([1, 2, 3, 4, 5],
                                   weights=[40, 30, 15, 10, 5])[0]
        chosen_products = random.sample(products, min(num_items, len(products)))

        order_total = 0
        items_for_order = []
        for prod_id, prod_price in chosen_products:
            qty = random.choices([1, 2, 3, 5],
                                 weights=[60, 25, 10, 5])[0]
            # Occasional discount
            discount = random.choice([1.0, 1.0, 1.0, 0.9, 0.85, 0.8, 0.75])
            unit_price = round(prod_price * discount, 2)
            item_total = round(unit_price * qty, 2)
            order_total += item_total
            items_for_order.append((prod_id, qty, unit_price, item_total))

        order_total = round(order_total, 2)
        orders.append((customer_id, order_date.isoformat(), status, payment,
                       order_total, items_for_order))

    # Insert orders and items
    for customer_id, order_date, status, payment, total, items in orders:
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, status, payment_method,
                                total_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (customer_id, order_date, status, payment, total))
        order_id = cursor.lastrowid

        for prod_id, qty, unit_price, item_total in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity,
                                         unit_price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, prod_id, qty, unit_price, item_total))

    conn.commit()

    # Update customer lifetime values
    cursor.execute("""
        UPDATE customers SET lifetime_value = (
            SELECT COALESCE(SUM(total_amount), 0)
            FROM orders WHERE orders.customer_id = customers.id
            AND orders.status NOT IN ('Cancelled', 'Refunded')
        )
    """)
    conn.commit()

    actual_count = cursor.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    items_count = cursor.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
    print(f"  ✓ Generated {actual_count} orders with {items_count} line items")


def print_summary(conn):
    """Print a summary of the generated data."""
    cursor = conn.cursor()
    print("\n📊 Database Summary:")
    print("─" * 40)

    for table in ["customers", "products", "orders", "order_items"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:>15}: {count:,} rows")

    revenue = cursor.execute("""
        SELECT SUM(total_amount) FROM orders
        WHERE status NOT IN ('Cancelled', 'Refunded')
    """).fetchone()[0]
    print(f"\n  💰 Total Revenue: ${revenue:,.2f}")

    date_range = cursor.execute("""
        SELECT MIN(order_date), MAX(order_date) FROM orders
    """).fetchone()
    print(f"  📅 Date Range: {date_range[0]} → {date_range[1]}")
    print("─" * 40)


def main():
    """Main entry point."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Removed existing database")

    print("🔧 Setting up e-commerce database...")
    conn = sqlite3.connect(DB_PATH)

    try:
        create_tables(conn)
        print("\n📦 Generating data...")
        generate_products(conn)
        generate_customers(conn)
        generate_orders(conn)
        print_summary(conn)
        print("\n✅ Database ready at:", DB_PATH)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
