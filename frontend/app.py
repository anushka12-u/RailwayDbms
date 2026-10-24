import streamlit as st
from api_client import ApiError, get
from html import escape

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="RailConnect | Railway Management",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PAGE ROUTES =================

PAGE_TRAIN_MANAGEMENT = "pages/2_Train_Management.py"
PAGE_BOOK_TICKET = "pages/4_Book_Ticket.py"
PAGE_PASSENGER_MANAGEMENT = "pages/3_Passenger_Management.py"
PAGE_BOOKING_HISTORY = "pages/5_Booking_History.py"
PAGE_PAYMENT_MANAGEMENT = "pages/6_Payment_Management.py"
PAGE_DASHBOARD = "pages/1_Dashboard.py"


# ================= CUSTOM CSS =================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

/* ================= REMOVE STREAMLIT HEADER ================= */

header[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ================= GLOBAL ================= */

html, body, .stApp {
    background-color: #080F1E !important;
    color: #E2E8F0;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1400px;
    padding-top: 1rem !important;
    padding-bottom: 2rem;
    margin-top: 0 !important;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #0D1729 !important;
    border-right: 1px solid #1E293B;
}

section[data-testid="stSidebar"] * {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] a {
    border-radius: 8px;
    transition: 0.2s;
}

section[data-testid="stSidebar"] a:hover {
    background: #1E3A5F;
}

/* ================= TYPOGRAPHY ================= */

h1, h2, h3 {
    font-family: 'Poppins', sans-serif;
    color: #F8FAFC !important;
}

p {
    color: #94A3B8;
}

/* ================= NAVBAR ================= */

.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 25px;
    background: #101C30;
    border: 1px solid #243247;
    border-radius: 14px;
    margin-bottom: 25px;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 15px;
}

.rail-logo {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    background: linear-gradient(135deg, #F97316, #EA580C);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    border: 2px solid #FDBA74;
}

.brand-title {
    font-family: 'Poppins', sans-serif;
    font-size: 23px;
    font-weight: 700;
    color: #FFFFFF;
}

.brand-subtitle {
    font-size: 11px;
    color: #94A3B8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.nav-status {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #4ADE80;
    font-size: 12px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4ADE80;
    box-shadow: 0 0 10px #22C55E;
}

/* ================= HERO ================= */

.hero {
    background:
        radial-gradient(
            circle at 85% 30%,
            rgba(37,99,235,0.24),
            transparent 40%
        ),
        linear-gradient(
            115deg,
            #10294B,
            #142D50,
            #0B1930
        );

    border: 1px solid #28476D;
    border-radius: 20px;
    padding: 45px;
    margin-bottom: 35px;
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "🚆";
    position: absolute;
    right: 60px;
    top: 30px;
    font-size: 120px;
    opacity: 0.13;
}

.hero-badge {
    display: inline-block;
    padding: 7px 14px;
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.35);
    border-radius: 20px;
    color: #FDBA74;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 37px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.3;
    margin-bottom: 15px;
}

.hero-title span {
    color: #FB923C;
}

.hero-subtitle {
    font-size: 15px;
    color: #CBD5E1;
    line-height: 1.8;
    max-width: 620px;
}

/* ================= SECTION HEADINGS ================= */

.section-heading {
    font-family: 'Poppins', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 25px;
    margin-bottom: 20px;
}

.section-subtitle {
    font-size: 13px;
    color: #94A3B8;
    margin-top: -15px;
    margin-bottom: 22px;
}

/* ================= METRIC CARDS ================= */

