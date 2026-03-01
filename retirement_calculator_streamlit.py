import streamlit as st

def retirement_calculator(current_age=46, retirement_age=65, annual_contribution=0, annual_return=1.5):
    # Code for calculating retirement amounts
    years_to_invest = retirement_age - current_age
    future_value = annual_contribution * (((1 + annual_return / 100) ** years_to_invest - 1) / (annual_return / 100))
    return future_value

st.title('Retirement Calculator')
st.write('Calculate how much you will have at retirement')

current_age = st.number_input('Current Age', value=46)
retirement_age = st.number_input('Retirement Age', value=65)
annual_contribution = st.number_input('Annual Contribution', value=0)
annual_return = st.number_input('Expected Annual Return (%)', value=1.5)

if st.button('Calculate'): 
    result = retirement_calculator(current_age, retirement_age, annual_contribution, annual_return)
    st.write(f'Future Value at retirement: ${result:,.2f}')
