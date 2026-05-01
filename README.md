<p align="center">
  <img src="banner.png" alt="Analytics Dashboard Banner" width="100%"/>
</p>

<h1 align="center">📊 E-Commerce Analytics Dashboard</h1>

<p align="center">
  <b>A premium, dark-themed data analytics dashboard powered by Python, SQL & Plotly</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dash-008DE4?style=for-the-badge&logo=dash&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

---

## 🚀 Launch Dashboard

> **Dashboard is live! Click below to open:**
>
> 

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **KPI Cards** | Real-time metrics — Revenue, Customers, AOV, Refunds |
| 📈 **Revenue Trend** | Monthly revenue with smooth spline area chart |
| 🏷️ **Category Sales** | Revenue breakdown across Software, Hardware, Services & Training |
| 🌍 **Geographic View** | Revenue distribution across 12 countries |
| 👥 **Customer Segments** | Enterprise, SMB, Consumer, Premium & Startup analysis |
| 💳 **Payment Methods** | Credit Card, PayPal, Bank Transfer, Crypto & Wire |
| 📊 **Customer Growth** | New signups + cumulative growth combo chart |
| 📦 **Order Status** | Completed, Shipped, Processing, Refunded & Cancelled |
| 📅 **Daily Revenue** | Recent daily revenue trend (last 6 months) |
| 🏆 **Top Products** | Top 10 products ranked by revenue with profit analysis |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────┐
│                 PRESENTATION                     │
│         Plotly Dash + Plotly.js Charts           │
├─────────────────────────────────────────────────┤
│                 DATA LAYER                       │
│            Pandas DataFrames                     │
├─────────────────────────────────────────────────┤
│                 DATABASE                         │
│     SQLite (4 tables, 27K+ rows, indexed)       │
├─────────────────────────────────────────────────┤
│                 LANGUAGE                          │
│              Python 3.10+                        │
└─────────────────────────────────────────────────┘
```

---

## 🗃️ Database Schema

The SQLite database contains **4 normalized tables** with realistic e-commerce data:

```sql
customers (1,200 rows)
├── id, first_name, last_name, email
├── city, state, country
├── segment (Enterprise | SMB | Consumer | Premium | Startup)
└── signup_date, lifetime_value

products (35 rows)
├── id, name, category
├── price, cost
└── margin (computed column)

orders (8,500 rows)
├── id, customer_id (FK)
├── order_date, status, payment_method
└── total_amount

order_items (17,678 rows)
├── id, order_id (FK), product_id (FK)
├── quantity, unit_price
└── total
```

### SQL Techniques Used

| Technique | Example |
|-----------|---------|
| `JOIN` (multi-table) | Products ↔ Orders ↔ Customers |
| `GROUP BY` + Aggregation | `SUM`, `COUNT`, `AVG`, `COUNT(DISTINCT)` |
| `CASE WHEN` | Conditional revenue/refund calculations |
| `strftime()` | Monthly/daily date grouping |
| `LEFT JOIN` | Customer segments including those with no orders |
| Computed columns | `margin GENERATED ALWAYS AS (price - cost) STORED` |
| Indexes | On `order_date`, `customer_id`, `product_id`, `country`, `segment` |

---

## 📁 Project Structure

```
analytics-dashboard/
├── 📄 README.md            ← You are here
├── 🖼️ banner.png           ← Project banner
├── 🐍 data_setup.py        ← Generates realistic data → SQLite
├── 🐍 dashboard.py         ← Main Dash application (10+ charts)
├── 🗄️ ecommerce.db         ← SQLite database (auto-generated)
└── 📋 requirements.txt     ← Python dependencies
```

---

## ⚡ Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Generate the Database

```bash
python data_setup.py
```

**Output:**
```
🔧 Setting up e-commerce database...

📦 Generating data...
  ✓ Generated 35 products
  ✓ Generated 1,200 customers
  ✓ Generated 8,500 orders with 17,678 line items

📊 Database Summary:
  💰 Total Revenue: $10,794,496.28
  📅 Date Range: 2023-01-17 → 2026-03-15
```

### 3️⃣ Launch the Dashboard

```bash
python dashboard.py
```

### 4️⃣ Open in Browser


---

## 🎨 Design Details

- **Theme:** Premium dark mode (`#0f1117` background)
- **Color palette:** Indigo `#6366f1` · Cyan `#06b6d4` · Amber `#f59e0b` · Emerald `#10b981` · Red `#ef4444` · Violet `#8b5cf6`
- **Typography:** Inter / Segoe UI system font stack
- **Cards:** Rounded corners (16px), subtle borders, ambient glow effects
- **Charts:** Transparent backgrounds, minimal gridlines, smooth spline curves
- **Interactivity:** Hover tooltips on all charts with formatted values

---

## 📊 Data Characteristics

The generated data includes realistic patterns:

- **📈 Growth Trend** — More customers and orders in recent months
- **🎄 Seasonal Spikes** — Higher sales in November–December (holiday season)
- **🌎 Global Distribution** — Customers from US, UK, India, Japan, Germany, France, Canada, Australia, Singapore, UAE, Brazil & Mexico
- **💰 Price Variety** — Products ranging from $49.99 to $2,999.99
- **📉 Realistic Churn** — ~16% cancel/refund rate

---

<p align="center">
  <b>Built with ❤️ using Python, Dash, Plotly & SQLite</b>
</p>
