"""
E-Commerce Analytics Dashboard
Premium dark-themed dashboard with interactive SQL-powered visualizations.
"""

import sqlite3
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, callback, Output, Input

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ecommerce.db")

# ── Color Palette ──────────────────────────────────────────────────────────
COLORS = {
    "bg": "#0f1117",
    "card": "#1a1d27",
    "card_border": "#2a2d3a",
    "text": "#e8eaf0",
    "text_muted": "#8b8fa3",
    "accent1": "#6366f1",  # indigo
    "accent2": "#06b6d4",  # cyan
    "accent3": "#f59e0b",  # amber
    "accent4": "#10b981",  # emerald
    "accent5": "#ef4444",  # red
    "accent6": "#8b5cf6",  # violet
    "gradient": ["#6366f1", "#818cf8", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"],
}

CHART_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": COLORS["text_muted"], "family": "Inter, sans-serif", "size": 12},
        "xaxis": {"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.05)"},
        "yaxis": {"gridcolor": "rgba(255,255,255,0.05)", "zerolinecolor": "rgba(255,255,255,0.05)"},
        "margin": {"l": 50, "r": 20, "t": 40, "b": 40},
    }
}


# ── SQL Queries ────────────────────────────────────────────────────────────
def run_query(sql, params=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df


def get_kpis():
    return run_query("""
        SELECT
            SUM(CASE WHEN status NOT IN ('Cancelled','Refunded') THEN total_amount ELSE 0 END) as revenue,
            COUNT(*) as total_orders,
            COUNT(DISTINCT customer_id) as unique_customers,
            AVG(CASE WHEN status NOT IN ('Cancelled','Refunded') THEN total_amount END) as avg_order,
            SUM(CASE WHEN status='Refunded' THEN total_amount ELSE 0 END) as refunds,
            ROUND(COUNT(CASE WHEN status IN ('Cancelled','Refunded') THEN 1 END)*100.0/COUNT(*),1) as churn_rate
        FROM orders
    """)


def get_monthly_revenue():
    return run_query("""
        SELECT strftime('%Y-%m', order_date) as month,
               SUM(CASE WHEN status NOT IN ('Cancelled','Refunded') THEN total_amount ELSE 0 END) as revenue,
               COUNT(*) as orders
        FROM orders
        GROUP BY month ORDER BY month
    """)


def get_category_sales():
    return run_query("""
        SELECT p.category,
               SUM(oi.total) as revenue,
               SUM(oi.quantity) as units_sold,
               COUNT(DISTINCT o.id) as order_count
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status NOT IN ('Cancelled','Refunded')
        GROUP BY p.category ORDER BY revenue DESC
    """)


def get_top_products():
    return run_query("""
        SELECT p.name, p.category, p.price,
               SUM(oi.quantity) as units_sold,
               SUM(oi.total) as total_revenue,
               ROUND(SUM(oi.total) - SUM(oi.quantity * p.cost), 2) as profit
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status NOT IN ('Cancelled','Refunded')
        GROUP BY p.id ORDER BY total_revenue DESC LIMIT 10
    """)


def get_geo_data():
    return run_query("""
        SELECT c.country,
               COUNT(DISTINCT o.id) as orders,
               SUM(o.total_amount) as revenue,
               COUNT(DISTINCT c.id) as customers
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status NOT IN ('Cancelled','Refunded')
        GROUP BY c.country ORDER BY revenue DESC
    """)


def get_segment_data():
    return run_query("""
        SELECT c.segment,
               COUNT(DISTINCT c.id) as customers,
               COUNT(o.id) as orders,
               SUM(o.total_amount) as revenue,
               AVG(o.total_amount) as avg_order
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id AND o.status NOT IN ('Cancelled','Refunded')
        GROUP BY c.segment ORDER BY revenue DESC
    """)


def get_payment_data():
    return run_query("""
        SELECT payment_method, COUNT(*) as count,
               SUM(total_amount) as revenue
        FROM orders
        WHERE status NOT IN ('Cancelled','Refunded')
        GROUP BY payment_method ORDER BY revenue DESC
    """)


def get_daily_orders_recent():
    return run_query("""
        SELECT order_date as date, COUNT(*) as orders,
               SUM(total_amount) as revenue
        FROM orders
        WHERE order_date >= date('2025-10-01')
        GROUP BY order_date ORDER BY order_date
    """)


def get_customer_growth():
    return run_query("""
        SELECT strftime('%Y-%m', signup_date) as month,
               COUNT(*) as new_customers
        FROM customers GROUP BY month ORDER BY month
    """)


def get_order_status():
    return run_query("""
        SELECT status, COUNT(*) as count,
               SUM(total_amount) as amount
        FROM orders GROUP BY status ORDER BY count DESC
    """)


# ── Helper: Styled Components ─────────────────────────────────────────────
def kpi_card(title, value, subtitle, color, icon):
    return html.Div([
        html.Div([
            html.Div(icon, style={
                "fontSize": "28px", "width": "52px", "height": "52px",
                "borderRadius": "14px", "display": "flex", "alignItems": "center",
                "justifyContent": "center",
                "background": f"linear-gradient(135deg, {color}22, {color}44)",
                "color": color, "flexShrink": "0",
            }),
            html.Div([
                html.P(title, style={
                    "margin": "0", "fontSize": "13px", "color": COLORS["text_muted"],
                    "fontWeight": "500", "letterSpacing": "0.5px", "textTransform": "uppercase",
                }),
                html.H2(value, style={
                    "margin": "4px 0 0 0", "fontSize": "28px", "fontWeight": "700",
                    "color": COLORS["text"], "letterSpacing": "-0.5px",
                }),
                html.P(subtitle, style={
                    "margin": "2px 0 0 0", "fontSize": "12px", "color": color,
                    "fontWeight": "500",
                }),
            ]),
        ], style={"display": "flex", "alignItems": "center", "gap": "16px"}),
    ], style={
        "background": COLORS["card"], "borderRadius": "16px",
        "padding": "24px", "border": f"1px solid {COLORS['card_border']}",
        "flex": "1", "minWidth": "200px",
        "boxShadow": f"0 0 20px {color}08",
        "transition": "transform 0.2s, box-shadow 0.2s",
    })


def section_title(text, subtitle=""):
    items = [html.H3(text, style={
        "margin": "0", "fontSize": "18px", "fontWeight": "600",
        "color": COLORS["text"], "letterSpacing": "-0.3px",
    })]
    if subtitle:
        items.append(html.P(subtitle, style={
            "margin": "4px 0 0 0", "fontSize": "13px", "color": COLORS["text_muted"],
        }))
    return html.Div(items, style={"marginBottom": "16px"})


def chart_card(children, span=1):
    return html.Div(children, style={
        "background": COLORS["card"], "borderRadius": "16px",
        "padding": "24px", "border": f"1px solid {COLORS['card_border']}",
        "gridColumn": f"span {span}",
    })


# ── Build Charts ───────────────────────────────────────────────────────────
def build_revenue_chart():
    df = get_monthly_revenue()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["revenue"], mode="lines",
        fill="tozeroy", name="Revenue",
        line={"color": COLORS["accent1"], "width": 2.5, "shape": "spline"},
        fillcolor="rgba(99,102,241,0.12)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_TEMPLATE["layout"], height=340,
        title=None, showlegend=False,
        xaxis_title=None, yaxis_title=None,
        yaxis_tickprefix="$", yaxis_tickformat=",.",
    )
    return fig


