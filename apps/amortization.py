from utils.utils import rate_conversion
import streamlit as st
import pandas as pd
import numpy as np

import utils

latex_eqs = {
    'PRICE': r"""
    PMT = PV \times \frac{(1+r)^N \times r}{(1+r)^N - 1} = \text{constante}
    \\\text{ }\\
    J_n = SD_{n-1} \times r = PMT - A_n
    \\\text{ }\\
    A_n = A_1 \times (1+r)^{n-1} = PMT - J_n
    \\\text{ }\\
    SD_n = SD_{n-1} - A_n
    """,

    'SAC':   r"""
    A = \tfrac{PV}{N} = \text{constante}
    \\\text{ }\\
    J_n = SD_{n-1} \times r = PMT_n - A
    \\\text{ }\\
    PMT_n = A + J_n
    \\\text{ }\\
    SD_n = SD_{n-1} - A
    """,

    'SAM':   r"""
    PMT_{SAM} = \frac{PMT_{PRICE} + PMT_{SAC}}{2}
    """,

    'AMERICANO':   r"""
    A_n=\begin{cases}
    0, & \text{quando } n < 0 \\
    PV, & \text{quando } n = N
    \end{cases}
    \\\text{ }\\
    J = PV \times r
    \\\text{ }\\
    PMT_n = A_n + J
    \\\text{ }\\
    SD_n=\begin{cases}
    PV, & \text{quando } n < 0 \\
    0, & \text{quando } n = N
    \end{cases}
    """
}

titles = {
    'PRICE': "Tabela PRICE",
    'SAC': "Sistema de Amortização Constante",
    'SAM': "Sistema de Amortização Misto",
    'AMERICANO': "Sistema Americano"
}


def amortization_df(N):
    df = pd.DataFrame(
        index=np.arange(N+1),
        columns=[
            'Saldo Devedor',
            'Amortização',
            'Juros',
            'Prestação'
        ]
    )
    return df


def price_table(principal, rate, periods):
    df = amortization_df(periods)
    df.loc[0,'Saldo Devedor'] = principal
    df.loc[0,['Amortização','Juros','Prestação']] = 0.0

    df.loc[1:,'Prestação'] = principal * rate * (1+rate)**periods / \
                             ((1+rate)**periods - 1) if rate > 0 else principal/periods

    for i in range(1, periods+1):
        df.loc[i,'Juros'] = df.loc[i-1,'Saldo Devedor']*rate
        df.loc[i,'Amortização'] = df.loc[i,'Prestação'] - df.loc[i,'Juros']
        df.loc[i,'Saldo Devedor'] = df.loc[i-1,'Saldo Devedor'] - df.loc[i,'Amortização']

    return df


def sac_table(principal, rate, periods):
    df = amortization_df(periods)
    df.loc[0,'Saldo Devedor'] = principal
    df.loc[0,['Amortização','Juros','Prestação']] = 0.0

    df.loc[1:,'Amortização'] = principal/periods

    for i in range(1, periods+1):
        df.loc[i,'Juros'] = df.loc[i-1,'Saldo Devedor']*rate
        df.loc[i,'Prestação'] = df.loc[i,'Amortização'] + df.loc[i,'Juros']
        df.loc[i,'Saldo Devedor'] = df.loc[i-1,'Saldo Devedor'] - df.loc[i,'Amortização']

    return df


def sam_table(principal, rate, periods):
    df_price = price_table(principal, rate, periods)
    df_sac = sac_table(principal, rate, periods)
    return (df_price+df_sac)/2


def americano_table(principal, rate, periods):

    df = amortization_df(periods)
    df.loc[:periods-1,'Saldo Devedor'] = principal
    df.loc[periods,'Saldo Devedor'] = 0.0
    df.loc[0,'Juros'] = 0.0
    df.loc[1:,'Juros'] = principal*rate
    df.loc[:periods-1,'Amortização'] = 0.0
    df.loc[periods,'Amortização'] = principal
    df.loc[:,'Prestação'] = df.loc[:,'Amortização'] + df.loc[:,'Juros']

    return df


@st.cache
def amortization_table(amort_system):
    if amort_system == "PRICE":
        return price_table
    elif amort_system == "SAC":
        return sac_table
    elif amort_system == "SAM":
        return sam_table
    elif amort_system == "AMERICANO":
        return americano_table
    else:
        return None


def app():

    amort = st.sidebar.selectbox("Sistema de Amortização",
        options=[
            "PRICE",
            "SAC",
            "SAM",
            "AMERICANO"
        ]
    )

    st.title("Amortização")
    st.header(titles[amort])

    P = st.sidebar.number_input('Valor do Principal ($)', value=1000.0, min_value=0.01, step=1.0, format="%.2f")

    rate_col1, rate_col2 = st.sidebar.beta_columns([15,10])
    r = rate_col1.number_input('Taxa de Juros (%)', value=1.0, min_value=0., step=0.5, format="%f")/100
    r_type = rate_col2.radio("ao",
        options=utils.period_keys,
        format_func=utils.format_period("singular"),
        key="rate_radio")

    period_col1, period_col2 = st.sidebar.beta_columns([15,10])
    N = period_col1.number_input('Número de Períodos', value=12, min_value=1)
    N_type = period_col2.radio("",
        options=utils.period_keys,
        format_func=utils.format_period("plural"),
        key="period_radio"
    )

    r = rate_conversion(r, r_type, N_type)

    df = amortization_table(amort)(P,r,N)

    st.write(f"Taxa de juros ao {utils.format_period('singular')(N_type)} = {round(r*100,3)} %")

    st.table(df.style.format("{:.2f}"))

    st.latex(latex_eqs[amort])
