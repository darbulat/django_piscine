from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def index(request):
    template = loader.get_template('ex00/index.html')
    context = {
        'latest_question_list': 'latest_question_list',
    }
    return HttpResponse(template.render(context, request))
