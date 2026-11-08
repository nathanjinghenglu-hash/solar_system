from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse

def home(request):
    return render(request, 'learning/home.html')


def science(request):
    return render(request, 'learning/science.html')


def solar_system(request):
    return FileResponse(
        (settings.BASE_DIR / 'solar-system.html').open('rb'),
        content_type='text/html; charset=utf-8',
    )
