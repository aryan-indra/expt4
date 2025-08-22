from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm
from .models import User

def user_form_view(request):
    """View to handle user form submission and display"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User information saved successfully!')
            return redirect('user_form')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm()
    
    # Get all users to display
    users = User.objects.all()
    
    context = {
        'form': form,
        'users': users,
    }
    return render(request, 'userform/user_form.html', context)

def user_list_view(request):
    """View to display all users"""
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'userform/user_list.html', context)