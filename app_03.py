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

    # Certificar que a coluna 'Progresso' é convertida para float
    df['Progresso'] = df['Progresso'].astype(float)

    # Função para renderizar a barra de progresso como HTML
    def render_progress_bar(value):
        bar = f'<div style="width: 100%; background-color: #ddd; height: 20px; position: relative;"><div style="width: {value * 100}%; background-color: #4CAF50; height: 100%;"></div><div style="position: absolute; width: 100%; text-align: center; top: 0; color: white;">{value * 100:.1f}%</div></div>'
        return bar

    # Aplicar a função para a coluna 'Progresso' e criar uma nova coluna HTML
    df['Progresso'] = df['Progresso'].apply(render_progress_bar)

    # Estilos CSS para ajustar a largura das colunas
    styles = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #f2f2f2;
        color: black;
        white-space: nowrap;
    }
    td {
        white-space: nowrap;
    }
    .wide {
        width: 300px;
    }
    .medium {
        width: 150px;
    }
    .narrow {
        width: 100px;
    }
    </style>
    """

    # Aplicar classes CSS às colunas
    col_classes = ['medium', 'wide', 'medium', 'medium', 'medium', 'narrow', 'narrow', 'narrow']

    # Criar tabela HTML com classes CSS
    df_html = df.to_html(escape=False, index=False)
    for i, col_class in enumerate(col_classes):
        df_html = df_html.replace(f'<th>{df.columns[i]}</th>', f'<th class="{col_class}">{df.columns[i]}</th>')

    # Renderizar estilos CSS e a tabela com barras de progresso
    st.markdown(styles + df_html, unsafe_allow_html=True)
