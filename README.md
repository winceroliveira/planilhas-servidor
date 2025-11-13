# Servidor API de Licenciamento

API Django para gerenciamento e validação de chaves de utilização.

## Configuração

1. Criar ambiente virtual:
```bash
python -m venv venv
```

2. Ativar ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar dependências:
```bash
pip install -r requirements.txt
```

4. Aplicar migrações:
```bash
python manage.py migrate
```

5. Criar superusuário:
```bash
python manage.py createsuperuser
```

## Executar Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: http://127.0.0.1:8000/

## Páginas e Endpoints

### Página Inicial
- **URL:** `/`
- **Método:** GET
- **Descrição:** Página inicial com informações sobre a API e links úteis

### Validar Chave
- **URL:** `/api/validar_chave/`
- **Método:** POST
- **Body (JSON):**
```json
{
  "chave": "uuid-da-chave"
}
```
- **Resposta (válida):**
```json
{
  "status": "valida"
}
```
- **Resposta (inválida):**
```json
{
  "status": "invalida"
}
```

## Webhooks Manus AI

O servidor agora funciona como intermediário para receber webhooks do Manus AI.

### Endpoints Manus AI

- **POST** `/api/manus/webhook/` - Recebe notificações do Manus AI
- **GET** `/api/manus/task/<task_id>/` - Verifica status de uma task
- **POST** `/api/manus/registrar/` - Registra uma task criada

Veja `WEBHOOKS_MANUS_AI.md` para mais detalhes.

## Painel Administrativo

Acesse http://127.0.0.1:8000/admin/ para:
- Criar novas chaves de utilização
- Visualizar chaves existentes
- Gerenciar status das chaves (Ativa, Inativa, Expirada)
- Ver último uso de cada chave
- **Gerenciar tasks do Manus AI** (novo)

