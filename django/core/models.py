from django.db import models
from django.conf import settings
from django.urls.base import reverse
from core.mailer import make_message

USERMODEL = settings.AUTH_USER_MODEL

class Question(models.Model):
    title = models.CharField('Заглавие вопроса', max_length=200)
    text = models.TextField('Текст вопроса')
    user = models.ForeignKey(to=USERMODEL, on_delete=models.CASCADE)
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    mailinglist_id = models.UUIDField(null=True, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:question', kwargs={'pk': self.id})

    def get_domain_link(self):
        link = 'http://' + settings.HOST_NAME + self.get_absolute_url()
        return link

    def can_accept_answers(self, user):
        return user == self.user

    def as_elasticsearch_dict(self):
        return {
            '_id': self.id,
            '_type': 'doc',
            'text': '{}\n{}'.format(self.title, self.text),
            'title': self.title,
            'id': self.id,
            'created': self.created,
        }

class Answer(models.Model):
    text = models.TextField('Текст ответа')
    user = models.ForeignKey(to=USERMODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_accepted = models.BooleanField('Принят ли ответ автором вопроса', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-created']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        make_message(self)

    def __str__(self):
        return self.text
