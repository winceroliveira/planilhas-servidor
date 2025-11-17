# 🔍 Verificar Variáveis de Ambiente na Vercel

## ⚠️ Erro 500 ao Executar Migrations

Se você está recebendo erro 500 ao tentar executar migrations, provavelmente a `DATABASE_URL` não está configurada na Vercel.

## ✅ Como Verificar e Configurar

### 1. Acessar Dashboard da Vercel

1. Acesse: https://vercel.com
2. Faça login
3. Selecione o projeto **planilhas-servidor**

### 2. Verificar Variáveis de Ambiente

1. Vá em **Settings** → **Environment Variables**
2. Verifique se existe a variável **`DATABASE_URL`**
3. Se não existir, você precisa adicioná-la

### 3. Adicionar DATABASE_URL (se necessário)

#### Se você já copiou do Supabase:

1. Clique em **"Add New"**
2. Configure:
   - **Name:** `DATABASE_URL`
   - **Value:** Cole a string do Supabase (começa com `postgresql://...`)
   - **Environment:** ☑ Production ☑ Preview ☑ Development
3. Clique em **"Save"**

#### Se ainda não copiou do Supabase:

1. Acesse o Supabase: https://supabase.com
2. Vá no seu projeto
3. Na seção **"Quickstart"**, clique em **"Show secret"**
4. Copie a variável **`POSTGRES_URL`** (a string completa)
5. Volte na Vercel e adicione como `DATABASE_URL`

### 4. Fazer Redeploy

Após adicionar a variável:

1. Vá em **Deployments**
2. Clique nos três pontos (...) do último deploy
3. Selecione **"Redeploy"**
4. Aguarde o deploy completar (2-5 minutos)

### 5. Executar Migrations Novamente

Após o redeploy, execute novamente:

```powershell
cd servidor
.\executar_migrations_vercel.ps1 -UrlProjeto "https://planilhas-servidor.vercel.app"
```

## 📋 Checklist de Variáveis Necessárias

Verifique se todas estas variáveis estão configuradas:

- [ ] **SECRET_KEY** - Chave secreta do Django
- [ ] **DEBUG** - `False` para produção
- [ ] **ALLOWED_HOSTS** - `planilhas-servidor.vercel.app` (ou seu domínio)
- [ ] **DATABASE_URL** - String de conexão do Supabase ⚠️ **IMPORTANTE**
- [ ] **MANUS_AI_API_KEY** - Chave da API do Manus AI

## 🔍 Verificar Logs na Vercel

Se ainda houver problemas:

1. Vá em **Deployments** → Último deploy
2. Clique em **"View Function Logs"** ou **"Logs"**
3. Procure por erros relacionados a:
   - `DATABASE_URL`
   - `psycopg2`
   - `connection`
   - `migrate`

## 💡 Dica

O endpoint de migrations agora retorna mensagens de erro mais detalhadas. Se ainda der erro 500, verifique a resposta JSON para ver o erro específico.

