from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
def index(request):
    #newest_movies = Movie.objects.order_by('-release_date')[:15]
    #context = {'newest_movies': newest_movies}
    #return render(request, 'recipies/index.html',context)
    return render(request, 'main/user_login.html')

# temporary view for display of 
def blood_view(request,id):
    return HttpResponse("<h1>%s</h1>" %id)