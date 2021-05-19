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
elif opt == "Renda Fixa":
    fixed()
elif opt == "Renda Variável":
    variable()
else:
    pass