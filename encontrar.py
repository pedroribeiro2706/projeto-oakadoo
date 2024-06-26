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

# Listar todas as planilhas disponíveis para a conta de serviço
try:
    spreadsheets = gc.openall()
    for sheet in spreadsheets:
        st.write(f"Encontrado: {sheet.title}")
except Exception as e:
    st.error(f"Erro ao listar planilhas: {e}")

# Tentar abrir a planilha específica
try:
    spreadsheet = gc.open("Acompanhamento Projeto Oakadoo")
    worksheet = spreadsheet.get_worksheet(0)
    data = worksheet.get_all_values()
except gspread.SpreadsheetNotFound:
    st.error("Planilha não encontrada. Verifique o nome e as permissões.")


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

    # Exibir barras de progresso para cada linha
    for index, row in df.iterrows():
        st.write(f"{row['Etapa']} - {row['Progresso'] * 100}%")
        st.progress(row['Progresso'])