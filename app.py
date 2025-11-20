import streamlit as st
import google.generativeai as genai
import os

# Configuração da página
st.set_page_config(
    page_title="Detecta Golpe - Verificador de Mensagens Suspeitas",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
    }
    .risk-badge {
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 18px;
        display: inline-block;
        margin: 10px 0;
    }
    .risk-low {
        background-color: #28a745;
        color: white;
    }
    .risk-medium {
        background-color: #ffc107;
        color: black;
    }
    .risk-high {
        background-color: #dc3545;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("🛡️ Detecta Golpe")
st.markdown("### Verificador Inteligente de Mensagens Suspeitas")
st.markdown("---")

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Sobre o App")
    st.markdown("""
    **Detecta Golpe** usa inteligência artificial para analisar mensagens 
    suspeitas e identificar possíveis golpes e fraudes.
    
    **Como usar:**
    1. Cole o texto da mensagem suspeita
    2. Selecione de onde veio
    3. Clique em "Analisar Mensagem"
    
    **O que você recebe:**
    - 🔴 Nível de risco
    - 🧠 Análise detalhada
    - ✅ Recomendações
    - 🛡️ Dicas de segurança
    """)
    
    st.markdown("---")
    st.markdown("**⚙️ Configuração da API**")
    
    # Tentar obter API Key dos secrets
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key configurada via secrets!")
    except (KeyError, FileNotFoundError):
        st.warning("⚠️ API Key não encontrada nos secrets")
        st.info("Configure o arquivo `.streamlit/secrets.toml` com sua chave")
        
        # Fallback: permitir inserir manualmente
        api_key = st.text_input(
            "Ou insira sua API Key manualmente:",
            type="password",
            help="Obtenha sua chave gratuita em: https://aistudio.google.com/app/apikey"
        )
        
        if api_key:
            st.success("✅ API Key manual configurada!")
    
    st.markdown("---")
    st.markdown("**📊 Desenvolvido para FATEC**")
    st.markdown("Projeto de Engenharia de Machine Learning")

# Container principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Cole a Mensagem Suspeita")
    mensagem = st.text_area(
        "Mensagem:",
        height=200,
        placeholder="Exemplo: 'Seu pacote está parado. Clique no link para liberar: http://exemplo-suspeito.com'",
        help="Cole aqui o texto completo da mensagem que você recebeu"
    )

with col2:
    st.subheader("📱 Origem da Mensagem")
    origem = st.selectbox(
        "De onde veio?",
        [
            "WhatsApp",
            "SMS",
            "E-mail",
            "Instagram",
            "Facebook",
            "Telegram",
            "Twitter/X",
            "Outro"
        ]
    )
    
    st.markdown("---")
    
    # Botão de análise
    analisar = st.button("🔍 Analisar Mensagem", type="primary", use_container_width=True)

# Função para criar o prompt otimizado
def criar_prompt(mensagem, origem):
    prompt = f"""
    Você é um especialista em cibersegurança e detecção de fraudes digitais, com anos de experiência 
    identificando golpes, phishing e mensagens maliciosas. Sua missão é proteger usuários comuns de 
    cair em armadilhas digitais.

    MENSAGEM RECEBIDA:
    "{mensagem}"

    ORIGEM: {origem}

    Por favor, analise essa mensagem e forneça uma avaliação completa seguindo EXATAMENTE esta estrutura:

    NÍVEL DE RISCO: [Escolha apenas um: BAIXO, MÉDIO ou ALTO]

    ANÁLISE DETALHADA:
    [Explique em 3-5 pontos por que a mensagem é ou não suspeita. Seja específico sobre os sinais 
    de alerta encontrados (urgência artificial, erros gramaticais, links suspeitos, solicitação de 
    dados pessoais, promessas irreais, etc.)]

    O QUE FAZER:
    [Forneça 2-3 ações práticas e claras que o usuário deve tomar imediatamente]

    DICAS DE SEGURANÇA:
    [Liste 3-4 dicas preventivas para evitar golpes similares no futuro]

    IMPORTANTE:
    - Seja claro e direto
    - Use linguagem acessível para usuários não técnicos
    - Se a mensagem for claramente um golpe, seja enfático
    - Se parecer legítima, explique por quê
    - Use emojis quando apropriado para tornar a resposta mais amigável
    """
    return prompt

# Função para analisar a mensagem com Gemini
def analisar_mensagem(mensagem, origem, api_key):
    try:
        # Configurar a API
        genai.configure(api_key=api_key)
        
        # Inicializar o modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Criar o prompt
        prompt = criar_prompt(mensagem, origem)
        
        # Gerar resposta
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"Erro ao analisar mensagem: {str(e)}"

# Processar análise quando o botão for clicado
if analisar:
    if not api_key:
        st.error("⚠️ Por favor, insira sua API Key do Google AI Studio na barra lateral!")
    elif not mensagem.strip():
        st.warning("⚠️ Por favor, cole uma mensagem para analisar!")
    else:
        with st.spinner("🔍 Analisando mensagem... Isso pode levar alguns segundos."):
            resultado = analisar_mensagem(mensagem, origem, api_key)
            
            st.markdown("---")
            st.subheader("📊 Resultado da Análise")
            
            # Extrair nível de risco da resposta
            resultado_lower = resultado.lower()
            if "alto" in resultado_lower.split("análise detalhada")[0]:
                st.markdown('<div class="risk-badge risk-high">🔴 RISCO ALTO</div>', unsafe_allow_html=True)
                st.error("⚠️ ATENÇÃO: Esta mensagem apresenta fortes indícios de golpe!")
            elif "médio" in resultado_lower.split("análise detalhada")[0]:
                st.markdown('<div class="risk-badge risk-medium">🟡 RISCO MÉDIO</div>', unsafe_allow_html=True)
                st.warning("⚠️ CUIDADO: Esta mensagem apresenta elementos suspeitos!")
            else:
                st.markdown('<div class="risk-badge risk-low">🟢 RISCO BAIXO</div>', unsafe_allow_html=True)
                st.info("✅ Esta mensagem parece menos suspeita, mas sempre fique atento!")
            
            # Exibir resultado completo
            st.markdown("---")
            st.markdown(resultado)
            
            # Botão para nova análise
            st.markdown("---")
            if st.button("🔄 Analisar Outra Mensagem"):
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p><strong>🛡️ Detecta Golpe</strong> - Proteja-se contra fraudes digitais</p>
        <p>Desenvolvido com ❤️ usando Streamlit e Google Gemini AI</p>
        <p><em>Dica: Sempre desconfie de mensagens com urgência excessiva, erros gramaticais e links suspeitos!</em></p>
    </div>
""", unsafe_allow_html=True)

