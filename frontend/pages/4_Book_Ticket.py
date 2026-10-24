from datetime import date
from html import escape

import streamlit as st

from api_client import ApiError, get, passengers, post, trains


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

/* ================= GLOBAL ================= */

html, body, .stApp {
    background-color: #080F1E !important;
    color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1600px !important;
    padding: 2rem 3rem !important;
}

/* ================= STREAMLIT HEADER ================= */

header[data-testid="stHeader"] {
    background-color: #080F1E !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

/* ================= SIDEBAR ================= */

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
    border-left: 3px solid #F97316 !important;
    border-radius: 8px;
}

/* ================= PAGE HEADER ================= */

.booking-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 30px;
}

.booking-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
}

.booking-header-subtitle {
    font-size: 14px;
    color: #A8BAD0;
    margin-top: 10px;
}

/* ================= SECTION HEADINGS ================= */

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

/* ================= METRIC CARDS ================= */

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
    font-size: 25px;
    margin-bottom: 12px;
}

.metric-label {
    color: #9FB0C6;
    font-size: 13px;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 8px;
}

/* ================= ROUTE CARD ================= */

.route-card {
    background: linear-gradient(125deg, #14243A, #111E31);
    border: 1px solid #2A3D57;
    border-radius: 15px;
    padding: 28px;
    margin-bottom: 22px;
}

.route-name {
    font-family: 'Poppins', sans-serif;
    font-size: 25px;
    font-weight: 700;
    color: #FFFFFF;
}

.route-details {
    color: #94A3B8;
    font-size: 14px;
    margin-top: 10px;
}

/* ================= BOOKING SUMMARY ================= */

.summary-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 28px;
    margin: 20px 0;
}

.summary-title {
    font-family: 'Poppins', sans-serif;
    font-size: 19px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 20px;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 14px 0;
    border-bottom: 1px solid #26364D;
}

.summary-label {
    color: #94A3B8;
    font-size: 14px;
}

.summary-value {
    color: #F8FAFC;
    font-size: 14px;
    font-weight: 600;
    text-align: right;
}

.fare-value {
    color: #FB923C;
    font-size: 21px;
    font-weight: 700;
}

/* ================= FORM INPUTS ================= */

[data-testid="stSelectbox"] > div > div,
[data-testid="stDateInput"] input {
    background-color: #0B1728 !important;
    color: #FFFFFF !important;
    border-color: #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stWidgetLabel"] p {
    color: #CBD5E1 !important;
    font-size: 13px;
    font-weight: 500;
}

/* ================= BUTTONS ================= */

.stButton > button {
    background: #182A44;
    color: #FFFFFF;
    border: 1px solid #304563;
    border-radius: 9px;
    font-weight: 600;
    transition: 0.25s;
    min-height: 45px;
}

.stButton > button:hover {
    background: #1E3A5F;
    border-color: #F97316;
    color: #FFFFFF;
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

/* ================= STREAMLIT CONTAINERS ================= */

[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-color: #26364D !important;
    border-radius: 14px !important;
}

/* ================= FOOTER ================= */

.booking-footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 25px;
}

/* ================= RESPONSIVE ================= */

