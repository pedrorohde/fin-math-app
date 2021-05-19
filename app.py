import streamlit as st
from apps import *

opt = st.sidebar.selectbox("Opções",
    options=[
        "Amortização",
        "Renda Fixa",
        "Renda Variável"
    ]
)


if opt == "Amortização":
    amortization()
else:
    pass