def build_category_chart():
    df = get_category_sales()
    fig = go.Figure(go.Bar(
        x=df["category"], y=df["revenue"],
        marker={"color": COLORS["gradient"][:len(df)],
                "cornerradius": 6},
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
        text=[f"${v:,.0f}" for v in df["revenue"]],
        textposition="outside", textfont={"color": COLORS["text_muted"], "size": 11},
    ))
    fig.update_layout(
        **CHART_TEMPLATE["layout"], height=340,
        yaxis_tickprefix="$", yaxis_tickformat=",.",
        xaxis_title=None, yaxis_title=None,
    )
    return fig


def build_geo_chart():
    df = get_geo_data()
    fig = go.Figure(go.Bar(
        y=df["country"], x=df["revenue"], orientation="h",
        marker={"color": df["revenue"],
                "colorscale": [[0, COLORS["accent2"]], [1, COLORS["accent1"]]],
                "cornerradius": 4},
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        text=[f"${v:,.0f}" for v in df["revenue"]],
        textposition="outside", textfont={"color": COLORS["text_muted"], "size": 11},
    ))
    layout = CHART_TEMPLATE["layout"].copy()
    layout.pop("yaxis", None)
    fig.update_layout(
        **layout, height=380,
        yaxis={"autorange": "reversed", "gridcolor": "rgba(255,255,255,0.05)",
               "zerolinecolor": "rgba(255,255,255,0.05)"},
        xaxis_tickprefix="$", xaxis_tickformat=",.",
        xaxis_title=None, yaxis_title=None,
    )
    return fig


