"""
WSGI config for planilhas_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planilhas_api.settings')

application = get_wsgi_application()

# Garantir que os arquivos estáticos sejam coletados na inicialização (apenas se necessário)
# Isso é útil para ambientes serverless como Vercel
try:
    from django.core.management import call_command
    import sys
    # Apenas executar collectstatic se não estiver em modo de teste
    if 'test' not in sys.argv and 'collectstatic' not in sys.argv:
        # Tentar coletar arquivos estáticos se não existirem
        static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
        if not os.path.exists(static_root) or not os.listdir(static_root):
            try:
                call_command('collectstatic', '--noinput', verbosity=0)
            except:
                pass  # Ignorar erros, WhiteNoise vai usar finders
except:
    pass  # Ignorar se houver problemas