from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm


# Create your views here.
def sign_up(request: WSGIRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('signin')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'users_system/signup.html', context=context)