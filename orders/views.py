from django.shortcuts import redirect, render
from orders.models import ConcreteExtraInOrder, ConcreteMenuInOrder, ConcreteWorkerInOrder, Order

# Create your views here.

def list_orders(request):
    """ List existing orders """
    
    pending_orders = Order.objects.filter(completed_flag=False,active_flag=True).order_by('-start_date')
    completed_orders = Order.objects.filter(completed_flag=True,active_flag=True).order_by('-start_date')

    context = {
        'pending_orders':pending_orders,
        'completed_orders':completed_orders,
    }
    return render(request,'orders/list.html',context)

def detailed_order(request,pk):
    """ Show detailed order """
    
    order = Order.objects.get(pk=pk)
    menus_in_order=ConcreteMenuInOrder.objects.filter(order=order)
    workers_in_order=ConcreteWorkerInOrder.objects.filter(order=order)
    extras_in_order=ConcreteExtraInOrder.objects.filter(order=order)

    context = {
        'order':order,
        'menus':menus_in_order,
        'workers':workers_in_order,
        'extras':extras_in_order,
    }

    return render(request,'orders/detail.html',context)

def generate_work_schedule(request,pk):
    order = Order.objects.get(pk=pk)
    workers_in_order=ConcreteWorkerInOrder.objects.filter(order=order).order_by('-start_date')
    
    context = {
        'order':order,
        'workers':workers_in_order,
    }
    return render(request,'orders/schedule.html',context)
