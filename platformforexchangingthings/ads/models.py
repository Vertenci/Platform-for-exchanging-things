from django.contrib.auth.models import User
from django.db import models


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField('Заголовок', max_length=255, blank=False)
    description = models.TextField('Описание', blank=False)
    image_url = models.ImageField(upload_to='ad/ad_images/', blank=False)
    category = models.CharField('Категория', max_length=100, blank=False)

    CONDITION_CHOICES = [
        ('Новое', 'Новое'),
        ('Б/У', 'Б/У'),
    ]

    condition = models.CharField('Состояние', max_length=5, choices=CONDITION_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    is_draft = models.BooleanField(default=True, verbose_name='Черновик')

    def __str__(self):
        return f"{self.title} - {self.created_at}"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ExchangeProposal(models.Model):
    id = models.AutoField(primary_key=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True, blank=False, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.SET_NULL, null=True, blank=False, related_name='received_proposals')
    comment = models.TextField('Комментарий', max_length=300)

    STATUS_CHOICES = [
        ('Ожидает', 'Ожидает'),
        ('Принята', 'Принята'),
        ('Отклонена', 'Отклонена')
    ]

    status = models.CharField('Статус', max_length=9, choices=STATUS_CHOICES, default='Ожидает')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Номер: {self.id}, Отправитель: {self.ad_sender}, Получатель: {self.ad_receiver}"

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
