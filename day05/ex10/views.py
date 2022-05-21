from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm
from .models import People


def display(request):
    peoples = People.objects.values('gender').distinct()
    choice = ((people['gender'], people['gender']) for people in peoples)

    if request.method == 'POST':
        data = SearchForm(choice, request.POST)
        if data.is_valid():
            min_movies_date = data.cleaned_data['min_movies_date']
            max_movies_date = data.cleaned_data['max_movies_date']
            min_planet_diameter = data.cleaned_data['min_planet_diameter']
            character_gender = data.cleaned_data['character_gender']
            peoples = People.objects.filter(
                gender=character_gender
            ).filter(
                homeworld__diameter__gt=min_planet_diameter
            ).filter(
                movies__release_date__range=(min_movies_date, max_movies_date)
            ).values(
                "movies__title",
                "name",
                "gender",
                "homeworld__name",
                "homeworld__diameter",
            )

            if not peoples:
                return HttpResponse("Nothing corresponding to your research")
            print(peoples[0])
            return render(
                request,
                'ex10/display.html',
                {"peoples": peoples},
            )
        else:
            return HttpResponse("Invalid data")
    search_form = SearchForm(choices=choice)
    return render(request, 'ex10/search.html',
                  {"SearchForm": search_form})