@media (max-width: 768px) {

    .block-container {
        padding: 1.5rem 1rem !important;
    }

    .booking-header {
        padding: 24px;
    }

    .booking-header-title {
        font-size: 25px;
    }

    .route-name {
        font-size: 20px;
    }

    .summary-card {
        padding: 18px;
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


def summary_row(label, value, highlight=False):

    value_class = (
        "summary-value fare-value"
        if highlight
        else "summary-value"
    )

    return f"""
    <div class="summary-row">
        <span class="summary-label">{safe(label)}</span>
        <span class="{value_class}">{safe(value)}</span>
    </div>
    """


def display_booking_summary(
    passenger,
    train,
    journey_date,
    seat_number
):

    fare = float(train.get("fare") or 0)

    html = """
    <div class="summary-card">
        <div class="summary-title">
            🎫 Booking Summary
        </div>
    """

    html += summary_row(
        "Passenger",
        passenger["name"]
    )

    html += summary_row(
        "Train",
        train["train_name"]
    )

    html += summary_row(
        "Train Number",
        train["train_number"]
    )

    html += summary_row(
        "Route",
        f"{train['source']} → {train['destination']}"
    )

    html += summary_row(
        "Journey Date",
        journey_date.strftime("%d %B %Y")
    )

    html += summary_row(
        "Seat Number",
        seat_number
    )

    html += summary_row(
        "Ticket Fare",
        f"₹{fare:,.2f}",
        highlight=True
    )

    html += "</div>"

    st.html(html)


# =====================================================
# PAGE HEADER
# =====================================================

st.html("""
<div class="booking-header">

    <div class="booking-header-title">
        🎟️ Book Railway Ticket
    </div>

    <div class="booking-header-subtitle">
        Plan your journey, check available seats,
        select your preferred seat and confirm your reservation.
    </div>

</div>
""")


# =====================================================
# LOAD DATA
# =====================================================

try:
    train_rows = trains() or []
    passenger_rows = passengers() or []

except ApiError as exc:
    st.error(
        f"Unable to load booking information: {exc}"
    )
    st.stop()


if not train_rows:
    st.warning(
        "No trains available. Please add a train first."
    )
    st.stop()

if not passenger_rows:
    st.warning(
        "No passengers registered. "
        "Please register a passenger first."
    )
    st.stop()


# =====================================================
# SESSION STATE
# =====================================================

if "booking_availability" not in st.session_state:
    st.session_state.booking_availability = None

if "booking_availability_key" not in st.session_state:
    st.session_state.booking_availability_key = None

if "booking_confirmation" not in st.session_state:
    st.session_state.booking_confirmation = None

if "booking_selection_key" not in st.session_state:
    st.session_state.booking_selection_key = None


# =====================================================
# JOURNEY DETAILS
# =====================================================

section_heading(
    "🚆 Journey Details",
    "Choose your train, passenger and travel date"
)

with st.container(border=True):

    col1, col2 = st.columns(2, gap="large")

    with col1:

        train = st.selectbox(
            "Select Train",
            train_rows,
            format_func=lambda row: (
                f"{row['train_number']} | "
                f"{row['train_name']}"
            ),
            key="booking_train"
        )

    with col2:

        passenger = st.selectbox(
            "Select Passenger",
            passenger_rows,
            format_func=lambda row: (
                f"#{row['passenger_id']} | "
                f"{row['name']}"
            ),
            key="booking_passenger"
        )

    journey_date = st.date_input(
        "Journey Date",
        value=date.today(),
        min_value=date.today(),
        key="booking_journey_date"
    )


# =====================================================
# RESET STATE WHEN SELECTION CHANGES
# =====================================================

selection_key = (
    train["train_id"],
    passenger["passenger_id"],
    journey_date.isoformat()
)

availability_key = (
    train["train_id"],
    journey_date.isoformat()
)

if st.session_state.booking_selection_key != selection_key:

    st.session_state.booking_selection_key = selection_key

    # Clear confirmation when the selection changes.
    st.session_state.booking_confirmation = None

if st.session_state.booking_availability_key != availability_key:

    st.session_state.booking_availability_key = availability_key
    st.session_state.booking_availability = None


# =====================================================
# SELECTED TRAIN INFORMATION
# =====================================================

section_heading(
    "🛤️ Selected Train",
    "Review your train route, schedule and ticket fare"
)

st.html(f"""
<div class="route-card">

    <div class="route-name">
        {safe(train['source'])}
        <span style="color:#F97316;">→</span>
        {safe(train['destination'])}
    </div>

    <div class="route-details">
        🚄 {safe(train['train_name'])}
        &nbsp; | &nbsp;
        Train No. {safe(train['train_number'])}
    </div>

</div>
""")


col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)

with col1:
    metric_card(
        "🕒",
        "Departure",
        str(train["departure_time"])[:5]
    )

with col2:
    metric_card(
        "🕔",
        "Arrival",
        str(train["arrival_time"])[:5]
    )

with col3:
    metric_card(
        "💺",
        "Total Seats",
        train["total_seats"]
    )

with col4:
    metric_card(
        "💰",
        "Ticket Fare",
        f"₹{float(train['fare']):,.2f}"
    )


# =====================================================
# CHECK SEAT AVAILABILITY
# =====================================================

section_heading(
    "💺 Seat Availability",
    "Check available seats for your selected journey"
)

if st.button(
    "🔍 Check Seat Availability",
    type="primary",
    use_container_width=True
):

    try:

        availability = get(
            f"/trains/{train['train_id']}/availability",
            params={
                "journey_date": journey_date.isoformat()
            }
        )

        st.session_state.booking_availability = availability

    except ApiError as exc:

        st.session_state.booking_availability = None

        st.error(
            f"Unable to check availability: {exc}"
        )


availability = st.session_state.booking_availability


# =====================================================
# DISPLAY AVAILABILITY
# =====================================================

if availability is not None:

    total_seats = int(train["total_seats"])

    available_count = int(
        availability.get("available_seats", 0)
    )

    booked_count = max(
        0,
        total_seats - available_count
    )

    section_heading(
        "📊 Seat Occupancy",
        "Current seat availability for your journey"
    )

    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    with col1:
        metric_card(
            "💺",
            "Total Seats",
            total_seats
        )

    with col2:
        metric_card(
            "✅",
            "Available Seats",
            available_count
        )

    with col3:
        metric_card(
            "🎫",
            "Booked Seats",
            booked_count
        )

    if total_seats > 0:

        occupancy = booked_count / total_seats

        st.write("")

        st.progress(
            min(max(occupancy, 0.0), 1.0),
            text=(
                f"{occupancy * 100:.1f}% "
                "of seats are booked"
            )
        )

    available_seats = (
        availability.get("available_seat_numbers") or []
    )

    # =================================================
    # SELECT SEAT
    # =================================================

    if not available_seats:

        st.warning(
            "No seats are available for this journey."
        )

    else:

        st.success(
            f"{len(available_seats)} seats are available."
        )

        section_heading(
            "🎫 Select Your Seat",
            "Choose an available seat to continue"
        )

        with st.container(border=True):

            seat_number = st.selectbox(
                "Available Seat Numbers",
                available_seats,
                format_func=lambda seat: f"💺 Seat {seat}",
                key=(
                    f"booking_seat_"
                    f"{train['train_id']}_"
                    f"{journey_date.isoformat()}"
                )
            )

        # =============================================
        # BOOKING SUMMARY
        # =============================================

        display_booking_summary(
            passenger,
            train,
            journey_date,
            seat_number
        )

        confirm_booking = st.button(
            "🎟️ Confirm Booking",
            type="primary",
            use_container_width=True
        )

        # =============================================
        # CREATE BOOKING
        # =============================================

        if confirm_booking:

            payload = {
                "train_id": train["train_id"],
                "passenger_id": passenger["passenger_id"],
                "journey_date": journey_date.isoformat(),
                "seat_number": int(seat_number)
            }

            try:

                result = post(
                    "/bookings/",
                    payload
                )

                booking_id = (
                    result.get("booking_id")
                    if isinstance(result, dict)
                    else result
                )

                st.session_state.booking_confirmation = {
                    "booking_id": booking_id,
                    "passenger": passenger["name"],
                    "train": train["train_name"],
                    "train_number": train["train_number"],
                    "source": train["source"],
                    "destination": train["destination"],
                    "journey_date": journey_date.isoformat(),
                    "seat_number": seat_number,
                    "fare": float(train["fare"])
                }

                # Invalidate old availability
                st.session_state.booking_availability = None

                st.rerun()

            except ApiError as exc:

                st.session_state.booking_availability = None

                st.error(
                    f"Booking failed: {exc}"
                )

                st.info(
                    "Seat availability may have changed. "
                    "Please check availability again."
                )


# =====================================================
# BOOKING CONFIRMATION
# =====================================================

confirmation = st.session_state.booking_confirmation

if confirmation:

    section_heading(
        "🎉 Booking Confirmation",
        "Your railway reservation has been created successfully"
    )

    st.success("Booking Created Successfully!")

    confirmation_html = f"""
    <div class="summary-card">

        <div class="summary-title">
            🎫 Booking #{safe(confirmation['booking_id'])}
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-bottom:20px;
        ">
            RailConnect Railway Reservation
        </div>
    """

    confirmation_html += summary_row(
        "Passenger Name",
        confirmation["passenger"]
    )

    confirmation_html += summary_row(
        "Train Name",
        confirmation["train"]
    )

    confirmation_html += summary_row(
        "Train Number",
        confirmation["train_number"]
    )

    confirmation_html += summary_row(
        "Route",
        (
            f"{confirmation['source']} → "
            f"{confirmation['destination']}"
        )
    )

    confirmation_html += summary_row(
        "Journey Date",
        confirmation["journey_date"]
    )

    confirmation_html += summary_row(
        "Seat Number",
        confirmation["seat_number"]
    )

    confirmation_html += summary_row(
        "Ticket Fare",
        f"₹{confirmation['fare']:,.2f}",
        highlight=True
    )

    confirmation_html += "</div>"

    st.html(confirmation_html)

    st.info(
        "Your booking has been created. "
        "Payment status is managed separately "
        "in Payment Management."
    )

    if st.button(
        "➕ Book Another Ticket",
        use_container_width=True
    ):

        st.session_state.booking_confirmation = None
        st.session_state.booking_availability = None

        st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.html("""
<div class="booking-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Railway Ticket Booking

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")