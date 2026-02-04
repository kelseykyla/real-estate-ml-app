import streamlit as st
from firebase_admin import auth
from firebase_init import initialize_firebase
import base64
from .forgot_password import forgot_password_page

# Initialize Firebase
initialize_firebase()

def login_page():

    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    img_base64 = get_base64_image('img/image.png')
    logo_base64 = get_base64_image('img/Logo1.png')

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url('data:image/avif;base64,{img_base64}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align: center;'>Login to Your Account</h3>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([0.3, 0.4, 0.3])

    if not st.session_state.get('forgot_password', False):
        with col2:
            with st.form("login_form", border=True):

                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <img src="data:image/png;base64,{logo_base64}" width="200">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                email = st.text_input("Email Address", key="email_input")
                password = st.text_input("Password", type="password", key="password_input")

                col_login, col_forgot = st.columns([0.6, 0.4])

                with col_login:
                    submit_button = st.form_submit_button("Login")

                with col_forgot:
                    if st.form_submit_button("Forgot Password?", type="secondary"):
                        st.session_state['forgot_password'] = True
                        st.rerun()

                if submit_button:
                    try:
                        user = auth.get_user_by_email(email)

                        # Store user in session
                        st.session_state["user"] = user

                        # 👑 ADMIN CHECK
                        admin_emails = ["admin@pricescope.com", "kelsey@admin.com"]
                        st.session_state["is_admin"] = user.email in admin_emails

                        # Go to dashboard
                        st.session_state["current_page"] = "dashboard"

                        st.success(f"Login successful! Welcome {user.display_name.split()[0]}")
                        st.rerun()

                    except Exception as e:
                        st.error("Invalid login credentials or user does not exist.")

    else:
        forgot_password_page()
