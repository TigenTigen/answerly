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