def build_segment_chart():
    df = get_segment_data()
    fig = go.Figure(go.Pie(
        labels=df["segment"], values=df["revenue"],
        hole=0.65, textinfo="label+percent",
        marker={"colors": COLORS["gradient"][:len(df)],
                "line": {"color": COLORS["bg"], "width": 3}},
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
        textfont={"color": COLORS["text"], "size": 12},
    ))
    fig.update_layout(
        **CHART_TEMPLATE["layout"], height=340,
        showlegend=False,
        annotations=[{
            "text": "<b>Segments</b>", "showarrow": False,
            "font": {"size": 14, "color": COLORS["text"]},
        }],
    )
    return fig


def build_payment_chart():
    df = get_payment_data()
    fig = go.Figure(go.Pie(
        labels=df["payment_method"], values=df["revenue"],
        hole=0.6, textinfo="label+percent",
        marker={"colors": [COLORS["accent2"], COLORS["accent6"],
                           COLORS["accent3"], COLORS["accent4"],
                           COLORS["accent5"]],
                "line": {"color": COLORS["bg"], "width": 3}},
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>",
        textfont={"color": COLORS["text"], "size": 11},
    ))
    fig.update_layout(
        **CHART_TEMPLATE["layout"], height=340, showlegend=False,
        annotations=[{
            "text": "<b>Payments</b>", "showarrow": False,
            "font": {"size": 14, "color": COLORS["text"]},
        }],
    )
    return fig


def build_customer_growth():
    df = get_customer_growth()
    df["cumulative"] = df["new_customers"].cumsum()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=df["month"], y=df["new_customers"], name="New Customers",
        marker={"color": COLORS["accent4"], "opacity": 0.7, "cornerradius": 4},
        hovertemplate="%{y} new<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["cumulative"], name="Total Customers",
        line={"color": COLORS["accent3"], "width": 2.5},
        hovertemplate="%{y:,} total<extra></extra>",
    ), secondary_y=True)
    layout = CHART_TEMPLATE["layout"].copy()
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)
    fig.update_layout(
        **layout, height=340, showlegend=True,
        legend={"orientation": "h", "y": 1.12, "x": 0,
                "font": {"color": COLORS["text_muted"]}},
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", secondary_y=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", secondary_y=True)
    return fig


def build_daily_chart():
    df = get_daily_orders_recent()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["revenue"], mode="lines",
        line={"color": COLORS["accent2"], "width": 2, "shape": "spline"},
        fill="tozeroy", fillcolor="rgba(6,182,212,0.1)",
        hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_TEMPLATE["layout"], height=340,
        yaxis_tickprefix="$", yaxis_tickformat=",.",
    )
    return fig


def build_status_chart():
    df = get_order_status()
    color_map = {"Completed": COLORS["accent4"], "Shipped": COLORS["accent2"],
                 "Processing": COLORS["accent3"], "Refunded": COLORS["accent5"],
                 "Cancelled": COLORS["text_muted"]}
    fig = go.Figure(go.Bar(
        x=df["status"], y=df["count"],
        marker={"color": [color_map.get(s, COLORS["accent1"]) for s in df["status"]],
                "cornerradius": 6},
        text=df["count"], textposition="outside",
        textfont={"color": COLORS["text_muted"]},
        hovertemplate="<b>%{x}</b><br>%{y} orders<extra></extra>",
    ))
    fig.update_layout(**CHART_TEMPLATE["layout"], height=340)
    return fig


