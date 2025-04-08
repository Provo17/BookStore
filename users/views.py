from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import EditAccountForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from payments.models import Sale  # Import the Sale model
from .forms import SignUpForm  # ✅ CORRECT NOW
from django.contrib.auth.forms import AuthenticationForm




def signup(request):
    if request.user.is_authenticated:
        return redirect('user_account')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_account')  # ✅ Redirect after signup
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('homepage')  # Or wherever you want authenticated users to go

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi {username}, welcome back!")
                return redirect('homepage')  # Or redirect wherever you want
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})



@login_required
def purchase_history(request):
    # Retrieve all sales for the currently logged-in user
    sales = Sale.objects.filter(user=request.user).order_by('-sale_date')
    return render(request, 'bookstore/purchase_history.html', {'sales': sales})

@login_required
def user_account(request):
    return render(request, 'bookstore/user_account.html', {'user': request.user})


@login_required
def edit_account(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('user_account')
    else:
        form = EditAccountForm(instance=request.user)

    return render(request, 'bookstore/edit_account.html', {'form': form})

