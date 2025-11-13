from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/validar_chave/', views.validar_chave, name='validar_chave'),
    path('api/manus/webhook/', views.webhook_manus_ai, name='webhook_manus_ai'),
    path('api/manus/task/<str:task_id>/', views.verificar_task_manus, name='verificar_task_manus'),
    path('api/manus/registrar/', views.registrar_task_manus, name='registrar_task_manus'),
]

