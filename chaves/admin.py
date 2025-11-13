from django.contrib import admin
from .models import ChaveDeUtilizacao, ManusAITask


@admin.register(ChaveDeUtilizacao)
class ChaveDeUtilizacaoAdmin(admin.ModelAdmin):
    list_display = ('chave', 'nome_usuario', 'status', 'data_criacao', 'ultimo_uso')
    list_filter = ('status', 'data_criacao')
    search_fields = ('chave', 'nome_usuario')
    readonly_fields = ('chave', 'data_criacao', 'ultimo_uso')


@admin.register(ManusAITask)
class ManusAITaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_title', 'status', 'stop_reason', 'data_criacao', 'data_completa')
    list_filter = ('status', 'data_criacao')
    search_fields = ('task_id', 'task_title')
    readonly_fields = ('task_id', 'data_criacao', 'data_atualizacao', 'data_completa')
    fieldsets = (
        ('Informações da Task', {
            'fields': ('task_id', 'task_title', 'task_url', 'status', 'stop_reason')
        }),
        ('Dados do Webhook', {
            'fields': ('attachments', 'message')
        }),
        ('Timestamps', {
            'fields': ('data_criacao', 'data_atualizacao', 'data_completa')
        }),
    )
