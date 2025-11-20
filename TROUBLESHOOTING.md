# 🔧 Guia de Solução de Problemas

## ❌ Erro: "404 models/gemini-1.5-pro is not found"

### Causa
Este erro ocorre quando o modelo Gemini especificado não está disponível para sua API Key.

### ✅ Solução RÁPIDA

O código já foi atualizado para usar automaticamente modelos disponíveis! Basta **gerar uma nova API Key**:

1. **Acesse:** https://aistudio.google.com/app/apikey
2. **Crie uma nova API Key** (botão "Create API Key")
3. **Copie a chave** gerada
4. **Atualize o arquivo** `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "sua-nova-chave-aqui"
   ```
5. **Reinicie o app** (Ctrl+C e `streamlit run app.py`)

---

## 🤖 Modelos Suportados

O app agora detecta automaticamente qual modelo está disponível na sua API Key e usa:

1. **gemini-1.5-flash** (preferencial) ⚡
   - Mais rápido e moderno
   - Suporta texto e imagem
   - Recomendado!

2. **gemini-pro-vision** 🖼️
   - Para análise de imagens
   - Ótimo para screenshots

3. **gemini-pro** 📝
   - Modelo padrão
   - Apenas texto

---

## 🔑 Problemas com API Key

### "API Key não encontrada nos secrets"

**Solução:**
1. Verifique se o arquivo existe: `Detecta-golpe/.streamlit/secrets.toml`
2. Certifique-se que o formato está correto:
   ```toml
   GOOGLE_API_KEY = "AIzaSyD..."
   ```
3. Não use aspas simples, apenas aspas duplas
4. Reinicie o Streamlit após modificar

### "Invalid API Key"

**Solução:**
1. Gere uma NOVA API Key em: https://aistudio.google.com/app/apikey
2. Copie a chave COMPLETA (começa com `AIzaSy...`)
3. Cole no `secrets.toml`
4. Salve o arquivo
5. Reinicie a aplicação

---

## 🚫 Erro de Quota/Limite

### "quota exceeded" ou "rate limit"

**Causas:**
- Muitas requisições em pouco tempo
- Limite diário atingido (API gratuita)

**Soluções:**
1. **Aguarde 1-2 minutos** entre análises
2. **Use o modo 🟢 Padrão** (consome menos recursos)
3. Se usar muito, considere **criar múltiplas API Keys**
4. Verifique limites em: https://aistudio.google.com/

---

## 🖼️ Problemas com Análise de Imagens

### "Image not supported"

**Solução:**
1. Use formatos: PNG, JPG, JPEG, WEBP
2. Tamanho máximo recomendado: 5MB
3. Certifique-se que a imagem não está corrompida
4. Tente converter a imagem para PNG

### "Cannot process image"

**Solução:**
1. O modelo `gemini-pro` padrão NÃO suporta imagens
2. Gere uma API Key nova (terá acesso ao gemini-1.5-flash)
3. O app detectará automaticamente e usará o modelo correto

---

## 🌐 Problemas de Conexão

### "Connection timeout" ou "Network error"

**Soluções:**
1. Verifique sua conexão com a internet
2. Desative VPN/Proxy temporariamente
3. Verifique se o firewall não está bloqueando
4. Tente novamente em alguns minutos

---

## 📦 Problemas de Instalação

### "ModuleNotFoundError: No module named 'PIL'"

**Solução:**
```bash
pip install -r requirements.txt
```

Ou instale individualmente:
```bash
pip install Pillow
pip install google-generativeai
pip install streamlit
```

### Erro ao importar `google.generativeai`

**Solução:**
```bash
pip install --upgrade google-generativeai
```

---

## 🔄 App Não Atualiza Após Mudanças

**Solução:**
1. Pare o Streamlit (Ctrl+C no terminal)
2. Limpe o cache:
   ```bash
   streamlit cache clear
   ```
3. Reinicie:
   ```bash
   streamlit run app.py
   ```

---

## 💡 Dicas de Performance

### App está lento?

1. **Use modo 🟢 Padrão** para análises mais rápidas
2. **Evite imagens muito grandes** (redimensione para max 1920x1080)
3. **Uma análise por vez** - aguarde finalizar antes de nova
4. **Desative análise de URLs** se não precisar

### Análise incompleta?

1. Aguarde! Análise rigorosa pode levar 10-30 segundos
2. Não clique várias vezes no botão "ANALISAR"
3. Se travar, recarregue a página (F5)

---

## 🆘 Ainda com problemas?

### Checklist Final:

- [ ] API Key nova e válida?
- [ ] Arquivo `secrets.toml` no lugar certo?
- [ ] Internet funcionando?
- [ ] Dependências instaladas? (`pip install -r requirements.txt`)
- [ ] Python 3.8+ instalado?
- [ ] Streamlit atualizado? (`pip install --upgrade streamlit`)

### Teste Básico:

Execute este teste no terminal Python:

```python
import google.generativeai as genai

# Substitua pela sua API Key
genai.configure(api_key="SUA_API_KEY_AQUI")

# Listar modelos disponíveis
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)
```

Isso mostrará quais modelos você tem acesso.

---

## 📚 Recursos Adicionais

- **Documentação Gemini:** https://ai.google.dev/docs
- **API Keys:** https://aistudio.google.com/app/apikey
- **Streamlit Docs:** https://docs.streamlit.io
- **Reportar Bug:** [Abra uma issue no GitHub]

---

**💪 Lembre-se:** A maioria dos problemas se resolve com uma API Key nova e fresca!

**🔗 Gere sua API Key:** https://aistudio.google.com/app/apikey

