from django.shortcuts import render
from django.http import HttpResponse

from .models import People


def display(request):

    try:
        peoples = People.objects.filter(
            homeworld__isnull=False
        ).filter(
            homeworld__climate__contains='windy'
        ).order_by('name')
        if not peoples:
            return HttpResponse(
                "No data available, "
                "please use the following command line before use:<br>"
                "./manage.py loaddata ex09_initial_data.json"
            )
        return render(request, 'ex09/display.html', {"people": peoples})
    except Exception as e:
        return HttpResponse(e)
