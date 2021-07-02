from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
from datetime import datetime, date


# Create your views here.

def homepage(request):
    # calendar = get_calendar(request)
    genre_concert = Genre.objects.filter(name='concert')
    genre_exhibition = Genre.objects.filter(name='exhibit')
    genre_musical = Genre.objects.filter(name='musical')
    genre_play = Genre.objects.filter(name='play')

    concerts = Show.objects.filter(genre__in=genre_concert).order_by('-likes')
    exhibits = Show.objects.filter(genre__in=genre_exhibition).order_by('-likes')
    musicals = Show.objects.filter(genre__in=genre_musical).order_by('-likes')
    plays = Show.objects.filter(genre__in=genre_play).order_by('-likes')

    return render(request, 'homepage.html',
                  {'concerts': concerts, 'exhibits': exhibits,
                   'musicals': musicals, 'plays': plays})


def show_list(request):
    shows = Show.objects.all()
    return render(request, 'VIEWNAME', {'shows': shows})


def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    return render(request, 'VIEWNAME', {'show': show})


def delete_show(request, pk):
    show = get_object_or_404(Show, pk=pk)
    show.delete()
    return redirect('VIEWNAME')


def get_calendar(request):
    d = get_date(request.GET.get('day', None))

    cal = Calendar(d.year, d.month)

    html_cal = cal.formatMonth(withyear=True)

    return mark_safe(html_cal)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
