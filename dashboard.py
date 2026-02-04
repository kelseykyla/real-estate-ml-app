# dashboard.py
import streamlit as st

def user_dashboard():
    st.markdown("""
    <style>
    .dashboard-card {
        background: #f8fafc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .card-title {
        color: #1a3c34;
        font-size: 1.25rem;
        margin-bottom: 12px;
    }
    .green-btn {
        background-color: #2f855a !important;
        color: white !important;
        border-radius: 8px !important;
    }
    ul { list-style: none; padding-left: 0; }
    li { margin: 8px 0; }
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")
    first_name = user.display_name.split()[0] if user and user.display_name else "User"

    st.title("🏡 Your PriceScope Dashboard")
    st.markdown(f"### Hello, **{first_name}** 👋")

    # Last login (dummy for now – later fetch from Supabase or auth metadata)
    st.markdown(
        '<div class="dashboard-card"><div class="card-title">🕒 Last Login</div>'
        '<p>February 3, 2026 at 6:15 PM</p></div>',
        unsafe_allow_html=True
    )

    # Notifications
    st.markdown(
        '<div class="dashboard-card"><div class="card-title">🔔 Notifications</div>'
        '<ul>'
        '<li>📉 Rent prices in Westlands dropped 4.2% this month</li>'
        '<li>🏘 3 new verified 2BR listings in Kilimani</li>'
        '<li>⭐ Your saved property in Lavington just got cheaper</li>'
        '</ul></div>',
        unsafe_allow_html=True
    )

    # Recently viewed
    st.subheader("👀 Recently Viewed Properties")
    cols = st.columns(3)
    props = [
        ("2BR Apartment – Kilimani", "https://images.unsplash.com/photo-1560185127-6ed189bf02f4"),
        ("Studio – Westlands", "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"),
        ("3BR House – Lavington", "https://images.unsplash.com/photo-1570129477492-45c003edd2be"),
    ]

    for col, (title, img) in zip(cols, props):
        with col:
            st.image(img, use_column_width=True)
            st.markdown(f"**{title}**")
            st.button("View Again", key=f"view_{title}", use_container_width=True)

    # Favorites
    st.markdown(
        '<div class="dashboard-card"><div class="card-title">⭐ Your Favorites</div>'
        '<ul><li>Modern Loft – Westlands</li><li>Family Home – Karen</li><li>Cozy 1BR – Parklands</li></ul></div>',
        unsafe_allow_html=True
    )

    # What's new
    st.markdown(
        '<div class="dashboard-card"><div class="card-title">🚀 What’s New</div>'
        '<ul>'
        '<li>Improved prediction model (better accuracy)</li>'
        '<li>Neighborhood trend charts added</li>'
        '<li>Price drop alerts now available</li>'
        '</ul></div>',
        unsafe_allow_html=True
    )

    # Articles
    st.markdown(
        '<div class="dashboard-card"><div class="card-title">📰 Helpful Articles</div>'
        '<ul>'
        '<li><a href="https://www.property24.com/articles/best-areas-to-rent-in-nairobi/..." target="_blank">Best Areas to Rent in Nairobi 2026</a></li>'
        '<li><a href="https://www.investopedia.com/articles/personal-finance/..." target="_blank">How to Spot an Overpriced Property</a></li>'
        '<li><a href="https://www.forbes.com/sites/.../understanding-rental-yield/" target="_blank">Rental Yield Explained</a></li>'
        '</ul></div>',
        unsafe_allow_html=True
    )

    # Feedback
    st.subheader("💬 Send Feedback / Ask a Question")
    comment = st.text_area("Your message to admin...", height=110)
    if st.button("Submit", type="primary"):
        if comment.strip():
            st.success("Message sent to admin! Thank you.")
        else:
            st.warning("Please write something first.")

    # Quick action
    st.markdown("---")
    if st.button("🔍 Predict a New Property Price", type="primary", use_container_width=True):
        st.session_state["current_page"] = "prediction"
        st.rerun()

    st.caption("© 2025 PriceScope | Built by Kelsey Kyla")