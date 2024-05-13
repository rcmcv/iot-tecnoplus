# 1. Importação das bibliotecas
import pandas as pd
import datetime as dt
import streamlit as st
import numpy as np
import plotly_express as px

# Configuração incial do sistema
st.set_page_config(page_title="IoT Tecnoplus", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")
st.title("IoT Tecnoplus")
st.subheader("Atacadão Aeroporto")

@st.cache_data
def load_data():
    data = pd.read_csv('tecnoplus-datalog.csv')
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data['ENTRADA'] = pd.to_datetime(data['ENTRADA'], format='%d/%m/%Y %H:%M:%S')
    data = data.dropna()
    return data

#data_load_state = st.text('Loading data...')
df = load_data()
#data_load_state.text("Done! (using st.cache_data)")

# Carrega o arquivo de dados csv
#df = pd.read_csv('tecnoplus-datalog.csv')
# Elimina as linha com dados nulos
#df = df.dropna()
# Converter o tipo de dado da coluna para datetime
#df['ENTRADA'] = pd.to_datetime(df['ENTRADA'], format='%d/%m/%Y %H:%M:%S')

#end_date = dt.datetime.today()
#start_date = dt.datetime(end_date.year-1,end_date.month,end_date.day)
# Defini a data inidial e data final de acordo com o data frame
start_date = df['ENTRADA'].min()
end_date = df['ENTRADA'].max()

# Menu lateral do sistema
with st.sidebar.container():
    st.header('Insira as informações abaixo')
    ativo = st.selectbox('Selecione o sensor desejado:', options=['PH', 'ORP', 'COND', 'STATUSREC', 'STATUSDRE','STATUSDOS', 'ALARMREC', 'ALARMDRE'])
    data_inicial = st.date_input('Data Inicial:', start_date)
    data_final = st.date_input('Data Final:', end_date)

# Filtrar o DataFrame com base no intervalo selecionado (apenas datas)
df = df[(df['ENTRADA'].dt.date >= data_inicial) & (df['ENTRADA'].dt.date <= data_final)]

# 2. Criar as métricas do sistema
ult_atualizacao = df['ENTRADA'].max()
pri_medicao = df.loc[df.index.min(), ativo]/100
ult_medicao = df.loc[df.index.max(), ativo]/100
menor_medicao = df[ativo].min()/100
maior_medicao = df[ativo].max()/100
delta_medicao = round(((ult_medicao-pri_medicao)/pri_medicao)*100, 2)

# 3. Apresentar o resultado na tela do sistema
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"Última atualização - {ult_atualizacao}", "{:,.2f}".format(ult_medicao), f"{delta_medicao}%")
    with col2:
        st.metric("Menor Medição", "{:,.2f}".format(menor_medicao))
    with col3:
        st.metric("Maior Medição", "{:,.2f}".format(maior_medicao))

with st.container():
    #st.checkbox("Use container width", value=False, key="use_container_width")
    # Mostrar o DataFrame filtrado na tela
    #st.dataframe(df, use_container_width=st.session_state.use_container_width)
    if st.checkbox('Mostar tabela de dados'):
        st.subheader('Tabela de Dados')
        st.dataframe(df, use_container_width=True)

with st.container():
    st.subheader('Gráfico de Acompanhamento - ' + ativo)
    st.line_chart(df.set_index('ENTRADA')[[ativo]])
    #st.line_chart(filtered_df[['PH', 'ORP', 'COND']])

# Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = df[df['ENTRADA'].dt.hour == hour_to_filter]
# st.write(filtered_data)
