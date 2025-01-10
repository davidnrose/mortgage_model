import streamlit as st
import mortgage as mt

st.title("Mortgage Calculator")

# calculate monthly repayment
# st.subheader("I want to calculate monthly repayments")

with st.expander("I want to calculate monthly repayments", expanded=False):

    col1, col2 = st.columns([0.65, 0.35], gap="medium")

    # choose variables for calculation
    with col1 :
        value = st.slider("Property value", value=300000, step=10000, min_value=80000, max_value=1000000)
        rate = st.slider("Interest Rate - %", min_value=0.1, max_value=10.0, step=0.01, value=4.0)
        rate /= 100

        col3, col4 = st.columns(2)
        with col3:
            deposit = st.number_input("Deposit %", value=10, min_value=5, max_value=50, step=5)
            deposit /= 100
        with col4:
            term = st.number_input("Term length in Years", value=25, min_value=5, max_value=50, step=5)

    # show calculated metrics
    # monthly repayment
    with col2:
        mortgage = mt.Mortgage(value, value*deposit, rate, term)
        repayment = mortgage.repayment
        st.metric("Monthly Repayment", f"£{repayment:,}", border=True)

    # caluclate total interest to pay
    with col2:
        interest_paid = mortgage.calc_interest_paid(term * 12)
        st.metric("Total interest", f"£{interest_paid:,}", border=True)

# calcualte max value
st.expander("I want to get the maximum property value I can afford")