# 🎯 Próximos Passos Após Criar Banco no Supabase

## ✅ Status Atual
- ✅ Banco de dados criado no Supabase
- ✅ Projeto Django configurado para PostgreSQL

## 📋 Passo 1: Copiar DATABASE_URL do Supabase

1. **Na interface do Supabase**, na seção **"Quickstart"**:
   - Clique em **"Show secret"** (ícone de olho) para revelar os valores
   - Procure pela variável **`POSTGRES_URL`** ou **`DATABASE_URL`**
   - Copie a string completa (começa com `postgresql://...`)

   **Exemplo:**
   ```
   postgresql://postgres.xxxxxxxxxxxxx:senha@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

2. **Alternativa:** Se não encontrar na interface:
   - Vá em **Settings** → **Database**
   - Procure por **"Connection string"** ou **"Connection pooling"**
   - Use a string de conexão do **"Connection pooling"** (recomendado)

## 🔧 Passo 2: Configurar Variável de Ambiente

### Opção A: Se estiver fazendo deploy na Vercel

1. **Acesse o dashboard da Vercel:**
   - Vá em: https://vercel.com
   - Selecione seu projeto

2. **Adicione a variável de ambiente:**
   - Vá em **Settings** → **Environment Variables**
   - Clique em **"Add New"**
   - Configure:
     - **Name:** `DATABASE_URL`
     - **Value:** Cole a string copiada do Supabase
     - **Environment:** ☑ Production ☑ Preview ☑ Development
   - Clique em **"Save"**

3. **Faça um novo deploy:**
   - Vá em **Deployments**
   - Clique nos três pontos (...) do último deploy
   - Selecione **"Redeploy"**
   - Ou faça um novo commit para trigger automático

### Opção B: Se estiver testando localmente

1. **Crie arquivo `.env` na pasta `servidor/`:**

```bash
cd servidor
```

2. **Crie o arquivo `.env`** (se não existir):

```bash
# Windows PowerShell
New-Item -Path .env -ItemType File

# Ou crie manualmente no editor
```

3. **Adicione a DATABASE_URL no arquivo `.env`:**

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/database
```

**⚠️ IMPORTANTE:** Substitua pelos valores reais do seu Supabase!

4. **Instale python-dotenv (se ainda não tiver):**

```bash
pip install python-dotenv
```

5. **Atualize `settings.py` para ler o `.env`:**

O arquivo já está configurado, mas verifique se tem:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Database
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ['DATABASE_URL'])
    }
```

## 🔄 Passo 3: Executar Migrations

### Se estiver na Vercel:

As migrations serão executadas automaticamente durante o build (já configurado no `vercel.json`).

**Ou use o endpoint temporário:**

1. **Acesse o endpoint de migrations:**
   ```
   https://seu-projeto.vercel.app/api/migrate/
   ```
   (Método: POST)

2. **Via PowerShell:**
   ```powershell
   Invoke-WebRequest -Uri "https://seu-projeto.vercel.app/api/migrate/" -Method POST
   ```

3. **⚠️ IMPORTANTE:** Remova o endpoint após usar (por segurança)!

### Se estiver localmente:

```bash
cd servidor

# Ativar venv (se necessário)
# Windows
venv\Scripts\activate

# Executar migrations
python manage.py migrate
```

## ✅ Passo 4: Verificar se Funcionou

### 1. Testar Conexão Localmente

```bash
cd servidor
python manage.py dbshell
```

Se conectar, digite:
```sql
\dt
```

Deve listar as tabelas criadas.

### 2. Verificar no Admin do Django

**Localmente:**
```
http://127.0.0.1:8000/admin/
```

**Na Vercel:**
```
https://seu-projeto.vercel.app/admin/
```

Faça login e verifique se as tabelas aparecem.

### 3. Testar API

**Localmente:**
```bash
curl -X POST http://127.0.0.1:8000/api/validar_chave/ \
  -H "Content-Type: application/json" \
  -d '{"chave": "teste"}'
```

**Na Vercel:**
```bash
curl -X POST https://seu-projeto.vercel.app/api/validar_chave/ \
  -H "Content-Type: application/json" \
  -d '{"chave": "teste"}'
```

## 🔍 Troubleshooting

### Erro: "could not connect to server"
- Verifique se a `DATABASE_URL` está correta
- Confirme que o banco está acessível (não bloqueado por firewall)
- Use a connection string do **"Connection pooling"** (porta 6543) em vez da direta

### Erro: "password authentication failed"
- Verifique se a senha está correta na `DATABASE_URL`
- No Supabase, vá em **Settings** → **Database** → **Reset database password** se necessário

### Erro: "relation does not exist"
- As migrations não foram executadas
- Execute: `python manage.py migrate`

### Erro: "Module not found: dj_database_url"
- Instale: `pip install dj-database-url`
- Ou: `pip install -r requirements.txt`

## 📝 Checklist Final

- [ ] DATABASE_URL copiada do Supabase
- [ ] Variável de ambiente configurada (Vercel ou .env local)
- [ ] Migrations executadas com sucesso
- [ ] Conexão testada e funcionando
- [ ] Admin do Django acessível
- [ ] API respondendo corretamente

## 🎉 Próximo Passo

Após configurar o banco de dados:

1. **Criar superusuário** (se ainda não tiver):
   ```bash
   python manage.py createsuperuser
   ```

2. **Criar chaves de utilização** via admin do Django

3. **Configurar webhook do Manus AI** (se necessário)

4. **Atualizar programa desktop** com a URL da API

---

**Documentação relacionada:**
- `DEPLOY_VERCEL.md` - Guia completo de deploy
- `COMO_EXECUTAR_MIGRATIONS.md` - Detalhes sobre migrations
- `PASSO_A_PASSO_DEPLOY.md` - Passo a passo completo

