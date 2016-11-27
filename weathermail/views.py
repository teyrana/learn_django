from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from .forms import RegisterForm
# Create your views here.

def register(request):
    form = RegisterForm()
    return render( request, 'register.html', {'form': form})

def result( request):
    if request.method == 'POST':
        form = RegisterForm( request.POST )
        context={};

        if form.is_valid():
            form.save();
            messages.success( request, 'Successfully Subscribed')
            context = { 'message': "You have been added to the list!"}
        else:
            messages.warning( request, 'Subscription Error')
            context = { 'message': "Error! Your address has not been added."}

        return render( request, 'result.html', context)
