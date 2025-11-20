# 🧪 Exemplos para Testar o Detecta Golpe

Use estes exemplos para testar as diferentes funcionalidades e níveis de análise do app.

## 🔴 Exemplo 1: Golpe Clássico de WhatsApp

**Origem:** WhatsApp  
**Modo:** 🔴 Máximo

```
URGENTE! Seu pacote dos Correios está retido por falta de pagamento de R$ 2,50. 
Clique no link para regularizar agora ou seu pedido será devolvido em 24h:

http://correios-brasil-rastreio.site/liberar/pacote?id=BR123456789

Acesse já e pague a taxa! Não perca seu pedido!
```

**Expectativa:** RISCO CRÍTICO/ALTO

---

## 🟡 Exemplo 2: Mensagem Suspeita Moderada

**Origem:** E-mail  
**Modo:** 🟡 Rigoroso

```
Olá,

Detectamos uma atividade incomum em sua conta Netflix. 
Para manter seu acesso ativo, precisamos que você confirme seus dados de pagamento.

Por favor, acesse: netflix-verificacao-brasil.com/conta

Atenciosamente,
Equipe Netflix
```

**Expectativa:** RISCO MÉDIO/ALTO

---

## 🟢 Exemplo 3: Mensagem Legítima

**Origem:** SMS  
**Modo:** 🟢 Padrão

```
Banco Itaú informa: Compra aprovada no valor de R$ 129,90 em MAGAZINE LUIZA em 20/11/2024 às 14:32. 
Em caso de dúvidas, ligue *611 do seu celular.
```

**Expectativa:** RISCO BAIXO

---

## 🚨 Exemplo 4: Golpe Sofisticado

**Origem:** Instagram  
**Modo:** 🔴 Máximo

```
🎉 PARABÉNS! 🎉

Você foi selecionado para receber R$ 5.000,00 do programa Auxílio Brasil!

Para receber, você precisa:
1. Clicar no link: bit.ly/auxilio5mil
2. Cadastrar seus dados (CPF, nome completo, número do cartão)
3. Pagar taxa administrativa de R$ 45,00

⏰ Você tem 2 horas para confirmar ou perderá o benefício!

✅ Aprovado pelo Governo Federal
✅ Programa 100% legítimo
✅ Já ajudamos 50.000 brasileiros

CLIQUE AQUI AGORA: bit.ly/auxilio5mil
```

**Expectativa:** RISCO CRÍTICO

---

## 💳 Exemplo 5: Phishing Bancário

**Origem:** E-mail  
**Modo:** 🔴 Máximo

```
Prezado Cliente,

Identificamos uma tentativa de acesso não autorizado em sua conta Banco do Brasil.

Por segurança, sua conta foi temporariamente bloqueada.

Para desbloquear, acesse imediatamente:
https://bb-com-br-seguranca.online/desbloqueio

Você precisará informar:
- Número da agência e conta
- Senha completa do internet banking
- Código do cartão (verso)

ATENÇÃO: Após 6 horas sem confirmação, sua conta será encerrada permanentemente.

Banco do Brasil
Segurança Digital
```

**Expectativa:** RISCO CRÍTICO

---

## 📱 Exemplo 6: Golpe de Clonagem

**Origem:** WhatsApp  
**Modo:** 🟡 Rigoroso

```
Oi mãe, sou eu! Meu celular caiu na água e estou usando o telefone de um amigo.

Preciso URGENTE que você faça um PIX pra mim. É uma emergência!

Chave PIX: 11 98765-4321 (CPF: 123.456.789-00)
Valor: R$ 800,00

Por favor mãe, é urgente! Meu amigo precisa desse dinheiro agora. 
Te explico depois!

Faz pra mim? 🙏
```

**Expectativa:** RISCO ALTO/CRÍTICO

---

## ✅ Exemplo 7: Notificação Legítima

**Origem:** E-mail  
**Modo:** 🟢 Padrão

```
Olá João,

Sua compra foi confirmada!

Pedido #123456
Item: Notebook Dell Inspiron
Valor: R$ 3.299,00
Previsão de entrega: 25/11/2024

Você pode acompanhar seu pedido através da sua conta no Mercado Livre.

Link direto (não clique se não reconhece a compra): 
https://www.mercadolivre.com.br/minhas-compras

Equipe Mercado Livre
```

**Expectativa:** RISCO BAIXO

---

## 🎯 Dicas para Testes

1. **Teste os 3 Modos de Análise:**
   - 🟢 Padrão: Análise equilibrada
   - 🟡 Rigoroso: Mais crítico e detalhado
   - 🔴 Máximo: Análise forense completa

2. **Teste com Imagens:**
   - Tire prints de mensagens reais
   - Use prints de e-mails
   - Teste com capturas de tela de SMS

3. **Combine Texto + Imagem:**
   - Adicione contexto textual à imagem
   - Teste a análise multimodal

4. **Verifique a Análise de URLs:**
   - Marque/desmarque a opção "Análise de URLs"
   - Veja como o app detecta padrões suspeitos

---

## 📊 O Que Observar nos Resultados

✅ **Boa Análise Inclui:**
- Score de confiança (0-100%)
- Nível de risco claro
- Análise técnica detalhada
- Indicadores específicos de fraude
- Ações práticas recomendadas
- Análise de URLs (quando aplicável)
- Veredicto final profissional

---

## ⚠️ Importante

- Estes são **exemplos fictícios** para teste
- **NUNCA** clique em links de mensagens suspeitas reais
- Use o app para **educar-se** sobre golpes
- Em caso de dúvida real, **contate a empresa diretamente**

---

**Bons testes! 🛡️**

