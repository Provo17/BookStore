from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.role = form.cleaned_data.get('role')
            user.profile.save()
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)  # Debugging output
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
