import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from html import escape
from api_client import ApiError, bookings, passengers, trains


# =====================================================
# PAGE CONFIGURATION
# =====================================================

# Do not call st.set_page_config() here if it is
# already configured by your application.


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap');

/* Main application */
html, body, .stApp {
    background-color: #080F1E !important;
    font-family: 'Inter', sans-serif;
}

/* Wider dashboard */
.block-container {
    max-width: 1600px !important;
    padding: 2rem 3rem !important;
}

/* Hide top toolbar but keep sidebar toggle */
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* Keep header dark instead of hiding it */
header[data-testid="stHeader"] {
    background: #080F1E !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #101D30 !important;
    border-right: 1px solid #26364D;
}

/* Sidebar navigation text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] p {
    color: #E2E8F0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Sidebar hover */
section[data-testid="stSidebar"] a:hover {
    background: #1E3555 !important;
    border-radius: 8px;
}

/* Active navigation */
section[data-testid="stSidebar"] a[aria-current="page"] {
    background: #1E3555 !important;
    border-left: 3px solid #F97316 !important;
    border-radius: 8px;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Page heading */
.dashboard-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 30px;
}

.dashboard-title {
    font-family: 'Poppins', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #FFFFFF;
}

.dashboard-subtitle {
    color: #A8BAD0;
    font-size: 14px;
    margin-top: 8px;
}

/* Section heading */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
    margin: 25px 0 20px;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(145deg, #14243A, #101C30);
    border: 1px solid #2A3D57;
    border-radius: 14px;
    padding: 25px;
    min-height: 160px;
    transition: 0.3s;
}

.metric-card:hover {
    border-color: #F97316;
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

.metric-icon {
    font-size: 27px;
    margin-bottom: 15px;
}

.metric-label {
    color: #9FB0C6;
    font-size: 13px;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 8px;
}

/* Analytics cards */
.analytics-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 14px;
    padding: 22px;
}

.analytics-title {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.analytics-subtitle {
    font-size: 13px;
    color: #94A3B8;
}

/* Status summary */
.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #26364D;
}

.status-label {
    color: #CBD5E1;
    font-size: 14px;
}

.status-value {
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
}

/* Table */
[data-testid="stDataFrame"] {
    border: 1px solid #26364D;
    border-radius: 12px;
    overflow: hidden;
}

/* Footer */
.dashboard-footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.html("""
<div class="dashboard-header">

    <div class="dashboard-title">
        🚆 Railway Dashboard
    </div>

    <div class="dashboard-subtitle">
        Monitor railway operations, passenger activity,
        reservations and booking performance.
    </div>

</div>
""")


# =====================================================
# FETCH DATA
# =====================================================

try:
    train_rows = trains() or []
    passenger_rows = passengers() or []
    booking_rows = bookings() or []

except ApiError as exc:
    st.error(f"Unable to load dashboard: {exc}")
    st.stop()


# =====================================================
# CALCULATE METRICS
# =====================================================

total_trains = len(train_rows)
total_passengers = len(passenger_rows)
total_bookings = len(booking_rows)

confirmed = sum(
    str(row.get("booking_status", "")).upper() == "CONFIRMED"
    for row in booking_rows
)

cancelled = sum(
    str(row.get("booking_status", "")).upper() == "CANCELLED"
    for row in booking_rows
)

pending = sum(
    str(row.get("booking_status", "")).upper() == "PENDING"
    for row in booking_rows
)

other = total_bookings - confirmed - cancelled - pending


# =====================================================
# METRIC CARD FUNCTION
# =====================================================

def metric_card(icon, label, value):

    st.html(f"""
    <div class="metric-card">

        <div class="metric-icon">{icon}</div>

        <div class="metric-label">
            {escape(str(label))}
        </div>

        <div class="metric-value">
            {escape(str(value))}
        </div>

    </div>
    """)


# =====================================================
# OVERVIEW
# =====================================================

st.html("""
<div class="section-title">
    📊 Operations Overview
</div>
""")

col1, col2, col3, col4, col5 = st.columns(
    5,
    gap="medium"
)

with col1:
    metric_card("🚄", "Total Trains", total_trains)