.metric-card {
    background: linear-gradient(
        145deg,
        #121F33,
        #0F1B2D
    );

    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 25px;
    min-height: 155px;
    transition: all 0.25s ease;
    position: relative;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #3B82F6;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

.metric-icon {
    font-size: 25px;
    margin-bottom: 18px;
}

.metric-label {
    color: #94A3B8;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #F8FAFC;
    overflow-wrap: anywhere;
}

.metric-accent {
    position: absolute;
    width: 35px;
    height: 3px;
    background: #F97316;
    bottom: 0;
    left: 25px;
    border-radius: 5px;
}

/* ================= ACTION CARDS ================= */

.action-card {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 27px;
    min-height: 190px;
    transition: 0.25s;
}

.action-card:hover {
    background: #162640;
    border-color: #3B82F6;
    transform: translateY(-3px);
}

.action-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1D3555;
    border-radius: 12px;
    font-size: 25px;
    margin-bottom: 18px;
}

.action-title {
    font-family: 'Poppins', sans-serif;
    font-size: 17px;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 9px;
}

.action-description {
    font-size: 13px;
    line-height: 1.7;
    color: #94A3B8;
}

/* ================= BUTTONS ================= */

.stButton > button {
    width: 100%;
    background: #182A44;
    color: #E2E8F0;
    border: 1px solid #304563;
    border-radius: 9px;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 12px 18px;
    transition: 0.25s;
}

.stButton > button:hover {
    background: #1D4ED8;
    border-color: #3B82F6;
    color: white;
    transform: translateY(-2px);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(120deg, #EA580C, #F97316);
    color: white;
    border: none;
}

.stButton > button[kind="primary"]:hover {
    background: #C2410C;
    color: white;
}

/* ================= SERVICE BOX ================= */

.service-box {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}

.service-title {
    font-size: 14px;
    color: #CBD5E1;
    font-weight: 600;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    padding: 25px;
    line-height: 2;
}

.footer span {
    color: #F97316;
}

hr {
    border-color: #26364D !important;
}

/* ================= RESPONSIVE ================= */

@media(max-width: 768px) {

    .hero {
        padding: 28px;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero::after {
        display: none;
    }

    .navbar {
        padding: 14px;
    }

    .brand-title {
        font-size: 17px;
    }

    .nav-status {
        display: none;
    }
}

</style>
""")


# ================= NAVBAR =================

st.html("""
<div class="navbar">

    <div class="nav-brand">

        <div class="rail-logo">🚆</div>

        <div>
            <div class="brand-title">
                RailConnect
            </div>

            <div class="brand-subtitle">
                Railway Management System
            </div>
        </div>

    </div>

    <div class="nav-status">
        <div class="status-dot"></div>
        Railway Portal
    </div>

</div>
""")


# ================= HERO =================

st.html("""
<div class="hero">

    <div class="hero-badge">
        🇮🇳 INDIAN RAILWAY MANAGEMENT
    </div>

    <div class="hero-title">
        Your Journey.<br>
        <span>Our Priority.</span>
    </div>

    <div class="hero-subtitle">
        Welcome to RailConnect — your intelligent railway
        management platform. Seamlessly manage train schedules,
        passenger records, ticket reservations and payments
        through one unified dashboard.
    </div>

</div>
""")


# ================= DASHBOARD METRICS =================

st.html("""
<div class="section-heading">
    📊 Railway Overview
</div>

<div class="section-subtitle">
    Overview of your railway management operations
</div>
""")


def metric_card(label, value, icon):

    st.html(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{escape(str(label))}</div>
        <div class="metric-value">{escape(str(value))}</div>
        <div class="metric-accent"></div>
    </div>
    """)


# ================= FETCH DATA =================

def load_dashboard_metrics():

    trains = get("/trains/") or []

    passengers = get("/passengers/") or []

    bookings = get("/bookings/") or []

    payments = get("/payments/") or []

    successful_payments = [
        payment
        for payment in payments
        if str(payment.get("payment_status", "")).upper() == "SUCCESS"
    ]

    revenue = sum(
        float(payment.get("amount") or 0)
        for payment in successful_payments
    )

    return (
        len(trains),
        len(passengers),
        len(bookings),
        revenue
    )


try:

    (
        total_trains,
        total_passengers,
        total_bookings,
        revenue
    ) = load_dashboard_metrics()

    dashboard_error = None

except ApiError as exc:

    total_trains = "N/A"
    total_passengers = "N/A"
    total_bookings = "N/A"
    revenue = "N/A"

    dashboard_error = str(exc)


# ================= DISPLAY METRICS =================

col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)

