from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import View

def error_404_view(request , exception):
    return render(request, '404.html')

class index(View):
    def get(self, request):
        return HttpResponse('Hola mundo desde PyWomabt.')


