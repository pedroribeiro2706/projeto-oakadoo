import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

# Autenticação no Google Drive (substitua pelas suas credenciais)
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
gc = gspread.authorize(credentials)

try:
    # Abrir a planilha pelo nome
    spreadsheet = gc.open("Acompanhamento Projeto Oakadoo")
    worksheet = spreadsheet.get_worksheet(0)

    # Obter todos os valores da planilha como uma lista de listas
    data = worksheet.get_all_values()

    # Verificar se há dados na planilha
    if not data:
        st.error("No data found in the spreadsheet.")
    else:
        # Converter os dados em um DataFrame do pandas
        df = pd.DataFrame(data[1:], columns=data[0])

        # Mostrar os dados no Streamlit (opcional, para verificação)
        st.write("Dados carregados da planilha:", df)

        # Verificar se a coluna 'Progresso' existe no DataFrame
        if 'Progresso' in df.columns:
            st.write("Coluna 'Progresso' encontrada. Aqui estão os dados brutos da coluna:", df['Progresso'])
            
            # Remover o símbolo de porcentagem e converter para float
            try:
                df['Progresso'] = df['Progresso'].str.rstrip('%').replace('', '0').astype(float)
                st.write("Dados da coluna 'Progresso' após conversão:", df['Progresso'])

                # Exibir barras de progresso para cada linha
                for index, row in df.iterrows():
                    st.write(f"{row['Progresso']}%")
                    st.progress(row['Progresso'] / 100)

            except ValueError as ve:
                st.error(f"Erro ao converter a coluna 'Progresso': {ve}")
        else:
            st.error("'Progresso' column not found in the spreadsheet.")

except Exception as e:
    st.error(f"Error: {e}")

# Converter colunas para os tipos corretos
df['Progresso'] = df['Progresso'].astype(str).str.replace('%', '', regex=False).astype(float)
df['Valor da Etapa Completa'] = (
    df['Valor da Etapa Completa']
    .astype(str)
    .str.replace(r'[R$\.]', '', regex=True)
    .str.replace(',', '.', regex=False)
)
df['Valor da Etapa Completa'] = pd.to_numeric(df['Valor da Etapa Completa'])
df['Valor pago'] = (
    df['Valor pago']
    .astype(str)
    .str.replace(r'[R$\.]', '', regex=True)
    .str.replace(',', '.', regex=False)
)
df['Valor pago'] = pd.to_numeric(df['Valor pago'])
df['Valor devido'] = (
    df['Valor devido']
    .astype(str)
    .str.replace(r'[R$\.]', '', regex=True)
    .str.replace(',', '.', regex=False)
)
df['Valor devido'] = pd.to_numeric(df['Valor devido'])


# Criar a página web
st.title("Acompanhamento Projeto Oakadoo")

# Exibir a tabela com progress bar
st.subheader("Tabela de Acompanhamento")
st.dataframe(df.style.format(
    {
        'Valor da Etapa Completa': 'R$ {:,.2f}',
        'Valor pago': 'R$ {:,.2f}',
        'Valor devido': 'R$ {:,.2f}',
    }
).bar(subset=['Progresso'], color='#4CAF50', vmin=0, vmax=100))

# Criar e exibir o histograma
st.subheader("Histograma de Progresso das Etapas")
st.bar_chart(df[['Etapa', 'Progresso']].set_index('Etapa'))
