# Importando Bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image

# Configuração do Streamlit
st.set_page_config(
    page_title='Telemarketing Analysis',
    page_icon='telmarketing_icon.png',
    layout="wide",
    initial_sidebar_state='expanded'
)

# Título da Página
st.write('# Telemarketing Analysis')
st.markdown("---")

# Adicionando imagem na Sidebar
image = Image.open("Bank-Branding.jpg")
st.sidebar.image(image)

# Carregando os dados
df = pd.read_csv('./data/input/bank-additional-full.csv', sep=';')

# Criando um DataFrame auxiliar para filtragem
df_filtrado = df.copy()

st.write('## Antes dos Filtros')
st.write(df.head())

# Sidebar - Filtros
with st.sidebar.form(key="formulario_filtros"):
    st.write("### Selecione os filtros desejados")

    # Filtro de Idade
    idade_min, idade_max = int(df["age"].min()), int(df["age"].max())
    idades = st.slider("Faixa etária", idade_min, idade_max, (idade_min, idade_max))

    # Criando filtros categóricos (visíveis por padrão)
    filtros_selecionados = {}
    colunas_categoricas = ['job', 'marital', 'education', 'default', 'housing', 'loan']
    
    for coluna in colunas_categoricas:
        opcoes = sorted(df[coluna].dropna().unique().tolist())  
        opcoes.insert(0, "Todos")  # Adiciona a opção "Todos" no início

        # Selecione "Todos" por padrão
        valores_selecionados = st.multiselect(f"Filtrar {coluna}", opcoes, default=["Todos"])

        # Lógica para manter tudo selecionado ao escolher "Todos"
        if "Todos" in valores_selecionados:
            filtros_selecionados[coluna] = df[coluna].unique().tolist()  # Todas as categorias
        else:
            filtros_selecionados[coluna] = valores_selecionados  # Apenas as selecionadas

    # Botão para aplicar os filtros
    submit_button = st.form_submit_button(label="Aplicar")

# Aplicação dos filtros após clique no botão
if submit_button:
    # Filtrar idade
    df_filtrado = df_filtrado[(df_filtrado['age'] >= idades[0]) & (df_filtrado['age'] <= idades[1])]

    # Aplicar filtros categóricos
    for coluna, valores in filtros_selecionados.items():
        df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

    # Exibir DataFrame filtrado
    st.write(f"### Dados Filtrados ({len(df_filtrado)} registros)")
    st.dataframe(df_filtrado)

st.markdown("---")

# Gráficos de Barras Comparativos
st.write("## Proporção de Aceite")

# Calculando percentuais
df_target_perc = df['y'].value_counts(normalize=True).mul(100).to_frame()
df_target_perc.columns = ["percentual"]

df_filtrado_target_perc = df_filtrado['y'].value_counts(normalize=True).mul(100).to_frame()
df_filtrado_target_perc.columns = ["percentual"]

# Criando subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=["Dados Brutos", "Dados Filtrados"])

# Gráfico 1: Dados Brutos
fig.add_trace(go.Bar(
    x=df_target_perc.index, 
    y=df_target_perc["percentual"], 
    text=df_target_perc["percentual"].round(2),  
    textposition="auto", name="Dados Brutos"), 
    row=1, col=1
)

# Gráfico 2: Dados Filtrados
fig.add_trace(go.Bar(
    x=df_filtrado_target_perc.index, 
    y=df_filtrado_target_perc["percentual"], 
    text=df_filtrado_target_perc["percentual"].round(2),
    textposition="auto", name="Dados Filtrados"), 
    row=1, col=2
)

# Ajuste do layout
fig.update_layout(
    title_text="Proporção dos Dados Filtrados",
    showlegend=False,
    height=500, width=900
)

# Exibir gráfico no Streamlit
st.plotly_chart(fig)
