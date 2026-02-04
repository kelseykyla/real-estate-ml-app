from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import io
import numpy as np
from supabase import create_client, Client # type: ignore
import streamlit as st
import supabase # type: ignore
import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO

# Supabase Initialization
url = os.environ.get("supabase_url")
key = os.environ.get("supabase_key")
supabase: Client = create_client(url, key) # type: ignore

def display_report():
    if "user" not in st.session_state:
        st.warning("You need to log in to access the report.")
        return

    user = st.session_state["user"]

    try:
        response = supabase.table("prediction").select("*").eq("user_id", user.uid).execute()

        if response.data:
            predictions = pd.DataFrame(response.data)

            # Fetch user details (Robust Metadata Handling)
            user_email = user.email
            user_name = "N/A"  # Default value
            if user.user_metadata:
                if isinstance(user.user_metadata, dict):
                    user_name = user.user_metadata.get('full_name', user.user_metadata.get('name', 'N/A'))
                else:
                    user_name = str(user.user_metadata)  # if it is not a dictionary.
            user_uid = user.uid

           

            # Save the plot to a BytesIO object
            plot_bytes = BytesIO()
            plt.savefig(plot_bytes, format='png')
            plot_bytes.seek(0)

            # Calculation
            #predictions["percentage_error"] = 100 * (predictions["predicted_price"] - predictions["Actual_price"]) / predictions["Actual_price"]
            #avg_percentage_error = predictions["percentage_error"].mean()

            # Display the data in the app
            st.write("Overview of prediction report:")
            simplified_predictions = predictions[[
                "sub_county", "neighborhood", "sq_mtrs", "bedrooms", "bathrooms", "predicted_price"
            ]]
            st.write(simplified_predictions)
            st.pyplot(plt) # type: ignore

            #st.write(f"Average Percentage Error: {avg_percentage_error:.2f}%")

            # Generate PDF report
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            page_width, page_height = letter

            # Logo
            logo_path = "./img/Logo1.png"  # Adjust the path as needed
            try:
                logo = ImageReader(logo_path)
                logo_width = 150 # logo width
                x_center = (page_width - logo_width) / 1.8 # calculate x center
                c.drawImage(logo, x_center, page_height - 100, width=logo_width, height=80)  # Adjust position and size
            except FileNotFoundError:
                st.warning("Logo file not found. Logo not included in PDF.")


            # Report Title
            title_text = "PREDICTION REPORT"
            font_size = 18
            font_name = "Helvetica-Bold"

            c.setFont(font_name, font_size)
            left_margin = 20

            text_width_approx = len(title_text) * (font_size / 2)
            x_center = (page_width - text_width_approx) / 2
            y_center = page_height - 118 -10

            c.drawString(x_center, y_center, title_text)




            # User Details title.
            title_text = "User Details."
            font_size = 12
            c.setFont(font_name, font_size)

            text_width_approx = len(title_text) * (font_size / 2)
            x_center = (page_width - text_width_approx) / 5.5
            y_center = 640

            c.drawString(x_center, y_center, title_text)

            # User Details.    
            c.setFont("Helvetica", 12)
            c.drawString(100, 620, f"User Email: {user_email}")
            c.drawString(100, 600, f"User Name: {user_uid}")
           # c.drawString(100, 550, f"Average Percentage Error: {avg_percentage_error:.2f}%")

            img = ImageReader(plot_bytes)
            c.drawImage(img, 100, 180, width=400, height=300)



            # Footer
            c.setFont("Helvetica", 10)
            now = datetime.now()
            dt_string = now.strftime("%Y")
            footer_text = f"© {dt_string} Kelvin Njuguna | All rights reserved."
            footer_width = c.stringWidth(footer_text, "Helvetica", 10)
            c.drawString((page_width - footer_width) / 2, 30, footer_text) #centered footer.

            c.save()
            pdf_buffer.seek(0)

            # Buttons
            col_submitted, col_report = st.columns([0.5, 1.5])

            with col_submitted:
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_buffer,
                    file_name="prediction_report.pdf",
                    mime="application/pdf"
                )

            with col_report:
                csv = predictions.to_csv(index=False)
                st.download_button(
                    label="Download Report as CSV",
                    data=csv,
                    file_name="prediction_report.csv",
                    mime="text/csv"
                )

        else:
            st.warning("No prediction data found for the logged-in user.")

    except Exception as e:
        st.error(f"An error occurred while fetching the data: {str(e)}")