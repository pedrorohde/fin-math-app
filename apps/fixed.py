import streamlit as st
import pandas as pd
import numpy as np
import utils


def fixed_df(N):
    df = pd.DataFrame(
        index=np.arange(N+1),
        columns=[
            'Aporte',
            'Rendimento',
            'Valor Total',
        ]
    )
    return df


def periodic_inflow_table(initial_value, inflow, rate, periods):

    df = fixed_df(periods)
    
    df.loc[0,'Valor Total'] = initial_value
    df.loc[0,['Aporte','Rendimento']] = 0.0

    for i in range(1, periods+1):
        df.loc[i,'Aporte'] = inflow
        df.loc[i,'Rendimento'] = (df.loc[i-1,'Valor Total'] + inflow)*rate
        df.loc[i,'Valor Total'] = df.loc[i-1,'Valor Total'] + df.loc[i,'Rendimento'] + df.loc[i,'Aporte']
    
    return df


def app():
    
    st.sidebar.markdown("_(mais opções de renda fixa em breve)_")

    P = st.sidebar.number_input("Valor Incial", min_value=0.0, value=1000.0, step=500.0)

    period_col1, period_col2 = st.sidebar.beta_columns([15,10])
    N = period_col1.number_input('Número de Períodos', value=12, min_value=1)
    N_type = period_col2.radio("",
        options=utils.period_keys,
        index=2,
        format_func=utils.format_period("plural"),
        key="period_radio"
    )

    F = st.sidebar.number_input(f"Aporte por {utils.format_period('singular')(N_type)}", min_value=0.0, value=100.0, step=100.0)

    rate_col1, rate_col2 = st.sidebar.beta_columns([15,10])
    r = rate_col1.number_input('Taxa de Juros (%)', value=1.0, min_value=0., step=0.5, format="%f")/100
    r_type = rate_col2.radio("ao",
        options=utils.period_keys,
        index=2,
        format_func=utils.format_period("singular"),
        key="rate_radio")

    r = utils.rate_conversion(r, r_type, N_type)
    df = periodic_inflow_table(P,F,r,N)


    st.title("Renda Fixa")
    st.header("Rendimento - Aporte Periódico")
    st.write(f"Aporte no começo de cada {utils.format_period('singular')(N_type)}, valor total ao final de cada {utils.format_period('singular')(N_type)}")

    st.write(f"Taxa de juros = {round(r*100,3)}% ao {utils.format_period('singular')(N_type)}")
    st.write(f"Valor após {N} {utils.format_period('plural' if N > 1 else 'singular')(N_type)} = ${round(df.loc[N,'Valor Total'],2)}")
    st.table(df.style.format("{:.2f}"))