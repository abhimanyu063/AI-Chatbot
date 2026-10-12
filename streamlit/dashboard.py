
from datetime import date, timedelta

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from streamlit_float import float_init, float_css_helper


# ----------------------------------------
# Page configuration
# ----------------------------------------

st.set_page_config(
    page_title="Retail Competitive Intelligence",
    page_icon="📊",
    layout="wide",
)

float_init()

# ----------------------------------------
# Demo data
# ----------------------------------------

PRODUCTS = {
    "Laundry": [
        "Tide Pods",
        "Persil Detergent",
    ],
    "Electronics": [
        "Wireless Headphones",
        "Bluetooth Speaker",
    ],
    "Grocery": [
        "Breakfast Cereal",
        "Ground Coffee",
    ],
}

COMPETITORS = [
    "Amazon",
    "Walmart",
    "Costco",
]

PRODUCT_IDS = {
    "Tide Pods": "SKU-001",
    "Persil Detergent": "SKU-002",
    "Wireless Headphones": "SKU-003",
    "Bluetooth Speaker": "SKU-004",
    "Breakfast Cereal": "SKU-005",
    "Ground Coffee": "SKU-006",
}

# ----------------------------------------
# Page header
# ----------------------------------------

st.title("Retail Competitive Intelligence Platform")

st.caption(
    "Category Manager Dashboard | "
    "Streamlit + React AI Assistant Demo"
)

st.info(
    "This dashboard uses simulated data for integration testing."
)

# ----------------------------------------
# Dashboard filters
# ----------------------------------------

st.subheader("Dashboard Filters")

# Category is outside the form so product options
# refresh immediately when category changes.
category = st.selectbox(
    "Category",
    options=list(PRODUCTS.keys()),
)

with st.form("dashboard_filter_form"):

    col1, col2 = st.columns(2)

    with col1:
        product = st.selectbox(
            "Product",
            options=PRODUCTS[category],
        )

    with col2:
        competitor = st.selectbox(
            "Competitor",
            options=COMPETITORS,
        )

    selected_dates = st.date_input(
        "Date Range",
        value=(
            date.today() - timedelta(days=30),
            date.today(),
        ),
    )

    submitted = st.form_submit_button(
        "Apply Filters",
        type="primary",
    )

# ----------------------------------------
# Applied filter state
# ----------------------------------------

if "applied_filters" not in st.session_state:
    st.session_state.applied_filters = {
        "category": category,
        "product": product,
        "competitor": competitor,
        "start_date": (
            date.today() - timedelta(days=30)
        ).isoformat(),
        "end_date": date.today().isoformat(),
    }

if submitted:
    if len(selected_dates) != 2:
        st.warning(
            "Please select both start and end dates."
        )
    else:
        start_date, end_date = selected_dates

        st.session_state.applied_filters = {
            "category": category,
            "product": product,
            "competitor": competitor,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        st.success("Dashboard filters applied.")

filters = st.session_state.applied_filters

# ----------------------------------------
# Selected context
# ----------------------------------------

st.divider()

st.subheader("Selected Product")

st.write(
    f"**Category:** {filters['category']}  |  "
    f"**Product:** {filters['product']}  |  "
    f"**Competitor:** {filters['competitor']}"
)

st.caption(
    f"Period: {filters['start_date']} "
    f"to {filters['end_date']}"
)

# ----------------------------------------
# KPI metrics (simulated)
# ----------------------------------------

st.subheader("Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Target Sales",
        "$125,000",
        "-10.7%",
    )

with col2:
    st.metric(
        "Target Profit",
        "$22,500",
        "-8.2%",
    )

with col3:
    st.metric(
        "Profit Margin",
        "18.0%",
        "-1.5 pp",
    )

with col4:
    st.metric(
        "Competitor Price",
        "$24.99",
        "+$2.00",
    )

# ----------------------------------------
# Sales trend
# ----------------------------------------

st.subheader("Sales Trend")

sales_data = pd.DataFrame(
    {
        "Target": [
            120, 132, 125, 118, 110, 105
        ],
        filters["competitor"]: [
            115, 122, 134, 140, 146, 155
        ],
    },
    index=[
        "Week 1",
        "Week 2",
        "Week 3",
        "Week 4",
        "Week 5",
        "Week 6",
    ],
)

st.line_chart(sales_data)

# ----------------------------------------
# Retailer comparison
# ----------------------------------------

st.subheader("Retailer Comparison")

comparison_data = pd.DataFrame(
    [
        {
            "Retailer": "Target",
            "Price": "$22.99",
            "Promotion": "5% off",
            "Availability": "In Stock",
        },
        {
            "Retailer": filters["competitor"],
            "Price": "$24.99",
            "Promotion": "10% off",
            "Availability": "In Stock",
        },
    ]
)

st.dataframe(
    comparison_data,
    use_container_width=True,
    hide_index=True,
)

# ----------------------------------------
# Floating AI Assistant
# ----------------------------------------


# ----------------------------------------
# Floating AI Assistant
# ----------------------------------------

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False


def open_chat():
    st.session_state.chat_open = True


def close_chat():
    st.session_state.chat_open = False


if not st.session_state.chat_open:
    # Show Ask AI only when the chatbot is closed
    launcher = st.container()

    with launcher:
        st.button(
            "💬 Ask AI",
            key="open_ai_chat",
            type="primary",
            on_click=open_chat,
        )

    launcher.float(
        float_css_helper(
            bottom="20px",
            right="24px",
            width="130px",
            z_index="9999",
        )
    )

else:
    # Chat is open: show a close button instead
    close_container = st.container()

    with close_container:
        st.button(
            "✕ Close",
            key="close_ai_chat",
            on_click=close_chat,
        )

    close_container.float(
        float_css_helper(
            bottom="635px",
            right="24px",
            width="100px",
            z_index="10001",
        )
    )

    # Floating React chatbot panel
    chat_panel = st.container()

    with chat_panel:
        components.iframe(
            src="http://localhost:5173/?embedded=true",
            height=540,
            scrolling=False,
        )

    chat_panel.float(
        float_css_helper(
            bottom="85px",
            right="24px",
            width="400px",
            z_index="9998",
        )
    )
