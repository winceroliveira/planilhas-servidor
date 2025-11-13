"""
Entry point para Vercel
"""
from planilhas_api.wsgi import application

# Vercel espera uma variável 'app'
app = application

