from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.associations.count() == 1:
            return redirect('association-detail', request.user.associations.first().id)
    return render(request, 'home.html')
