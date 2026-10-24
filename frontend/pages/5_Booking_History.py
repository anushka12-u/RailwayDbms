from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api_client import ApiError, get, passengers


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap');

/* GLOBAL */

html, body, .stApp {
    background-color: #080F1E !important;
    color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1600px !important;
    padding: 2rem 3rem !important;
}

/* STREAMLIT HEADER */

header[data-testid="stHeader"] {
    background: #080F1E !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #101D30 !important;
    border-right: 1px solid #26364D;
}

section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] button {
    color: #E2E8F0 !important;
}

section[data-testid="stSidebar"] a:hover {
    background: #1E3555 !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] a[aria-current="page"] {
    background: #1E3555 !important;
    border-left: 3px solid #F97316;
    border-radius: 8px;
}

/* PAGE HEADER */

.history-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 30px;
}

.history-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
}

.history-header-subtitle {
    font-size: 14px;
    color: #A8BAD0;
    margin-top: 10px;
}

/* SECTION HEADINGS */

.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 21px;
    font-weight: 600;
    color: #FFFFFF;
    margin-top: 30px;
    margin-bottom: 18px;
}

.section-subtitle {
    color: #94A3B8;
    font-size: 13px;
    margin-top: -10px;
    margin-bottom: 20px;
}

/* METRIC CARDS */

.metric-card {
    background: linear-gradient(145deg, #14243A, #101C30);
    border: 1px solid #2A3D57;
    border-radius: 14px;
    padding: 25px;
    min-height: 150px;
    transition: 0.25s;
}

.metric-card:hover {
    transform: translateY(-3px);
    border-color: #F97316;
}

.metric-icon {
    font-size: 26px;
    margin-bottom: 12px;
}

.metric-label {
    color: #9FB0C6;
    font-size: 13px;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 29px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 8px;
}

/* PASSENGER CARD */

.passenger-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 24px;
    margin: 15px 0;
}

.passenger-name {
    color: #FFFFFF;
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
}

.passenger-info {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
}

.info-label {
    color: #94A3B8;
    font-size: 12px;
    margin-bottom: 7px;
}

.info-value {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 600;
}

/* BOOKING DETAILS */

.booking-detail-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 12px;
    padding: 22px;
    margin: 10px 0;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 12px 0;
    border-bottom: 1px solid #26364D;
}

.detail-label {
    color: #94A3B8;
    font-size: 13px;
}

.detail-value {
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    text-align: right;
}

/* STATUS BADGES */

.status-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
}

.status-confirmed {
    background: rgba(34,197,94,0.15);
    color: #4ADE80;
}

.status-cancelled {
    background: rgba(239,68,68,0.15);
    color: #F87171;
}

.status-pending {
    background: rgba(245,158,11,0.15);
    color: #FBBF24;
}

/* INPUTS */

[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] input {
    background: #0B1728 !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stWidgetLabel"] p {
    color: #CBD5E1 !important;
}

/* BUTTONS */

.stButton > button {
    background: #182A44;
    color: #FFFFFF;
    border: 1px solid #304563;
    border-radius: 9px;
    font-weight: 600;
    min-height: 45px;
}

.stButton > button:hover {
    background: #1E3A5F;
    color: #FFFFFF;
    border-color: #F97316;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, #EA580C, #F97316);
    border: none;
    color: #FFFFFF;
}

.stButton > button[kind="primary"]:hover {
    background: #C2410C;
    color: #FFFFFF;
}

/* EXPANDERS */

[data-testid="stExpander"] {
    background: #111E31 !important;
    border: 1px solid #26364D !important;
    border-radius: 12px !important;
    margin-bottom: 12px;
}

[data-testid="stExpander"] summary {
    color: #E2E8F0 !important;
}

/* FOOTER */

.history-footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 25px;
}

