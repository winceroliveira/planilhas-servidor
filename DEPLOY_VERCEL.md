# 🚀 Guia de Deploy na Vercel

## 📋 Pré-requisitos

1. Conta na Vercel (https://vercel.com)
2. Repositório no GitHub já configurado
3. Vercel CLI instalado (opcional, mas recomendado)

## 🔧 Passo 1: Preparar o Projeto

### 1.1 Criar Migration (se ainda não fez)

```bash
cd servidor
python manage.py makemigrations
```

Isso criará a migration para o modelo `ManusAITask`.

### 1.2 Commit e Push da Migration

```bash
git add chaves/migrations/
git commit -m "Adicionar migration para ManusAITask"
git push
```

## 🌐 Passo 2: Deploy na Vercel

### Opção A: Via Dashboard da Vercel (Recomendado)

1. **Acesse https://vercel.com e faça login**

2. **Clique em "Add New Project"**

3. **Importe o repositório:**
   - Selecione `planilhas-servidor` do GitHub
   - Clique em "Import"

4. **Configure o projeto:**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (deixe padrão)
   - **Build Command:** Deixe vazio (Vercel detecta automaticamente)
   - **Output Directory:** Deixe vazio
   - **Install Command:** `pip install -r requirements.txt`

5. **Configure Variáveis de Ambiente:**
   Clique em "Environment Variables" e adicione:
   
   ```
   SECRET_KEY = sua-chave-secreta-aqui (gere uma nova!)
   DEBUG = False
   ALLOWED_HOSTS = seu-projeto.vercel.app,seu-dominio.com
   MANUS_AI_API_KEY = sk-6mrwm3G-9Y5Fbsguirsnbom066uPeJ4JX4aYGGVxc4IN9DdQ8uXRsBuCyjJfSxedvM_Nak3K3u310yOfstgBKcrDkDAf
   ```

   **Para gerar uma nova SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Clique em "Deploy"**

### Opção B: Via Vercel CLI

1. **Instalar Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login na Vercel:**
   ```bash
   vercel login
   ```

3. **No diretório do servidor:**
   ```bash
   cd servidor
   vercel
   ```

4. **Siga as instruções:**
   - Link to existing project? **N** (primeira vez)
   - Project name: **planilhas-servidor**
   - Directory: **./**
   - Override settings? **N**

5. **Configure variáveis de ambiente:**
   ```bash
   vercel env add SECRET_KEY
   vercel env add DEBUG
   vercel env add ALLOWED_HOSTS
   vercel env add MANUS_AI_API_KEY
   ```

## 🔄 Passo 3: Executar Migrations

Após o deploy, você precisa executar as migrations. A Vercel não executa migrations automaticamente.

### Opção 1: Via Vercel CLI (Recomendado)

```bash
cd servidor
vercel env pull .env.local  # Baixar variáveis de ambiente
vercel --prod  # Fazer deploy de produção
```

Depois, execute migrations via shell da Vercel ou crie um script de build.

### Opção 2: Criar Script de Build

Crie um arquivo `build.sh` na raiz do servidor:

```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py migrate --noinput
```

E configure no `vercel.json`:

```json
{
  "buildCommand": "bash build.sh"
}
```

### Opção 3: Executar Manualmente (Temporário)

Use o shell da Vercel ou crie um endpoint temporário para executar migrations.

## 🔗 Passo 4: Configurar Webhook do Manus AI

Após o deploy, você terá uma URL como: `https://seu-projeto.vercel.app`

1. **Atualize o webhook no Manus AI:**
   - Acesse: https://open.manus.ai/docs/webhooks
   - Registre webhook: `https://seu-projeto.vercel.app/api/manus/webhook/`

2. **Atualize o programa desktop:**
   - No `config.ini`, atualize a `api_url` para:
   ```
   api_url = https://seu-projeto.vercel.app/api/validar_chave/
   ```

## ⚙️ Passo 5: Configurações Adicionais

### 5.1 Banco de Dados

A Vercel não suporta SQLite persistente. Para produção, você precisará:

**Opção 1: Usar PostgreSQL (Recomendado)**
- Use Vercel Postgres ou outro serviço (Railway, Supabase)
- Atualize `settings.py` para usar PostgreSQL

**Opção 2: Usar Vercel KV (Redis)**
- Para armazenamento temporário de tasks

**Opção 3: Usar banco externo**
- Railway, Render, ou Supabase oferecem PostgreSQL gratuito

### 5.2 Atualizar settings.py para PostgreSQL

Se usar PostgreSQL, adicione ao `settings.py`:

```python
import os
import dj_database_url

# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

E adicione ao `requirements.txt`:
```
dj-database-url>=2.1.0
psycopg2-binary>=2.9.9
```

## 📝 Passo 6: Verificar Deploy

1. **Acesse a URL do projeto:** `https://seu-projeto.vercel.app`
2. **Teste o endpoint:** `https://seu-projeto.vercel.app/api/validar_chave/`
3. **Verifique logs:** No dashboard da Vercel, vá em "Logs"

## 🔍 Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Certifique-se que o `vercel.json` está configurado corretamente

### Erro: "Database locked" ou problemas com SQLite
- SQLite não funciona bem na Vercel (serverless)
- Use PostgreSQL ou outro banco de dados

### Erro: "ALLOWED_HOSTS"
- Adicione o domínio da Vercel nas variáveis de ambiente
- Formato: `seu-projeto.vercel.app,seu-dominio.com`

### Webhooks não funcionam
- Verifique se a URL do webhook está correta
- Certifique-se que o servidor está acessível publicamente
- Verifique os logs da Vercel para ver se o webhook está chegando

## 📚 Recursos Adicionais

- [Documentação Vercel Python](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Django na Vercel](https://vercel.com/guides/deploying-django-to-vercel)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

## ⚠️ Nota Importante

A Vercel é uma plataforma serverless, o que significa:
- Cada requisição pode ser em uma instância diferente
- SQLite não funciona bem (use PostgreSQL)
- Migrations precisam ser executadas manualmente ou via script
- Arquivos temporários não persistem entre requisições

Para uma solução mais adequada para Django, considere:
- **Railway** (https://railway.app) - Melhor para Django
- **Render** (https://render.com) - Suporta Django nativamente
- **Heroku** (https://heroku.com) - Clássico para Django

