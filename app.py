import streamlit as st
import mortgage as mt

st.title("Mortgage Calculator")

# calculate monthly repayment
st.write("I want to calculate monthly repayments")

value = st.number_input("Property value", value=300000, step=10000)
rate = st.slider("Interest Rate - %", min_value=0.1, max_value=10.0, step=0.1)
rate /= 100
deposit = st.number_input("Deposit Percentage", value=10, min_value=5, max_value=50, step=5)
deposit /= 100
term = st.number_input("Length of Term - Years", value=25, min_value=5, max_value=50, step=5)

mortgage = mt.Mortgage(value, value*deposit, rate, term)
repayment = mortgage.repayment

st.write(f"{repayment}")