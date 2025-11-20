# 🛡️ Detecta Golpe

Projeto desenvolvido para a disciplina de Engenharia de Machine Learning da FATEC

## 📋 Sobre o Projeto

**Detecta Golpe** é uma aplicação web que utiliza inteligência artificial (Google Gemini) para analisar mensagens suspeitas e identificar possíveis golpes, fraudes e tentativas de phishing.

## 🚀 Como Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure a API Key

#### Opção A: Usando Secrets (Recomendado) 🔒

1. Obtenha sua API Key gratuita do Google AI Studio:
   - Acesse: https://aistudio.google.com/app/apikey
   - Crie uma nova chave

2. Edite o arquivo `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "sua-api-key-aqui"
   ```

3. **IMPORTANTE**: O arquivo `secrets.toml` já está no `.gitignore` e não será commitado

#### Opção B: Inserir Manualmente

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

- ✅ Análise inteligente de mensagens com IA
- ✅ Classificação de nível de risco (Baixo, Médio, Alto)
- ✅ Recomendações personalizadas
- ✅ Dicas de segurança
- ✅ Interface amigável e intuitiva
- ✅ Suporte para múltiplas plataformas (WhatsApp, SMS, E-mail, etc.)

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para aplicações web
- **Google Gemini AI**: Modelo de linguagem para análise
- **Python**: Linguagem de programação

## 📝 Deploy no Streamlit Cloud

Para fazer deploy no Streamlit Cloud:

1. Faça push do código (sem o `secrets.toml`)
2. No painel do Streamlit Cloud, adicione os secrets:
   - Vá em "Settings" > "Secrets"
   - Cole o conteúdo do seu `secrets.toml`

## 🔧 Solução de Problemas

Se encontrar erros como "404 model not found" ou problemas com a API:

1. **Gere uma NOVA API Key** em: https://aistudio.google.com/app/apikey
2. Atualize o arquivo `.streamlit/secrets.toml`
3. Reinicie a aplicação

📚 **Guia completo:** Veja o arquivo [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluções detalhadas

## 🤖 Modelos de IA Utilizados

O app detecta automaticamente o melhor modelo disponível:
- ⚡ **Gemini 1.5 Flash** (preferencial - rápido e poderoso)
- 🖼️ **Gemini Pro Vision** (para imagens)
- 📝 **Gemini Pro** (padrão)

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
