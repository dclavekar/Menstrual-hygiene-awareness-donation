from django.shortcuts import render
from django.http import HttpResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from .models import Donate
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Create your views here.
def homepage(request):
    if(request.method=="POST"):
        return render(request,'paymentgateway/payment.html')
    return render(request, 'paymentGateway/homepage.html')

def payment(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount= int(request.POST.get('amount')) *100
        
        client = razorpay.Client( auth=("rzp_test_QE24PJAWl3Y6rc", "PaR3sOfMRCf8SwPVL9T0Yo5e")) #api keys taken from razorpay dashboard
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        print(payment)
        donor= Donate(name=name,amount=amount,email=email, donor_id=payment['id'])
        donor.save()
        return render(request, "paymentGateway/razor.html", {'payment': payment})

    return render(request,'paymentGateway/payment.html')

def razor(request):
    if(request.method=="POST"):
        return render(request,"paymentGateway/success.html")
    return render(request, "paymentGateway/razor.html")

def success(request):
    if(request.method=="POST"):
        a=request.POST
        order_id=""
        for key,val in a.items():
            if(key=="razorpay_order_id"):
                order_id=val;
        user=Donate.objects.filter(donor_id=order_id).first()
        user.save()
        msg_plain= render_to_string('paymentGateway/email.txt')
        msg_html= render_to_string('paymentGateway/email.html')
        send_mail("Your donation has been recieved. Thank You!", msg_plain, settings.EMAIL_HOST_USER, [user.email] , html_message=msg_html)
    return render(request, "paymentGateway/success.html")