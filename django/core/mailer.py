from django.conf import settings
import requests

ROOT_URL = settings.MAILER_URL

def create_mailinglist(question):
    url = ROOT_URL + 'mailinglist'
    new_mailinglist_dict = {'name': 'Answerly: {}'.format(question.title)}
    r = requests.post(url, json = new_mailinglist_dict)
    if r.status_code == 201:
        result_dict = r.json()
        new_mailinglist_id = result_dict['id']
        question.mailinglist_id = new_mailinglist_id
        question.save()

def get_mailinglist_id(question):
    if question.mailinglist_id == None:
        create_mailinglist(question)
    return str(question.mailinglist_id)

def subscribe_user_to_question_updates(user, question):
    mailinglist_id = get_mailinglist_id(question)
    url = ROOT_URL + 'mailinglist/{}/subscribers'.format(mailinglist_id)
    new_subscriber_dict = {
        'email': user.email,
        'mailinglist': mailinglist_id,
    }
    r = requests.post(url, json = new_subscriber_dict)
    return r.status_code == 201

def subscribers(question, user):
    mailinglist_id = get_mailinglist_id(question)
    url = ROOT_URL + 'mailinglist/{}/subscribers'.format(mailinglist_id)
    r = requests.get(url)
    subscribers = r.json()
    count = len(subscribers)
    is_subscribed = False
    if user.is_authenticated and user.email:
        for subscriber in subscribers:
            if subscriber['email'] == user.email:
                is_subscribed = True
                break
    return count, is_subscribed

def make_message(answer):
    question = answer.question
    mailinglist_id = get_mailinglist_id(question)
    url = ROOT_URL + 'mailinglist/{}/messages'.format(mailinglist_id)
    new_message_dict = {
        'subject': 'Новый ответ к вопросу "{}" на Answerly'.format(question.title),
        'body': answer.text + '\n Сыллка для перехода к странице вопроса: {}'.format(question.get_domain_link())
    }
    r = requests.post(url, json = new_message_dict)
    return r.status_code == 201
