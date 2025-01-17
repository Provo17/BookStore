from django.shortcuts import render

def index(request):
    return render(request, 'bookstore/homepage.html')  # Include the 'bookstore/' prefix