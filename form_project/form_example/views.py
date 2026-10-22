from django.shortcuts import render
from .forms import OrderForm

# Create your views here.
from django.shortcuts import render
def form_example(request):
    initial= {'email':'user@example.com'}
    if request.method == "POST":
        form = OrderForm(request.POST, initial=initial)
        if form.is_valid():
            print ("Validation checked!")
            for name, value in form.cleaned_data.items():
                print("{}: ({}) {}".format(name, type(value), value))
        else:
            print ( "Validation failed!")
    else:
        form = OrderForm(initial=initial)

    return render(request, 'form_example.html', {'method':request.method ,'form': form})
