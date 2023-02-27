from django.shortcuts import render, redirect
from django.contrib import messages
from order.models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from authentication.models import CustomUser
from .forms import BookForm
from .serializers import BookSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        snippets = Book.objects.all()
        serializer = BookSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        snippet = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def search_book(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(name__icontains=searched)
        context={
            'searched': searched,
            'books': books,
            }

        return render (request, "book/search_books.html", context=context)
    else:
         return render (request, "book/search_books.html", {})


def search_user(request):
    
    if request.method == 'POST':
        orders = Order.get_all()
        searched = request.POST['searched_user']
        users = CustomUser.objects.filter(id__icontains=searched)
        context={
            'users': users,
            'searched': searched,
            'orders': orders,
            }

        return render (request, "book/search_user.html", context=context)
    else:
         return render (request, "book/search_user.html", {})         


def all_books(request):
    books = Book.get_all()
    user = request.user
    orders = Order.get_all()
    context = {
        'user':user,
        'orders':orders,
        'books': books
        }
    return render (request, "book/all_books.html", context=context)


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    else:
        form = BookForm
        return render(request, 'book/create_book.html', {'form': form})


def view_book (request, book_id):
    book = Book.get_by_id(book_id)
    authors = [author.__str__() for author in book.authors.all()]
    
    context = {
        'authors': authors,
        'book': book
        }
    return render (request, 'book/view_book.html',context=context)

