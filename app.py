
import streamlit as st
import mortgage as mt
from math import floor

# title and image
st.title("Mortgage Calculator")
st.image("scott-webb-1ddol8rgUH8-unsplash.jpg")

# introduction
st.write("I designed this calculator to help you work out some important mortgage questions: ")
st.write("1. Based on the cost of a house, how much will your monthly repayments be?")
st.write("2. Based on how much you can afford to pay each month, what is the maximum house value?")
st.write("3. Given a certain savings rate, how long will it take you to save for a deposit?")
st.divider()
st.write("Remember: the results you get from this calculator don't indicate that mortgage providers will lend to you in those circumstances. The purpose of the calculator is to better understand how different factors (deposit, interest rate) change the total total and the amount of interest you pay. If you're looking to apply for a mortgage, you should check what's available in the market, rather than what is mathematically possible.")
st.divider()

# calculate monthly repayment
# st.subheader("I want to calculate monthly repayments")

with st.expander("How much will my monthly repayments be?", expanded=False):

    col1, col2 = st.columns([0.65, 0.35], gap="medium")

    # choose variables for calculation
    with col1 :
        value = st.slider("Property value", value=300000, step=10000, min_value=80000, max_value=1000000)
        rate = st.slider("Interest Rate - %", min_value=0.1, max_value=10.0, step=0.01, value=4.0)
        rate /= 100

        col3, col4 = st.columns(2)
        with col3:
            deposit = st.number_input("Deposit %", value=10, min_value=0, max_value=50, step=5)
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
        interest_paid = round(mortgage.calc_interest_paid(term * 12))
        st.metric("Total interest", f"£{interest_paid:,}", border=True)

# calcualte max value
with st.expander("What value of property can I afford?", expanded=False):

    col1, col2 = st.columns([0.65, 0.35], gap="medium")

    # choose variables for calculation
    with col1:
        repay = st.slider("Monthly Repayment", value=1600, step=50, min_value=300, max_value=6000, key="maxval_repay")
        rate= st.slider("Interest Rate - %", min_value=0.1, max_value=10.0, step=0.01, value=4.0, key="maxval_rate")
        rate /= 100

        col3, col4 = st.columns(2)
        with col3:
            deposit = st.number_input("Deposit %", value=10, min_value=5, max_value=50, step=5, key="maxval_deposit")
            deposit /= 100
        with col4:
            term = st.number_input("Term length in Years", value=25, min_value=5, max_value=50, step=5, key="maxval_term")

    with col2:
        max_value = round(mt.calc_prop_value(repay, deposit, rate, term))
        st.metric("Properties up to a value of", f"£{max_value:,}", border=True)

        # caluclate total interest to pay
        mortgage2 = mt.Mortgage(max_value, max_value * deposit, rate, term)
        interest_paid = round(mortgage2.calc_interest_paid(term * 12))
        st.metric("Total interest", f"£{interest_paid:,}", border=True)

# calculate time to save
with st.expander("How long will I have to save?"):

    col1, col2 = st.columns(2)

    with col1:
        val_target = st.slider("Target property value", value=300000, step=10000, min_value=80000, max_value=1000000, key="tarval_value")
        target_dep = st.number_input("Deposit %", value=10, min_value=5, max_value=50, step=5, key="tarval_deposit")
        # convert to multiplier
        target_dep /= 100

        growth = st.slider("House price growth", value=2.5, min_value=0.1, max_value=15.0, step=0.01, key="tarval_price_growth")
        # convert to multiplier
        growth /= 100

    with col2:
        already_saved = st.number_input("Amount already saved", min_value=0, max_value=100000, step=100, value=500, key="tarval_saving_amount_prior")
        saving_per_month = st.slider("Saving amount per month", value=200, min_value=20, max_value=1000, step=10, key="tarval_saving_amount")
        saving_annual_rate = st.slider("Annual savings interest rate", value=3.5, min_value=0.1, max_value=8.0, step=0.1, key="tarval_saving_rate")
        # convert to multiplier
        saving_annual_rate /= 100

    # present target deposit value
    target_deposit_value = round(target_dep * val_target)

    # initialise mortgage: value, target deposit, (rate - ignore), (term - ignore)
    mortgage3 = mt.Mortgage(val_target, val_target * target_dep, 0.045, 25)

    # initialise savings: monthly saving amount, savings rate
    months, exceeded = mt.saving(mortgage3, saving_per_month, saving_annual_rate, house_price_growth=growth, deposit_perc=target_dep, saved=already_saved, deposit=target_deposit_value)

    years = floor(months/12)
    months_remainder = months % 12

    # format the text to return
    if years == 1:
        years_text = "year"
    else:
        years_text = "years"
    if months_remainder ==1:
        months_text = "month"
    else: months_text = "months"

    if exceeded:
        over_text = "Over "
    else:
        over_text = ""

    # compile the text
    metric_saving_result_text = f"{over_text} {years} {years_text} and {months_remainder} {months_text}"
    # display target deposit and time to save
    col3, col4 = st.columns([.3,.7])

    with col3:
        st.metric("Target deposit value", f"£{target_deposit_value:,}",border=True)
    with col4:
        st.metric("Time to save for goal deposit", metric_saving_result_text, border=True)