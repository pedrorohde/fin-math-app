import streamlit as st
from apps import *

st.set_page_config(page_title='Calculadora Financeira')

st.sidebar.markdown("# Calculadora de Matemática Financeira")

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

# st.sidebar.markdown('*<div style="text-align: center">feito por <a href="https://github.com/pedrorohde">pedrorohde</a>. </div>*', unsafe_allow_html=True)