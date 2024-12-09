from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

#function to register a an user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('register')  # Redirect to home page or another page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    
def react_index(request):
    return render(request, 'index.html')

@csrf_exempt  # Disables CSRF validation for the API view, but only for testing purposes
def login_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and password are required.'}, status=400)

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                return JsonResponse({'message': 'Login successful', 'username': username,'authenticated':True}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password.','authenticated':False}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.','authenticated':False}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.','authenticated':False}, status=405)