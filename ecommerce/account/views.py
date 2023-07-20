from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from payment.models import Order, OrderItem

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

# import our custome made domain
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# login and logout URLS
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

# prevent unauthorized login
from django.contrib.auth.decorators import login_required

# messages
from django.contrib import messages


# Registration
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            user.is_active = False
            user.save()

            # email verificxaation setup - template

            current_site = get_current_site(request)
            subject = 'Account verificaation email'

            message = render_to_string('account/registration/email-verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),

            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')


    # use the form in the register template
    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)



def email_verification(request, uidb64, token):
    # unique id
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    # failed
    else:
        return redirect('email-verification-failed')



def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


# login gorm
def my_login(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username,  password=password)

            # if user already exixts
            if user is not None:
                auth.login(request, user)

                return  redirect('dashboard')

    context = {'form': form}
    return render(request, 'account/my-login.html', context=context)


# logout form
def user_logout(request):
    try:

        for key in list(request.session.keys()):

            if key == 'session_key':
                continue
            else:
                del request.session[key]

    except KeyError:
        pass

    messages.success(request, 'Logout success')

    return redirect('store')


# dashboard
@login_required(login_url='my-login')
def dashboard(request):

    return render(request,'account/dashboard.html')


# account management
@login_required(login_url='my-login')
def profile_management(request):

# updating our user's username and email
    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, 'Account updated')

            return redirect('dashboard')

    context = {'user_form': user_form}


    return render(request,'account/profile-management.html', context=context)


# delete user account
@login_required(login_url='my-login')
def delete_account(request):

    # ge the current id of the user
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()

        messages.error(request, 'Account deleted')

        return redirect('store')

    return render(request, 'account/delete-account.html')


# shipping view
@login_required(login_url='my-login')
def manage_shipping(request):

    try:
        # account user with shipment info
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

        # account user with n o shipment info
        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():
            # assign the juser fk to the object
            shipping_user = form.save(commit=False)

            # add the fk itself
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)


# track orders
@login_required(login_url='my-login')
def track_orders(request):

     try:

        orders = OrderItem.objects.filter(user=request.user)

        context = {'orders':orders}

        return render(request, 'account/track-orders.html', context=context)

     except:

        return render(request, 'account/track-orders.html')


