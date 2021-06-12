from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import ContactForm, PatientInformation
from django.contrib import messages
from django.contrib.auth.models import User
import random
from django.core.files.storage import FileSystemStorage
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

#  new imports
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
import http.client
from django.conf import settings

# xhtml2html
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from keras.models import model_from_json
import cv2   # (pip install opencv-python-headless)

# twilio
from twilio.rest import Client

cl = load_model('models/Covid_model.h5')

# Create your views here.


def index(request):
    return render(request, "index.html")


def predictImage(request):
    # pass
    print(request.POST.dict())
    print(request.FILES.getlist('uploadFromPC'))
    fileObj = request.FILES['uploadFromPC']
    fs = FileSystemStorage()
    pathname = fs.save(fileObj.name, fileObj)
    pathname = fs.url(pathname)
    imageTest = '.'+pathname

    # filter model
    json_file = open('models/filter_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/filter_model.h5")
    print("Loaded model from disk")
    loaded_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    imag = cv2.imread(imageTest)
    imag = cv2.resize(imag, (50, 50), cv2.INTER_AREA)
    imag = imag.reshape(1, 50, 50, 3)

    result = loaded_model.predict_classes(imag)
    print(result)
    if (result[0][0] == 0):
        mobile = request.session['mobile']
        return render(request, "testNow.html", {'pathname': pathname, 'error': 'object', 'mobile': mobile})
    else:
        print("I guess this must be a xray!")

    test_image = image.load_img(imageTest, target_size=(224,224))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    res = cl.predict(test_image)
    if res[0][0] == 0:
        prediction = 'COVID DETECTED'
    else:
        prediction = 'NO COVID DETECTED'
    print(prediction)

    mobile = request.session['mobile']
    patient = PatientInformation.objects.filter(mobile=mobile).first()
    patient.result = prediction
    patient.x_ray = fileObj
    patient.save()
    print("==============mobile"+mobile)
    send_email(request, mobile)
    return render(request, "testNow.html", {'pathname': pathname, 'prediction': prediction, 'mobile': mobile})


def symptoms(request):
    return render(request, "symptoms.html")


def prevention(request):
    return render(request, "prevention.html")


def contact(request):
    print(request.POST)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['fname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if fname and lname and email and subject and message:
            object = ContactForm(first_name = fname, last_name = lname, email = email, subject = subject, message = message)
            # print(object.id)
            object.save()
            messages.success(request, 'Form submission successful')

    return render(request, "contact.html")


def testnow(request):
    mobile = request.session['mobile']
    return render(request, 'testNow.html', {'mobile': mobile})

# ================================================= NEW CHANGES ==================================================


def register(req):
    number = User.objects.filter(is_active=True).count()
    print(str(number) + "===================")
    if req.method == "POST":
        email = req.POST.get('email')
        mobile = req.POST.get('mobile')
        name = req.POST.get('fname')+' '+req.POST.get('lname')
        gender = req.POST.get('gender')
        age = req.POST.get('age')
        address = req.POST.get('address')
        aadhaar_card = req.POST.get('aadhaar_card')


        # we create a check for user
        duplicate_check = User.objects.filter(username = name).first()
        if duplicate_check:
            ctx = {"msg": "Username", "class": "danger", 'number': number}
            return render(req, "registration.html", ctx)


        if PatientInformation.objects.filter(mobile=mobile).exists():
            ctx = {"msg": "mobile", "class": "danger", 'number': number}
            return render(req, "registration.html", ctx)

        us = User(email=email, username=name)
        us.is_active = False
        us.save()
        otp = str(random.randint(1000, 9999))
        patient = PatientInformation(user = us, name = name, email_id = email, age = age, gender = gender, mobile = mobile, otp=otp, aadhaar_card = aadhaar_card, address = address)
        patient.save()

        # calling helper function
        send_otp(mobile, name, otp)
        req.session['mobile'] = mobile  # new session

        print("==============mobile"+mobile)
        return redirect('otp')
    return render(req, 'registration.html')


def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if PatientInformation.objects.filter(mobile=mobile).exists():
            patient = PatientInformation.objects.filter(mobile=mobile).first()
            print(patient)
            if otp == patient.otp:
                us = patient.user
                us.is_active = True
                us.save()
                return redirect('testNow')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp_verify.html', context)

    return render(request, 'otp_verify.html', context)


def send_otp(mobile, name, otp):
    print("FUNCTION CALLED")
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # authkey = settings.AUTH_KEY
    # headers = {'content-type': "application/json"}
    # url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    # conn.request("GET", url, headers=headers)
    # res = conn.getresponse()
    # data = res.read()
    # print(data)
    # return None

    # twilio
    account_sid = 'AC85f2001e8ebb3f8bf4688e1a5cc5184e'
    auth_token = '3bc6057aa867ef48c8af64b6664a55eb'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='MGbbceb1a00185ef587293b3e1be718ccc',
        body='Hi '+name+'. Thank you for opting this website. Your one time password is '+otp,
        to=mobile
    )
    print(mobile +" "+ otp)
    return None



def login(req):
    if req.method == "POST":
        mobile = req.POST.get('mobile')
        patient = PatientInformation.objects.filter(mobile=mobile).first()
        if patient == None:
            return render(req, 'login.html', {'message': 'You are not registered !'})
        us = patient.user
        if patient and us.is_active:
            req.session['mobile'] = mobile  # new session
            return redirect('testNow')
        else:
            return render(req, 'login.html', {'message': 'Your otp is not verified yet !'})

    return render(req, 'login.html')


def send_email(req, mobile):
    patient = PatientInformation.objects.filter(mobile=mobile).first()
    user = patient.user
    to_mail = patient.email_id
    print(to_mail)

    # mail_subject = 'Your reports'
    # message = render_to_string('Email.html', {
    #     'mobile': mobile
    # })
    # email = EmailMessage(
    #     mail_subject, message, to=[to_mail]
    # )
    # email.send()
    t = get_template('Email.html').render({'mobile':mobile, 'patient': patient})
    msg = EmailMultiAlternatives("Your final reports", t, settings.EMAIL_HOST_USER, [to_mail])
    msg.attach_alternative(t, "text/html")
    msg.send()
    # return HttpResponse('Please confirm your email address to complete the registration')
    return redirect('testNow')


def render_pdf_view(request, *args, **kwargs):
    mobile = kwargs.get('mobile')
    patient = get_object_or_404(PatientInformation, mobile = mobile)
    template_path = 'user_printer.html'
    image = patient.x_ray
    context = {'myvar': mobile, 'image': image, 'patient': patient}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def cases(request):
    return render(request, "cases.html")
