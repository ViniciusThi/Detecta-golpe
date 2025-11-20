import streamlit as st
import google.generativeai as genai
import re
from urllib.parse import urlparse
from PIL import Image
import io

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
    **Detecta Golpe** usa IA avançada (Google Gemini Pro) para análise 
    profunda de mensagens e imagens suspeitas.
    
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
    st.markdown("**⚙️ Modo de Análise**")
    
    modo_analise = st.radio(
        "Escolha o rigor:",
        ["🟢 Padrão", "🟡 Rigoroso", "🔴 Máximo"],
        help="Quanto mais rigoroso, mais detalhada e crítica será a análise"
    )
    
    st.markdown("---")
    st.markdown("**⚙️ Configuração da API**")
    
    # Tentar obter API Key dos secrets
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key configurada!")
        st.caption("Usando Gemini 1.5 Pro")
    except (KeyError, FileNotFoundError):
        st.warning("⚠️ API Key não encontrada")
        st.info("Configure `.streamlit/secrets.toml`")
        
        # Fallback: permitir inserir manualmente
        api_key = st.text_input(
            "Ou insira manualmente:",
            type="password",
            help="https://aistudio.google.com/app/apikey"
        )
        
        if api_key:
            st.success("✅ API Key configurada!")
    
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

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎯 NÍVEL DE RISCO: [BAIXO | MÉDIO | ALTO | CRÍTICO]
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    📊 SCORE DE CONFIANÇA: [0-100]% (0 = Golpe Certeza | 100 = Legítimo)
    
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

# Função para analisar a mensagem com Gemini (com suporte a imagens)
def analisar_mensagem(mensagem, origem, api_key, modo_analise, imagem=None, verificar_urls=True):
    try:
        # Configurar a API
        genai.configure(api_key=api_key)
        
        # Usar modelo PRO para análise mais rigorosa
        model = genai.GenerativeModel('gemini-1.5-pro')
        
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
        
        return response.text
    except Exception as e:
        return f"❌ Erro ao analisar: {str(e)}\n\nVerifique se sua API Key está correta e se o modelo Gemini 1.5 Pro está disponível."

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
        
        status_text.text("🧠 Processando com IA (Gemini Pro)...")
        progress_bar.progress(60)
        
        # Realizar análise
        resultado = analisar_mensagem(mensagem, origem, api_key, modo_analise, imagem, verificar_urls)
        
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
        
        # Extrair e exibir nível de risco
        resultado_lower = resultado.lower()
        
        # Buscar por diferentes padrões de risco
        if "crítico" in resultado_lower[:500]:
            st.markdown('<div class="risk-badge risk-high">🚨 RISCO CRÍTICO</div>', unsafe_allow_html=True)
            st.markdown('<div class="danger-box"><h3>🚨 ALERTA MÁXIMO</h3><p>Esta mensagem apresenta <strong>EVIDÊNCIAS CLARAS DE GOLPE/FRAUDE</strong>. NÃO interaja com ela!</p></div>', unsafe_allow_html=True)
        elif "alto" in resultado_lower[:500]:
            st.markdown('<div class="risk-badge risk-high">🔴 RISCO ALTO</div>', unsafe_allow_html=True)
            st.markdown('<div class="danger-box"><h3>⚠️ PERIGO</h3><p>Esta mensagem apresenta <strong>fortes indícios de golpe</strong>. Não clique em links e não forneça dados!</p></div>', unsafe_allow_html=True)
        elif "médio" in resultado_lower[:500]:
            st.markdown('<div class="risk-badge risk-medium">🟡 RISCO MÉDIO</div>', unsafe_allow_html=True)
            st.markdown('<div class="warning-box"><h3>⚠️ ATENÇÃO</h3><p>Esta mensagem apresenta <strong>elementos suspeitos</strong>. Proceda com cautela!</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-badge risk-low">🟢 RISCO BAIXO</div>', unsafe_allow_html=True)
            st.info("✅ Análise indica menor probabilidade de golpe, mas mantenha sempre a vigilância!")
        
        # Exibir resultado completo formatado
        st.markdown("---")
        st.markdown(resultado)
        
        # Informações adicionais
        st.markdown("---")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.metric("🎯 Modo de Análise", modo_analise)
        
        with col_info2:
            st.metric("📱 Origem", origem)
        
        with col_info3:
            tipo_entrada = "Texto" if mensagem and not imagem else "Imagem" if imagem and not mensagem else "Texto + Imagem"
            st.metric("📄 Tipo de Entrada", tipo_entrada)
        
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
        <p><strong>Powered by:</strong> Google Gemini 1.5 Pro | Streamlit | Python</p>
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

