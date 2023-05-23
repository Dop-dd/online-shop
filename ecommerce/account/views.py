from django.shortcuts import render


# Registration
def register(request):
    return render(request, 'account/registration/register.html')
