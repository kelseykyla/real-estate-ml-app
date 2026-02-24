import streamlit as st
# Page Title and Configuration
st.set_page_config(
    page_title="""Predictive Real Estate Pricing Model Using Machine Learning Algorithm and Historical Data Analysis.""",
    layout="wide",
)

from streamlit_option_menu import option_menu
from form.login import login_page
from form.signup import signup_page
import home # Import home page function
import about
import contact
import report
from account import account_page  # Import the account page functionality
from firebase_init import initialize_firebase  # Ensure Firebase initialization

st.write("Home module path:", home.__file__)
# Initialize Firebase
initialize_firebase()



# Initialize session state for page management
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"  # Default to home page

if "notifications" not in st.session_state:
    st.session_state["notifications"] = [
        "🏘 New property listed in Kilimani",
        "📉 Price drop alert in Westlands",
        "⭐ A saved property has new photos"
    ]

if "show_notifications" not in st.session_state:
    st.session_state["show_notifications"] = False


def get_notification_count():
    # 🔔 Dummy number for now
    # Later this can come from Supabase per user
    return 3


# Sidebar menu with option menu
def sidebar_menu():
    with st.sidebar:
        st.image("./img/Logo1.png", use_container_width=True)

        options = ['Dashboard', 'Prediction', 'Account', 'About', 'Contact']

        if st.session_state.get("is_admin"):
            options.append('Admin')

        options.append('Logout')

        app = option_menu(
            menu_title='PRICE SCOPE',
            options=options,
            icons=['speedometer2','graph-up','person-circle','info-circle','chat-dots','gear','box-arrow-right'],
            menu_icon='🏡',
            default_index=0,
        )
        return app




# Main navigation logic
def main():

    # NOT LOGGED IN
    if "user" not in st.session_state:

        if st.session_state["current_page"] == "home":
            home.home_page()

        elif st.session_state["current_page"] == "login":
            login_page()

        elif st.session_state["current_page"] == "signup":
            signup_page()
        
        # Direct dashboard routing after login
        if st.session_state["current_page"] == "dashboard":
            if st.session_state.get("is_admin"):
                home.admin_dashboard()
            else:
                home.dashboard_page()
            return


    # LOGGED IN
    else:
        app = sidebar_menu()

        if app == "Dashboard":
            if st.session_state.get("is_admin"):
                home.admin_dashboard()   # 👑 Admin sees admin dashboard
            else:
                home.dashboard_page()    # 👤 Normal user sees user dashboard


        elif app == "Prediction":
            home.prediction_page()

        elif app == "Account":
            account_page()

        elif app == "About":
            about.app()

        elif app == "Contact":
            contact.app()

        elif app == "Admin" and st.session_state.get("is_admin"):
            home.admin_dashboard()

        elif app == "Logout":
            del st.session_state["user"]
            st.session_state["current_page"] = "home"
            st.rerun()

# Run the app
if __name__ == "__main__":
    main()
