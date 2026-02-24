import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
from supabase import create_client
from datetime import datetime
import report


# ================= SUPABASE INITIALIZATION =================
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


# ================= LANDING PAGE =================
def home_page():

    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 600;
        color: #1b1b1b;
    }
    .hero-sub {
        font-size: 18px;
        color: #555;
    }
    .section-card {
        background-color: #ffffff;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown('<div class="hero-title">Smarter Property Pricing Starts Here</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">AI-powered insights to help you rent, buy, or invest with confidence.</div>', unsafe_allow_html=True)

    with col2:
        if "user" not in st.session_state:
            if st.button("Login"):
                st.session_state["current_page"] = "login"
                st.rerun()
            if st.button("Sign Up"):
                st.session_state["current_page"] = "signup"
                st.rerun()

    try:
        with open("./img/dapper.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-top:20px;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="width:100%; height:480px; object-fit:cover; border-radius:18px;">
        </div>
        """, unsafe_allow_html=True)
    except:
        pass


# ================= USER DASHBOARD =================
def dashboard_page():

    user = st.session_state.get("user", None)
    name = user.display_name.split()[0] if user and user.display_name else "User"

    st.title("Your Property Dashboard")
    st.markdown(f"Welcome back, **{name}**")

    st.markdown("### Recently Viewed Properties")
    col1, col2, col3 = st.columns(3)

    properties = [
        {"title": "2BR Apartment – Kilimani", "image": "https://images.unsplash.com/photo-1560185127-6ed189bf02f4"},
        {"title": "Studio – Westlands", "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"},
        {"title": "3BR House – Lavington", "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be"}
    ]

    for col, prop in zip([col1, col2, col3], properties):
        with col:
            st.image(prop["image"], width="stretch")
            st.markdown(f"**{prop['title']}**")

    if st.button("Predict Property Price"):
        st.session_state["current_page"] = "prediction"
        st.rerun()


# ================= ADMIN DASHBOARD =================
def admin_dashboard():

    st.title("Admin Dashboard")
    st.subheader("Platform Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", "1,284")
    col2.metric("Total Listings", "856")
    col3.metric("New Users This Month", "73")

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    last_year = [50,60,55,70,65,80,90,85,100,95,110,120]
    this_year = [80,90,95,110,105,130,140,150,160,170,180,200]

    df = pd.DataFrame({
        "Month": months,
        "Last Year": last_year,
        "This Year": this_year
    }).set_index("Month")

    st.line_chart(df)


# ================= PREDICTION PAGE =================
def prediction_page():

    st.title("Property Price Prediction")

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

    supabase = init_supabase()

    model = joblib.load("best_svm_model.pkl")
    preprocessor = joblib.load("pipeline.pkl")
    residual_std_log = joblib.load("residual_std_log.pkl")
    data = pd.read_csv("dataset/preprocessed_data.csv")

    with st.form("prediction_form"):
        sub = st.selectbox("Sub County", data["Sub_County"].unique())
        neigh = st.selectbox("Neighborhood", data["Neighborhood"].unique())
        sqm = st.number_input("Square Meters", min_value=1)
        beds = st.selectbox("Bedrooms", sorted(data["Bedrooms"].dropna().unique()))
        baths = st.selectbox("Bathrooms", sorted(data["Bathrooms"].dropna().unique()))

        submitted = st.form_submit_button("Predict")

    if submitted:
        if "user" not in st.session_state:
            st.warning("Login required.")
            return

        user_input = pd.DataFrame({
            "Sub_County": [sub],
            "Neighborhood": [neigh],
            "sq_mtrs": [sqm],
            "Bedrooms": [beds],
            "Bathrooms": [baths],
        })

        processed = preprocessor.transform(user_input)
        log_pred = model.predict(processed)
        price = round(np.exp(log_pred[0]), -3)

        st.success(f"Predicted Rent: KES {price:,.0f}")

        prediction_record = {
            "user_id": st.session_state["user"].uid,
            "sub_county": sub,
            "neighborhood": neigh,
            "sq_mtrs": int(sqm),
            "bedrooms": int(beds),
            "bathrooms": int(baths),
            "predicted_price": float(price),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            supabase.table("prediction").insert(prediction_record).execute()
            st.success("Stored successfully.")
        except Exception as e:
            st.error(f"Database error: {e}")