@media (max-width: 768px) {

    .block-container {
        padding: 1.5rem 1rem !important;
    }

    .history-header {
        padding: 24px;
    }

    .history-header-title {
        font-size: 25px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def safe(value):
    return escape(str(value))


def section_heading(title, subtitle=None):

    st.html(f"""
    <div class="section-title">
        {safe(title)}
    </div>
    """)

    if subtitle:
        st.html(f"""
        <div class="section-subtitle">
            {safe(subtitle)}
        </div>
        """)


def metric_card(icon, label, value):

    st.html(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{safe(label)}</div>
        <div class="metric-value">{safe(value)}</div>
    </div>
    """)


def detail_row(label, value):

    return f"""
    <div class="detail-row">
        <span class="detail-label">{safe(label)}</span>
        <span class="detail-value">{safe(value)}</span>
    </div>
    """


def status_badge(status):

    status = str(status).upper()

    if status == "CONFIRMED":
        css_class = "status-confirmed"

    elif status == "CANCELLED":
        css_class = "status-cancelled"

    else:
        css_class = "status-pending"

    return f"""
    <span class="status-badge {css_class}">
        {safe(status)}
    </span>
    """


# =====================================================
# DARK PLOTLY TABLE
# =====================================================

def display_dark_table(df):

    row_colors = [
        "#111E31" if i % 2 == 0 else "#16263D"
        for i in range(len(df))
    ]

    fig = go.Figure(
        data=[
            go.Table(

                columnwidth=[
                    90, 180, 140, 90, 120, 170
                ],

                header=dict(
                    values=[
                        f"<b>{safe(col)}</b>"
                        for col in df.columns
                    ],

                    fill_color="#1E3555",

                    font=dict(
                        family="Arial",
                        color="#FFFFFF",
                        size=13
                    ),

                    align="left",
                    height=45,

                    line=dict(
                        color="#304563",
                        width=1
                    )
                ),

                cells=dict(
                    values=[
                        [
                            safe(value)
                            for value in df[col].fillna("—").tolist()
                        ]
                        for col in df.columns
                    ],

                    fill_color=[
                        row_colors
                        for _ in df.columns
                    ],

                    font=dict(
                        family="Arial",
                        color="#E2E8F0",
                        size=12
                    ),

                    align="left",
                    height=42,

                    line=dict(
                        color="#26364D",
                        width=1
                    )
                )
            )
        ]
    )

    fig.update_layout(
        paper_bgcolor="#080F1E",
        plot_bgcolor="#080F1E",
        margin=dict(l=0, r=0, t=0, b=0),
        height=min(600, 50 + len(df) * 42)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )


# =====================================================
# PAGE HEADER
# =====================================================

st.html("""
<div class="history-header">

    <div class="history-header-title">
        📜 Booking History
    </div>

    <div class="history-header-subtitle">
        View passenger reservations, journey details
        and booking status.
    </div>

</div>
""")


# =====================================================
# LOAD PASSENGERS
# =====================================================

try:
    passenger_rows = passengers() or []

except ApiError as exc:
    st.error(f"Unable to load passengers: {exc}")
    st.stop()


if not passenger_rows:
    st.info("No passengers are registered yet.")
    st.stop()


# =====================================================
# SESSION STATE
# =====================================================

if "history_rows" not in st.session_state:
    st.session_state.history_rows = None

if "history_passenger_id" not in st.session_state:
    st.session_state.history_passenger_id = None


# =====================================================
# PASSENGER SELECTION
# =====================================================

section_heading(
    "👤 Select Passenger",
    "Choose a passenger to view their reservation history"
)

passenger = st.selectbox(
    "Passenger",
    passenger_rows,
    format_func=lambda row: (
        f"#{row['passenger_id']} — {row['name']}"
    ),
    key="history_passenger_selector"
)


# =====================================================
# PASSENGER INFORMATION CARD
# =====================================================

st.html(f"""
<div class="passenger-card">

    <div class="passenger-name">
        👤 {safe(passenger['name'])}
    </div>

    <div class="passenger-info">

        <div>
            <div class="info-label">PASSENGER ID</div>
            <div class="info-value">
                #{safe(passenger['passenger_id'])}
            </div>
        </div>

        <div>
            <div class="info-label">EMAIL ADDRESS</div>
            <div class="info-value">
                {safe(passenger.get('email') or 'Not provided')}
            </div>
        </div>

        <div>
            <div class="info-label">PHONE NUMBER</div>
            <div class="info-value">
                {safe(passenger.get('phone') or 'Not provided')}
            </div>
        </div>

    </div>

</div>
""")


# =====================================================
# RESET HISTORY WHEN PASSENGER CHANGES
# =====================================================

selected_passenger_id = passenger["passenger_id"]

if st.session_state.history_passenger_id != selected_passenger_id:

    st.session_state.history_rows = None
    st.session_state.history_passenger_id = selected_passenger_id


# =====================================================
# LOAD BOOKING HISTORY
# =====================================================

if st.button(
    "🔍 Load Booking History",
    type="primary",
    use_container_width=True
):

    try:

        rows = get(
            f"/bookings/passenger/{selected_passenger_id}"
        )

        st.session_state.history_rows = rows

    except ApiError as exc:

        st.session_state.history_rows = None

        st.error(
            f"Unable to load booking history: {exc}"
        )


rows = st.session_state.history_rows


# =====================================================
# DISPLAY BOOKING HISTORY
# =====================================================

if rows is not None:

    if not rows:

        st.info(
            f"No booking history found for {passenger['name']}."
        )

    else:

        # =================================================
        # BOOKING STATISTICS
        # =================================================

        section_heading(
            "📊 Booking Overview",
            "Reservation statistics for the selected passenger"
        )

        total_bookings = len(rows)

        confirmed_bookings = sum(
            str(row.get("booking_status", "")).upper()
            == "CONFIRMED"
            for row in rows
        )

        cancelled_bookings = sum(
            str(row.get("booking_status", "")).upper()
            == "CANCELLED"
            for row in rows
        )

        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )

        with col1:
            metric_card(
                "🎟️",
                "Total Bookings",
                total_bookings
            )

        with col2:
            metric_card(
                "✅",
                "Confirmed",
                confirmed_bookings
            )

        with col3:
            metric_card(
                "❌",
                "Cancelled",
                cancelled_bookings
            )

        # =================================================
        # FILTER BOOKINGS
        # =================================================

        section_heading(
            "🔎 Filter Bookings",
            "Search reservations by train, booking ID or status"
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:

            status_filter = st.selectbox(
                "Booking Status",
                ["All", "CONFIRMED", "CANCELLED"],
                key="history_status_filter"
            )

        with col2:

            search_query = st.text_input(
                "Search Bookings",
                placeholder="Train name, number or booking ID",
                key="history_search"
            )

        filtered_rows = rows

        if status_filter != "All":

            filtered_rows = [
                row for row in filtered_rows
                if str(
                    row.get("booking_status", "")
                ).upper() == status_filter
            ]

        if search_query.strip():

            query = search_query.strip().casefold()

            filtered_rows = [
                row for row in filtered_rows
                if any(
                    query in str(row.get(field) or "").casefold()
                    for field in (
                        "booking_id",
                        "train_name",
                        "train_number"
                    )
                )
            ]

        # =================================================
        # BOOKING TABLE
        # =================================================

        section_heading(
            "📋 Booking Records",
            "Browse reservations for the selected passenger"
        )

        if filtered_rows:

            table_rows = []

            for row in filtered_rows:

                table_rows.append({
                    "Booking ID": row.get("booking_id"),
                    "Train": (
                        row.get("train_name")
                        or f"Train #{row.get('train_id', '—')}"
                    ),
                    "Journey Date": row.get(
                        "journey_date", "—"
                    ),
                    "Seat": row.get(
                        "seat_number", "—"
                    ),
                    "Status": row.get(
                        "booking_status", "—"
                    ),
                    "Booked On": row.get(
                        "booking_date", "—"
                    )
                })

            df = pd.DataFrame(table_rows)

            display_dark_table(df)

            st.caption(
                f"Showing {len(filtered_rows)} "
                f"of {total_bookings} bookings"
            )

        else:

            st.info(
                "No bookings match your selected filters."
            )

        # =================================================
        # DETAILED BOOKING CARDS
        # =================================================

        if filtered_rows:

            section_heading(
                "🎫 Booking Details",
                "Expand a reservation to view its details"
            )

            for row in filtered_rows:

                booking_id = row.get("booking_id")

                train_name = (
                    row.get("train_name")
                    or f"Train #{row.get('train_id', '—')}"
                )

                status = str(
                    row.get("booking_status", "UNKNOWN")
                ).upper()

                with st.expander(
                    f"🎟️ Booking #{booking_id} | "
                    f"{train_name} | {status}"
                ):

                    detail_html = '<div class="booking-detail-card">'

                    detail_html += detail_row(
                        "Booking ID",
                        booking_id
                    )

                    detail_html += detail_row(
                        "Passenger",
                        passenger["name"]
                    )

                    detail_html += detail_row(
                        "Train",
                        train_name
                    )

                    detail_html += detail_row(
                        "Journey Date",
                        row.get("journey_date") or "—"
                    )

                    detail_html += detail_row(
                        "Seat Number",
                        row.get("seat_number") or "—"
                    )

                    detail_html += detail_row(
                        "Booking Date",
                        row.get("booking_date") or "—"
                    )

                    if row.get("source") and row.get("destination"):

                        detail_html += detail_row(
                            "Journey Route",
                            (
                                f"{row['source']} → "
                                f"{row['destination']}"
                            )
                        )

                    detail_html += """
                    <div style="margin-top:20px;">
                    """

                    detail_html += status_badge(status)

                    detail_html += "</div></div>"

                    st.html(detail_html)


else:

    st.info(
        "Select a passenger and click "
        "'Load Booking History' to view reservations."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.html("""
<div class="history-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Booking History

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")