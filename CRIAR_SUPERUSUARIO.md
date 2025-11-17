# 👤 Criar Superusuário na Vercel

## ⚠️ Importante

Como a Vercel é serverless, não podemos executar comandos Django diretamente. Por isso, criamos um endpoint temporário para criar o superusuário.

## 🚀 Como Usar

### Passo 1: Aguardar Deploy

O endpoint foi adicionado e está sendo deployado automaticamente. Aguarde 2-5 minutos.

### Passo 2: Executar o Script

Use o script PowerShell criado:

```powershell
cd servidor
.\criar_superusuario_vercel.ps1 `
  -UrlProjeto "https://planilhas-servidor.vercel.app" `
  -Username "admin" `
  -Email "admin@example.com" `
  -Password "sua_senha_segura_aqui"
```

**Exemplo:**
```powershell
.\criar_superusuario_vercel.ps1 `
  -UrlProjeto "https://planilhas-servidor.vercel.app" `
  -Username "admin" `
  -Email "admin@seuemail.com" `
  -Password "MinhaSenh@Segura123"
```

### Passo 3: Verificar se Funcionou

Se der sucesso, você verá:
```json
{
    "status": "success",
    "message": "Superusuário 'admin' criado com sucesso!",
    "username": "admin",
    "email": "admin@example.com",
    "is_superuser": true,
    "is_staff": true
}
```

### Passo 4: Fazer Login no Admin

Acesse: `https://planilhas-servidor.vercel.app/admin/`

Use as credenciais que você criou:
- **Username:** (o que você definiu)
- **Password:** (a senha que você definiu)

### Passo 5: Remover Endpoint (IMPORTANTE!)

Após criar o superusuário, **REMOVA O ENDPOINT** por segurança:

1. Edite `servidor/chaves/urls.py`
2. Remova a linha:
   ```python
   path('api/create-superuser/', create_superuser_view.criar_superusuario, name='criar_superusuario'),
   ```
3. Remova o import:
   ```python
   from . import create_superuser_view
   ```
4. Delete o arquivo `servidor/chaves/create_superuser_view.py`
5. Faça commit e push:
   ```bash
   git add chaves/urls.py
   git rm chaves/create_superuser_view.py
   git commit -m "Remover endpoint temporário de criação de superusuário"
   git push
   ```

## 🔒 Requisitos de Senha

- Mínimo de 8 caracteres
- Recomendado: use letras maiúsculas, minúsculas, números e símbolos

## ⚠️ Segurança

- **NUNCA** compartilhe suas credenciais
- **SEMPRE** remova o endpoint após usar
- Use uma senha forte e única
- Não commite o endpoint no código de produção

## 🆘 Problemas Comuns

### Erro: "Usuário já existe"
- O username já foi criado anteriormente
- Use um username diferente ou remova o usuário existente

### Erro: "Password deve ter pelo menos 8 caracteres"
- Use uma senha com pelo menos 8 caracteres

### Erro 500
- Verifique se o deploy foi concluído
- Verifique os logs na Vercel
- Certifique-se de que as migrations foram executadas

