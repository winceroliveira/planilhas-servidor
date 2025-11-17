# 🔧 Configurar Variáveis de Ambiente na Vercel

## 📋 Variáveis do Supabase

Baseado nas variáveis que o Supabase forneceu, você precisa configurar na Vercel:

### ✅ Variáveis Obrigatórias

#### 1. DATABASE_URL (ou POSTGRES_URL)
- **Name:** `DATABASE_URL`
- **Value:** Use o valor de `POSTGRES_URL` do Supabase:
  ```
  postgres://postgres.rzttwnmrfikpevxxulaw:AO0kiugJtl4W4Wg5@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x
  ```
- **Environment:** ☑ Production ☑ Preview ☑ Development

**OU** (alternativa - o código aceita ambas):
- **Name:** `POSTGRES_URL`
- **Value:** (mesmo valor acima)

#### 2. SECRET_KEY
- **Name:** `SECRET_KEY`
- **Value:** Gere uma nova chave (veja abaixo)
- **Environment:** ☑ Production ☑ Preview ☑ Development

**Como gerar:**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 3. DEBUG
- **Name:** `DEBUG`
- **Value:** `False`
- **Environment:** ☑ Production ☑ Preview ☑ Development

#### 4. ALLOWED_HOSTS
- **Name:** `ALLOWED_HOSTS`
- **Value:** `planilhas-servidor.vercel.app`
- **Environment:** ☑ Production ☑ Preview ☑ Development

#### 5. MANUS_AI_API_KEY
- **Name:** `MANUS_AI_API_KEY`
- **Value:** `sk-6mrwm3G-9Y5Fbsguirsnbom066uPeJ4JX4aYGGVxc4IN9DdQ8uXRsBuCyjJfSxedvM_Nak3K3u310yOfstgBKcrDkDAf`
- **Environment:** ☑ Production ☑ Preview ☑ Development

### 📝 Variáveis Opcionais (do Supabase)

Estas não são necessárias para o Django funcionar, mas podem ser úteis:

- `SUPABASE_URL` - URL da API do Supabase
- `SUPABASE_ANON_KEY` - Chave anônima do Supabase
- `SUPABASE_SERVICE_ROLE_KEY` - Chave de serviço do Supabase

## 🚀 Passo a Passo na Vercel

### 1. Acessar Dashboard

1. Acesse: https://vercel.com
2. Faça login
3. Selecione o projeto **planilhas-servidor**

### 2. Adicionar Variáveis

1. Vá em **Settings** → **Environment Variables**
2. Para cada variável obrigatória:
   - Clique em **"Add New"**
   - Preencha Name e Value
   - Marque os ambientes (Production, Preview, Development)
   - Clique em **"Save"**

### 3. Fazer Redeploy

Após adicionar todas as variáveis:

1. Vá em **Deployments**
2. Clique nos três pontos (...) do último deploy
3. Selecione **"Redeploy"**
4. Aguarde o deploy completar (2-5 minutos)

### 4. Verificar se Funcionou

Após o redeploy, teste:

```powershell
cd servidor
.\executar_migrations_vercel.ps1 -UrlProjeto "https://planilhas-servidor.vercel.app"
```

## ⚠️ Importante

- **NÃO compartilhe** as variáveis publicamente
- **NÃO commite** variáveis de ambiente no Git
- Use valores diferentes para produção e desenvolvimento
- A `SECRET_KEY` deve ser única e segura

## 🔍 Verificar Variáveis Configuradas

Na Vercel, você pode ver todas as variáveis em:
**Settings** → **Environment Variables**

Certifique-se de que todas as 5 variáveis obrigatórias estão configuradas!

