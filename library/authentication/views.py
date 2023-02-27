from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .forms import CustomUserForm
from .models import CustomUser
from .serializers import CustomUserSerializer, UserOrderSerializer, UserOrderDetailSerialiser
from rest_framework import viewsets
from rest_framework import generics
from order.models import Order


class CustomUserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    viewsets = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        custom_id = self.kwargs['pk']
        return CustomUser.objects.filter(pk=custom_id)


class UserOrderListView(generics.ListAPIView):
    serializer_class = UserOrderDetailSerialiser

    def get_queryset(self):
        userid = self.kwargs['user_id']
        return Order.objects.filter(user=userid)


class UserOrderDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserOrderDetailSerialiser
    lookup_field = 'pk'

    def get_queryset(self):
        if self.kwargs['pk']:
            return Order.objects.filter(user_id=self.kwargs['user_id'])
        else:
            return Order.objects.all()


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are now Loged In"))
            return redirect('home')
            

        else:
            messages.success(request, ("There was an error logging in, Try again..."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logout!"))
    return redirect('home')


def register_user(request):

    if request.method == 'POST':
        userform = CustomUserForm(request.POST)
        if userform.is_valid():
            form = userform.save()
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                form.set_password(form.password)
                form.save()
                email = userform.cleaned_data['email']
                password = userform.cleaned_data['password']
                user = authenticate(email = email, password = password)
                login(request, user)
                messages.success(request, ("You Have Created a New Account!"))
                return redirect ('home')
            else:
                messages.success(request, ("Passwords do not Match, Please Try Again"))
                return redirect ('register_user')
        else:
            messages.success(request, ("This email is alredy taken, Please enter another..."))
            return redirect ('register_user')

    else:
        form = CustomUserForm
        return render(request, 'authenticate/register_user.html', {'form': form})


def all_users(request):
    users = CustomUser.get_all()
    context = {
        'users': users
        }
    return render (request, "authenticate/all_users.html", context=context)


def view_user (request, user_id):
    user = CustomUser.get_by_id(user_id)
    context = {
        'user': user
        }
    return render (request, 'authenticate/view_user.html',context=context)

