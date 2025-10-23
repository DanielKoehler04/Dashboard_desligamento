import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração inicial ---
st.set_page_config(page_title="Análises de Desligamentos", layout="wide")
st.title("Análises de Desligamentos")

# --- Upload do arquivo Excel ---
arquivo = st.sidebar.file_uploader("Carregar planilha de desligamentos", type=["xlsx"])

if arquivo is not None:
    # Lê a planilha enviada
    df = pd.read_excel(arquivo)

    # Extrai e trata a data corretamente
    if "Data da Demissão - Tipo de Demissão" in df.columns:
        df["Data"] = df["Data da Demissão - Tipo de Demissão"].str.split(" - ").str[0]
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce",  dayfirst=True)
        df["Mes_Ano"] = df["Data"].dt.strftime("%m/%Y")
    else:
        st.error("A coluna 'Data da Demissão - Tipo de Demissão' não foi encontrada na planilha.")
        st.stop()

    # --- Filtros laterais ---
    st.sidebar.header("Filtros")

    # Filtro de mês e ano
    meses = sorted(df["Mes_Ano"].dropna().unique().tolist(), key=lambda x: pd.to_datetime("01/" + x, dayfirst=True))
    meses.insert(0, "Todos")
    mes_escolhido = st.sidebar.selectbox("Mês e Ano:", meses)

    # Filtro de tipo de ingresso (case-insensitive)
    df["Tipo de ingresso"] = df["Tipo de ingresso"].astype(str)
    tipos_ingresso = sorted(df["Tipo de ingresso"].str.lower().unique().tolist())
    tipos_ingresso_display = ["Todos"] + [t.title() for t in tipos_ingresso]
    ingresso_escolhido = st.sidebar.selectbox("Tipo de ingresso:", tipos_ingresso_display)

    # --- Aplicando filtros ---
    df_filt = df.copy()

    # Filtro por tipo de ingresso
    if ingresso_escolhido != "Todos":
        df_filt = df_filt[df_filt["Tipo de ingresso"].str.lower() == ingresso_escolhido.lower()]

    # Filtro por mês/ano
    if mes_escolhido != "Todos":
        df_filt = df_filt[df_filt["Mes_Ano"] == mes_escolhido]

    
    if "Data da Demissão - Tipo de Demissão" in df_filt.columns:
    # Extrai tipo de demissão e padroniza (case insensitive)
        df_filt["Tipo de Demissão"] = (
         df_filt["Data da Demissão - Tipo de Demissão"]
            .str.split(" - ")
            .str[-1]
            .str.strip()
            .str.lower()
            .str.capitalize()
        )

        resumo = df_filt["Tipo de Demissão"].value_counts().reset_index()
        resumo.columns = ["Tipo de Demissão", "Quantidade"]

        # Total geral
        total_deslig = resumo["Quantidade"].sum()
        st.markdown(
            f"<h3 style='color:#2E86C1'>Total de desligamentos: {total_deslig}</h3>",
            unsafe_allow_html=True
        )

        # Exibir cards
        cols = st.columns(len(resumo))
        for i, row in resumo.iterrows():
            with cols[i]:
                st.metric(label=row["Tipo de Demissão"], value=int(row["Quantidade"]))
    else:
        st.warning("Coluna 'Data da Demissão - Tipo de Demissão' não encontrada na planilha.")
    # --- Exibição opcional da tabela ---

    mostrar_tabela = st.checkbox("Mostrar tabela completa filtrada")
    if mostrar_tabela:
        st.dataframe(df_filt, use_container_width=True)

    # --- Gráficos ---
    st.divider()


    graficos = [
        "Descricao Experiencia",
        "Clima Organizacional",
        "Discriminação e Assédio",
        "Experiência Comunicação Interna",
        "Oportunidade Para Crescimento",
        "Avaliação Programa de Treinamento",
        "Apoio e Valorizacao Pela Lideranca",
        "Remuneração e Benefícios"
    ]

    # Criação das colunas (4 linhas x 2 colunas)
    cols = [st.columns(2) for _ in range(4)]
    colunas = [c for dupla in cols for c in dupla]

    def gera_grafico(coluna, col):
        if coluna not in df_filt.columns:
            return
        cont = df_filt[coluna].dropna().value_counts().reset_index()
        if cont.empty:
            return
        cont.columns = [coluna, "Quantidade"]
        fig = px.pie(cont, values="Quantidade", names=coluna, title=coluna)
        fig.update_traces(textinfo="percent+value", textfont_size=13)
        col.plotly_chart(fig, use_container_width=True)

    # Gera todos os gráficos
    for i, nome in enumerate(graficos):
        gera_grafico(nome, colunas[i])

else:
    st.info("Envie um arquivo Excel (.xlsx) na barra lateral para iniciar a análise.")
