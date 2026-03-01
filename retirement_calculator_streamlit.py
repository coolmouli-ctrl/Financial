# Retirement Calculator Streamlit App

import streamlit as st

# Default values
current_age = 46
annual_contribution = 0
annual_return = 1.5

# Streamlit app configuration
st.title("Retirement Calculator")

# Input fields
current_age = st.number_input("Current Age", value=current_age)
annual_contribution = st.number_input("Annual Contribution", value=annual_contribution)
annual_return = st.number_input("Annual Return (%)", value=annual_return)
