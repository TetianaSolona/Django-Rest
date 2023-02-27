from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from book.models import Book
from rest_framework import generics, status
from .serializers import OrderSerializer


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        snippets = Order.objects.all()
        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def all_orders(request):
    orders = Order.get_all()
    user = request.user
    context = {
        'orders': orders,
        'user' : user
        }
    return render (request, "order/all_orders.html", context=context)

def create_order(request, book_id):
    book = Book.get_by_id(book_id)
    if request.method == 'POST':
        book = Book.get_by_id(book_id)
        user = request.user
        pland_end_at = request.POST['planed_end_at']
        if book.count >0:
            book.count-=1
            book.save()
            order = Order.create(user, book, pland_end_at)
            if order:
                order.save()
                messages.success(request, f"You have created {order.book.name}")
                return redirect('all_orders')

            else:
                messages.error(request, f"You have entered wrong data ")
                return redirect('create_order')
        else:
            messages.success(request, f"There is no free {book.name}")
            return redirect('all_orders')

    else:
        
        context = {
            'book':book
        
        }
        return render(request, 'order/create_order.html', context=context)

def end_order(request, order_id):
    order = Order.get_by_id(order_id)
    end_date = datetime.now()
    book=order.book
    book.count+=1
    book.update()
    order.update(end_at=end_date)
    order.save()

    return redirect('all_orders')

def delete_order(request, order_id):
    order = Order.delete_by_id(order_id)
    return redirect('all_orders')