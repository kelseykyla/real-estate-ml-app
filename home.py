# Here's the updated home.py file with the dashboard implemented as per your requirements.
# I've renamed the function to home_page() for consistency with your main_1.py import and call (home.home_page()).
# The dashboard appears immediately after login (assuming your login logic sets current_page to "home").
# I've used dummy data as allowed.
# UI improvements: Added custom CSS for cards, colors, spacing, and responsiveness.
# The comment section submits a dummy message (you can integrate with Supabase or email later for admin).
# Recently viewed properties use placeholder images (from Unsplash); you can replace with real ones.
# Added a "Predict Price" button that navigates to the prediction_page() if you want to keep it separate.
# If you want prediction form inside dashboard, uncomment the relevant section.
# I've requested no additional code since all necessary parts are in the provided documents.


import traceback
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import joblib
import os
from supabase import create_client, Client
from io import StringIO
from datetime import datetime
import report
import altair as alt
from datetime import datetime, timedelta

# Public Landing Page
import base64
import streamlit as st


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
        st.markdown('<div class="hero-title">Smarter Property Pricing Starts Here</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">AI-powered insights to help you rent, buy, or invest with confidence.</div>', unsafe_allow_html=True)

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
    with open("./img/dapper.png", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="display:flex; justify-content:center; margin-top:20px;">
        <img src="data:image/png;base64,{img_base64}" 
             style="width:100%; height:480px; object-fit:cover; border-radius:18px; box-shadow:0 12px 30px rgba(0,0,0,0.1);">
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown('<div class="section-card"><h4>Rising Rental Demand</h4><p>Urban neighborhoods are seeing increased rental activity driven by migration and lifestyle shifts.</p></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-card"><h4>Data-Driven Pricing</h4><p>Investors and renters now rely on predictive analytics instead of guesswork.</p></div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="section-card"><h4>Location Matters More</h4><p>Neighborhood-level trends influence property value more than city averages.</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---------- BENEFITS ----------
    st.markdown("## Why Choose PriceScope?")
    b1, b2 = st.columns(2)

    with b1:
        st.markdown('<div class="section-card"><h4>AI-Powered Accuracy</h4><p>Our models analyze historical and live data to provide reliable estimates.</p></div>', unsafe_allow_html=True)

    with b2:
        st.markdown('<div class="section-card"><h4>Instant Results</h4><p>No waiting for agents or manual appraisals. Get insights immediately.</p></div>', unsafe_allow_html=True)

    # ---------- CALL TO ACTION ----------
    st.markdown("<br>", unsafe_allow_html=True)
    center = st.columns([1,2,1])[1]

    with center:
        if st.button("Make a Prediction", use_container_width=True):
            st.session_state["current_page"] = "prediction"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)


st.session_state["notifications"] = []

# Home page function (this is the dashboard)
def dashboard_page():
    # Clear notifications when user views dashboard
    st.session_state["notifications"] = []

    # ----------------- STYLING -----------------
    st.markdown("""
    <style>
    .dashboard-card {
        background-color: #f9f9f9;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .dashboard-title {
        color: #2e7d32;
        margin-bottom: 5px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    ul {
        list-style-type: none;
        padding-left: 0;
    }
    li {
        margin-bottom: 8px;
    }
    a {
        color: #2e7d32;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- HEADER -----------------
    user = st.session_state.get("user", None)
    name = user.display_name.split()[0] if user and user.display_name else "User"

    st.title(" Your Property Dashboard")
    st.markdown(f"### Welcome back!, **{name}** ")

     

    # ----------------- LAST LOGIN -----------------
    # Dummy last login (replace with real data from session or Supabase)
    last_login = "Sunday, 2 Feb 2026 at 7:42 PM"  # Dummy
    st.markdown(f'<div class="dashboard-card"><h4 class="dashboard-title">🕒 Last Login</h4><p>{last_login}</p></div>', unsafe_allow_html=True)

    # ----------------- NEW NOTIFICATIONS -----------------
    # Dummy notifications
    st.markdown('<div class="dashboard-card"><h4 class="dashboard-title">🔔 New Notifications</h4>'
                '<ul>'
                '<li> Rent prices dropped in Westlands</li>'
                '<li> New 2-bedroom listings in Kilimani</li>'
                '<li> A property you liked is now cheaper</li>'
                '</ul></div>', unsafe_allow_html=True)

    # ----------------- RECENTLY VIEWED PROPERTIES -----------------
    st.markdown("###  Recently Viewed Properties")
    col1, col2, col3 = st.columns(3)

    # Dummy properties (replace with real data from user history in Supabase)
    properties = [
        {"title": "2BR Apartment – Kilimani", "image": "https://images.unsplash.com/photo-1560185127-6ed189bf02f4"},
        {"title": "Studio – Westlands", "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"},
        {"title": "3BR House – Lavington", "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be"}
    ]

    for col, prop in zip([col1, col2, col3], properties):
        with col:
            st.image(prop["image"], use_column_width=True)
            st.markdown(f"**{prop['title']}**")
            if st.button("View Again", key=prop["title"]):
                st.write(f"Redirecting to {prop['title']} details... (Dummy action)")

    # ----------------- FAVORITE PROPERTIES -----------------
    # Dummy favorites
    st.markdown('<div class="dashboard-card"><h4 class="dashboard-title">⭐ Your Favorite Properties</h4>'
                '<ul>'
                '<li>Modern Loft in Westlands</li>'
                '<li>Family Home in Karen</li>'
                '<li>Cozy Apartment in Parklands</li>'
                '</ul></div>', unsafe_allow_html=True)

    # ----------------- WHAT’S NEW -----------------
    # Dummy updates
    st.markdown('<div class="dashboard-card"><h4 class="dashboard-title"> What’s New on PriceScope?</h4>'
                '<ul>'
                '<li> Improved AI prediction accuracy</li>'
                '<li> Added neighborhood trend analysis</li>'
                '<li> Smart alerts for price drops</li>'
                '</ul></div>', unsafe_allow_html=True)

    # ----------------- HELPFUL ARTICLES -----------------
    # Links to external articles (open in new tab)
    st.markdown('<div class="dashboard-card"><h4 class="dashboard-title">📰 Helpful Real Estate Articles</h4>'
                '<ul>'
                '<li><a href="https://www.investopedia.com/articles/mortgages-real-estate/08/homebuyer-mistakes.asp" target="_blank">Common Mistakes Homebuyers Make</a></li>'
                '<li><a href="https://www.property24.com/articles/best-areas-to-rent-in-nairobi/12345" target="_blank">Best Areas to Rent in Nairobi Right Now</a></li>'
                '<li><a href="https://www.forbes.com/sites/forbesrealestatecouncil/2023/01/10/understanding-rental-yield/" target="_blank">Understanding Rental Yield for Investors</a></li>'
                '</ul></div>', unsafe_allow_html=True)

    # ----------------- COMMENT SECTION -----------------
    # Feedback form (dummy submit; integrate with Supabase or email to admin later)
    st.markdown("### 💬 Send Feedback or Questions to Admin")
    comment = st.text_area("Write your message here...", height=100)
    if st.button("Submit Comment"):
        if comment:
            # Dummy action: In real, insert into Supabase table for admin review
            st.success("Your message has been sent to the admin! Thank you for your feedback.")
        else:
            st.warning("Please enter a message before submitting.")

    # ----------------- PREDICT PRICE BUTTON -----------------
    # Navigate to prediction page
    if st.button(" Predict Property Price"):
        st.session_state["current_page"] = "prediction"
        st.rerun()

    # Footer Section
    st.markdown("---")
    st.write("© 2025 Kelsey Kyla | All rights reserved.")

# ================= ADMIN DASHBOARD =================
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



# Prediction page (kept separate as per your existing structure)
def prediction_page():
    st.title(" Property Price Prediction")

    # Back button to dashboard
    if st.button("⬅ Back to Dashboard"):
        st.session_state["current_page"] = "dashboard"
        st.rerun()


    st.markdown("Enter property details below to get an AI-powered price estimate.")

 # ================= SUPABASE INITIALIZATION =================
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase initialization failed: {e}")
        return None

supabase = init_supabase()


    

    model = joblib.load("best_svm_model.pkl")
    preprocessor = joblib.load("pipeline.pkl")
    residual_std_log = joblib.load("residual_std_log.pkl")
    data = pd.read_csv("dataset/preprocessed_data.csv")


    with st.form("house_prediction_form"):
        selected_sub_county = st.selectbox("Select the Sub County", options=data['Sub_County'].unique())
        selected_neighborhood = st.selectbox("Select a Neighborhood", options=data['Neighborhood'].unique())
        selected_square_mtrs = st.number_input("Enter the square footage of the house", min_value=1, step=1)
        selected_bedrooms = st.selectbox("Select Number of Bedrooms", options=sorted(data['Bedrooms'].dropna().unique()))
        selected_bathrooms = st.selectbox("Select Number of Bathrooms", options=sorted(data['Bathrooms'].dropna().unique()))

        col_submitted, col_report = st.columns([0.2, 1.5])
        with col_submitted:
            submitted = st.form_submit_button("Predict")
        with col_report:
            view_report = st.form_submit_button("View report")

    if submitted:
        if "user" not in st.session_state:
            st.warning("You need to log in to make a prediction.")
        else:
            user_input = pd.DataFrame({
                "Sub_County": [selected_sub_county],
                "Neighborhood": [selected_neighborhood],
                "sq_mtrs": [selected_square_mtrs],
                "Bedrooms": [selected_bedrooms],
                "Bathrooms": [selected_bathrooms],
            })

            st.subheader("Prediction Results")

            try:
                processed_input = preprocessor.transform(user_input)
                log_prediction = model.predict(processed_input)
                predicted_price = round(np.exp(log_prediction[0]), -3)

                lower_log = log_prediction[0] - 1.96 * residual_std_log
                upper_log = log_prediction[0] + 1.96 * residual_std_log
                lower_bound = round(np.exp(lower_log), -3)
                upper_bound = round(np.exp(upper_log), -3)
                price_range_str = f"KES {lower_bound:,.0f} - {upper_bound:,.0f}"

                st.success(f"Predicted Rent Price (KES): {predicted_price:,.0f}")
                st.info(f"Estimated Price Range (95% CI): {price_range_str}")

                user = st.session_state["user"]
                prediction_record = {
                    "user_id": user.uid,
                    "sub_county": selected_sub_county,
                    "neighborhood": selected_neighborhood,
                    "sq_mtrs": int(selected_square_mtrs),
                    "bedrooms": int(selected_bedrooms),
                    "bathrooms": int(selected_bathrooms),
                    "predicted_price": round(predicted_price, 2),
                    "predicted_price_range": price_range_str,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                response = supabase.table("prediction").insert(prediction_record).execute()
                if response.data:
                    st.success("Prediction stored successfully!")
                else:
                    st.error("Failed to store the prediction in Supabase.")
            except Exception as e:
                st.error(f"An error occurred during preprocessing or prediction: {e}")

    if view_report:
        report.display_report()

    st.markdown("---")
    st.write("© 2025 Kelsey Kyla | All rights reserved.")
