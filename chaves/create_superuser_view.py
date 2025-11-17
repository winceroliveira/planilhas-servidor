"""
Endpoint temporário para criar superusuário na Vercel
⚠️ REMOVER APÓS USAR - É UMA FALHA DE SEGURANÇA DEIXAR ATIVO!
"""
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()


@csrf_exempt
def criar_superusuario(request):
    """
    Cria um superusuário no Django
    ⚠️ REMOVER ESTE ENDPOINT APÓS USAR!
    
    Body JSON esperado:
    {
        "username": "admin",
        "email": "admin@example.com",
        "password": "senha_segura"
    }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Use POST'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        
        username = data.get('username')
        email = data.get('email', '')
        password = data.get('password')
        
        # Validações
        if not username:
            return JsonResponse({
                'status': 'error',
                'message': 'Username é obrigatório'
            }, status=400)
        
        if not password:
            return JsonResponse({
                'status': 'error',
                'message': 'Password é obrigatório'
            }, status=400)
        
        if len(password) < 8:
            return JsonResponse({
                'status': 'error',
                'message': 'Password deve ter pelo menos 8 caracteres'
            }, status=400)
        
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Usuário "{username}" já existe'
            }, status=400)
        
        # Criar superusuário
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Superusuário "{username}" criado com sucesso!',
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Body deve ser JSON válido'
        }, status=400)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__,
            'traceback': error_details.split('\n')[-10:] if error_details else None
        }, status=500)