def build_top_products_table():
    df = get_top_products()
    th_base = {
        "textAlign": "left", "padding": "12px 16px", "fontSize": "12px",
        "textTransform": "uppercase", "letterSpacing": "0.5px",
        "color": COLORS["text_muted"], "fontWeight": "600",
    }
    td_base = {"padding": "12px 16px"}

    rows = []
    for i, row in df.iterrows():
        bg = COLORS["card"] if i % 2 == 0 else "#1e2130"
        rows.append(html.Tr([
            html.Td(f"#{i+1}", style={**td_base, "color": COLORS["accent1"], "fontWeight": "700", "width": "40px"}),
            html.Td([
                html.Div(row["name"], style={"fontWeight": "600", "color": COLORS["text"]}),
                html.Div(row["category"], style={"fontSize": "11px", "color": COLORS["text_muted"]}),
            ], style=td_base),
            html.Td(f"${row['price']:,.2f}", style={**td_base, "color": COLORS["text_muted"]}),
            html.Td(f"{row['units_sold']:,}", style={**td_base, "color": COLORS["accent2"]}),
            html.Td(f"${row['total_revenue']:,.0f}", style={**td_base, "color": COLORS["accent4"], "fontWeight": "600"}),
            html.Td(f"${row['profit']:,.0f}", style={**td_base, "color": COLORS["accent3"], "fontWeight": "600"}),
        ], style={"background": bg}))

    header = html.Thead(html.Tr([
        html.Th("#", style={**th_base, "width": "40px"}),
        html.Th("Product", style=th_base),
        html.Th("Price", style=th_base),
        html.Th("Units", style=th_base),
        html.Th("Revenue", style=th_base),
        html.Th("Profit", style=th_base),
    ], style={"borderBottom": f"2px solid {COLORS['card_border']}"}))

    return html.Table([header, html.Tbody(rows)], style={
        "width": "100%", "borderCollapse": "collapse",
        "color": COLORS["text_muted"], "fontSize": "13px",
    })


# ── App Layout ─────────────────────────────────────────────────────────────
app = Dash(__name__)
app.title = "Analytics Dashboard | E-Commerce Intelligence"

# Load KPI data
kpi = get_kpis().iloc[0]

