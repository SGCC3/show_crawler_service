from django.shortcuts import render, get_object_or_404, redirect
from .models import *
# Create your views here.

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