with col1:
    metric_card(
        "Total Trains",
        total_trains,
        "🚄"
    )

with col2:
    metric_card(
        "Registered Passengers",
        total_passengers,
        "👥"
    )

with col3:
    metric_card(
        "Total Reservations",
        total_bookings,
        "🎫"
    )

with col4:

    revenue_value = (
        f"₹{revenue:,.2f}"
        if isinstance(revenue, (int, float))
        else revenue
    )

    metric_card(
        "Total Revenue",
        revenue_value,
        "💰"
    )


if dashboard_error:
    st.warning(
        f"Dashboard data unavailable: {dashboard_error}"
    )


# ================= QUICK ACTIONS =================

st.html("""
<div class="section-heading">
    ⚡ Quick Actions
</div>

<div class="section-subtitle">
    Access essential railway services
</div>
""")


col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


# ================= TRAIN MANAGEMENT =================

with col1:

    st.html("""
    <div class="action-card">

        <div class="action-icon">🚄</div>

        <div class="action-title">
            Train Management
        </div>

        <div class="action-description">
            Add, update and manage trains,
            railway routes and train schedules.
        </div>

    </div>
    """)

    st.write("")

    if st.button(
        "Manage Trains →",
        key="trains",
        type="primary"
    ):
        st.switch_page(PAGE_TRAIN_MANAGEMENT)


# ================= BOOK TICKET =================

with col2:

    st.html("""
    <div class="action-card">

        <div class="action-icon">🎟️</div>

        <div class="action-title">
            Ticket Reservation
        </div>

        <div class="action-description">
            Search available trains,
            check seat availability
            and reserve railway tickets.
        </div>

    </div>
    """)

    st.write("")

    if st.button(
        "Book Ticket →",
        key="booking"
    ):
        st.switch_page(PAGE_BOOK_TICKET)


# ================= PASSENGER MANAGEMENT =================

with col3:

    st.html("""
    <div class="action-card">

        <div class="action-icon">👥</div>

        <div class="action-title">
            Passenger Management
        </div>

        <div class="action-description">
            Register passengers,
            manage passenger information
            and view passenger records.
        </div>

    </div>
    """)

    st.write("")

    if st.button(
        "View Passengers →",
        key="passengers"
    ):
        st.switch_page(PAGE_PASSENGER_MANAGEMENT)


# ================= MORE SERVICES =================

st.html("""
<div class="section-heading">
    🛠️ Additional Services
</div>

<div class="section-subtitle">
    Manage your railway operations efficiently
</div>
""")


col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


# BOOKING HISTORY

with col1:

    st.html("""
    <div class="service-box">
        <div class="service-title">
            📜 Reservation History
        </div>
    </div>
    """)

    if st.button(
        "View Booking History",
        key="history"
    ):
        st.switch_page(PAGE_BOOKING_HISTORY)


# PAYMENT MANAGEMENT

with col2:

    st.html("""
    <div class="service-box">
        <div class="service-title">
            💳 Payment Services
        </div>
    </div>
    """)

    if st.button(
        "Manage Payments",
        key="payments"
    ):
        st.switch_page(PAGE_PAYMENT_MANAGEMENT)


# DASHBOARD

with col3:

    st.html("""
    <div class="service-box">
        <div class="service-title">
            📈 Railway Analytics
        </div>
    </div>
    """)

    if st.button(
        "View Dashboard",
        key="dashboard"
    ):
        st.switch_page(PAGE_DASHBOARD)


# ================= FOOTER =================

st.divider()

st.html("""
<div class="footer">

    <span>RailConnect</span> |
    Railway Management System

    <br>

    Powered by FastAPI • MySQL • Streamlit

    <br>

    DBMS Academic Project | Made in India 🇮🇳

</div>
""")