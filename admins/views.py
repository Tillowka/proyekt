from django.shortcuts import render,redirect
from .forms import adminForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages

def login_view(request):
    if request.method == "GET":
        form = adminForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == "POST":
        form = adminForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                messages.success(
                    request,
                    f"Salom {username.title()}, xush kelibsiz"
                )
                return redirect('admin_page')

            messages.error(request, 'Login yoki parol notog‘ri.')
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni toldiring.')

        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')