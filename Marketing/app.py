import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

# Carrega as variáveis de ambiente
load_dotenv(ROOT_DIR / ".env")

# Conexão com a LLM
id_model = "qwen/qwen3.8-27b"
llm = ChatGroq(
    model = id_model,
    temperature = 0.7,
    max_tokens = None,
    timeout = None,
    max_retries = 2,
)

# Função de geração
def llm_generate(llm, prompt):
  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
      ("human", "{prompt}"),
  ])

  chain = template | llm | StrOutputParser()

  res = chain.invoke({"prompt": prompt})
  return res

# Configuração de Página
st.set_page_config(page_title = "Gerador de conteúdo", page_icon="🤖")
st.title("Gerador de Conteúdo")

# Campos do Formulário
topic = st.text_input("Tema: ", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")
platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])
cta = st.text_input("Chamada para Ação (CTA)", placeholder="Ex: Clique para entrar em contato...")
hashtags = st.checkbox("Retornar Hashtags")
keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")

if st.button("Gerar conteúdo"):
  prompt = f"""
  Escreva um texto com SEO otimizado sobre o tema '{topic}'.
  Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
  - Onde será publicado: {platform}.
  - Tom: {tone}.
  - Público-alvo: {audience}.
  - Comprimento: {length}.
  - {"Inclua uma chamada para ação clara ao final do texto." + cta if cta else "Não inclua chamada para ação"}
  - {"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."}
  {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""}
  """
  try:
      res = llm_generate(llm, prompt)
      st.markdown(res)
  except Exception as e:
      st.error(f"Erro: {e}")