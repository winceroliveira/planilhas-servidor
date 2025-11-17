from django.urls import path
from . import views
from . import create_superuser_view

urlpatterns = [
    path('', views.index, name='index'),
    path('api/validar_chave/', views.validar_chave, name='validar_chave'),
    path('api/manus/webhook/', views.webhook_manus_ai, name='webhook_manus_ai'),
    path('api/manus/task/<str:task_id>/', views.verificar_task_manus, name='verificar_task_manus'),
    path('api/manus/registrar/', views.registrar_task_manus, name='registrar_task_manus'),
    # ⚠️ TEMPORÁRIO: Remover após criar superusuário
    path('api/create-superuser/', create_superuser_view.criar_superusuario, name='criar_superusuario'),
]

