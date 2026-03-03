import streamlit as st
import pandas as pd
import numpy as np
import joblib
from supabase import create_client, Client
from datetime import datetime
import report
import base64


# ===================== HOME PAGE =====================
def home_page():

    # ---------- GLOBAL MINIMALIST STYLE ----------
    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 600;
        color: #1b1b1b;
        margin-bottom: 10px;
    }

    .hero-sub {
        font-size: 18px;
        color: #555;
        margin-bottom: 25px;
    }

    .section-card {
        background-color: #ffffff;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .stat-number {
        font-size: 34px;
        font-weight: 600;
        color: #1b5e20;
    }

    .stat-label {
        font-size: 14px;
        color: #666;
    }

    .stButton>button {
        background-color: #1b5e20;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        font-size: 15px;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #2e7d32;
        color: white;
        transform: translateY(-2px);
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------- HEADER ----------
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(
            '<div class="hero-title">Smarter Property Pricing Starts Here</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="hero-sub">AI-powered insights to help you rent, buy, or invest with confidence.</div>',
            unsafe_allow_html=True
        )

    with col2:
        if "user" not in st.session_state:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Login"):
                    st.session_state["current_page"] = "login"
                    st.rerun()
            with c2:
                if st.button("Sign Up"):
                    st.session_state["current_page"] = "signup"
                    st.rerun()

    # ---------- HERO IMAGE ----------
    try:
        with open("./img/dapper.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-top:20px;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="width:100%; height:480px; object-fit:cover; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
    except:
        st.warning("Hero image not found.")

    # ---------- STATS ----------
    st.markdown("<br>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown("""
        <div style="text-align:center;">
            <div class="stat-number">10,000+</div>
            <div class="stat-label">Properties Analyzed</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div style="text-align:center;">
            <div class="stat-number">95%</div>
            <div class="stat-label">Prediction Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div style="text-align:center;">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Instant Valuations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------- MARKET INFO ----------
    st.markdown("## Market Intelligence")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="section-card"><h4>Rising Rental Demand</h4><p>Urban neighborhoods are seeing increased rental activity driven by migration and lifestyle shifts.</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="section-card"><h4>Data-Driven Pricing</h4><p>Investors and renters now rely on predictive analytics instead of guesswork.</p></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="section-card"><h4>Location Matters More</h4><p>Neighborhood-level trends influence property value more than city averages.</p></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---------- BENEFITS ----------
    st.markdown("## Why Choose PriceScope?")
    b1, b2 = st.columns(2)

    with b1:
        st.markdown(
            '<div class="section-card"><h4>AI-Powered Accuracy</h4><p>Our models analyze historical and live data to provide reliable estimates.</p></div>',
            unsafe_allow_html=True
        )

    with b2:
        st.markdown(
            '<div class="section-card"><h4>Instant Results</h4><p>No waiting for agents or manual appraisals. Get insights immediately.</p></div>',
            unsafe_allow_html=True
        )

# ---------- CALL TO ACTION ----------
    st.markdown("<br>", unsafe_allow_html=True)
    center = st.columns([1,2,1])[1]
    
    with center:
        if st.button("Make a Prediction", width="stretch"):
            if "user" not in st.session_state:
                st.session_state["current_page"] = "login"
            else:
                st.session_state["current_page"] = "prediction"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)

# ===================== USER DASHBOARD =====================
def dashboard_page():

    user = st.session_state.get("user", None)
    name = user.display_name.split()[0] if user and user.display_name else "User"

    st.title(" Your Property Dashboard")
    st.markdown(f"### Welcome back, **{name}** ")

    st.markdown("---")

    # ---------- METRICS ----------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Predictions Made", "124")
    col2.metric("Saved Properties", "18")
    col3.metric("Favorite Location", "Westlands")
    col4.metric("Average Rent", "KES 78,500")

    st.markdown("---")

    # ---------- RENT TREND CHART ----------
    st.subheader(" Rent Trend Overview")

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"]
    rents = [65000,67000,69000,71000,72000,74000,76000,78500]

    df_rent = pd.DataFrame({
        "Month": months,
        "Average Rent": rents
    }).set_index("Month")

    st.line_chart(df_rent)

    st.markdown("---")

    # ---------- LOCATION DISTRIBUTION ----------
    st.subheader(" Popular Locations")

    df_locations = pd.DataFrame({
        "Location": ["Westlands","Kilimani","Karen","Lavington","Embakasi"],
        "Listings": [120,95,70,85,60]
    }).set_index("Location")

    st.bar_chart(df_locations)

    st.markdown("---")

    # ---------- RECENTLY VIEWED ----------
    st.subheader(" Recently Viewed Properties")

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

    st.markdown("---")

    # ---------- NOTIFICATIONS ----------
    st.subheader(" Notifications")

    notifications = [
        "Rent prices dropped in Westlands",
        "New 2-bedroom listing in Kilimani",
        "A saved property is now cheaper"
    ]

    for note in notifications:
        st.write("•", note)

    st.markdown("---")

    # ---------- FEEDBACK ----------
    st.subheader(" Send Feedback")

    comment = st.text_area("Write your message here...", height=100)
    if st.button("Submit Feedback"):
        if comment:
            st.success("Message sent successfully!")
        else:
            st.warning("Please enter a message.")

    st.markdown("---")

    if st.button(" Predict Property Price"):
        st.session_state["current_page"] = "prediction"
        st.rerun()

    st.markdown("---")
    st.write("© 2026 Kelsey Kyla | All rights reserved.")

# ===================== ADMIN DASHBOARD =====================
def admin_dashboard():
    st.title("🛠 Admin Dashboard")
    st.markdown("Overview of system performance and user activity")

    st.markdown("---")
    st.subheader(" Platform Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Registered Users", "1,284")
    col2.metric("🏠 Total Listings", "856")
    col3.metric("📈 New Users This Month", "73")

    st.markdown("---")
    st.subheader(" Growth Trends")

    import pandas as pd
    import numpy as np

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_year_users = [50, 60, 55, 70, 65, 80, 90, 85, 100, 95, 110, 120]
    this_year_users = [80, 90, 95, 110, 105, 130, 140, 150, 160, 170, 180, 200]

    df_users = pd.DataFrame({
        "Month": months,
        "Last Year": last_year_users,
        "This Year": this_year_users
    }).set_index("Month")

    st.line_chart(df_users)

    st.markdown("---")
    st.subheader("🏘 Listing Activity Trends")

    last_year_listings = np.random.randint(20, 50, 12)
    this_year_listings = np.random.randint(40, 80, 12)

    df_listings = pd.DataFrame({
        "Month": months,
        "Last Year Listings": last_year_listings,
        "This Year Listings": this_year_listings
    }).set_index("Month")

    st.bar_chart(df_listings)

    st.markdown("---")
    st.subheader(" Property Insights")

    colA, colB = st.columns(2)

    with colA:
        st.info("**Last Posted Property**\n\n3 Bedroom Apartment in Kilimani")

        st.success(" **Most Popular Location**\n\nWestlands")

        st.warning("**Least Popular Location**\n\nEmbakasi")

    with colB:
        st.metric("💰 Average Rent Price", "KES 78,500")
        st.metric("⭐ Most Viewed Property", "2BR Apartment – Kilimani")

    st.markdown("---")
    st.subheader("👤 User Activity & Feedback")

    if st.button("View User Comments"):
        comments = [
            "Alice: Love the prediction feature!",
            "Brian: Please add house sale predictions too.",
            "Cynthia: Very accurate for Westlands listings.",
            "David: Add price history charts please."
        ]
        for c in comments:
            st.write("💬", c)

    if st.button("View User Activity Log"):
        activity = [
            "User123 searched for 2BR in Kilimani",
            "User456 made a prediction for Westlands property",
            "User789 viewed listing in Karen",
            "User321 saved property in Parklands"
        ]
        for a in activity:
            st.write("📌", a)

    st.markdown("---")
    st.caption("Admin Panel • PriceScope System Monitoring")

# ===================== PREDICTION PAGE =====================
def prediction_page():

    st.title(" Property Price Prediction")

    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()

    st.markdown("Enter property details below to get an AI-powered estimate.")

    # Supabase inside function
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    model = joblib.load("best_svm_model.pkl")
    data = pd.read_csv("dataset/preprocessed_data.csv")

    with st.form("house_prediction_form"):
        sub = st.selectbox("Sub County", data["Sub_County"].unique())
        neigh = st.selectbox("Neighborhood", data["Neighborhood"].unique())
        sqm = st.number_input("Square Meters", min_value=1)
        beds = st.selectbox("Bedrooms", sorted(data["Bedrooms"].dropna().unique()))
        baths = st.selectbox("Bathrooms", sorted(data["Bathrooms"].dropna().unique()))
        submitted = st.form_submit_button("Predict")

    if submitted:
        if "user" not in st.session_state:
            st.warning("You need to log in to make a prediction.")
            return

        user_input = pd.DataFrame({
            "Sub_County": [sub],
            "Neighborhood": [neigh],
            "sq_mtrs": [sqm],
            "Bedrooms": [beds],
            "Bathrooms": [baths],
        })

        log_prediction = model.predict(user_input)
        predicted_price = round(np.exp(log_prediction[0]), -3)

        st.success(f"Predicted Rent Price (KES): {predicted_price:,.0f}")

        try:
            prediction_record = {
                "user_id": st.session_state["user"].uid,
                "sub_county": sub,
                "neighborhood": neigh,
                "sq_mtrs": int(sqm),
                "bedrooms": int(beds),
                "bathrooms": int(baths),
                "predicted_price": float(predicted_price),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            supabase.table("prediction").insert(prediction_record).execute()
        except Exception as e:
            st.error(f"Database error: {e}")

    st.markdown("---")
    st.write("© 2026 Kelsey Kyla | All rights reserved.")
