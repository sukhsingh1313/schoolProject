from django.shortcuts import render,redirect,HttpResponse
from .models import *



def AdmissionGuidelines_view(request):
    school_guidelines = School_Guidelines.objects.all()
    admission_guidelines = Admission_Guidelines.objects.all()
    context = {
        'school_guidelines':school_guidelines,
        'admission_guidelines':admission_guidelines,
        }
    return render(request,'Admission/admission_guides.html',context)



def online_application_view(request):
    
    return render(request,'admission/online_application.html')




def admission_form_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        join_class_id = request.POST.get('join_class')
        additional_info = request.POST.get('additional_info')

        # Validate and save data
        join_class = Class.objects.get(id=join_class_id)
        admission = AdmissionForm(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            join_class=join_class,
            additional_info=additional_info
        )
        admission.save()
        return redirect('online_applications')  

   
    classes = Class.objects.all()
    return render(request, 'admission/AddmissionForm.html', {'classes': classes})
