from django.shortcuts import render,HttpResponse

# Create your views here.
def the_first(request):
    return HttpResponse('MY APP')

def the_second(request):
    return HttpResponse('MY API')