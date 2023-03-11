import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import streamlit as st
from financing import MortgageCalculator
import numpy as np
from itertools import product
import pandas as pd
import plotly.express as px


total_amount = st.slider("Total mortgage amount", 100_000, 500_000, step=10_000)
fees = st.slider("Fees", 0, 100, value=35, step=3)
fees_every = st.slider("Months interval for fees payment", 1, 12, value=3, step=1)

years = st.slider("Select number of years", 10, 30, step=1)
interest_rates = np.arange(2.0, 5.5, 0.5)
number_of_years = np.arange(10, 35, 1)
data = list()
for interest_rate, years in product(interest_rates, number_of_years):
    mortgage = MortgageCalculator(total_amount, years, interest_rate, fees_every, fees)
    data.append(
        {
            "interest_rate": interest_rate,
            "number_of_years": years,
            "monthly_rate": mortgage.monthly_rate,
            "total interests": mortgage.total_interest_lost,
        }
    )
df = pd.DataFrame(data)
df["interest_rate"] = df["interest_rate"].astype(str)

st.plotly_chart(
    px.scatter(
        df,
        color="interest_rate",
        y="total interests",
        size="monthly_rate",
        x="number_of_years",
    )
)

st.plotly_chart(
    px.scatter(
        df,
        color="interest_rate",
        size="total interests",
        y="monthly_rate",
        x="number_of_years",
    )
)
