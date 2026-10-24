import re
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api_client import ApiError, passengers, post, put


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');

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

/* Keep sidebar toggle visible */

header[data-testid="stHeader"] {
    background-color: #080F1E !important;
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

.passenger-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 30px;
}

.passenger-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
}

.passenger-header-subtitle {
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
    min-height: 160px;
    transition: 0.25s;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #F97316;
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

/* FORMS */

[data-testid="stForm"] {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 25px;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #0B1728 !important;
    color: #FFFFFF !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #F97316 !important;
}

[data-testid="stWidgetLabel"] p {
    color: #CBD5E1 !important;
    font-size: 13px;
    font-weight: 500;
}

/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button {
    background: #182A44;
    color: #FFFFFF;
    border: 1px solid #304563;
    border-radius: 9px;
    font-weight: 600;
    transition: 0.25s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #1E3A5F;
    border-color: #F97316;
    color: white;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(120deg, #EA580C, #F97316);
    border: none;
    color: white;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #C2410C;
    color: white;
}

/* TABS */

button[data-baseweb="tab"] {
    color: #CBD5E1 !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FB923C !important;
}

[data-baseweb="tab-highlight"] {
    background-color: #F97316 !important;
}

/* FOOTER */

.passenger-footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 25px;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1.5rem 1rem !important;
    }

    .passenger-header {
        padding: 24px;
    }

    .passenger-header-title {
        font-size: 25px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def metric_card(icon, label, value):
    st.html(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{escape(str(label))}</div>
        <div class="metric-value">{escape(str(value))}</div>
    </div>
    """)


def section_heading(title, subtitle=None):
    st.html(f"""
    <div class="section-title">
        {escape(title)}
    </div>
    """)

    if subtitle:
        st.html(f"""
        <div class="section-subtitle">
            {escape(subtitle)}
        </div>
        """)


def valid_email(email):
    email = email.strip()

    if not email:
        return True

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        )
    )


def valid_phone(phone):
    phone = phone.strip()

    if not phone:
        return True

    return bool(
        re.fullmatch(
            r"[6-9]\d{9}",
            phone
        )
    )


def validate_passenger(name, email, phone):
    if not name.strip():
        return "Passenger name is required."

    if not valid_email(email):
        return "Enter a valid email address."

    if not valid_phone(phone):
        return "Enter a valid 10-digit Indian mobile number."

    return None


def save_success(message):
    st.session_state["passenger_success"] = message
    st.rerun()


def show_success_message():
    message = st.session_state.pop(
        "passenger_success",
        None
    )

    if message:
        st.success(message)


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
                columnwidth=[85, 150, 60, 90, 230, 130],

                header=dict(
                    values=[
                        f"<b>{escape(str(col))}</b>"
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
                            escape(str(value))
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
<div class="passenger-header">

    <div class="passenger-header-title">
        👥 Passenger Management
    </div>

    <div class="passenger-header-subtitle">
        Register passengers, manage profiles
        and maintain passenger records.
    </div>

</div>
""")

show_success_message()


# =====================================================
# LOAD PASSENGERS
# =====================================================

try:
    rows = passengers() or []

except ApiError as exc:
    st.error(f"Unable to load passengers: {exc}")
    st.stop()

if not isinstance(rows, list):
    st.error("Unexpected response from passengers API.")
    st.stop()


# =====================================================
# PASSENGER STATISTICS
# =====================================================

total_passengers = len(rows)

male_count = sum(
    str(p.get("gender", "")).strip().casefold() == "male"
    for p in rows
)

female_count = sum(
    str(p.get("gender", "")).strip().casefold() == "female"
    for p in rows
)

ages = []

for passenger in rows:
    try:
        if passenger.get("age") is not None:
            ages.append(int(passenger["age"]))
    except (ValueError, TypeError):
        pass

average_age = (
    round(sum(ages) / len(ages), 1)
    if ages else 0
)


section_heading(
    "📊 Passenger Overview",
    "Passenger statistics and demographic information"
)

col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)

with col1:
    metric_card("👥", "Total Passengers", total_passengers)

with col2:
    metric_card("👨", "Male Passengers", male_count)

with col3:
    metric_card("👩", "Female Passengers", female_count)

with col4:
    metric_card("📊", "Average Age", average_age)


# =====================================================
# SEARCH PASSENGERS
# =====================================================

section_heading(
    "🔍 Search Passengers",
    "Find passengers by name, email, phone number or ID"
)

search_query = st.text_input(
    "Search Passenger",
    placeholder="Search by name, email, phone or passenger ID...",
    key="passenger_search"
)

query = search_query.strip().casefold()

filtered_rows = [
    passenger
    for passenger in rows
    if not query or any(
        query in str(passenger.get(field) or "").casefold()
        for field in (
            "name",
            "email",
            "phone",
            "passenger_id"
        )
    )
]


# =====================================================
# PASSENGER DIRECTORY
# =====================================================

section_heading(
    "📋 Passenger Directory",
    "Browse registered passenger records"
)

if filtered_rows:

    formatted_rows = []

    for passenger in filtered_rows:
        formatted_rows.append({
            "Passenger ID": passenger.get("passenger_id"),
            "Name": passenger.get("name"),
            "Age": passenger.get("age"),
            "Gender": passenger.get("gender"),
            "Email": passenger.get("email") or "—",
            "Phone": passenger.get("phone") or "—"
        })

    df = pd.DataFrame(formatted_rows)

    display_dark_table(df)

    st.caption(
        f"Showing {len(filtered_rows)} "
        f"of {total_passengers} passengers"
    )

else:
    st.info("No passengers match your search.")


# =====================================================
# PASSENGER OPERATIONS
# =====================================================

section_heading(
    "⚙️ Manage Passengers",
    "Register new passengers or update existing profiles"
)

register_tab, update_tab = st.tabs([
    "➕ Register Passenger",
    "✏️ Update Passenger"
])


# =====================================================
# REGISTER PASSENGER
# =====================================================

with register_tab:

    st.subheader("Register New Passenger")
    st.caption("Fields marked with * are required.")

    with st.form("register_passenger_form"):

        col1, col2 = st.columns(2, gap="large")

        with col1:

            name = st.text_input(
                "Full Name *",
                placeholder="Enter passenger name"
            )

            age = st.number_input(
                "Age *",
                min_value=1,
                max_value=119,
                value=18
            )

            gender = st.selectbox(
                "Gender *",
                ["Male", "Female", "Other"]
            )

        with col2:

            email = st.text_input(
                "Email Address",
                placeholder="example@gmail.com"
            )

            phone = st.text_input(
                "Phone Number",
                placeholder="10-digit mobile number"
            )

        submitted = st.form_submit_button(
            "➕ Register Passenger",
            type="primary",
            use_container_width=True
        )

    if submitted:

        error = validate_passenger(
            name,
            email,
            phone
        )

        if error:
            st.warning(error)

        else:

            payload = {
                "name": name.strip(),
                "age": int(age),
                "gender": gender,
                "email": email.strip() or None,
                "phone": phone.strip() or None
            }

            try:

                result = post(
                    "/passengers/",
                    payload
                )

                passenger_id = (
                    result.get("passenger_id", "Created")
                    if isinstance(result, dict)
                    else result or "Created"
                )

                save_success(
                    f"Passenger registered successfully! "
                    f"Passenger ID: {passenger_id}"
                )

            except ApiError as exc:
                st.error(
                    f"Unable to register passenger: {exc}"
                )


# =====================================================
# UPDATE PASSENGER
# =====================================================

with update_tab:

    st.subheader("Update Existing Passenger")

    if not rows:
        st.info("No passengers available to update.")

    else:

        passenger_options = {
            int(p["passenger_id"]): p
            for p in rows
        }

        selected_id = st.selectbox(
            "Select Passenger",
            options=list(passenger_options.keys()),
            format_func=lambda pid: (
                f"#{pid} — {passenger_options[pid]['name']}"
            ),
            key="passenger_update_selector"
        )

        current = passenger_options[selected_id]

        with st.form(
            f"update_passenger_form_{selected_id}"
        ):

            col1, col2 = st.columns(2, gap="large")

            with col1:

                update_name = st.text_input(
                    "Full Name *",
                    value=current.get("name") or "",
                    key=f"passenger_name_{selected_id}"
                )

                update_age = st.number_input(
                    "Age *",
                    min_value=1,
                    max_value=119,
                    value=int(current.get("age") or 18),
                    key=f"passenger_age_{selected_id}"
                )

                gender_options = [
                    "Male",
                    "Female",
                    "Other"
                ]

                current_gender = str(
                    current.get("gender") or "Other"
                ).capitalize()

                if current_gender not in gender_options:
                    current_gender = "Other"

                update_gender = st.selectbox(
                    "Gender *",
                    gender_options,
                    index=gender_options.index(
                        current_gender
                    ),
                    key=f"passenger_gender_{selected_id}"
                )

            with col2:

                update_email = st.text_input(
                    "Email Address",
                    value=current.get("email") or "",
                    key=f"passenger_email_{selected_id}"
                )

                update_phone = st.text_input(
                    "Phone Number",
                    value=current.get("phone") or "",
                    key=f"passenger_phone_{selected_id}"
                )

            update_submitted = st.form_submit_button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True
            )

        if update_submitted:

            error = validate_passenger(
                update_name,
                update_email,
                update_phone
            )

            if error:
                st.warning(error)

            else:

                payload = {
                    "name": update_name.strip(),
                    "age": int(update_age),
                    "gender": update_gender,
                    "email": update_email.strip() or None,
                    "phone": update_phone.strip() or None
                }

                try:

                    put(
                        f"/passengers/{selected_id}",
                        payload
                    )

                    save_success(
                        "Passenger details updated successfully!"
                    )

                except ApiError as exc:
                    st.error(
                        f"Unable to update passenger: {exc}"
                    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.html("""
<div class="passenger-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Passenger Management System

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")