from datetime import time, datetime
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api_client import ApiError, delete, get, post, put, trains


# ==========================================================
# CUSTOM CSS
# ==========================================================

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

.train-header {
    background: linear-gradient(110deg, #132D50, #0E1D35);
    border: 1px solid #28476D;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 30px;
}

.train-header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #FFFFFF;
}

.train-header-subtitle {
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

/* ================= FORMS ================= */

[data-testid="stForm"] {
    background: #111E31;
    border: 1px solid #26364D;
    border-radius: 15px;
    padding: 25px;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTimeInput"] input {
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

/* ================= BUTTONS ================= */

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
    color: white;
    border-color: #F97316;
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

/* ================= TABS ================= */

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

/* ================= FOOTER ================= */

.train-footer {
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

    .train-header {
        padding: 24px;
    }

    .train-header-title {
        font-size: 25px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

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


def parse_time(value):

    if isinstance(value, time):
        return value

    if isinstance(value, datetime):
        return value.time()

    if value is None:
        return time(9, 0)

    value = str(value).strip()

    try:
        return time.fromisoformat(value)

    except ValueError:
        return time(9, 0)


def format_time(value):

    if value is None:
        return "N/A"

    try:
        return parse_time(value).strftime("%I:%M %p")

    except (ValueError, TypeError):
        return str(value)


def train_label(train):

    return (
        f"{train.get('train_number', 'N/A')} — "
        f"{train.get('train_name', 'Unnamed Train')} "
        f"(ID: {train.get('train_id')})"
    )


def validate_train_data(number, name, source, destination):

    if not all([
        number.strip(),
        name.strip(),
        source.strip(),
        destination.strip()
    ]):
        return "Please fill in all required fields."

    if source.strip().casefold() == destination.strip().casefold():
        return "Source and destination cannot be the same."

    return None


def save_success(message):

    st.session_state["train_success"] = message
    st.rerun()


def show_success_message():

    message = st.session_state.pop(
        "train_success",
        None
    )

    if message:
        st.success(message)


# ==========================================================
# DARK PLOTLY TRAIN TABLE
# ==========================================================

def display_dark_train_table(df):

    row_colors = [
        "#111E31" if i % 2 == 0 else "#16263D"
        for i in range(len(df))
    ]

    fig = go.Figure(
        data=[
            go.Table(

                columnwidth=[
                    70,   # Train ID
                    110,  # Train Number
                    180,  # Train Name
                    120,  # From
                    120,  # To
                    110,  # Departure
                    110,  # Arrival
                    100,  # Seats
                    100   # Fare
                ],

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

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        height=min(
            650,
            50 + len(df) * 42
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )


# ==========================================================
# PAGE HEADER
# ==========================================================

st.html("""
<div class="train-header">

    <div class="train-header-title">
        🚆 Train Management
    </div>

    <div class="train-header-subtitle">
        Manage railway schedules, train routes,
        seat capacity and ticket fares from one place.
    </div>

</div>
""")

show_success_message()


# ==========================================================
# FETCH TRAINS
# ==========================================================

try:
    train_rows = trains() or []

except ApiError as exc:
    st.error(f"Unable to load trains: {exc}")
    st.stop()

if not isinstance(train_rows, list):
    st.error("Unexpected response from the trains API.")
    st.stop()


# ==========================================================
# TRAIN STATISTICS
# ==========================================================

total_trains = len(train_rows)

total_seats = sum(
    int(train.get("total_seats") or 0)
    for train in train_rows
)

unique_routes = len({
    (
        str(train.get("source", "")).strip().casefold(),
        str(train.get("destination", "")).strip().casefold()
    )
    for train in train_rows
})


section_heading(
    "📊 Railway Overview",
    "Current train inventory and route statistics"
)

col1, col2, col3 = st.columns(
    3,
    gap="medium"
)

with col1:
    metric_card("🚄", "Total Trains", total_trains)

with col2:
    metric_card("💺", "Total Seat Capacity", total_seats)

with col3:
    metric_card("🛤️", "Available Routes", unique_routes)


# ==========================================================
# SEARCH TRAINS
# ==========================================================

section_heading(
    "🔍 Search Trains",
    "Filter trains by departure and arrival stations"
)

search_col1, search_col2, search_col3 = st.columns(
    [2, 2, 1],
    gap="medium"
)

with search_col1:

    source_filter = st.text_input(
        "Departure Station",
        placeholder="e.g. Kanpur",
        key="train_source_filter"
    )

with search_col2:

    destination_filter = st.text_input(
        "Arrival Station",
        placeholder="e.g. Delhi",
        key="train_destination_filter"
    )

with search_col3:

    st.write("")
    st.write("")

    if st.button(
        "Clear Filters",
        use_container_width=True
    ):

        st.session_state["train_source_filter"] = ""
        st.session_state["train_destination_filter"] = ""
        st.rerun()


# ==========================================================
# FILTER TRAINS
# ==========================================================

display_rows = [
    train
    for train in train_rows
    if (
        not source_filter.strip()
        or source_filter.strip().casefold()
        in str(train.get("source", "")).casefold()
    )
    and (
        not destination_filter.strip()
        or destination_filter.strip().casefold()
        in str(train.get("destination", "")).casefold()
    )
]


# ==========================================================
# TRAIN DIRECTORY
# ==========================================================

section_heading(
    "📋 Train Directory",
    "Browse train schedules, routes and ticket fares"
)

if display_rows:

    formatted_rows = []

    for train in display_rows:

        formatted_rows.append({
            "Train ID": train.get("train_id"),
            "Train Number": train.get("train_number"),
            "Train Name": train.get("train_name"),
            "From": train.get("source"),
            "To": train.get("destination"),
            "Departure": format_time(
                train.get("departure_time")
            ),
            "Arrival": format_time(
                train.get("arrival_time")
            ),
            "Total Seats": train.get("total_seats"),
            "Fare (₹)": f"₹{float(train.get('fare') or 0):,.2f}"
        })

    df = pd.DataFrame(formatted_rows)

    display_dark_train_table(df)

    st.caption(
        f"Showing {len(display_rows)} "
        f"of {total_trains} trains"
    )

else:
    st.info("No trains match the selected filters.")


# ==========================================================
# TRAIN OPERATIONS
# ==========================================================

section_heading(
    "⚙️ Manage Trains",
    "Register, update or remove railway train records"
)

add_tab, update_tab, delete_tab = st.tabs([
    "➕ Add Train",
    "✏️ Update Train",
    "🗑️ Delete Train"
])


# ==========================================================
# ADD TRAIN
# ==========================================================

with add_tab:

    st.subheader("Register a New Train")

    st.caption("Fields marked with * are required.")

    with st.form("add_train_form"):

        col1, col2 = st.columns(2, gap="large")

        with col1:

            train_number = st.text_input(
                "Train Number *",
                placeholder="e.g. 12001"
            )

            train_name = st.text_input(
                "Train Name *",
                placeholder="e.g. Shatabdi Express"
            )

            form_source = st.text_input(
                "Source Station *",
                placeholder="e.g. Kanpur"
            )

            departure = st.time_input(
                "Departure Time",
                value=time(9, 0)
            )

            total_seats_input = st.number_input(
                "Total Seats",
                min_value=1,
                value=100,
                step=1
            )

        with col2:

            form_destination = st.text_input(
                "Destination Station *",
                placeholder="e.g. Delhi"
            )

            arrival = st.time_input(
                "Arrival Time",
                value=time(17, 0)
            )

            fare = st.number_input(
                "Ticket Fare (₹)",
                min_value=0.01,
                value=500.0,
                step=50.0
            )

        submitted = st.form_submit_button(
            "➕ Register Train",
            type="primary",
            use_container_width=True
        )

    if submitted:

        error = validate_train_data(
            train_number,
            train_name,
            form_source,
            form_destination
        )

        if error:
            st.warning(error)

        else:

            payload = {
                "train_number": train_number.strip(),
                "train_name": train_name.strip(),
                "source": form_source.strip(),
                "destination": form_destination.strip(),
                "departure_time": departure.isoformat(),
                "arrival_time": arrival.isoformat(),
                "total_seats": int(total_seats_input),
                "fare": float(fare)
            }

            try:

                result = post(
                    "/trains/",
                    payload
                )

                train_id = (
                    result.get("train_id", "Created")
                    if isinstance(result, dict)
                    else "Created"
                )

                save_success(
                    f"Train registered successfully! "
                    f"Train ID: {train_id}"
                )

            except ApiError as exc:
                st.error(
                    f"Unable to add train: {exc}"
                )


# ==========================================================
# UPDATE TRAIN
# ==========================================================

with update_tab:

    st.subheader("Update Existing Train")

    if not train_rows:
        st.info("No trains available to update.")

    else:

        train_options = {
            train["train_id"]: train
            for train in train_rows
        }

        selected_id = st.selectbox(
            "Select Train",
            options=list(train_options.keys()),
            format_func=lambda train_id: train_label(
                train_options[train_id]
            ),
            key="update_train_selector"
        )

        current_train = train_options[selected_id]

        with st.form(
            f"update_train_form_{selected_id}"
        ):

            col1, col2 = st.columns(2, gap="large")

            with col1:

                update_number = st.text_input(
                    "Train Number",
                    value=str(
                        current_train.get("train_number") or ""
                    ),
                    key=f"train_number_{selected_id}"
                )

                update_name = st.text_input(
                    "Train Name",
                    value=str(
                        current_train.get("train_name") or ""
                    ),
                    key=f"train_name_{selected_id}"
                )

                update_source = st.text_input(
                    "Source Station",
                    value=str(
                        current_train.get("source") or ""
                    ),
                    key=f"train_source_{selected_id}"
                )

                update_departure = st.time_input(
                    "Departure Time",
                    value=parse_time(
                        current_train.get("departure_time")
                    ),
                    key=f"train_departure_{selected_id}"
                )

                update_seats = st.number_input(
                    "Total Seats",
                    min_value=1,
                    value=int(
                        current_train.get("total_seats") or 1
                    ),
                    step=1,
                    key=f"train_seats_{selected_id}"
                )

            with col2:

                update_destination = st.text_input(
                    "Destination Station",
                    value=str(
                        current_train.get("destination") or ""
                    ),
                    key=f"train_destination_{selected_id}"
                )

                update_arrival = st.time_input(
                    "Arrival Time",
                    value=parse_time(
                        current_train.get("arrival_time")
                    ),
                    key=f"train_arrival_{selected_id}"
                )

                update_fare = st.number_input(
                    "Ticket Fare (₹)",
                    min_value=0.01,
                    value=max(
                        0.01,
                        float(current_train.get("fare") or 0.01)
                    ),
                    step=50.0,
                    key=f"train_fare_{selected_id}"
                )

            update_submitted = st.form_submit_button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True
            )

        if update_submitted:

            error = validate_train_data(
                update_number,
                update_name,
                update_source,
                update_destination
            )

            if error:
                st.warning(error)

            else:

                payload = {
                    "train_number": update_number.strip(),
                    "train_name": update_name.strip(),
                    "source": update_source.strip(),
                    "destination": update_destination.strip(),
                    "departure_time": update_departure.isoformat(),
                    "arrival_time": update_arrival.isoformat(),
                    "total_seats": int(update_seats),
                    "fare": float(update_fare)
                }

                try:

                    put(
                        f"/trains/{selected_id}",
                        payload
                    )

                    save_success(
                        "Train details updated successfully!"
                    )

                except ApiError as exc:
                    st.error(
                        f"Unable to update train: {exc}"
                    )


# ==========================================================
# DELETE TRAIN
# ==========================================================

with delete_tab:

    st.subheader("Delete Train")

    st.warning(
        "Deleting a train is permanent. "
        "Trains with existing bookings may not be removable."
    )

    if not train_rows:
        st.info("No trains available to delete.")

    else:

        delete_options = {
            train["train_id"]: train
            for train in train_rows
        }

        delete_id = st.selectbox(
            "Select Train to Delete",
            options=list(delete_options.keys()),
            format_func=lambda train_id: train_label(
                delete_options[train_id]
            ),
            key="delete_train_selector"
        )

        selected_train = delete_options[delete_id]

        st.info(
            f"Selected train: "
            f"{selected_train['train_name']} "
            f"({selected_train['train_number']})"
        )

        confirm_delete = st.checkbox(
            "I understand that this action cannot be undone.",
            key=f"confirm_delete_{delete_id}"
        )

        if st.button(
            "🗑️ Delete Selected Train",
            type="primary",
            disabled=not confirm_delete,
            use_container_width=True
        ):

            try:

                delete(
                    f"/trains/{delete_id}"
                )

                save_success(
                    "Train deleted successfully!"
                )

            except ApiError as exc:
                st.error(
                    f"Unable to delete train: {exc}"
                )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.html("""
<div class="train-footer">

    <span style="color:#F97316;font-weight:600;">
        RailConnect
    </span>

    | Train Management System

    <br>

    Powered by FastAPI • MySQL • Streamlit

</div>
""")