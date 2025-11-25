# 🛡️ Detecta Golpe

Aplicação web que usa IA (Google Gemini) para identificar golpes e fraudes em mensagens.

## 🚀 Como Usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Obter API Key do Google Gemini (Gratuita)

1. Acesse: https://aistudio.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada

### 3. Configurar API Key

**Opção A - Streamlit Secrets (Recomendado para deploy):**

Crie o arquivo `.streamlit/secrets.toml`:

```toml
GOOGLE_API_KEY = "sua-chave-aqui"
```

**Opção B - Manual:**

Cole a API Key diretamente na interface do app.

### 4. Executar

```bash
streamlit run app.py
```

## 📋 Funcionalidades

- ✅ Análise de mensagens suspeitas com IA
- ✅ Suporte a imagens (screenshots, prints)
- ✅ Verificação automática de URLs
- ✅ 3 níveis de análise (Padrão, Rigoroso, Máximo)
- ✅ Relatório completo exportável

## 🔧 Tecnologias

- Python 3.8+
- Streamlit
- Google Gemini 2.5 Flash (Gratuito)

## 📝 Estrutura do Projeto

```
Detecta-golpe/
├── app.py              # Aplicação principal
├── requirements.txt     # Dependências Python
├── README.md           # Documentação
└── .gitignore          # Arquivos ignorados pelo Git
```

## ⚠️ Importante

- **NUNCA** commite sua API Key no Git
- Use apenas o Google Gemini (gratuito) para testes
- DeepSeek e ChatGPT requerem créditos pagos

## 🎓 FATEC

Projeto de Engenharia de Machine Learning
