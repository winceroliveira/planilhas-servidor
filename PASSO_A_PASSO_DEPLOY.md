# 📋 Passo a Passo Completo - Deploy na Vercel

## ✅ Status Atual

- ✅ Código enviado para GitHub:
  - **Programa:** https://github.com/winceroliveira/planilhas-programas.git
  - **Servidor:** https://github.com/winceroliveira/planilhas-servidor.git

## 🚀 Passo a Passo para Deploy na Vercel

### 1️⃣ Criar Migration (Local)

```bash
cd servidor
python manage.py makemigrations
git add chaves/migrations/
git commit -m "Adicionar migration ManusAITask"
git push
```

### 2️⃣ Acessar Vercel

1. Acesse: https://vercel.com
2. Faça login com sua conta GitHub
3. Clique em **"Add New Project"**

### 3️⃣ Importar Repositório

1. Na lista de repositórios, encontre **`planilhas-servidor`**
2. Clique em **"Import"**

### 4️⃣ Configurar Projeto

**Configurações do Projeto:**
- **Framework Preset:** `Other`
- **Root Directory:** `./` (deixe padrão)
- **Build Command:** `pip install -r requirements.txt && python manage.py migrate --noinput`
- **Output Directory:** (deixe vazio)
- **Install Command:** (deixe vazio)

### 5️⃣ Configurar Variáveis de Ambiente

**IMPORTANTE:** Configure ANTES de fazer o deploy!

Clique em **"Environment Variables"** e adicione:

#### Variável 1: SECRET_KEY
```
Name: SECRET_KEY
Value: [GERE UMA NOVA CHAVE - veja abaixo]
Environment: ☑ Production ☑ Preview ☑ Development
```

**Para gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Variável 2: DEBUG
```
Name: DEBUG
Value: False
Environment: ☑ Production ☑ Preview ☑ Development
```

#### Variável 3: ALLOWED_HOSTS
```
Name: ALLOWED_HOSTS
Value: [deixe vazio por enquanto, será preenchido após primeiro deploy]
Environment: ☑ Production ☑ Preview ☑ Development
```

**Após o primeiro deploy**, volte e atualize com:
```
seu-projeto.vercel.app
```

#### Variável 4: MANUS_AI_API_KEY
```
Name: MANUS_AI_API_KEY
Value: sk-6mrwm3G-9Y5Fbsguirsnbom066uPeJ4JX4aYGGVxc4IN9DdQ8uXRsBuCyjJfSxedvM_Nak3K3u310yOfstgBKcrDkDAf
Environment: ☑ Production ☑ Preview ☑ Development
```

### 6️⃣ Fazer Deploy

1. Clique em **"Deploy"**
2. Aguarde o build completar (pode levar 2-5 minutos)
3. Anote a URL gerada: `https://seu-projeto.vercel.app`

### 7️⃣ Atualizar ALLOWED_HOSTS

Após o primeiro deploy:

1. Volte em **Settings > Environment Variables**
2. Edite `ALLOWED_HOSTS`
3. Adicione: `seu-projeto.vercel.app` (substitua pelo seu domínio real)
4. Salve

### 8️⃣ Configurar Webhook do Manus AI

1. Acesse: https://open.manus.ai/docs/webhooks
2. Registre webhook apontando para:
   ```
   https://seu-projeto.vercel.app/api/manus/webhook/
   ```

### 9️⃣ Atualizar Programa Desktop

No arquivo `programa/config.ini`, atualize:

```ini
[DEFAULT]
api_url = https://seu-projeto.vercel.app/api/validar_chave/
```

## ⚠️ IMPORTANTE: Banco de Dados

A Vercel é serverless e **SQLite não funciona** em produção. Você precisa de um banco PostgreSQL.

### Opção 1: Vercel Postgres (Recomendado)

1. No dashboard da Vercel, vá em **Storage**
2. Clique em **"Create Database"**
3. Selecione **Postgres**
4. Copie a `DATABASE_URL` gerada
5. Adicione como variável de ambiente:
   ```
   Name: DATABASE_URL
   Value: [URL gerada pela Vercel]
   ```

### Opção 2: Banco Externo (Railway, Supabase, etc)

1. Crie um banco PostgreSQL em:
   - Railway: https://railway.app
   - Supabase: https://supabase.com
   - Render: https://render.com

2. Copie a connection string
3. Adicione como variável de ambiente `DATABASE_URL`

## 🔍 Verificar se Funcionou

1. Acesse: `https://seu-projeto.vercel.app`
2. Deve aparecer a página inicial da API
3. Teste: `https://seu-projeto.vercel.app/api/validar_chave/`
4. Verifique logs no dashboard da Vercel

## 📝 Checklist Final

- [ ] Migration criada e commitada
- [ ] Projeto importado na Vercel
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] ALLOWED_HOSTS atualizado com domínio da Vercel
- [ ] Banco de dados PostgreSQL configurado
- [ ] Webhook do Manus AI configurado
- [ ] Programa desktop atualizado com nova URL

## 🆘 Problemas Comuns

### Erro: "Module not found"
- Verifique se `requirements.txt` está completo
- Veja os logs do build na Vercel

### Erro: "Database locked"
- SQLite não funciona na Vercel
- Configure PostgreSQL (veja acima)

### Erro: "ALLOWED_HOSTS"
- Adicione o domínio `.vercel.app` nas variáveis de ambiente
- Formato: `seu-projeto.vercel.app`

### Webhooks não funcionam
- Verifique se a URL está correta
- Certifique-se que o servidor está acessível publicamente
- Veja os logs na Vercel

## 📚 Documentação Adicional

- Guia completo: `servidor/DEPLOY_VERCEL.md`
- Webhooks: `servidor/WEBHOOKS_MANUS_AI.md`
- README do servidor: `servidor/README.md`

