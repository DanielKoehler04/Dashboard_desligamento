import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração inicial ---
st.set_page_config(page_title="Análises de Desligamentos", layout="wide")
st.title("Análises de Desligamentos")

# --- Upload do arquivo Excel ---

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vScLqa5xJGjya4saNm2_Vfo5jiOpPyyINfpPgeQXtDXhG4t_FL83BdSGhMyR30kfPS0D4OL8ODZ770D/pub?output=csv"

if url is not None:
    # Lê a planilha enviada
    df = pd.read_csv(url, on_bad_lines='skip')
    
    # --- Filtros laterais ---
    st.sidebar.header("Filtros")

    supervisor = df["Supervisor"].dropna().unique().tolist()
    supervisor.insert(0, "Todos")
    supervisor_escolhido = st.sidebar.selectbox("Supervisor:", supervisor)

    departamentos = df["Departamento"].dropna().unique().tolist()
    departamentos.insert(0, "Todos")
    departamento_escolhido = st.sidebar.selectbox("Departamento:", departamentos)

    ingresso = df["Tipo de ingresso (para função de Agente de Soluções em Telecomunicação)"].dropna().unique().tolist()
    ingresso.insert(0, "Todos")
    ingresso_escolhido = st.sidebar.selectbox("Tipo de Ingresso:", ingresso)

    demissao = df["Tipo de demissão"].dropna().unique().tolist()
    demissao.insert(0, "Todos")
    demissao_escolhido = st.sidebar.selectbox("Tipo de Demissão:", demissao)

    tempo = df["Tempo de empresa"].dropna().unique().tolist()
    tempo.insert(0, "Todos")
    tempo_escolhido = st.sidebar.selectbox("Tempo de Empresa:", tempo)

    df_filt = df.copy()

    # Filtro por tipo de ingresso
    if supervisor_escolhido != "Todos":
        df_filt = df_filt[df_filt["Supervisor"].str.lower() == supervisor_escolhido.lower()]

    if departamento_escolhido != "Todos":
        df_filt = df_filt[df_filt["Departamento"].str.lower() == departamento_escolhido.lower()]

    # Filtro por mês/ano
    if ingresso_escolhido != "Todos":
        df_filt = df_filt[df_filt["Tipo de ingresso (para função de Agente de Soluções em Telecomunicação)"].str.lower() == ingresso_escolhido.lower()]

    if demissao_escolhido != "Todos":
        df_filt = df_filt[df_filt["Tipo de demissão"].str.lower() == demissao_escolhido.lower()]
    
    if tempo_escolhido != "Todos":
        df_filt = df_filt[df_filt["Tempo de empresa"].str.lower() == tempo_escolhido.lower()]


    # --- Exibição opcional da tabela ---

    mostrar_tabela = st.checkbox("Mostrar tabela completa filtrada")
    if mostrar_tabela:
        st.dataframe(df_filt, use_container_width=True)
    
    jovens = df_filt[df_filt["Tipo de ingresso (para função de Agente de Soluções em Telecomunicação)"] == "Jovens na Base"]
    exp = df_filt[df_filt["Tipo de ingresso (para função de Agente de Soluções em Telecomunicação)"] == "Com experiência"] 

    ped = df_filt[df_filt["Tipo de demissão"] == "Pedido de demissão"]
    

    saidas = df_filt["Nome"].count()
    jovens_na_base = jovens["Nome"].count()
    com_exp = exp["Nome"].count()
    pedido = ped["Nome"].count()
    desligamento = df["Nome"].count() - pedido

    st.markdown("""
    <style>                                                                                                      
        @keyframes float{
            0%, 100%{
                transform: translateY(0.1rem);
            }
            50%{
                transform: translateY(-0.2rem);
        }
            }
        label{
            font-weight: 600;
        }
        .subtitle{
            font-size: 14px;
            color: #8f8f8f;
            margin-top:5px;
            
        }
       .row1{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 20px;
            
            overflow: scroll;
        }
        .row2{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 10px;
            margin-bottom: 30px
        }
        .row3{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(1, 1fr);
            gap: 10px;
        }
        .card{
            min-width: 175px;
            display: flex;
            flex-direction: column;
            border-radius: 10px;
            background: #262730;
            text-align: center;
            font-size: 20px;
            padding: 8px 10px; 
            box-shadow: 0px 4px 12px rgba(71, 72, 89, 0.2);
            border: solid 1px #61626b;
        }
        .img{
            background-image: url("../group.png");
            width:30px;
        }
        .title{
            display: flex;
            margin: auto;
            gap: 15px;
        }
        .text{
            display: flex;
            margin: auto;
            gap: 10px;
            align-items: center;
        }
        .green{
            color:#009127;
        }
        .red{
            color:#b50000;
        }
        .blue{
            color: #1F37D8;
        }
        .orange{
            color: #E07500;   
        }
        .num{
            font-size:30px;
        }
       
        .subs{
            display:flex;
            max-width: 75%;
            flex-wrap: wrap;
            
            margin: auto;
        }
        
    </style>  
""", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="row1">
        <div class="card">
            <div class="title">
                <label>Saidas</label>
            </div>
            <label class="num">{saidas}</label>
        </div>
        <div class="card">
            <div class="title">
                <label>Jovens na Base</label>
            </div>
            <label class="num">{jovens_na_base}</label>
        </div>
        <div class="card">
            <div class="title">
                <label>Com Experiência</label>
            </div>
            <label class="num">{com_exp}</label>
        </div>
        <div class="card">
            <div class="title">
                <label>Pedidos de Saída</label>
            </div>
            <label class="num">{pedido}</label>
        </div>
        <div class="card">
            <div class="title">
                <label>Desligamentos</label>
            </div>
            <label class="num">{desligamento}</label>
        </div>
        
    </div>

    """, unsafe_allow_html=True)

    # --- Gráficos ---
   

    graficos = [
        "2. Como você descreveria sua experiência geral trabalhando aqui?",
        "5. Como você avalia o clima organizacional da empresa?",
        "6. Você recebeu metas claras e atingíveis?",
        "7. Como você avalia a comunicação interna da empresa?",
        "8. Você se sentiu apoiado(a) e valorizado(a) pela liderança?",
        "10. Você sentiu que teve oportunidades de crescimento e desenvolvimento aqui?",
        "11. Você estava satisfeito(a) com sua remuneração e benefícios?",
        "14. Você consideraria voltar a trabalhar aqui no futuro?"
    ]

    titulos = [
        "Descricao Experiencia",
        "Clima Organizacional",
        "Metas claras e Atingíveis",
        "Experiência Comunicação Interna",
        "Apoio e Valorizacao Pela Lideranca",
        "Oportunidade Para Crescimento",
        "Satisfação com Remuneração e benfícios",
        "Voltaria a trabalhar"
    ]

    ordens = [["Muito positiva", "Positiva", "Neutra", "Muito negativa", "Negativa"], ["Excelente", "Bom", "Satisfatório","Insatisfatório", "Ruim"], 
              ["Sim", "Não"], ["Excelente", "Boa", "Satisfatória", "Insatisfatória", "Ruim"],["Sempre", "Frequentemente", "Às vezes", "Raramente", "Nunca"],
              ["Sempre", "Frequentemente", "Às vezes", "Raramente", "Nunca"], ["Excelente", "Bom", "Satisfatório","Insatisfatório", "Ruim"],
              ["Muito Satisfeito", "Satisfeito", "Neutro", "Insatisfeito", "Muito insatisfeito"]
            ]

    # Criação das colunas (4 linhas x 2 colunas)
    cols = [st.columns(3) for _ in range(3)]
    colunas = [c for dupla in cols for c in dupla]

    def gera_grafico(coluna, col, titulo, ordem):
        if coluna not in df_filt.columns:
            return
        cont = df_filt[coluna].dropna().value_counts().reset_index()
        if cont.empty:
            return
        cont.columns = [coluna, "Quantidade"]
        fig = px.pie(cont, values="Quantidade", names=coluna, title=titulo, category_orders={coluna: ordem})
        fig.update_traces(textinfo="percent+value", textfont_size=22, sort=False)
        fig.update_layout(
            title_font_size=25,
              legend=dict(
                font=dict(
                    size=18  # tamanho da legenda
                )
            )  # tamanho do título
        )   

        col.plotly_chart(fig, use_container_width=True)

    # Gera todos os gráficos
    for i, nome in enumerate(graficos):
        gera_grafico(nome, colunas[i], titulos[i], ordens[i])

else:
    st.info("Envie um arquivo Excel (.xlsx) na barra lateral para iniciar a análise.")
