from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ChaveDeUtilizacao, ManusAITask
import json


@csrf_exempt
def validar_chave(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        chave_str = data.get('chave', '')
        
        if not chave_str:
            return JsonResponse({'status': 'invalida'}, status=400)
        
        # Buscar a chave no banco
        try:
            chave_obj = ChaveDeUtilizacao.objects.get(chave=chave_str)
        except ChaveDeUtilizacao.DoesNotExist:
            return JsonResponse({'status': 'invalida'})
        
        # Verificar se está ativa
        if chave_obj.status != 'Ativa':
            return JsonResponse({'status': 'invalida'})
        
        # Atualizar último uso
        chave_obj.ultimo_uso = timezone.now()
        chave_obj.save()
        
        return JsonResponse({'status': 'valida'})
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'erro', 'mensagem': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=500)


def index(request):
    """Página inicial com informações da API"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API de Licenciamento - Planilhas</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            .endpoint {
                background-color: #f9f9f9;
                padding: 15px;
                margin: 15px 0;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }
            .endpoint h3 {
                margin-top: 0;
                color: #4CAF50;
            }
            code {
                background-color: #e8e8e8;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            .admin-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
            .admin-link:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 API de Licenciamento</h1>
            <p>Bem-vindo à API de validação de chaves de utilização.</p>
            
            <div class="endpoint">
                <h3>📋 Endpoints Disponíveis</h3>
                <p><strong>POST</strong> <code>/api/validar_chave/</code></p>
                <p>Valida uma chave de acesso.</p>
                <p><strong>Body (JSON):</strong></p>
                <pre style="background-color: #e8e8e8; padding: 10px; border-radius: 4px;">{
  "chave": "uuid-da-chave"
}</pre>
                <p><strong>Resposta (válida):</strong></p>
                <pre style="background-color: #e8e8e8; padding: 10px; border-radius: 4px;">{
  "status": "valida"
}</pre>
                <p><strong>Resposta (inválida):</strong></p>
                <pre style="background-color: #e8e8e8; padding: 10px; border-radius: 4px;">{
  "status": "invalida"
}</pre>
            </div>
            
            <div class="endpoint">
                <h3>⚙️ Painel Administrativo</h3>
                <p>Acesse o painel administrativo para gerenciar chaves de utilização.</p>
                <a href="/admin/" class="admin-link">Acessar Admin</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


@csrf_exempt
def webhook_manus_ai(request):
    """
    Endpoint para receber webhooks do Manus AI
    Conforme documentação: https://open.manus.ai/docs/webhooks
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        event_type = data.get('event_type')
        task_detail = data.get('task_detail', {})
        
        task_id = task_detail.get('task_id')
        if not task_id:
            return JsonResponse({'error': 'task_id missing'}, status=400)
        
        # Buscar ou criar task
        task, created = ManusAITask.objects.get_or_create(
            task_id=task_id,
            defaults={
                'task_title': task_detail.get('task_title', ''),
                'task_url': task_detail.get('task_url', ''),
                'status': 'pending'
            }
        )
        
        # Atualizar dados da task
        if not created:
            task.task_title = task_detail.get('task_title', task.task_title)
            task.task_url = task_detail.get('task_url', task.task_url)
        
        # Processar eventos
        if event_type == 'task_created':
            task.status = 'running'
            task.message = 'Task criada e iniciada'
        
        elif event_type == 'task_stopped':
            stop_reason = task_detail.get('stop_reason', '')
            task.stop_reason = stop_reason
            
            if stop_reason == 'finish':
                task.status = 'completed'
                task.data_completa = timezone.now()
                # Salvar anexos se houver
                attachments = task_detail.get('attachments', [])
                if attachments:
                    task.attachments = attachments
            elif stop_reason == 'ask':
                task.status = 'running'
                task.message = task_detail.get('message', 'Aguardando input do usuário')
            else:
                task.status = 'failed'
                task.message = task_detail.get('message', f'Task parou: {stop_reason}')
        
        task.save()
        
        return JsonResponse({'status': 'ok', 'task_id': task_id}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def verificar_task_manus(request, task_id):
    """
    Endpoint para o programa desktop verificar status de uma task
    GET /api/manus/task/<task_id>/
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        task = ManusAITask.objects.get(task_id=task_id)
        
        response_data = {
            'task_id': task.task_id,
            'status': task.status,
            'task_title': task.task_title,
            'task_url': task.task_url,
            'stop_reason': task.stop_reason,
            'message': task.message,
            'attachments': task.attachments,
            'data_criacao': task.data_criacao.isoformat() if task.data_criacao else None,
            'data_completa': task.data_completa.isoformat() if task.data_completa else None,
        }
        
        return JsonResponse(response_data, status=200)
    
    except ManusAITask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def registrar_task_manus(request):
    """
    Endpoint para registrar uma task criada (chamado pelo programa desktop)
    POST /api/manus/registrar/
    Body: {"task_id": "...", "task_title": "...", "task_url": "..."}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        
        if not task_id:
            return JsonResponse({'error': 'task_id required'}, status=400)
        
        task, created = ManusAITask.objects.get_or_create(
            task_id=task_id,
            defaults={
                'task_title': data.get('task_title', ''),
                'task_url': data.get('task_url', ''),
                'status': 'pending'
            }
        )
        
        if not created:
            # Atualizar se já existir
            task.task_title = data.get('task_title', task.task_title)
            task.task_url = data.get('task_url', task.task_url)
            task.save()
        
        return JsonResponse({
            'status': 'ok',
            'task_id': task.task_id,
            'created': created
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
