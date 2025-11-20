# 🛡️ Detecta Golpe

Projeto desenvolvido para a disciplina de Engenharia de Machine Learning da FATEC

## 📋 Sobre o Projeto

**Detecta Golpe** é uma aplicação web avançada que utiliza inteligência artificial de múltiplas fontes (**Google Gemini** e **DeepSeek**) para analisar mensagens suspeitas e identificar possíveis golpes, fraudes e tentativas de phishing.

## 🚀 Como Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure as API Keys

Você pode usar **uma** ou **ambas** as APIs. O app permite escolher qual usar na interface.

#### 🔷 Google Gemini (Gratuita)

1. Acesse: https://aistudio.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada

#### 🔶 DeepSeek

1. Acesse: https://platform.deepseek.com/
2. Crie uma conta (pode usar GitHub)
3. Vá em "API Keys" e crie uma nova
4. Copie a chave gerada

#### Configurar no Secrets (Recomendado) 🔒

Edite o arquivo `.streamlit/secrets.toml`:

```toml
# Configure UMA ou AMBAS
GOOGLE_API_KEY = "sua-google-api-key-aqui"
DEEPSEEK_API_KEY = "sua-deepseek-api-key-aqui"
```

**IMPORTANTE**: O arquivo `secrets.toml` já está no `.gitignore` e não será commitado

#### Inserir Manualmente

Se você não configurar os secrets, o app permitirá que você insira a API Key manualmente na interface.

### 3. Execute o aplicativo

```bash
streamlit run app.py
```

## 📦 Estrutura do Projeto

```
Detecta-golpe/
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências Python
├── .streamlit/
│   └── secrets.toml           # Configurações secretas (não commitado)
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Este arquivo
```

## 🔒 Segurança

- ⚠️ **NUNCA** commite seu arquivo `secrets.toml` no Git
- ⚠️ **NUNCA** compartilhe sua API Key publicamente
- O arquivo `.gitignore` já está configurado para proteger seus secrets

## 🎯 Funcionalidades

- ✅ **Dual AI**: Escolha entre Google Gemini ou DeepSeek
- ✅ Análise inteligente de mensagens com IA avançada
- ✅ Suporte a **imagens** (screenshots, prints, etc.)
- ✅ Análise **multimodal** (texto + imagem)
- ✅ 3 níveis de rigor (Padrão, Rigoroso, Máximo)
- ✅ Verificação automática de URLs suspeitas
- ✅ Score de confiança (0-100%)
- ✅ Classificação de risco (Baixo, Médio, Alto, Crítico)
- ✅ Recomendações personalizadas e práticas
- ✅ Relatório completo exportável
- ✅ Links para denúncias oficiais
- ✅ Interface moderna e intuitiva
- ✅ Suporte para múltiplas plataformas (WhatsApp, SMS, E-mail, Instagram, etc.)

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para aplicações web
- **Google Gemini AI**: IA multimodal do Google
- **DeepSeek AI**: IA avançada para análise textual
- **Python**: Linguagem de programação
- **Pillow**: Processamento de imagens
- **Requests**: Comunicação com APIs

## 📝 Deploy no Streamlit Cloud

Para fazer deploy no Streamlit Cloud:

1. Faça push do código (sem o `secrets.toml`)
2. No painel do Streamlit Cloud, adicione os secrets:
   - Vá em "Settings" > "Secrets"
   - Cole o conteúdo do seu `secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "sua-chave-google"
   DEEPSEEK_API_KEY = "sua-chave-deepseek"
   ```
3. Configure pelo menos UMA das duas APIs

## 🔧 Solução de Problemas

Se encontrar erros como "404 model not found" ou problemas com a API:

1. **Gere uma NOVA API Key** em: https://aistudio.google.com/app/apikey
2. Atualize o arquivo `.streamlit/secrets.toml`
3. Reinicie a aplicação

📚 **Guia completo:** Veja o arquivo [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluções detalhadas

## 🤖 IAs Disponíveis

### 🔷 Google Gemini
- ⚡ **Gemini 2.5 Flash** (mais rápido e moderno)
- 🖼️ **Gemini Pro Vision** (análise de imagens)
- 📝 **Gemini Pro** (padrão)
- ✅ **Gratuito** com limites generosos
- 🌐 Detecção automática do melhor modelo

### 🔶 DeepSeek
- 🧠 **DeepSeek Chat** (modelo avançado)
- 🔍 Análise profunda e detalhada
- 💬 Ótimo para textos complexos
- 💰 Custo-benefício excelente
- 🖼️ Suporte a imagens (multimodal)

## 🆕 Recursos Avançados

- ✅ Análise multimodal (texto + imagem)
- ✅ 3 níveis de rigor (Padrão, Rigoroso, Máximo)
- ✅ Verificação automática de URLs suspeitas
- ✅ Score de confiança (0-100%)
- ✅ Detecção de padrões de phishing
- ✅ Análise forense detalhada
- ✅ Relatório exportável
- ✅ Links para denúncia oficial

## 👨‍💻 Desenvolvido para FATEC

Projeto de Engenharia de Machine Learning
