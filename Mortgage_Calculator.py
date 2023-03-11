import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from financing import MortgageCalculator
import numpy as np

st.set_page_config(
    page_title="Mortgage Calculator",
)

total_amount = st.slider("Total mortgage amount", 100_000, 500_000, step=10_000)
number_of_years = st.slider("Number of years", 10, 30, value=10, step=1)
interest_rate = st.slider("Interest rate", 2.5, 5.5)
fees = st.slider("Fees", 0, 100, value=35, step=3)
fees_every = st.slider("Months interval for fees payment", 1, 12, value=3, step=1)
mortgage = MortgageCalculator(
    total_amount, number_of_years, interest_rate, fees=fees, fees_every=fees_every
)
summary = "Monthly rate: {rate:2.2f}. Total money lost on interests: {loss:2.0f}"
summary = summary.format(rate=mortgage.monthly_rate, loss=mortgage.total_interest_lost)
st.write(summary)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=np.arange(mortgage.number_of_months),
        y=mortgage.interest_payed,
        fill="tozeroy",
        name="money lost in interest",
    )
)
fig.add_trace(
    go.Scatter(
        x=np.arange(mortgage.number_of_months),
        y=mortgage.money_payed,
        fill="tonexty",
        name="total amount payed",
    )
)
st.plotly_chart(fig)


fig = make_subplots(cols=1, rows=2, shared_xaxes=True)
x = np.arange(mortgage.number_of_months)
fig.add_trace(
    go.Scatter(
        x=x,
        y=mortgage.monthly_debt,
        name="remaining debt",
    ),
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=mortgage.monthly_interests / mortgage.monthly_rate,
        name="fraction of monthly rate in interest",
    ),
    row=2,
    col=1,
)
st.plotly_chart(fig)
