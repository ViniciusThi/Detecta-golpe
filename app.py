import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import requests
import json
import re
from urllib.parse import urlparse
from PIL import Image
import io
import base64

# Configuração da página
st.set_page_config(
    page_title="Detecta Golpe - Verificador de Mensagens Suspeitas",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado profissional
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
        padding: 15px 30px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 22px;
        display: inline-block;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-transform: uppercase;
    }
    .risk-low {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
    }
    .risk-medium {
        background: linear-gradient(135deg, #ffc107, #ff9800);
        color: black;
    }
    .risk-high {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    .metric-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 10px 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .danger-box {
        background: #f8d7da;
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
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
    **Detecta Golpe** usa IA avançada (Google Gemini 2.5 Flash - Gratuito) 
    para análise profunda de mensagens e imagens suspeitas.
    
    **Como usar:**
    1. Cole o texto OU faça upload de imagem
    2. Selecione a origem
    3. Escolha o modo de análise
    4. Clique em "Analisar"
    
    **O que você recebe:**
    - 🔴 Nível de risco detalhado
    - 🧠 Análise técnica profunda
    - 🔍 Verificação de URLs e padrões
    - ⚠️ Indicadores de phishing
    - 📊 Score de confiança
    - ✅ Recomendações práticas
    - 🛡️ Relatório completo
    """)
    
    st.markdown("---")
    st.markdown("**🤖 Escolha a IA**")
    
    # Seletor de API
    api_escolhida = st.selectbox(
        "Qual API usar?",
        ["🔷 Google Gemini", "🔶 DeepSeek", "🟢 ChatGPT (OpenAI)"],
        help="Escolha qual inteligência artificial deseja usar para análise"
    )
    
    st.markdown("---")
    st.markdown("**⚙️ Modo de Análise**")
    
    modo_analise = st.radio(
        "Escolha o rigor:",
        ["🟢 Padrão", "🟡 Rigoroso", "🔴 Máximo"],
        help="Quanto mais rigoroso, mais detalhada e crítica será a análise"
    )
    
    st.markdown("---")
    st.markdown("**🔑 Configuração das APIs**")
    
    # Variáveis para as chaves
    google_api_key = None
    deepseek_api_key = None
    openai_api_key = None
    
    # Tentar obter as API Keys dos secrets
    try:
        google_api_key = st.secrets.get("GOOGLE_API_KEY", None)
        deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", None)
        openai_api_key = st.secrets.get("OPENAI_API_KEY", None)
        
        apis_configuradas = []
        if google_api_key:
            apis_configuradas.append("✅ Google Gemini")
        if deepseek_api_key:
            apis_configuradas.append("✅ DeepSeek")
        if openai_api_key:
            apis_configuradas.append("✅ ChatGPT")
            
        if apis_configuradas:
            for api in apis_configuradas:
                st.success(api)
        else:
            st.warning("⚠️ Nenhuma API configurada nos secrets")
            
    except (KeyError, FileNotFoundError, AttributeError):
        st.warning("⚠️ Arquivo secrets.toml não encontrado")
    
    # Verificar qual API está sendo usada e se está configurada
    if api_escolhida == "🔷 Google Gemini":
        if not google_api_key:
            st.info("🔷 Configure a Google API Key")
            google_api_key = st.text_input(
                "Google API Key:",
                type="password",
                help="https://aistudio.google.com/app/apikey",
                key="google_manual"
            )
        else:
            st.caption("🤖 Usando Gemini AI")
        
        api_key = google_api_key
        
    elif api_escolhida == "🔶 DeepSeek":
        st.warning("⚠️ **DeepSeek requer créditos pagos**\n\nPara usar DeepSeek, você precisa adicionar créditos em sua conta.\n\n💡 **Recomendação:** Use Google Gemini (gratuito) para testes.")
        if not deepseek_api_key:
            st.info("🔶 Configure a DeepSeek API Key")
            deepseek_api_key = st.text_input(
                "DeepSeek API Key:",
                type="password",
                help="https://platform.deepseek.com/api_keys - Requer créditos pagos",
                key="deepseek_manual"
            )
        else:
            st.caption("🤖 Usando DeepSeek AI (requer créditos)")
        
        api_key = deepseek_api_key
        
    else:  # ChatGPT
        st.warning("⚠️ **ChatGPT requer créditos pagos**\n\nPara usar ChatGPT, você precisa adicionar créditos em sua conta OpenAI.\n\n💡 **Recomendação:** Use Google Gemini (gratuito) para testes.")
        if not openai_api_key:
            st.info("🟢 Configure a OpenAI API Key")
            openai_api_key = st.text_input(
                "OpenAI API Key:",
                type="password",
                help="https://platform.openai.com/api-keys - Requer créditos pagos",
                key="openai_manual"
            )
        else:
            st.caption("🤖 Usando ChatGPT (GPT-4) - Requer créditos")
        
        api_key = openai_api_key
    
    # Status da configuração
    if api_key:
        if api_escolhida == "🔷 Google Gemini":
            st.success(f"✅ {api_escolhida} pronto para usar! (Gratuito)")
        else:
            st.success(f"✅ {api_escolhida} configurado (requer créditos)")
    else:
        if api_escolhida == "🔷 Google Gemini":
            st.error("⚠️ Insira a API Key do Google Gemini para continuar")
        else:
            st.error("⚠️ Insira a API Key e adicione créditos para continuar")
    
    st.markdown("---")
    st.markdown("**📊 FATEC**")
    st.caption("Engenharia de ML")

# Tabs para tipo de entrada
tab_texto, tab_imagem, tab_ambos = st.tabs(["📝 Texto", "🖼️ Imagem", "📝🖼️ Texto + Imagem"])

mensagem = ""
imagem = None

with tab_texto:
    st.subheader("Cole a Mensagem Suspeita")
    mensagem = st.text_area(
        "Mensagem:",
        height=250,
        placeholder="Exemplo: 'Seu pacote está parado. Clique no link para liberar: http://exemplo-suspeito.com'\n\nOu cole toda a conversa suspeita aqui...",
        help="Cole o texto completo da mensagem suspeita",
        key="texto_apenas"
    )

with tab_imagem:
    st.subheader("Faça Upload da Imagem")
    st.info("📸 Faça upload de prints de mensagens, e-mails, SMS, etc.")
    imagem = st.file_uploader(
        "Escolha uma imagem:",
        type=["png", "jpg", "jpeg", "webp"],
        help="Formatos suportados: PNG, JPG, JPEG, WEBP",
        key="imagem_apenas"
    )
    
    if imagem:
        st.image(imagem, caption="Imagem para análise", use_container_width=True)

with tab_ambos:
    st.subheader("Texto + Imagem para Análise Completa")
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.markdown("**📝 Texto:**")
        mensagem_ambos = st.text_area(
            "Mensagem:",
            height=200,
            placeholder="Adicione contexto ou informações extras...",
            help="Texto adicional para análise",
            key="texto_ambos"
        )
    
    with col_b:
        st.markdown("**🖼️ Imagem:**")
        imagem_ambos = st.file_uploader(
            "Imagem:",
            type=["png", "jpg", "jpeg", "webp"],
            key="imagem_ambos"
        )
        
        if imagem_ambos:
            st.image(imagem_ambos, use_container_width=True)
    
    # Unificar variáveis
    if mensagem_ambos:
        mensagem = mensagem_ambos
    if imagem_ambos:
        imagem = imagem_ambos

# Container de configurações e análise
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("📱 Origem da Mensagem")
    origem = st.selectbox(
        "De onde veio?",
        [
            "WhatsApp",
            "SMS",
            "E-mail",
            "Instagram",
            "Facebook Messenger",
            "Telegram",
            "Twitter/X DM",
            "LinkedIn",
            "TikTok",
            "Site/Formulário Web",
            "Ligação Telefônica",
            "Outro"
        ]
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    verificar_urls = st.checkbox("🔍 Análise de URLs", value=True, help="Verifica URLs suspeitas na mensagem")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    # Botão de análise
    analisar = st.button("🚀 ANALISAR", type="primary", use_container_width=True)

# Função para extrair e analisar URLs
def extrair_urls(texto):
    """Extrai todas as URLs de um texto"""
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.findall(texto)

def analisar_url(url):
    """Analisa uma URL em busca de sinais suspeitos"""
    suspeitas = []
    try:
        parsed = urlparse(url)
        dominio = parsed.netloc.lower()
        
        # Verificações
        if len(dominio) > 50:
            suspeitas.append("⚠️ Domínio muito longo")
        
        if dominio.count('-') > 3:
            suspeitas.append("⚠️ Muitos hífens no domínio")
        
        if any(char.isdigit() for char in dominio):
            if sum(char.isdigit() for char in dominio) > 4:
                suspeitas.append("⚠️ Muitos números no domínio")
        
        # Padrões comuns de phishing
        padroes_suspeitos = ['secure', 'account', 'verify', 'login', 'update', 'confirm', 
                             'banking', 'paypal', 'amazon', 'microsoft', 'google', 
                             'whatsapp', 'netflix', 'apoio', 'suporte', 'urgente']
        
        for padrao in padroes_suspeitos:
            if padrao in dominio and not dominio.endswith(('.com.br', '.gov.br', '.org', '.edu')):
                suspeitas.append(f"⚠️ Usa palavra '{padrao}' suspeita")
                break
        
        # IPs ao invés de domínio
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', dominio):
            suspeitas.append("🚨 Usa endereço IP direto (muito suspeito)")
        
        # Subdomínios suspeitos
        if dominio.count('.') > 3:
            suspeitas.append("⚠️ Muitos subdomínios")
        
    except:
        suspeitas.append("❌ URL mal formatada")
    
    return suspeitas

# Função para criar o prompt ultra-rigoroso
def criar_prompt(mensagem, origem, modo_analise, info_urls=""):
    """Cria um prompt personalizado baseado no modo de análise"""
    
    rigor_config = {
        "🟢 Padrão": {
            "profundidade": "moderada",
            "tom": "equilibrado",
            "criterios": "Analise considerando o contexto geral"
        },
        "🟡 Rigoroso": {
            "profundidade": "profunda",
            "tom": "crítico",
            "criterios": "Seja bastante crítico. Mesmo pequenos sinais devem aumentar o nível de alerta"
        },
        "🔴 Máximo": {
            "profundidade": "extremamente detalhada",
            "tom": "hipercrítico",
            "criterios": "ANÁLISE FORENSE COMPLETA. Qualquer anomalia deve ser tratada como suspeita. Assuma o pior cenário até provar o contrário"
        }
    }
    
    config = rigor_config.get(modo_analise, rigor_config["🟢 Padrão"])
    
    prompt = f"""
    Você é um ESPECIALISTA SÊNIOR em Cibersegurança Forense e Análise de Fraudes Digitais, com certificações 
    em CEH, CISSP e experiência em investigação de crimes cibernéticos. Você trabalha protegendo milhões 
    de usuários contra phishing, scams, engenharia social e fraudes digitais.

    ═══════════════════════════════════════════════════════════════
    DADOS DA ANÁLISE
    ═══════════════════════════════════════════════════════════════
    
    📱 ORIGEM: {origem}
    🎯 MODO DE ANÁLISE: {modo_analise} ({config['profundidade']})
    
    📄 CONTEÚDO ANALISADO:
    {mensagem}
    
    {info_urls}
    
    ═══════════════════════════════════════════════════════════════
    INSTRUÇÕES DE ANÁLISE ({config['tom'].upper()})
    ═══════════════════════════════════════════════════════════════
    
    {config['criterios']}
    
    Forneça uma análise EXTREMAMENTE DETALHADA seguindo EXATAMENTE esta estrutura:
    
    ⚠️ CRÍTICO: O NÍVEL DE RISCO DEVE SER A PRIMEIRA COISA NA SUA RESPOSTA! ⚠️
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎯 NÍVEL DE RISCO: [ESCOLHA APENAS UM: BAIXO | MÉDIO | ALTO | CRÍTICO]
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    📊 SCORE DE CONFIANÇA: [0-100]% (0 = Golpe Certeza | 100 = Legítimo)
    
    IMPORTANTE: 
    - O NÍVEL DE RISCO deve aparecer EXATAMENTE no formato acima, no início da resposta
    - Use APENAS uma das opções: BAIXO, MÉDIO, ALTO ou CRÍTICO
    - Seja CONSISTENTE: se você classificar como CRÍTICO, toda a análise deve refletir isso
    - NÃO contradiga o nível de risco na análise - se é CRÍTICO, a análise deve ser crítica
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔍 ANÁLISE TÉCNICA DETALHADA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Analise PROFUNDAMENTE cada aspecto:
    
    1. **LINGUAGEM E COMUNICAÇÃO** 📝
       - Gramática e ortografia
       - Tom de urgência ou pressão psicológica
       - Uso de linguagem profissional vs amadora
       - Técnicas de engenharia social identificadas
    
    2. **ELEMENTOS TÉCNICOS** 🔧
       - URLs e links (estrutura, domínio, HTTPS, certificados)
       - Endereços de e-mail ou números (autenticidade)
       - Metadados e informações técnicas
    
    3. **TÁTICAS DE FRAUDE DETECTADAS** 🎯
       - Senso de urgência artificial
       - Promessas irreais ou ofertas boas demais
       - Solicitação de dados pessoais/financeiros
       - Ameaças ou consequências negativas
       - Pretextos falsos (falsa autoridade, falsa empresa)
    
    4. **INDICADORES DE PHISHING/SCAM** 🚨
       - Liste TODOS os red flags encontrados
       - Padrões conhecidos de golpes
       - Similaridades com fraudes documentadas
    
    5. **ANÁLISE DE CONTEXTO** 🧩
       - A mensagem faz sentido para a origem indicada?
       - Empresas legítimas usariam essa abordagem?
       - Existem inconsistências lógicas?
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ⚠️ AÇÕES IMEDIATAS RECOMENDADAS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Liste 3-5 ações práticas e ESPECÍFICAS que o usuário deve tomar AGORA:
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🛡️ RECOMENDAÇÕES DE SEGURANÇA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Forneça 4-6 dicas preventivas detalhadas e práticas
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📋 VEREDICTO FINAL
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Em 2-3 frases, dê seu veredicto profissional sobre esta mensagem.
    
    ═══════════════════════════════════════════════════════════════
    
    IMPORTANTE:
    - Use linguagem técnica mas acessível
    - Seja EXTREMAMENTE detalhado na análise
    - Se for golpe, seja ENFÁTICO e direto
    - Se for legítimo, explique CLARAMENTE por quê
    - Use emojis para destacar pontos importantes
    - Numere e estruture bem a resposta
    - NÃO economize em detalhes - quanto mais informação, melhor
    """
    return prompt

# Função para analisar com ChatGPT (OpenAI)
def analisar_com_chatgpt(mensagem, origem, api_key, modo_analise, imagem=None, verificar_urls=True, info_urls=""):
    """Analisa mensagem usando a API do ChatGPT (OpenAI)"""
    try:
        # Configurar cliente OpenAI
        client = OpenAI(api_key=api_key)
        
        # Criar o prompt
        prompt = criar_prompt(mensagem if mensagem else "[IMAGEM FORNECIDA - ANALISE O CONTEÚDO VISUAL]", 
                             origem, modo_analise, info_urls)
        
        # Preparar mensagens
        messages = []
        
        if imagem:
            # Converter imagem para base64
            image_data = Image.open(imagem)
            buffered = io.BytesIO()
            image_data.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            })
            
            # Usar GPT-4 Vision para imagens
            modelo = "gpt-4o"
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Usar GPT-4 para texto
            modelo = "gpt-4o"
        
        # Fazer requisição
        response = client.chat.completions.create(
            model=modelo,
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        
        texto_resposta = response.choices[0].message.content
        texto_resposta += f"\n\n---\n\n*Análise realizada com: {modelo.upper()}*"
        return texto_resposta
        
    except Exception as e:
        erro_msg = str(e)
        if "insufficient_quota" in erro_msg or "billing" in erro_msg.lower():
            return """❌ **Erro: Quota/Créditos Insuficientes**

Sua conta OpenAI não tem créditos suficientes.

**Soluções:**
1. Adicione créditos em: https://platform.openai.com/account/billing
2. Verifique seu plano atual
3. Use outra API (Google Gemini ou DeepSeek)

**Erro:** """ + erro_msg
        else:
            return f"❌ Erro ao usar ChatGPT: {erro_msg}\n\nVerifique se sua API Key está correta."

# Função para analisar com DeepSeek
def analisar_com_deepseek(mensagem, origem, api_key, modo_analise, imagem=None, verificar_urls=True, info_urls=""):
    """Analisa mensagem usando a API do DeepSeek"""
    try:
        # Criar o prompt
        prompt = criar_prompt(mensagem if mensagem else "[IMAGEM FORNECIDA - ANALISE O CONTEÚDO VISUAL]", 
                             origem, modo_analise, info_urls)
        
        # Preparar mensagens
        messages = []
        
        if imagem:
            # Converter imagem para base64
            image_data = Image.open(imagem)
            buffered = io.BytesIO()
            image_data.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]
            })
        else:
            messages.append({
                "role": "user",
                "content": prompt
            })
        
        # Fazer requisição para DeepSeek
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            texto_resposta = result['choices'][0]['message']['content']
            texto_resposta += f"\n\n---\n\n*Análise realizada com: DeepSeek Chat (Requer créditos)*"
            return texto_resposta
        elif response.status_code == 402 or "insufficient" in response.text.lower() or "balance" in response.text.lower():
            return """❌ **Erro: Créditos Insuficientes no DeepSeek**

Sua conta DeepSeek não tem créditos suficientes.

**Soluções:**
1. Adicione créditos em: https://platform.deepseek.com/account/balance
2. Verifique seu saldo atual
3. Use Google Gemini (gratuito) como alternativa

**Erro:** """ + response.text
        else:
            return f"❌ Erro DeepSeek (código {response.status_code}): {response.text}\n\n💡 Lembre-se: DeepSeek requer créditos pagos. Use Google Gemini para testes gratuitos."
            
    except Exception as e:
        erro_msg = str(e)
        if "insufficient" in erro_msg.lower() or "balance" in erro_msg.lower() or "quota" in erro_msg.lower():
            return """❌ **Erro: Créditos Insuficientes no DeepSeek**

Sua conta DeepSeek não tem créditos suficientes.

**Soluções:**
1. Adicione créditos em: https://platform.deepseek.com/account/balance
2. Verifique seu saldo atual
3. Use Google Gemini (gratuito) como alternativa

**Erro:** """ + erro_msg
        return f"❌ Erro ao usar DeepSeek: {erro_msg}\n\n💡 Lembre-se: DeepSeek requer créditos pagos. Verifique sua API Key e saldo."

# Função para analisar a mensagem com Gemini (com suporte a imagens)
def analisar_mensagem(mensagem, origem, api_key, modo_analise, imagem=None, verificar_urls=True):
    try:
        # Configurar a API
        genai.configure(api_key=api_key)
        
        # Usar APENAS gemini-2.5-flash (disponível gratuitamente em novembro 2025)
        # Este modelo suporta texto e imagens
        modelo_usado = 'gemini-2.5-flash'
        model = genai.GenerativeModel(modelo_usado)
        
        # Análise de URLs se habilitado
        info_urls = ""
        if verificar_urls and mensagem:
            urls = extrair_urls(mensagem)
            if urls:
                info_urls = "\n🔗 URLS ENCONTRADAS E PRÉ-ANÁLISE:\n"
                for url in urls:
                    info_urls += f"\n📍 URL: {url}\n"
                    problemas = analisar_url(url)
                    if problemas:
                        info_urls += "   ALERTAS:\n"
                        for problema in problemas:
                            info_urls += f"   - {problema}\n"
                    else:
                        info_urls += "   ✅ Nenhum problema óbvio detectado\n"
                info_urls += "\n"
        
        # Criar o prompt
        prompt = criar_prompt(mensagem if mensagem else "[IMAGEM FORNECIDA - ANALISE O CONTEÚDO VISUAL]", 
                             origem, modo_analise, info_urls)
        
        # Preparar conteúdo para análise
        if imagem:
            # Processar imagem
            image_data = Image.open(imagem)
            
            # Se tiver texto também, fazer análise multimodal
            if mensagem and mensagem.strip():
                response = model.generate_content([prompt, image_data])
            else:
                # Só imagem
                response = model.generate_content([
                    "Analise esta imagem em busca de sinais de golpe, fraude ou phishing. ",
                    prompt, 
                    image_data
                ])
        else:
            # Só texto
            response = model.generate_content(prompt)
        
        resultado_texto = response.text
        
        # Adicionar informação do modelo usado
        resultado_texto += f"\n\n---\n\n*Análise realizada com: {modelo_usado} (Gratuito)*"
        
        return resultado_texto
        
    except Exception as e:
        erro_msg = str(e)
        
        # Mensagens de erro mais amigáveis
        if "404" in erro_msg or "not found" in erro_msg:
            return """❌ **Erro: Modelo gemini-2.5-flash não encontrado**

O modelo `gemini-2.5-flash` não está disponível para sua API Key.

**Soluções:**

1. **Gere uma NOVA API Key (IMPORTANTE):**
   - Acesse: https://aistudio.google.com/app/apikey
   - Clique em "Create API Key" para gerar uma chave nova
   - Chaves antigas podem não ter acesso ao modelo mais recente
   - Copie a nova chave e atualize no Streamlit Secrets

2. **Verifique a data:**
   - O modelo `gemini-2.5-flash` está disponível gratuitamente a partir de novembro de 2025
   - Certifique-se de que sua conta tem acesso aos modelos mais recentes

3. **Aguarde alguns minutos:**
   - Às vezes a API do Google pode estar temporariamente indisponível

**Detalhes do erro técnico:**
```
""" + erro_msg + """
```

💡 **Dica:** Sempre gere uma API Key NOVA para garantir acesso aos modelos mais recentes!
🔗 Obter nova API Key: https://aistudio.google.com/app/apikey"""
        
        elif "quota" in erro_msg.lower() or "limit" in erro_msg.lower():
            return f"""❌ **Erro: Limite de uso atingido**

Você atingiu o limite de requisições da sua API Key.

**Soluções:**
- Aguarde alguns minutos e tente novamente
- Verifique seus limites em: https://aistudio.google.com/
- Considere gerar uma nova API Key

**Erro:** {erro_msg}"""
        
        else:
            return f"""❌ **Erro ao processar análise**

Ocorreu um erro inesperado durante a análise.

**Detalhes:**
```
{erro_msg}
```

**Possíveis soluções:**
1. Verifique sua conexão com a internet
2. Confirme se sua API Key está correta
3. Tente novamente em alguns instantes
4. Se o erro persistir, gere uma nova API Key

🔗 Obtenha/renove sua API Key: https://aistudio.google.com/app/apikey"""

# Processar análise quando o botão for clicado
if analisar:
    if not api_key:
        st.error("⚠️ Por favor, configure sua API Key do Google AI Studio na barra lateral!")
    elif not mensagem.strip() and not imagem:
        st.warning("⚠️ Por favor, forneça pelo menos uma mensagem de texto OU uma imagem para analisar!")
    else:
        # Animação de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Iniciando análise...")
        progress_bar.progress(20)
        
        if verificar_urls and mensagem:
            status_text.text("🔍 Verificando URLs...")
            progress_bar.progress(40)
        
        # Definir qual IA está sendo usada
        if api_escolhida == "🔷 Google Gemini":
            nome_ia = "Google Gemini"
        elif api_escolhida == "🔶 DeepSeek":
            nome_ia = "DeepSeek"
        else:
            nome_ia = "ChatGPT"
            
        status_text.text(f"🧠 Processando com {nome_ia}...")
        progress_bar.progress(60)
        
        # Realizar análise com a API escolhida
        if api_escolhida == "🔷 Google Gemini":
            resultado = analisar_mensagem(mensagem, origem, api_key, modo_analise, imagem, verificar_urls)
            
        elif api_escolhida == "🔶 DeepSeek":
            # Fazer análise de URLs primeiro se necessário
            info_urls = ""
            if verificar_urls and mensagem:
                urls = extrair_urls(mensagem)
                if urls:
                    info_urls = "\n🔗 URLS ENCONTRADAS E PRÉ-ANÁLISE:\n"
                    for url in urls:
                        info_urls += f"\n📍 URL: {url}\n"
                        problemas = analisar_url(url)
                        if problemas:
                            info_urls += "   ALERTAS:\n"
                            for problema in problemas:
                                info_urls += f"   - {problema}\n"
                        else:
                            info_urls += "   ✅ Nenhum problema óbvio detectado\n"
                    info_urls += "\n"
            
            resultado = analisar_com_deepseek(mensagem, origem, api_key, modo_analise, imagem, verificar_urls, info_urls)
            
        else:  # ChatGPT
            # Fazer análise de URLs primeiro se necessário
            info_urls = ""
            if verificar_urls and mensagem:
                urls = extrair_urls(mensagem)
                if urls:
                    info_urls = "\n🔗 URLS ENCONTRADAS E PRÉ-ANÁLISE:\n"
                    for url in urls:
                        info_urls += f"\n📍 URL: {url}\n"
                        problemas = analisar_url(url)
                        if problemas:
                            info_urls += "   ALERTAS:\n"
                            for problema in problemas:
                                info_urls += f"   - {problema}\n"
                        else:
                            info_urls += "   ✅ Nenhum problema óbvio detectado\n"
                    info_urls += "\n"
            
            resultado = analisar_com_chatgpt(mensagem, origem, api_key, modo_analise, imagem, verificar_urls, info_urls)
        
        progress_bar.progress(100)
        status_text.text("✅ Análise concluída!")
        
        # Limpar barra de progresso
        import time
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
        
        # Exibir resultados
        st.markdown("---")
        st.markdown("## 📊 RELATÓRIO DE ANÁLISE COMPLETO")
        st.markdown("---")
        
        # Extrair e exibir nível de risco - busca mais precisa
        resultado_lower = resultado.lower()
        
        # Buscar padrões específicos de nível de risco no texto completo
        # Priorizar busca por "nível de risco:" ou "risco:" seguido do nível
        nivel_risco = None
        
        # Padrões para encontrar o nível de risco explicitamente mencionado
        import re
        
        # Buscar por padrão "NÍVEL DE RISCO: [NÍVEL]" ou "RISCO: [NÍVEL]"
        padrao_risco = re.search(r'(?:nível\s+de\s+risco|risco)[:\s]+(crítico|alto|médio|medio|baixo)', resultado_lower, re.IGNORECASE)
        if padrao_risco:
            nivel_encontrado = padrao_risco.group(1).lower()
            if nivel_encontrado in ['crítico', 'critico']:
                nivel_risco = 'CRÍTICO'
            elif nivel_encontrado == 'alto':
                nivel_risco = 'ALTO'
            elif nivel_encontrado in ['médio', 'medio']:
                nivel_risco = 'MÉDIO'
            elif nivel_encontrado == 'baixo':
                nivel_risco = 'BAIXO'
        
        # Se não encontrou pelo padrão, buscar por palavras-chave no contexto
        if not nivel_risco:
            # Buscar nas primeiras 2000 caracteres (onde geralmente está o nível de risco)
            texto_inicial = resultado_lower[:2000]
            
            # Prioridade: crítico > alto > médio > baixo
            if 'crítico' in texto_inicial or 'critico' in texto_inicial:
                # Verificar se não é um falso positivo (ex: "análise crítica")
                if re.search(r'\b(risco|nível|nivel).*?(crítico|critico)', texto_inicial, re.IGNORECASE):
                    nivel_risco = 'CRÍTICO'
            elif 'alto' in texto_inicial:
                if re.search(r'\b(risco|nível|nivel).*?alto', texto_inicial, re.IGNORECASE):
                    nivel_risco = 'ALTO'
            elif 'médio' in texto_inicial or 'medio' in texto_inicial:
                if re.search(r'\b(risco|nível|nivel).*?(médio|medio)', texto_inicial, re.IGNORECASE):
                    nivel_risco = 'MÉDIO'
            elif 'baixo' in texto_inicial:
                if re.search(r'\b(risco|nível|nivel).*?baixo', texto_inicial, re.IGNORECASE):
                    nivel_risco = 'BAIXO'
        
        # Exibir o nível de risco detectado
        if nivel_risco == 'CRÍTICO':
            st.markdown('<div class="risk-badge risk-high">🚨 RISCO CRÍTICO</div>', unsafe_allow_html=True)
            st.markdown('<div class="danger-box"><h3>🚨 ALERTA MÁXIMO</h3><p>Esta mensagem apresenta <strong>EVIDÊNCIAS CLARAS DE GOLPE/FRAUDE</strong>. NÃO interaja com ela!</p></div>', unsafe_allow_html=True)
        elif nivel_risco == 'ALTO':
            st.markdown('<div class="risk-badge risk-high">🔴 RISCO ALTO</div>', unsafe_allow_html=True)
            st.markdown('<div class="danger-box"><h3>⚠️ PERIGO</h3><p>Esta mensagem apresenta <strong>fortes indícios de golpe</strong>. Não clique em links e não forneça dados!</p></div>', unsafe_allow_html=True)
        elif nivel_risco == 'MÉDIO':
            st.markdown('<div class="risk-badge risk-medium">🟡 RISCO MÉDIO</div>', unsafe_allow_html=True)
            st.markdown('<div class="warning-box"><h3>⚠️ ATENÇÃO</h3><p>Esta mensagem apresenta <strong>elementos suspeitos</strong>. Proceda com cautela!</p></div>', unsafe_allow_html=True)
        elif nivel_risco == 'BAIXO':
            st.markdown('<div class="risk-badge risk-low">🟢 RISCO BAIXO</div>', unsafe_allow_html=True)
            st.info("✅ Análise indica menor probabilidade de golpe, mas mantenha sempre a vigilância!")
        else:
            # Se não conseguiu detectar, mostrar aviso genérico
            st.markdown('<div class="risk-badge risk-medium">⚠️ ANÁLISE REALIZADA</div>', unsafe_allow_html=True)
            st.warning("⚠️ Verifique o nível de risco na análise completa abaixo.")
        
        # Exibir resultado completo formatado
        st.markdown("---")
        st.markdown(resultado)
        
        # Informações adicionais
        st.markdown("---")
        
        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
        
        with col_info1:
            st.metric("🤖 IA Utilizada", api_escolhida.replace("🔷 ", "").replace("🔶 ", ""))
        
        with col_info2:
            st.metric("🎯 Modo", modo_analise.split()[1] if len(modo_analise.split()) > 1 else modo_analise)
        
        with col_info3:
            st.metric("📱 Origem", origem)
        
        with col_info4:
            tipo_entrada = "Texto" if mensagem and not imagem else "Imagem" if imagem and not mensagem else "Texto + Imagem"
            st.metric("📄 Entrada", tipo_entrada)
        
        # Botões de ação
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 Nova Análise", use_container_width=True):
                st.rerun()
        
        with col_btn2:
            st.download_button(
                label="📥 Baixar Relatório",
                data=resultado,
                file_name=f"relatorio_analise_golpe_{origem.lower().replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_btn3:
            if st.button("ℹ️ Denunciar Golpe", use_container_width=True, help="Links para canais oficiais"):
                st.info("""
                **Canais para Denúncia:**
                - 🌐 [Safernet Brasil](https://new.safernet.org.br/denuncie)
                - 📱 [WhatsApp Oficial](https://faq.whatsapp.com/general/security-and-privacy/how-to-report-spam-or-block-a-contact)
                - 🏛️ [Polícia Federal - Cibercrimes](https://www.gov.br/pf/pt-br)
                - 💳 [Banco Central - Golpes Financeiros](https://www.bcb.gov.br/acessoinformacao/denuncias)
                """)

# Footer informativo
st.markdown("---")
st.markdown("## 💡 Dicas Rápidas de Segurança")

col_dica1, col_dica2, col_dica3 = st.columns(3)

with col_dica1:
    st.markdown("""
    **🚫 Nunca Compartilhe:**
    - Senhas completas
    - Códigos de verificação
    - Dados bancários
    - CPF/RG por mensagem
    """)

with col_dica2:
    st.markdown("""
    **🔍 Sempre Verifique:**
    - URLs antes de clicar
    - Remetente da mensagem
    - Erros de português
    - Senso de urgência falso
    """)

with col_dica3:
    st.markdown("""
    **✅ Boas Práticas:**
    - Use autenticação 2FA
    - Contate empresa diretamente
    - Desconfie de prêmios
    - Não clique em links suspeitos
    """)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
        <h3 style='color: #333;'>🛡️ Detecta Golpe - Análise Avançada com IA</h3>
        <p><strong>Powered by:</strong> Google Gemini 2.5 Flash (Gratuito) | Streamlit | Python</p>
        <p>🎓 <strong>Projeto FATEC</strong> - Engenharia de Machine Learning</p>
        <p style='font-size: 14px; margin-top: 15px;'>
            <em>⚠️ Este app é uma ferramenta auxiliar. Sempre use seu julgamento crítico e, em caso de dúvida, 
            contate diretamente a empresa/instituição através dos canais oficiais.</em>
        </p>
        <p style='font-size: 12px; color: #999; margin-top: 10px;'>
            Desenvolvido com ❤️ para proteger brasileiros contra fraudes digitais
        </p>
    </div>
""", unsafe_allow_html=True)

