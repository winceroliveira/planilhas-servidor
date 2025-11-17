# 🚀 Executar Migrations na Vercel - AGORA

## ⚠️ Problema Identificado

O `buildCommand` no `vercel.json` **não é executado** quando você usa `builds` na configuração. Por isso, as migrations não rodaram automaticamente durante o build.

## ✅ Solução: Executar via Endpoint

O endpoint temporário de migrations já está configurado e deployado. Siga os passos abaixo:

### Passo 1: Descobrir a URL do seu Projeto

1. Acesse o dashboard da Vercel: https://vercel.com
2. Vá em **Deployments**
3. Clique no último deploy
4. Copie a URL (exemplo: `https://planilhas-servidor.vercel.app`)

### Passo 2: Executar Migrations

**Opção A - Via PowerShell (Windows - Recomendado):**

```powershell
# Substitua pela URL real do seu projeto
$url = "https://planilhas-servidor.vercel.app"
Invoke-WebRequest -Uri "$url/api/migrate/" -Method POST
```

**Ou use o script criado:**

```powershell
cd servidor
.\executar_migrations_vercel.ps1 -UrlProjeto "https://planilhas-servidor.vercel.app"
```

**Opção B - Via Navegador (não funciona - precisa ser POST):**
- Use Postman, Insomnia ou PowerShell

**Opção C - Via curl (se tiver):**

```bash
curl -X POST https://planilhas-servidor.vercel.app/api/migrate/
```

### Resposta Esperada:

```json
{
  "status": "success",
  "message": "Migrations executadas com sucesso!"
}
```

### Se der erro:

```json
{
  "status": "error",
  "message": "mensagem de erro aqui"
}
```

## ✅ Passo 3: Verificar se Funcionou

### 1. Verificar no Admin do Django:

Acesse: `https://seu-projeto.vercel.app/admin/`

- Faça login
- Verifique se aparece "Manus AI Tasks" no menu

### 2. Testar API:

```powershell
# Testar endpoint de validação
Invoke-WebRequest -Uri "https://seu-projeto.vercel.app/api/validar_chave/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"chave": "teste"}'
```

### 3. Verificar Logs na Vercel:

- Dashboard → Deployments → Último deploy → Logs
- Procure por mensagens de erro relacionadas ao banco de dados

## ⚠️ IMPORTANTE: Remover Endpoint Após Usar

Por segurança, **remova o endpoint** após executar as migrations:

1. Edite `servidor/chaves/urls.py`
2. Remova ou comente a linha:
   ```python
   path('api/migrate/', migrations_view.executar_migrations, name='executar_migrations'),
   ```
3. Remova o import:
   ```python
   from . import migrations_view
   ```
4. Faça commit e push:
   ```bash
   git add chaves/urls.py
   git commit -m "Remover endpoint temporário de migrations"
   git push
   ```

## 🔧 Solução Permanente (Opcional)

Se quiser que as migrations executem automaticamente no build, você pode:

1. **Remover `builds` do `vercel.json`** e usar apenas `buildCommand`
2. **Ou criar um script de inicialização** que executa migrations na primeira requisição

Mas por enquanto, usar o endpoint é a solução mais rápida!

---

**Precisa de ajuda?** Execute o comando e me envie a resposta!

