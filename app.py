import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Gerador de Nota PMMG", page_icon="👮")

st.title("Gerador de Nota - PMMG")

# --- FUNÇÃO AUXILIAR PARA DATA (Formato PMMG) ---
def get_data_militar():
    agora = datetime.now()
    meses = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
             7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    dias_sem = {0: 'Seg', 1: 'Ter', 2: 'Qua', 3: 'Qui', 4: 'Sex', 5: 'Sab', 6: 'Dom'}
    
    # Ex: 061942Jan26-Ter (DDHHMMMesAA-Dia)
    data_fmt = f"{agora.day:02d}{agora.hour:02d}{agora.minute:02d}{meses[agora.month]}{str(agora.year)[2:]}-{dias_sem[agora.weekday()]}"
    return data_fmt

# --- ÁREA DE INPUT ---
st.sidebar.header("Cabeçalho Padrão")
unidade = st.sidebar.text_input("Unidade", value="DIVINÓPOLIS (23° BPM/ 7ª RPM)")
setor = st.sidebar.text_input("Setor/Cia", value="Centro/53ª Cia PM")

st.subheader("Dados da Ocorrência")

col1, col2 = st.columns(2)
with col1:
    local = st.text_input("Local", placeholder="Rua Itapecerica n. 151, Centro")
    # Tenta preencher a data automaticamente no formato militar
    data_hora = st.text_input("Data/Hora", value=get_data_militar())

with col2:
    natureza = st.text_input("Natureza", placeholder="C01. 157 - Roubo consumado...")
    reds = st.text_input("REDS", placeholder="2026-000...")

preso = st.text_area("Preso(s)", height=68, placeholder="⛓️ Nome, idade...", help="Os dados aparecerão na frente do título.")

sintese = st.text_area("Síntese", height=200, placeholder="Cole o histórico aqui...")

st.subheader("Guarnições")
guarnicoes = st.text_area("Lista de Viaturas", height=150, 
                          placeholder="🚔 *CPCia A* 🚔\nTen Messi\nCb Romário...")

# --- LÓGICA DE FORMATAÇÃO ---
def gerar_texto():
    # 1. Formata Guarnições (Adiciona * na primeira linha de cada bloco separado por enter duplo)
    txt_guarnicoes = ""
    if guarnicoes:
        blocos = guarnicoes.strip().split('\n\n') # Divide onde houver linha vazia
        blocos_formatados = []
        for bloco in blocos:
            linhas = bloco.strip().split('\n')
            if linhas:
                # Remove asteriscos se o usuário já tiver colocado e adiciona os novos
                titulo_limpo = linhas[0].strip().replace('*', '') 
                linhas[0] = f"*{titulo_limpo}*" 
                blocos_formatados.append('\n'.join(linhas))
        txt_guarnicoes = '\n\n'.join(blocos_formatados)

    # 2. Tratamento do Preso
    txt_preso = f"{preso}" if preso else "Não houve prisão."
    
    # 3. Montagem do texto final
    texto_final = f"""*{unidade}*
*SETOR/CIA:* {setor}

📍 *LOCAL:* {local}

🚨 *NATUREZA:* {natureza}

🗓️ *DATA/HORA:* {data_hora}

🔗 *PRESO:* {txt_preso}

📜 *SÍNTESE*: 
{sintese}

*REDS:* {reds}

{txt_guarnicoes}

“RELEASE INTERNO, NÃO AUTORIZADO SUA REPRODUÇÃO AO PÚBLICO EXTERNO À PMMG”.

_*Polícia Militar de Minas Gerais, rumo aos 250 anos!!!*_"""
    return texto_final

# --- ÁREA DE OUTPUT ---
st.divider()

if st.button("Gerar Nota Formatada", type="primary"):
    resultado = gerar_texto()
    st.success("Nota gerada! Clique no ícone de copiar no canto do bloco abaixo:")
    
    # O st.code cria um bloco com formatação preservada e botão de cópia nativo
    st.code(resultado, language="markdown")