import streamlit as st
from PIL import Image
import pickle
import numpy as np
import tornado.web
import tornado.websocket
import threading
import asyncio
# Define a function to handle WebSocket messages
def handle_message(message):
    st.write("Received message:", message)

def main():
    st.title("Streamlit App with WebSocket")

    # Display a message to let the user know to open the WebSocket connection
    st.write("Open WebSocket connection in your browser.")

    # Get WebSocket data
    ws = st.websocket("ws://localhost:8888/websocket", on_message=handle_message)









# Load the model
model = pickle.load(open('./Model/ML_Model.pkl', 'rb'))

def run():
    img1 = Image.open('bank.png')
    img1 = img1.resize((156, 145))
    st.image(img1, use_column_width=False)
    st.title("Bank Loan Prediction using Machine Learning")

    # Account No
    account_no = st.text_input('Account number')

    # Full Name
    fn = st.text_input('Full Name')

    # Gender
    gen_display = ('Female', 'Male')
    gen_options = list(range(len(gen_display)))
    gen = st.selectbox("Gender", gen_options, format_func=lambda x: gen_display[x])

    # Marital Status
    mar_display = ('No', 'Yes')
    mar_options = list(range(len(mar_display)))
    mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])

    # Number of Dependents
    dep_display = ('No', 'One', 'Two', 'More than Two')
    dep_options = list(range(len(dep_display)))
    dep = st.selectbox("Dependents", dep_options, format_func=lambda x: dep_display[x])

    # Education
    edu_display = ('Not Graduate', 'Graduate')
    edu_options = list(range(len(edu_display)))
    edu = st.selectbox("Education", edu_options, format_func=lambda x: edu_display[x])

    # Employment Status
    emp_display = ('Job', 'Business')
    emp_options = list(range(len(emp_display)))
    emp = st.selectbox("Employment Status", emp_options, format_func=lambda x: emp_display[x])

    # Property Area
    prop_display = ('Rural', 'Semi-Urban', 'Urban')
    prop_options = list(range(len(prop_display)))
    prop = st.selectbox("Property Area", prop_options, format_func=lambda x: prop_display[x])

    # Credit Score
    cred_display = ('Between 300 to 500', 'Above 500')
    cred_options = list(range(len(cred_display)))
    cred = st.selectbox("Credit Score", cred_options, format_func=lambda x: cred_display[x])

    # Applicant Monthly Income
    mon_income = st.number_input("Applicant's Monthly Income($)", value=0, min_value=0, step=1)

    # Co-Applicant Monthly Income
    co_mon_income = st.number_input("Co-Applicant's Monthly Income($)", value=0, min_value=0, step=1)

    # Loan Amount
    loan_amt = st.number_input("Loan Amount", value=0, min_value=0, step=1)

    # Loan Duration
    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
    dur_options = list(range(len(dur_display)))
    dur = st.selectbox("Loan Duration", dur_options, format_func=lambda x: dur_display[x])

    # Convert duration to days
    duration_dict = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
    duration = duration_dict.get(dur, 0)

    if st.button("Submit"):
        try:
            # Ensure all inputs are correctly cast to integers
            gen = int(gen)
            mar = int(mar)
            dep = int(dep)
            edu = int(edu)
            emp = int(emp)
            mon_income = int(mon_income)
            co_mon_income = int(co_mon_income)
            loan_amt = int(loan_amt)
            cred = int(cred)
            prop = int(prop)
            duration = int(duration)
            
            features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
            st.write(f"Features: {features}")  # Debug statement
            prediction = model.predict(features)
            ans = int(prediction[0])
            if ans == 0:
                st.error(
                    f"Hello: {fn} || "
                    f"Account number: {account_no} || "
                    'According to our calculations, you will not get the loan from the bank.'
                )
            else:
                st.success(
                    f"Hello: {fn} || "
                    f"Account number: {account_no} || "
                    'Congratulations!! You will get the loan from the bank.'
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")

run()
