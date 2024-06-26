import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

# Autenticação no Google Drive
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
gc = gspread.authorize(credentials)

# Carregar os dados da planilha
spreadsheet = gc.open("Acompanhamento Projeto Oakadoo")
worksheet = spreadsheet.get_worksheet(0)
data = worksheet.get_all_values()

if not data:
    st.error("No data found in the spreadsheet.")
else:
    # Converter os dados em um DataFrame do pandas
    df = pd.DataFrame(data[1:], columns=data[0])

    # Mostrar os dados no Streamlit (opcional, para verificação)
    st.write("Dados carregados da planilha:", df)

    # Certificar que a coluna 'Progresso' é convertida para float
    df['Progresso'] = df['Progresso'].astype(float)

    # Exibir barras de progresso para cada linha
    for index, row in df.iterrows():
        st.write(f"{row['Etapa']} - {row['Progresso'] * 100}%")
        st.progress(row['Progresso'])
