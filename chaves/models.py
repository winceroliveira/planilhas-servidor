from django.db import models
import uuid
from django.utils import timezone


class ChaveDeUtilizacao(models.Model):
    STATUS_CHOICES = [
        ('Ativa', 'Ativa'),
        ('Inativa', 'Inativa'),
        ('Expirada', 'Expirada'),
    ]
    
    chave = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nome_usuario = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativa')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultimo_uso = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.chave} - {self.nome_usuario or 'Sem nome'}"
    
    class Meta:
        verbose_name = "Chave de Utilização"
        verbose_name_plural = "Chaves de Utilização"


class ManusAITask(models.Model):
    """Armazena tasks do Manus AI e seus status"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('running', 'Em execução'),
        ('completed', 'Completa'),
        ('failed', 'Falhou'),
    ]
    
    task_id = models.CharField(max_length=100, unique=True, db_index=True)
    task_title = models.CharField(max_length=500, blank=True, null=True)
    task_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stop_reason = models.CharField(max_length=50, blank=True, null=True)
    
    # Dados do webhook
    attachments = models.JSONField(default=list, blank=True)
    message = models.TextField(blank=True, null=True)
    
    # Timestamps
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_completa = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.task_id} - {self.status}"
    
    class Meta:
        verbose_name = "Manus AI Task"
        verbose_name_plural = "Manus AI Tasks"
        ordering = ['-data_criacao']
