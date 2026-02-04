import streamlit as st

def account_page():
    if "user" in st.session_state:
        user = st.session_state.get("user")

        display_name = user.display_name if user.display_name else ""
        name_parts = display_name.split()

        first_name = name_parts[0] if len(name_parts) > 0 else "Admin"
        last_name = name_parts[1] if len(name_parts) > 1 else "Admin"

        
        st.title(f"Welcome, {first_name} ")
        
        # Display account details
        st.subheader("Your Account Overview")
        st.write(f"**First Name:** {first_name}")
        st.write(f"**Last Name:** {last_name}")
        st.write(f"**Username:** {user.uid}")
        st.write(f"**Email:** {user.email}")
        
        # Add an option to sign out
        if st.button("Sign Out"):
            del st.session_state["user"]
            st.session_state["current_page"] = "home"  # Redirect to login page
            st.success("You have been signed out.")
            st.rerun()  # Rerun to show login page

    else:
        st.warning("Please log in to view your account.")

    # Footer Section
    st.markdown("---")
    st.write("© 2025 Kelsey Kyla | All rights reserved.")
