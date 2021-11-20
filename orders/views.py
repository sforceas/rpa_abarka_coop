from django.shortcuts import render

from orders.models import Order

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
