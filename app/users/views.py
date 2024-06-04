from django.shortcuts import render, get_object_or_404, redirect
from .models import RepairOrder
from .forms import RepairOrderForm

def main(request):
    return render(request,"main.html",)

def order_success(request):
    return render(request, 'order_success.html')



def check_status(request):
    repair_code = request.GET.get('repair_code')
    repair_order = None

    if repair_code:
        try:
            repair_order = RepairOrder.objects.get(repair_code=repair_code)
        except RepairOrder.DoesNotExist:
            repair_order = None

    return render(request, 'check_status.html', {'repair_order': repair_order, 'repair_code': repair_code})

def add_order(request):
    if request.method == "POST":
        form = RepairOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')
    else:
        form = RepairOrderForm()

    return render(request, 'add_order.html', {'form': form})