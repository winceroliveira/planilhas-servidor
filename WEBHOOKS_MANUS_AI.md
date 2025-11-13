# Webhooks Manus AI - Guia de Uso

## 📋 Visão Geral

O servidor Django agora funciona como intermediário entre o programa desktop e o Manus AI, recebendo webhooks quando tasks completam.

## 🔄 Fluxo de Funcionamento

1. **Programa Desktop cria task no Manus AI**
2. **Programa registra webhook** apontando para o servidor
3. **Programa registra task no servidor** (para rastreamento)
4. **Manus AI processa a task**
5. **Manus AI envia webhook para o servidor** quando completa
6. **Servidor atualiza status da task** no banco de dados
7. **Programa desktop faz polling no servidor** para verificar status
8. **Quando completa, programa baixa o arquivo** automaticamente

## 🚀 Configuração

### 1. Criar Migration

```bash
cd servidor
python manage.py makemigrations
python manage.py migrate
```

### 2. Iniciar Servidor

```bash
python manage.py runserver
```

O servidor deve estar rodando em `http://127.0.0.1:8000`

### 3. Configurar Webhook no Manus AI (Opcional)

O programa desktop tenta registrar o webhook automaticamente, mas você também pode fazer manualmente:

- Acesse: https://open.manus.ai/docs/webhooks
- Registre webhook apontando para: `http://seu-servidor:8000/api/manus/webhook/`

**Nota:** Para produção, você precisará de um servidor público acessível (não localhost).

## 📡 Endpoints Disponíveis

### POST `/api/manus/webhook/`
Recebe notificações do Manus AI quando tasks completam.

**Body (do Manus AI):**
```json
{
  "event_type": "task_stopped",
  "task_detail": {
    "task_id": "...",
    "stop_reason": "finish",
    "attachments": [...]
  }
}
```

### GET `/api/manus/task/<task_id>/`
Verifica status de uma task (usado pelo programa desktop).

**Resposta:**
```json
{
  "task_id": "...",
  "status": "completed",
  "attachments": [...],
  "data_completa": "..."
}
```

### POST `/api/manus/registrar/`
Registra uma task criada (usado pelo programa desktop).

**Body:**
```json
{
  "task_id": "...",
  "task_title": "...",
  "task_url": "..."
}
```

## 🗄️ Modelo de Dados

O modelo `ManusAITask` armazena:
- `task_id`: ID da task
- `status`: pending, running, completed, failed
- `attachments`: Lista de arquivos gerados
- `data_completa`: Quando a task completou

## 🔍 Verificar Tasks no Admin

Acesse `/admin/` e veja a seção "Manus AI Tasks" para monitorar todas as tasks.

## ⚠️ Notas Importantes

1. **Servidor deve estar rodando** quando o programa desktop tentar usar
2. **Para produção**, configure um servidor público ou use ngrok/tunneling
3. **Webhooks do Manus AI** precisam de um endpoint acessível publicamente
4. O programa desktop faz **polling no servidor** (não na API do Manus diretamente)

