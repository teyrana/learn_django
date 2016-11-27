from django.shortcuts import render
from django.http import HttpResponse

from .forms import RegisterForm
# Create your views here.

def index(request):
    return register( request);


def register( request):
    if request.method == 'GET':
        form = RegisterForm()
        return render( request, 'register.html', {'form': form})
        #raise Http404(" This url does not accept GET requests")
    if request.method == 'POST':
        form = RegisterForm( request.POST )
        if form.is_valid():
            form.save();
            return HttpResponse(str(form)+
                    "<h2>successfully Subscribed.</h2>")
        else:
            return HttpResponse("Subscription Error!")
