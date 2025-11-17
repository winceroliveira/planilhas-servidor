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
    
    # Verificar se DATABASE_URL ou POSTGRES_URL está configurada
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
    if not database_url:
        return JsonResponse({
            'status': 'error',
            'message': 'DATABASE_URL ou POSTGRES_URL não configurada',
            'details': 'Configure a variável de ambiente DATABASE_URL ou POSTGRES_URL na Vercel (Settings → Environment Variables)',
            'help': 'Veja servidor/PROXIMOS_PASSOS_SUPABASE.md para instruções'
        }, status=500)
    
    try:
        # Executar migrations com mais verbosidade para debug
        from io import StringIO
        import sys
        
        # Capturar output das migrations
        output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = output
        
        try:
            call_command('migrate', verbosity=2, interactive=False)
            migration_output = output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        return JsonResponse({
            'status': 'success',
            'message': 'Migrations executadas com sucesso!',
            'output': migration_output.split('\n')[-10:] if migration_output else None
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        # Capturar mais informações sobre o erro
        error_info = {
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__,
            'traceback': error_details.split('\n')[-10:] if error_details else None,
        }
        
        # Verificar se é erro de conexão
        if 'connection' in str(e).lower() or 'database' in str(e).lower():
            error_info['help'] = 'Erro de conexão com banco de dados. Verifique se POSTGRES_URL está correta.'
        elif 'no such table' in str(e).lower():
            error_info['help'] = 'Tabelas não existem. As migrations precisam ser executadas.'
        else:
            error_info['help'] = 'Verifique os logs na Vercel para mais detalhes'
        
        return JsonResponse(error_info, status=500)

