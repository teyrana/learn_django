from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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
            context['message']= "You have been added to the list!"
        else:
            messages.warning( request, 'Subscription Error')
            context['message']= "Error! Your address has not been added."
        return render( request, 'result.html', context)

@login_required( login_url='/admin/login')
def list( request):
    if request.user.is_staff:
        if request.method == 'GET':
            return render( request, 'send.html')
    else:
        raise PermissionDenied

@login_required( login_url='/admin/login' )
def send( request):
    if request.user.is_staff:
        if request.method == 'GET':

            # spin off email worker
            # fork.worker( send_emails )

            messages.warning( request, 'Messages Sent!')
            context = {'message': "The email list has been notified of weather conditions."}
            return render( request, 'result.html', context)
    else:
        raise PermissionDenied
