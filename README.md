# 🛡️ Detecta Golpe

## O que é?

**Detecta Golpe** é uma aplicação web que usa Inteligência Artificial (Google Gemini) para identificar golpes, fraudes e tentativas de phishing em mensagens recebidas por WhatsApp, SMS, e-mail e outras plataformas.

## Para que serve?

O sistema analisa mensagens suspeitas e fornece:
- 🎯 Nível de risco (BAIXO, MÉDIO, ALTO, CRÍTICO)
- 🔍 Análise técnica detalhada
- ⚠️ Identificação de red flags e padrões de golpe
- 🛡️ Recomendações de segurança
- 📊 Relatório completo exportável

**Problema que resolve:** Milhões de pessoas recebem mensagens fraudulentas diariamente. Este app ajuda a identificar golpes antes que causem prejuízos financeiros ou roubo de dados.

## Como usar?

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

### 5. Usar o app

1. Cole o texto suspeito OU faça upload de uma imagem
2. Selecione a origem da mensagem (WhatsApp, SMS, etc.)
3. Escolha o modo de análise (Padrão, Rigoroso ou Máximo)
4. Clique em "ANALISAR"
5. Leia o relatório completo com nível de risco e recomendações

---

**Projeto FATEC - Engenharia de Machine Learning**
