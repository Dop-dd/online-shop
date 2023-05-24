from django.shortcuts import render, redirect
from .forms import CreateUserForm


# Registration
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('store')

    # use the form in the register template
    context = {'form': form}


    return render(request, 'account/registration/register.html', context=context)
