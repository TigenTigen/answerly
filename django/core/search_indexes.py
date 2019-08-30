import datetime
from django.db import models
from haystack_es import indexes
from haystack import signals
from core.models import Question

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    content_auto = indexes.EdgeNgramField(model_attr='title')
    rendered = indexes.CharField(use_template=True, indexed=False)

    '''
    var: {
    'app_label': 'core',
    'model_name': 'question',
    'pk': '51',
    'score': 1.3773504,
    '_object': None,
    '_model': None,
    '_verbose_name': None,
    '_additional_fields': ['id', 'text', 'created'],
    '_point_of_origin': None,
    '_distance': None,
    'stored_fields': None,
    'log': <haystack.utils.log.LoggingFacade object at 0x7f1d474c8470>,
    'id': 'core.question.51',
    'text': 'first question\ndfdfsdfsdfsdf\n29.08.2019 19:57:12\n',
    'created': datetime(2019, 8, 29, 12, 57, 12)}
    '''

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class QuestionOnlySignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        # Listen only to the ``Question`` model.
        models.signals.post_save.connect(self.handle_save, sender=Question)
        models.signals.post_delete.connect(self.handle_delete, sender=Question)

    def teardown(self):
        # Disconnect only for the ``Question`` model.
        models.signals.post_save.disconnect(self.handle_save, sender=Question)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Question)
