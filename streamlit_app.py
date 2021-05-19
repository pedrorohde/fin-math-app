import streamlit as st
from apps import *

st.sidebar.markdown("# Calculadora de Matemática Financeira")
st.sidebar.markdown('*<div style="text-align: right">feito por <a href="https://github.com/pedrorohde">pedrorohde</a>. </div>*', unsafe_allow_html=True)

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
