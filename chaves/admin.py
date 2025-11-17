from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ChaveDeUtilizacao, ManusAITask


# Personalizar o Admin Site
admin.site.site_header = "🔐 Sistema de Licenciamento"
admin.site.site_title = "Admin - Planilhas"
admin.site.index_title = "Painel de Controle"


@admin.register(ChaveDeUtilizacao)
class ChaveDeUtilizacaoAdmin(admin.ModelAdmin):
    list_display = ('chave_formatado', 'nome_usuario', 'status_badge', 'data_criacao_formatada', 'ultimo_uso_formatado', 'acoes')
    list_filter = ('status', 'data_criacao')
    search_fields = ('chave', 'nome_usuario')
    readonly_fields = ('chave', 'data_criacao', 'ultimo_uso', 'chave_formatado_detalhe')
    list_per_page = 25
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('🔑 Informações da Chave', {
            'fields': ('chave_formatado_detalhe', 'nome_usuario', 'status'),
            'classes': ('wide',)
        }),
        ('📅 Datas', {
            'fields': ('data_criacao', 'ultimo_uso'),
            'classes': ('collapse',)
        }),
    )
    
    def chave_formatado(self, obj):
        """Exibe apenas os primeiros 8 caracteres da chave"""
        chave_str = str(obj.chave)
        return format_html(
            '<code style="background: #f0f0f0; padding: 4px 8px; border-radius: 4px; font-size: 11px;">{}</code>',
            chave_str[:8] + '...'
        )
    chave_formatado.short_description = 'Chave'
    chave_formatado.admin_order_field = 'chave'
    
    def chave_formatado_detalhe(self, obj):
        """Exibe a chave completa no formulário de edição"""
        return format_html(
            '<code style="background: #f0f0f0; padding: 8px; border-radius: 4px; display: block; font-size: 12px; word-break: break-all;">{}</code>',
            str(obj.chave)
        )
    chave_formatado_detalhe.short_description = 'Chave Completa'
    
    def status_badge(self, obj):
        """Exibe status com badge colorido"""
        cores = {
            'Ativa': '#28a745',
            'Inativa': '#6c757d',
            'Expirada': '#dc3545'
        }
        cor = cores.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, obj.status
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def data_criacao_formatada(self, obj):
        """Formata data de criação"""
        if obj.data_criacao:
            return obj.data_criacao.strftime('%d/%m/%Y %H:%M')
        return '-'
    data_criacao_formatada.short_description = 'Data de Criação'
    data_criacao_formatada.admin_order_field = 'data_criacao'
    
    def ultimo_uso_formatado(self, obj):
        """Formata último uso"""
        if obj.ultimo_uso:
            return obj.ultimo_uso.strftime('%d/%m/%Y %H:%M')
        return format_html('<span style="color: #999;">Nunca usado</span>')
    ultimo_uso_formatado.short_description = 'Último Uso'
    ultimo_uso_formatado.admin_order_field = 'ultimo_uso'
    
    def acoes(self, obj):
        """Botões de ação"""
        url = reverse('admin:chaves_chavedeutilizacao_change', args=[obj.pk])
        return format_html(
            '<a href="{}" style="background: #007bff; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">Editar</a>',
            url
        )
    acoes.short_description = 'Ações'
    
    def get_queryset(self, request):
        """Otimizar queries"""
        qs = super().get_queryset(request)
        return qs.select_related()


@admin.register(ManusAITask)
class ManusAITaskAdmin(admin.ModelAdmin):
    list_display = ('task_id_formatado', 'task_title_formatado', 'status_badge', 'data_criacao_formatada', 'data_completa_formatada', 'link_task')
    list_filter = ('status', 'data_criacao', 'stop_reason')
    search_fields = ('task_id', 'task_title', 'message')
    readonly_fields = ('task_id', 'data_criacao', 'data_atualizacao', 'data_completa', 'attachments_formatado')
    list_per_page = 25
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('🤖 Informações da Task', {
            'fields': ('task_id', 'task_title', 'task_url', 'status', 'stop_reason'),
            'classes': ('wide',)
        }),
        ('📎 Dados do Webhook', {
            'fields': ('attachments_formatado', 'message'),
            'classes': ('collapse',)
        }),
        ('📅 Timestamps', {
            'fields': ('data_criacao', 'data_atualizacao', 'data_completa'),
            'classes': ('collapse',)
        }),
    )
    
    def task_id_formatado(self, obj):
        """Formata task_id"""
        return format_html(
            '<code style="background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 11px;">{}</code>',
            obj.task_id[:20] + '...' if len(obj.task_id) > 20 else obj.task_id
        )
    task_id_formatado.short_description = 'Task ID'
    task_id_formatado.admin_order_field = 'task_id'
    
    def task_title_formatado(self, obj):
        """Formata título da task"""
        if obj.task_title:
            titulo = obj.task_title[:50] + '...' if len(obj.task_title) > 50 else obj.task_title
            return format_html('<span title="{}">{}</span>', obj.task_title, titulo)
        return format_html('<span style="color: #999;">Sem título</span>')
    task_title_formatado.short_description = 'Título'
    task_title_formatado.admin_order_field = 'task_title'
    
    def status_badge(self, obj):
        """Exibe status com badge colorido"""
        cores = {
            'pending': '#ffc107',
            'running': '#17a2b8',
            'completed': '#28a745',
            'failed': '#dc3545'
        }
        textos = {
            'pending': '⏳ Pendente',
            'running': '🔄 Em execução',
            'completed': '✅ Completa',
            'failed': '❌ Falhou'
        }
        cor = cores.get(obj.status, '#6c757d')
        texto = textos.get(obj.status, obj.status)
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            cor, texto
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def data_criacao_formatada(self, obj):
        """Formata data de criação"""
        if obj.data_criacao:
            return obj.data_criacao.strftime('%d/%m/%Y %H:%M')
        return '-'
    data_criacao_formatada.short_description = 'Criada em'
    data_criacao_formatada.admin_order_field = 'data_criacao'
    
    def data_completa_formatada(self, obj):
        """Formata data de conclusão"""
        if obj.data_completa:
            return obj.data_completa.strftime('%d/%m/%Y %H:%M')
        return format_html('<span style="color: #999;">-</span>')
    data_completa_formatada.short_description = 'Concluída em'
    data_completa_formatada.admin_order_field = 'data_completa'
    
    def link_task(self, obj):
        """Link para a task"""
        if obj.task_url:
            return format_html(
                '<a href="{}" target="_blank" style="background: #007bff; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">🔗 Abrir</a>',
                obj.task_url
            )
        return '-'
    link_task.short_description = 'Link'
    
    def attachments_formatado(self, obj):
        """Formata attachments"""
        if obj.attachments:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for att in obj.attachments:
                if isinstance(att, dict):
                    nome = att.get('name', 'Sem nome')
                    url = att.get('url', '#')
                    html += f'<li><a href="{url}" target="_blank">{nome}</a></li>'
                else:
                    html += f'<li>{att}</li>'
            html += '</ul>'
            return format_html(html)
        return format_html('<span style="color: #999;">Nenhum anexo</span>')
    attachments_formatado.short_description = 'Anexos'
    
    def get_queryset(self, request):
        """Otimizar queries"""
        qs = super().get_queryset(request)
        return qs
