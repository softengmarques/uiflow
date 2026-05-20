import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="UIFlow",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_PROMPT = """
Você é o "UIFlow", um assistente de IA especializado em design digital, com foco em UI/UX.
Seu objetivo é ajudar iniciantes a criar interfaces modernas, organizadas e funcionais.
"""

# SIDEBAR
with st.sidebar:

    st.title("UIFlow - Assistente de Design UI/UX")

    st.markdown(
        "Assistente de IA especializado em Design UI/UX, criação de interfaces e organização visual."
    )

    groq_api_key = st.text_input(
        "Insira sua API Key da Groq:",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/",
    )

    st.markdown("---")

    st.markdown(
        "Este assistente ajuda na criação de interfaces, cores, layouts e UX."
    )

    st.markdown("---")

    st.markdown("🔗 Conheça meu perfil no GitHub")
    st.markdown("[GitHub](https://github.com/softengmarques)")

# TÍTULO PRINCIPAL
st.title("Assistente - UIFlow")
st.title("UIFlow - Seu Assistente de Design Digital")

st.markdown(
    "Faça suas perguntas sobre design, organização visual, criação de interfaces e muito mais!"
)

# HISTÓRICO
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

# API
if groq_api_key:
    try:
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.sidebar.error(f"Erro ao conectar com a API da Groq: {e}")
        st.stop()

elif st.session_state.messages:
    st.warning("Insira sua API Key da Groq para continuar.")

# CHAT INPUT
if prompt := st.chat_input("Digite sua pergunta sobre design..."):

    if not client:
        st.warning("Insira sua API Key da Groq.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}] + st.session_state.messages

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):

            try:
                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048,
                )

                resposta = chat_completion.choices[0].message.content
                st.markdown(resposta)

                st.session_state.messages.append(
                    {"role": "assistant", "content": resposta}
                )

            except Exception as e:
                st.error(f"Erro ao obter resposta da API da Groq: {e}")

# RODAPÉ
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
<hr>
<p>Desenvolvido por <a href="https://www.linkedin.com/in/anapaulaqs/" target="_blank">Ana Paula Marques</a> - 2024</p>
</div>
""", unsafe_allow_html=True) 