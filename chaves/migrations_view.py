"""
Endpoint temporário para executar migrations na Vercel
⚠️ REMOVER APÓS USAR - É UMA FALHA DE SEGURANÇA DEIXAR ATIVO!
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import os


@csrf_exempt
def executar_migrations(request):
    """
    Executa migrations do Django
    ⚠️ REMOVER ESTE ENDPOINT APÓS USAR!
    """
    # Verificação básica de segurança (adicione uma chave secreta se quiser)
    # Por enquanto, apenas verifica se está em produção
    if request.method != 'POST':
        return JsonResponse({'error': 'Use POST'}, status=405)
    
    # Verificação opcional: adicione um token secreto
    # token = request.headers.get('X-Migration-Token')
    # if token != os.environ.get('MIGRATION_TOKEN', 'sua-chave-secreta-aqui'):
    #     return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    # Verificar se DATABASE_URL está configurada
    if 'DATABASE_URL' not in os.environ:
        return JsonResponse({
            'status': 'error',
            'message': 'DATABASE_URL não configurada',
            'details': 'Configure a variável de ambiente DATABASE_URL na Vercel (Settings → Environment Variables)',
            'help': 'Veja servidor/PROXIMOS_PASSOS_SUPABASE.md para instruções'
        }, status=500)
    
    try:
        # Executar migrations
        call_command('migrate', verbosity=0, interactive=False)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Migrations executadas com sucesso!'
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'details': error_details.split('\n')[-3] if error_details else None,
            'help': 'Verifique os logs na Vercel para mais detalhes'
        }, status=500)

