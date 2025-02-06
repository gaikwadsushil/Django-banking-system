from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User

class Register(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect("login")
        return render(request, 'user/register.html', {'form': form})

class Login(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate using either email or username
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                # Try authenticating as email
                try:
                    from .models import User
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("index")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please provide valid inputs.")

        return render(request, 'user/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class AdminPanel(View):
    def get(self, request):
        if request.user.role != "ADMIN":
            messages.error(request, "Access denied.")
            return redirect("profile")
        users = User.objects.all()
        return render(request, 'user/admin_panel.html', {'users': users})

    def post(self, request):
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        user = User.objects.get(id=user_id)
        if action == "approve":
            user.is_active = True
        elif action == "deactivate":
            user.is_active = False
        elif action == "delete":
            user.delete()
        user.save()
        messages.success(request, f"User {action}d successfully!")
        return redirect("admin_panel")

class PostLoginOptions(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/post_login_options.html')
        else:
            messages.error(request, "You need to log in first.")
            return redirect("login")