with col2:
    metric_card("👥", "Passengers", total_passengers)

with col3:
    metric_card("🎫", "Total Bookings", total_bookings)

with col4:
    metric_card("✅", "Confirmed", confirmed)

with col5:
    metric_card("❌", "Cancelled", cancelled)


# =====================================================
# BOOKING ANALYTICS
# =====================================================

st.html("""
<div class="section-title">
    📈 Booking Analytics
</div>
""")

chart_col, summary_col = st.columns(
    [1.7, 1],
    gap="large"
)


# =====================================================
# DONUT CHART
# =====================================================

with chart_col:

    st.html("""
    <div class="analytics-card">

        <div class="analytics-title">
            Reservation Distribution
        </div>

        <div class="analytics-subtitle">
            Overview of ticket booking statuses
        </div>

    </div>
    """)

    status_labels = []
    status_values = []
    status_colors = []

    status_items = [
        ("Confirmed", confirmed, "#22C55E"),
        ("Cancelled", cancelled, "#EF4444"),
        ("Pending", pending, "#F59E0B"),
        ("Other", other, "#64748B")
    ]

    for label, value, color in status_items:
        if value > 0:
            status_labels.append(label)
            status_values.append(value)
            status_colors.append(color)

    if status_values:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=status_labels,
                    values=status_values,
                    hole=0.72,
                    marker=dict(
                        colors=status_colors,
                        line=dict(
                            color="#111E31",
                            width=3
                        )
                    ),
                    textinfo="none",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Bookings: %{value}<br>"
                        "Share: %{percent}"
                        "<extra></extra>"
                    )
                )
            ]
        )

        fig.update_layout(
            paper_bgcolor="#111E31",
            plot_bgcolor="#111E31",
            font=dict(
                family="Inter",
                color="#CBD5E1"
            ),
            height=340,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            showlegend=True,
            legend=dict(
                orientation="v",
                x=1,
                y=0.5,
                font=dict(size=13)
            ),
            annotations=[
                dict(
                    text=(
                        f"<b>{total_bookings}</b>"
                        "<br><span style='font-size:12px'>"
                        "Bookings</span>"
                    ),
                    x=0.5,
                    y=0.5,
                    font=dict(
                        size=27,
                        color="#FFFFFF"
                    ),
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    else:
        st.info("No bookings available.")


# =====================================================
# RESERVATION SUMMARY
# =====================================================

with summary_col:

    st.html(f"""
    <div class="analytics-card">

        <div class="analytics-title">
            📋 Reservation Summary
        </div>

        <div class="analytics-subtitle">
            Current booking statistics
        </div>

        <br>

        <div class="status-row">
            <span class="status-label">🟢 Confirmed</span>
            <span class="status-value">{confirmed}</span>
        </div>

        <div class="status-row">
            <span class="status-label">🔴 Cancelled</span>
            <span class="status-value">{cancelled}</span>
        </div>

        <div class="status-row">
            <span class="status-label">🟡 Pending</span>
            <span class="status-value">{pending}</span>
        </div>

        <div class="status-row">
            <span class="status-label">⚪ Other</span>
            <span class="status-value">{other}</span>
        </div>

        <div class="status-row">
            <span class="status-label">Total Reservations</span>
            <span class="status-value">{total_bookings}</span>
        </div>

    </div>
    """)


# =====================================================
# RECENT BOOKINGS
# =====================================================

st.html("""
<div class="section-title">
    📜 Recent Reservations
</div>
""")

if booking_rows:

    df = pd.DataFrame(booking_rows)

    if "booking_date" in df.columns:
        df = df.sort_values(
            by="booking_date",
            ascending=False
        )

    df = df.head(10)

    # Rename columns for better readability
    df = df.rename(
        columns={
            "booking_id": "Booking ID",
            "passenger_id": "Passenger ID",
            "train_id": "Train ID",
            "journey_date": "Journey Date",
            "seat_number": "Seat",
            "booking_status": "Status",
            "booking_date": "Booked On"
        }
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=320
    )

else:
    st.info("No reservations found.")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.html("""
<div class="dashboard-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Railway Management Dashboard

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")