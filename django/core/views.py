from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DayArchiveView, RedirectView, ListView, TemplateView
from django.utils import timezone

from core.models import *
from core.forms import *
from core.elasticsearch import search_for_questions

class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'core/ask.html'

    def get_initial(self):
        return {'user': self.request.user.id}

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'save':
            return super().form_valid(form)
        elif action == 'preview':
            preview = Question(title = form.cleaned_data['title'], text = form.cleaned_data['text'], user = self.request.user)
            context = self.get_context_data(preview=preview)
            return self.render_to_response(context=context)
        return HttpResponseBadRequest()

class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'answer_form': AnswerForm(initial={'user': self.request.user.id, 'question': self.object.id})})
        if self.object.can_accept_answers(self.request.user):
            context.update({
                'accept_form': AnswerAcceptanceForm(initial={'is_accepted': True}),
                'reject_form': AnswerAcceptanceForm(initial={'is_accepted': False})
                })
        return context

class CreateAnswerView(CreateView):
    form_class = AnswerForm
    template_name = 'core/answer.html'

    def get_initial(self):
        return {'user': self.request.user.id, 'question': Question.objects.get(pk=self.kwargs['pk']).id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object': Question.objects.get(pk=self.kwargs['pk'])})
        context.update({'context': context, 'some': 'wow'})
        return context

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form, **kwargs):
        action = self.request.POST.get('action')
        if action == 'save':
            return super().form_valid(form)
        elif action == 'preview':
            preview = Answer(text = form.cleaned_data['text'], user = self.request.user, question = Question.objects.get(pk=self.kwargs['pk']))
            context = self.get_context_data(preview=preview)
            return self.render_to_response(context=context)
        return HttpResponseBadRequest()

class UpdateAnswerAcceptanceView(UpdateView):
    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return HttpResponseBadRedirect(redirect_to=self.object.question.get_absolute_url())

class QuestionList(ListView):
    queryset = Question.objects.all()[:20:]

class UserQuestionList(ListView):
    template_name = 'core/question_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.question_set.all()
        return queryset

class DailyQuestionListView(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created'
    month_format = '%m'
    allow_empty = True

class TodayQuestionListView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse('core:daily_questions', kwargs={'day': today.day, 'month': today.month, 'year': today.year})

class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query', None)
        context = super().get_context_data(query=query, **kwargs)
        if query:
            results = search_for_questions(query)
            id = []
            for hit in results:
                id.append(hit['id'])
            context['hits'] = Question.objects.filter(id__in = id)
        return context
