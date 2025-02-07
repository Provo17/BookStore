from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Sale  # Import the Sale model

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Ensure profile exists
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = form.cleaned_data.get('role')
            profile.save()

            login(request, user)
            return redirect('index')  # Redirect to homepage after signup
        else:
            print(form.errors)  # Debugging output

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi {username}, welcome back!")
                return redirect('homepage')  # Replace 'homepage' with the name of your homepage view
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def purchase_history(request):
    # Retrieve all sales for the currently logged-in user
    sales = Sale.objects.filter(user=request.user).order_by('-sale_date')
    return render(request, 'users/purchase_history.html', {'sales': sales})

@login_required
def user_account(request):
    return render(request, 'registration/signup.html', {'user': request.user})