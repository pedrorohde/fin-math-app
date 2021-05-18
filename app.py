import streamlit as st
import pandas as pd
import numpy as np

st.title("Tabela PRICE")

P = st.number_input('Valor do Principal', value=1000.0)
r = st.number_input('Taxa de Juros', value=0.01)
N = st.number_input('Número de Períodos', value=12)

df = pd.DataFrame(
    index=np.arange(N+1),
    columns=[
        'Saldo Devedor',
        'Amortização',
        'Juros',
        'Prestação'
    ]
)

df = df.rename_axis("Período")

df.loc[0,'Saldo Devedor'] = P
df.loc[0,['Amortização','Juros','Prestação']] = 0.0

df.loc[1:,'Prestação'] = P * r * (1+r)**N / ((1+r)**N - 1)

for i in range(1, N+1):
    df.loc[i,'Juros'] = df.loc[i-1,'Saldo Devedor']*r
    df.loc[i,'Amortização'] = df.loc[i,'Prestação'] - df.loc[i,'Juros']
    df.loc[i,'Saldo Devedor'] = df.loc[i-1,'Saldo Devedor'] - df.loc[i,'Amortização']

# df.append(
#     pd.DataFrame(
#         df.sum(),
#     )
# )

st.dataframe(df.style.format("{:.2f}"))