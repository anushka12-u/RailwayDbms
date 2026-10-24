from html import escape

import streamlit as st

from api_client import ApiError, get, post


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
    background: #080F1E !important;
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

.payment-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 25px;
}

.payment-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
}

.payment-header-subtitle {
    font-size: 14px;
    color: #A8BAD0;
    margin-top: 10px;
}

/* ================= DEMO NOTICE ================= */

.demo-notice {
    background: rgba(249, 115, 22, 0.08);
    border: 1px solid rgba(249, 115, 22, 0.35);
    border-left: 4px solid #F97316;
    border-radius: 10px;
    padding: 16px 20px;
    color: #FED7AA;
    font-size: 13px;
    margin-bottom: 25px;
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

/* ================= DETAIL CARDS ================= */

.detail-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 28px;
    margin: 18px 0;
}

.detail-title {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 18px;
}

.detail-subtitle {
    color: #94A3B8;
    font-size: 13px;
    margin-bottom: 20px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 13px 0;
    border-bottom: 1px solid #26364D;
}

.detail-label {
    color: #94A3B8;
    font-size: 13px;
}

.detail-value {
    color: #F8FAFC;
    font-size: 14px;
    font-weight: 600;
    text-align: right;
    overflow-wrap: anywhere;
}

.highlight-value {
    color: #FB923C;
    font-size: 21px;
    font-weight: 700;
}

/* ================= PAYMENT STATUS ================= */

.status-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
}

.status-success {
    background: rgba(34, 197, 94, 0.15);
    color: #4ADE80;
}

.status-failed {
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
}

.status-pending {
    background: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
}

/* ================= INPUTS ================= */

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: #0B1728 !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
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
    min-height: 45px;
    transition: 0.25s;
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

/* ================= FOOTER ================= */

