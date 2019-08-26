from django.urls import path
from core.views import *

app_name = 'core'
urlpatterns = [
    path('', QuestionList.as_view(), name='last_questions'),
    path('ask', AskQuestionView.as_view(), name='ask'),
    path('question/<int:pk>', QuestionDetailView.as_view(), name='question'),
    path('question/<int:pk>/answer', CreateAnswerView.as_view(), name='answer'),
    path('answer/<int:pk>/accept', UpdateAnswerAcceptanceView.as_view(), name='update_answer_acceptance'),
    path('user_questions/my/', UserQuestionList.as_view(), name='my_questions'),
    path('daily_questions/<int:year>/<int:month>/<int:day>', DailyQuestionListView.as_view(), name='daily_questions'),
    path('today_questions', TodayQuestionListView.as_view(), name='today_questions'),
    path('search', SearchView.as_view(), name='search'),
]
