# 🔄 Como Executar Migrations na Vercel

## ✅ Método 1: Endpoint Temporário (Mais Fácil)

Criei um endpoint temporário que você pode chamar uma vez para executar as migrations.

### Passo 1: Fazer Deploy do Endpoint

O endpoint já está no código. Faça commit e push:

```bash
cd servidor
git add .
git commit -m "Adicionar endpoint temporário para migrations"
git push
```

Aguarde o deploy na Vercel (1-2 minutos).

### Passo 2: Executar Migrations

Após o deploy, acesse a URL do seu projeto e chame o endpoint:

**Opção A - Via Navegador (mais fácil):**
```
https://planilhas-servidor.vercel.app/api/migrate/
```

Mas precisa ser POST. Use a **Opção B**.

**Opção B - Via PowerShell (Windows):**
```powershell
Invoke-WebRequest -Uri "https://planilhas-servidor.vercel.app/api/migrate/" -Method POST
```

**Opção C - Via curl (se tiver):**
```bash
curl -X POST https://planilhas-servidor.vercel.app/api/migrate/
```

**Opção D - Via Postman ou Insomnia:**
- Método: POST
- URL: `https://planilhas-servidor.vercel.app/api/migrate/`

### Resposta Esperada:

```json
{
  "status": "success",
  "message": "Migrations executadas com sucesso!"
}
```

### ⚠️ IMPORTANTE: Remover Endpoint Após Usar

Após executar as migrations com sucesso, **REMOVA O ENDPOINT** por segurança:

1. Edite `servidor/chaves/urls.py`
2. Remova a linha:
   ```python
   path('api/migrate/', migrations_view.executar_migrations, name='executar_migrations'),
   ```
3. Delete o arquivo `servidor/chaves/migrations_view.py`
4. Faça commit e push:
   ```bash
   git add .
   git commit -m "Remover endpoint temporário de migrations"
   git push
   ```

---

## 🔧 Método 2: Via Vercel CLI (Alternativa)

Se preferir usar a CLI:

### 1. Instalar Vercel CLI:
```bash
npm i -g vercel
```

### 2. Login:
```bash
vercel login
```

### 3. No diretório do servidor:
```bash
cd servidor
vercel link  # Conectar ao projeto existente
```

### 4. Executar migrations:
```bash
vercel env pull .env.local  # Baixar variáveis de ambiente
python manage.py migrate --noinput
```

**Nota:** Este método requer que você tenha o banco de dados acessível localmente, o que pode não ser o caso se estiver usando Vercel Postgres.

---

## 🗄️ Método 3: Via Build Command (Já Configurado)

O `vercel.json` já está configurado para executar migrations durante o build:

```json
"buildCommand": "pip install -r requirements.txt && python manage.py migrate --noinput"
```

**Problema:** Isso só funciona se:
- O banco de dados já estiver configurado
- A variável `DATABASE_URL` estiver definida

Se você ainda não configurou o PostgreSQL, as migrations falharão silenciosamente durante o build.

---

## ✅ Verificar se Funcionou

Após executar as migrations, verifique:

1. **Acesse o admin do Django:**
   ```
   https://planilhas-servidor.vercel.app/admin/
   ```

2. **Verifique se o modelo `ManusAITask` aparece:**
   - Faça login no admin
   - Procure por "Manus AI Tasks" no menu

3. **Ou teste criando uma task via API:**
   ```bash
   curl -X POST https://planilhas-servidor.vercel.app/api/manus/registrar/ \
     -H "Content-Type: application/json" \
     -d '{"task_id": "test-123", "task_title": "Teste"}'
   ```

---

## 🆘 Problemas Comuns

### Erro: "no such table: chaves_manusaitask"
- As migrations não foram executadas
- Use o Método 1 (endpoint temporário)

### Erro: "Database locked"
- Você está usando SQLite (não funciona na Vercel)
- Configure PostgreSQL (veja `DEPLOY_VERCEL.md`)

### Erro: "DATABASE_URL not found"
- Configure a variável de ambiente `DATABASE_URL` na Vercel
- Use Vercel Postgres ou outro serviço de PostgreSQL

---

## 📝 Checklist

- [ ] Endpoint temporário deployado
- [ ] Migrations executadas via endpoint
- [ ] Verificado que funcionou (admin ou API)
- [ ] Endpoint removido do código
- [ ] Commit e push da remoção