app.layout = html.Div([
    # ── Sidebar glow effect ──
    html.Div(style={
        "position": "fixed", "top": "-200px", "left": "-200px",
        "width": "600px", "height": "600px", "borderRadius": "50%",
        "background": f"radial-gradient(circle, {COLORS['accent1']}15, transparent 70%)",
        "pointerEvents": "none", "zIndex": "0",
    }),
    html.Div(style={
        "position": "fixed", "bottom": "-300px", "right": "-200px",
        "width": "800px", "height": "800px", "borderRadius": "50%",
        "background": f"radial-gradient(circle, {COLORS['accent2']}10, transparent 70%)",
        "pointerEvents": "none", "zIndex": "0",
    }),

    # ── Main content ──
    html.Div([
        # ── Header ──
        html.Div([
            html.Div([
                html.H1("Analytics Dashboard", style={
                    "margin": "0", "fontSize": "28px", "fontWeight": "800",
                    "background": f"linear-gradient(135deg, {COLORS['accent1']}, {COLORS['accent2']})",
                    "WebkitBackgroundClip": "text", "WebkitTextFillColor": "transparent",
                    "letterSpacing": "-0.5px",
                }),
                html.P("E-Commerce Intelligence Platform", style={
                    "margin": "4px 0 0 0", "color": COLORS["text_muted"],
                    "fontSize": "14px",
                }),
            ]),
            html.Div([
                html.Div([
                    html.Span("LIVE", style={
                        "background": COLORS["accent4"], "color": "#fff",
                        "padding": "3px 10px", "borderRadius": "20px",
                        "fontSize": "11px", "fontWeight": "700", "letterSpacing": "1px",
                    }),
                    html.Span(" SQLite + Plotly", style={
                        "color": COLORS["text_muted"], "fontSize": "13px", "marginLeft": "8px",
                    }),
                ], style={"display": "flex", "alignItems": "center"}),
            ]),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "center", "marginBottom": "32px",
        }),

        # ── KPI Row ──
        html.Div([
            kpi_card("Total Revenue", f"${kpi['revenue']:,.0f}",
                     f"{kpi['total_orders']:,.0f} total orders",
                     COLORS["accent1"], "$"),
            kpi_card("Active Customers", f"{kpi['unique_customers']:,.0f}",
                     f"${kpi['avg_order']:,.0f} avg order",
                     COLORS["accent2"], "U"),
            kpi_card("Avg Order Value", f"${kpi['avg_order']:,.2f}",
                     "Per transaction",
                     COLORS["accent4"], "A"),
            kpi_card("Refunds", f"${kpi['refunds']:,.0f}",
                     f"{kpi['churn_rate']}% cancel/refund rate",
                     COLORS["accent5"], "R"),
        ], style={
            "display": "flex", "gap": "20px", "marginBottom": "28px",
            "flexWrap": "wrap",
        }),

        # ── Row 1: Revenue Trend + Category Breakdown ──
        html.Div([
            chart_card([
                section_title("Revenue Trend", "Monthly revenue over time"),
                dcc.Graph(figure=build_revenue_chart(), config={"displayModeBar": False}),
            ], span=1),
            chart_card([
                section_title("Sales by Category", "Revenue distribution across categories"),
                dcc.Graph(figure=build_category_chart(), config={"displayModeBar": False}),
            ], span=1),
        ], style={
            "display": "grid", "gridTemplateColumns": "1fr 1fr",
            "gap": "20px", "marginBottom": "20px",
        }),

        # ── Row 2: Geography + Segments + Payment ──
        html.Div([
            chart_card([
                section_title("Revenue by Country", "Geographic sales distribution"),
                dcc.Graph(figure=build_geo_chart(), config={"displayModeBar": False}),
            ], span=1),
            html.Div([
                chart_card([
                    section_title("Customer Segments", "Revenue by business segment"),
                    dcc.Graph(figure=build_segment_chart(), config={"displayModeBar": False}),
                ]),
                html.Div(style={"height": "20px"}),
                chart_card([
                    section_title("Payment Methods", "Preferred payment distribution"),
                    dcc.Graph(figure=build_payment_chart(), config={"displayModeBar": False}),
                ]),
            ], style={"display": "flex", "flexDirection": "column"}),
        ], style={
            "display": "grid", "gridTemplateColumns": "1fr 1fr",
            "gap": "20px", "marginBottom": "20px",
        }),

        # ── Row 3: Customer Growth + Order Status ──
        html.Div([
            chart_card([
                section_title("Customer Growth", "New signups and cumulative customers"),
                dcc.Graph(figure=build_customer_growth(), config={"displayModeBar": False}),
            ], span=1),
            chart_card([
                section_title("Order Status", "Distribution of order statuses"),
                dcc.Graph(figure=build_status_chart(), config={"displayModeBar": False}),
            ], span=1),
        ], style={
            "display": "grid", "gridTemplateColumns": "1fr 1fr",
            "gap": "20px", "marginBottom": "20px",
        }),

        # ── Row 4: Recent Daily Revenue ──
        chart_card([
            section_title("Recent Daily Revenue", "Daily revenue since Oct 2025"),
            dcc.Graph(figure=build_daily_chart(), config={"displayModeBar": False}),
        ]),
        html.Div(style={"height": "20px"}),

        # ── Row 5: Top Products Table ──
        chart_card([
            section_title("Top 10 Products", "Best performing products by revenue"),
            build_top_products_table(),
        ]),

        # ── Footer ──
        html.Div([
            html.P("Built with Python, Dash, Plotly & SQLite", style={
                "textAlign": "center", "color": COLORS["text_muted"],
                "fontSize": "13px", "padding": "32px 0",
            }),
        ]),

    ], style={
        "maxWidth": "1400px", "margin": "0 auto",
        "padding": "40px 32px", "position": "relative", "zIndex": "1",
    }),

], style={
    "backgroundColor": COLORS["bg"], "minHeight": "100vh",
    "fontFamily": "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
    "color": COLORS["text"], "position": "relative", "overflow": "hidden",
})


# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n  Dashboard running at: http://127.0.0.1:8050\n")
    app.run(debug=True, host="127.0.0.1", port=8050)
