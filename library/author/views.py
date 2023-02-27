from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Author
from book.models import Book
from .forms import AuthorFrom
from .serializers import AuthorSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def author_list(request):
    if request.method == 'GET':
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def home(request):
    return render(request, 'author/home.html', {})


def create_author(request):
    if request.method == 'POST':
        form = AuthorFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_authors')
    else:
        form = AuthorFrom
        return render(request, 'author/create_author.html', {'form': form})


def all_authors(request):
    authors = Author.get_all()
    context = {
        'authors': authors
        }
    return render (request, "author/all_authors.html", context=context)


def delete_author(request, author_id):
    if Author.objects.filter(books__isnull=False, id=author_id):
        messages.success(request, f"Author has book, you can`t delete")
    else:
        Author.delete_by_id(author_id)
    return redirect('all_authors')


def add_book_to_author(request, author_id):
    books = Book.get_all()
    author = Author.get_by_id(author_id)
    
    if request.method == 'POST':
        chosen_book = request.POST['book']
        author = Author.get_by_id(author_id)
        if author:
            author.books.add(chosen_book)
            author.save()
            messages.success(request, f"You have Added Author: {author} to Book Id: {chosen_book}")
            return redirect('all_authors')
        else:
            messages.success(request, "Something went wrong")
            return redirect('all_authors')
    else:
        
        context = {
        "books": books,
        "author": author
        }
        return render(request, 'author/author_add_book.html', context=context)