.payment-footer {
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

    .payment-header {
        padding: 24px;
    }

    .payment-header-title {
        font-size: 25px;
    }

    .detail-card {
        padding: 18px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def safe(value):
    if value is None:
        return "—"

    return escape(str(value))


def format_currency(amount):
    try:
        return f"₹{float(amount):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


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


def detail_row(label, value, highlight=False):

    value_class = (
        "detail-value highlight-value"
        if highlight
        else "detail-value"
    )

    return f"""
    <div class="detail-row">
        <span class="detail-label">{safe(label)}</span>
        <span class="{value_class}">{safe(value)}</span>
    </div>
    """


def status_badge(status):

    status = str(status or "UNKNOWN").upper()

    if status in ("SUCCESS", "COMPLETED", "PAID"):
        css_class = "status-success"

    elif status in ("FAILED", "CANCELLED"):
        css_class = "status-failed"

    else:
        css_class = "status-pending"

    return f"""
    <span class="status-badge {css_class}">
        {safe(status)}
    </span>
    """


def render_receipt(confirmation):

    section_heading(
        "🧾 Transaction Receipt",
        "Payment transaction details"
    )

    receipt_html = f"""
    <div class="detail-card">

        <div class="detail-title">
            💳 Payment #{safe(confirmation.get('payment_id'))}
        </div>

        <div class="detail-subtitle">
            RailConnect • Demo Payment Receipt
        </div>
    """

    receipt_html += detail_row(
        "Booking ID",
        confirmation.get("booking_id")
    )

    receipt_html += detail_row(
        "Payment ID",
        confirmation.get("payment_id")
    )

    receipt_html += detail_row(
        "Payment Method",
        confirmation.get("payment_method")
    )

    receipt_html += detail_row(
        "Amount",
        format_currency(confirmation.get("amount")),
        highlight=True
    )

    receipt_html += """
        <div style="margin-top:20px;">
    """

    receipt_html += status_badge(
        confirmation.get("payment_status")
    )

    receipt_html += "</div></div>"

    st.html(receipt_html)


def load_bookings():

    try:

        rows = get("/bookings/")

        if not isinstance(rows, list):
            raise ValueError(
                "Unexpected bookings API response."
            )

        st.session_state.payment_bookings = rows
        st.session_state.payment_loaded = True

        return True

    except (ApiError, ValueError) as exc:

        st.session_state.payment_loaded = False
        st.session_state.payment_bookings = []

        st.error(
            f"Unable to load bookings: {exc}"
        )

        return False


# =====================================================
# SESSION STATE
# =====================================================

if "payment_bookings" not in st.session_state:
    st.session_state.payment_bookings = []

if "payment_loaded" not in st.session_state:
    st.session_state.payment_loaded = False

if "payment_confirmation" not in st.session_state:
    st.session_state.payment_confirmation = None

if "payment_selected_booking_id" not in st.session_state:
    st.session_state.payment_selected_booking_id = None


# =====================================================
# PAGE HEADER
# =====================================================

st.html("""
<div class="payment-header">

    <div class="payment-header-title">
        💳 Payment Management
    </div>

    <div class="payment-header-subtitle">
        Manage railway booking payments,
        process transactions and view payment receipts.
    </div>

</div>
""")

st.html("""
<div class="demo-notice">
    ℹ️ <strong>Demo Payment System:</strong>
    All transactions are simulated.
    No real money is transferred.
</div>
""")


# =====================================================
# LOAD BOOKINGS
# =====================================================

section_heading(
    "🎟️ Select Booking",
    "Load railway reservations to begin payment processing"
)

col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.write(
        "Load existing railway bookings to select "
        "a reservation for payment."
    )

with col2:

    if st.button(
        "🔄 Load Bookings",
        use_container_width=True,
        type="primary"
    ):
        load_bookings()


booking_rows = st.session_state.payment_bookings


# =====================================================
# EMPTY STATE
# =====================================================

if not st.session_state.payment_loaded:

    st.info(
        "Click 'Load Bookings' to view reservations."
    )

    st.stop()


if not booking_rows:

    st.warning("No bookings are available.")
    st.stop()


# =====================================================
# BOOKING STATISTICS
# =====================================================

confirmed_bookings = [
    booking
    for booking in booking_rows
    if str(
        booking.get("booking_status", "CONFIRMED")
    ).upper() == "CONFIRMED"
]

cancelled_count = sum(
    str(booking.get("booking_status", "")).upper()
    == "CANCELLED"
    for booking in booking_rows
)

section_heading(
    "📊 Booking Overview",
    "Current railway reservation statistics"
)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    metric_card(
        "🎟️",
        "Total Bookings",
        len(booking_rows)
    )

with col2:
    metric_card(
        "✅",
        "Confirmed",
        len(confirmed_bookings)
    )

with col3:
    metric_card(
        "❌",
        "Cancelled",
        cancelled_count
    )


# =====================================================
# SELECT CONFIRMED BOOKING
# =====================================================

section_heading(
    "🚆 Choose Reservation",
    "Select a confirmed booking to view payment options"
)

if not confirmed_bookings:

    st.warning(
        "No confirmed bookings are available for payment."
    )

    st.stop()


booking = st.selectbox(
    "Choose Booking",
    confirmed_bookings,
    format_func=lambda row: (
        f"Booking #{row['booking_id']} | "
        f"Passenger #{row.get('passenger_id', '—')} | "
        f"Train #{row.get('train_id', '—')}"
    ),
    key="payment_booking_selector"
)

selected_booking_id = booking["booking_id"]


# =====================================================
# RESET RECEIPT WHEN BOOKING CHANGES
# =====================================================

if (
    st.session_state.payment_selected_booking_id
    != selected_booking_id
):

    st.session_state.payment_selected_booking_id = (
        selected_booking_id
    )

    st.session_state.payment_confirmation = None


# =====================================================
# BOOKING DETAILS
# =====================================================

section_heading(
    "📋 Booking Details",
    "Review reservation information before payment"
)

booking_html = f"""
<div class="detail-card">

    <div class="detail-title">
        🎟️ Booking #{safe(booking['booking_id'])}
    </div>

    <div class="detail-subtitle">
        Railway Reservation Details
    </div>
"""

booking_html += detail_row(
    "Passenger ID",
    booking.get("passenger_id")
)

booking_html += detail_row(
    "Train ID",
    booking.get("train_id")
)

booking_html += detail_row(
    "Journey Date",
    booking.get("journey_date")
)

booking_html += detail_row(
    "Seat Number",
    booking.get("seat_number")
)

booking_html += detail_row(
    "Booking Status",
    booking.get("booking_status", "CONFIRMED")
)

booking_html += detail_row(
    "Booking Date",
    booking.get("booking_date")
)

booking_html += "</div>"

st.html(booking_html)


# =====================================================
# PAYMENT DETAILS
# =====================================================

section_heading(
    "💰 Payment Details",
    "Review payment status and complete your transaction"
)


# =====================================================
# DISPLAY CURRENT TRANSACTION RECEIPT
# =====================================================

confirmation = st.session_state.payment_confirmation

if (
    confirmation
    and confirmation.get("booking_id") == selected_booking_id
):

    status = str(
        confirmation.get("payment_status", "")
    ).upper()

    if status in ("SUCCESS", "COMPLETED", "PAID"):
        st.success("Payment completed successfully!")

    elif status == "FAILED":
        st.error("Payment was not successful.")

    else:
        st.info(
            f"Payment status: {status or 'UNKNOWN'}"
        )

    render_receipt(confirmation)

    if st.button(
        "🔄 Make Another Payment",
        use_container_width=True
    ):

        st.session_state.payment_confirmation = None
        load_bookings()
        st.rerun()

    st.stop()


# =====================================================
# CHECK EXISTING PAYMENT
# =====================================================

existing_payment = None
payment_lookup_failed = False

try:

    existing_payment = get(
        f"/payments/booking/{selected_booking_id}"
    )

except ApiError as exc:

    # The endpoint may return 404 when no payment exists.
    # For other errors, payment processing should be blocked.
    error_text = str(exc).lower()

    if (
        "404" not in error_text
        and "not found" not in error_text
    ):

        payment_lookup_failed = True

        st.error(
            f"Unable to verify existing payment: {exc}"
        )


if payment_lookup_failed:
    st.stop()


# =====================================================
# EXISTING PAYMENT DISPLAY
# =====================================================

if isinstance(existing_payment, list):

    existing_payment = next(
        (
            payment
            for payment in existing_payment
            if str(payment.get("payment_status", "")).upper() == "SUCCESS"
        ),
        None,
    )

if isinstance(existing_payment, dict):

    payment_status = str(
        existing_payment.get("payment_status", "")
    ).upper()

    if payment_status in ("SUCCESS", "COMPLETED", "PAID"):

        st.success(
            "This booking has already been paid."
        )

        render_receipt({
            "booking_id": selected_booking_id,
            "payment_id": existing_payment.get("payment_id"),
            "amount": existing_payment.get("amount"),
            "payment_method": existing_payment.get("payment_method"),
            "payment_status": payment_status
        })

        st.stop()


# =====================================================
# COMPLETE PAYMENT
# =====================================================

section_heading(
    "💳 Complete Payment",
    "Select your payment method and confirm the transaction"
)

st.caption(
    "This is a simulated payment. "
    "No bank account or payment gateway is involved."
)

with st.container(border=True):

    fare = booking.get("fare")
    if fare is None:
        st.error("The ticket fare is unavailable. Payment is disabled.")
        st.stop()

    amount = float(fare)
    st.metric("Amount Payable", format_currency(amount))

    payment_method = st.selectbox(
        "Payment Method",
        [
            "UPI",
            "CARD",
            "NET_BANKING",
            "CASH"
        ],
        key=f"payment_method_{selected_booking_id}"
    )

    st.html(
        '<div style="height:10px;"></div>'
    )

    payment_summary = """
    <div class="detail-card">
        <div class="detail-title">
            💰 Payment Summary
        </div>
    """

    payment_summary += detail_row(
        "Booking ID",
        selected_booking_id
    )

    payment_summary += detail_row(
        "Payment Method",
        payment_method
    )

    payment_summary += detail_row(
        "Amount Payable",
        format_currency(amount),
        highlight=True
    )

    payment_summary += "</div>"

    st.html(payment_summary)

    confirm = st.checkbox(
        "I confirm that I want to simulate this payment.",
        key=f"payment_confirm_{selected_booking_id}"
    )

    pay_clicked = st.button(
        f"💳 Pay {format_currency(amount)}",
        type="primary",
        use_container_width=True,
        disabled=not confirm,
        key=f"payment_submit_{selected_booking_id}"
    )


# =====================================================
# PROCESS PAYMENT
# =====================================================

if pay_clicked:

    payload = {
        "booking_id": selected_booking_id,
        "amount": float(amount),
        "payment_method": payment_method
    }

    try:

        result = post(
            "/payments/",
            payload
        )

        if not isinstance(result, dict):
            result = {
                "payment_id": result,
                "payment_status": "UNKNOWN"
            }

        st.session_state.payment_confirmation = {
            "booking_id": selected_booking_id,
            "payment_id": result.get("payment_id", "—"),
            "amount": result.get("amount", amount),
            "payment_method": result.get(
                "payment_method",
                payment_method
            ),
            "payment_status": result.get(
                "payment_status",
                "UNKNOWN"
            )
        }

        st.rerun()

    except ApiError as exc:

        st.error(
            f"Payment could not be processed: {exc}"
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.html("""
<div class="payment-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Payment Management

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")