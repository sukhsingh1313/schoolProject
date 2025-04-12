from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import logout
import random
import string


# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# Student registration view
def register_student(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        mothername = request.POST.get('mothername')
        fathername = request.POST.get('fathername')
        address = request.POST.get('address')
        gender = request.POST.get('inlineRadioOptions')
        state = request.POST.get('state')
        city = request.POST.get('city')
        dob = request.POST.get('dob')
        pincode = request.POST.get('pincode')
        course = request.POST.get('course')
        email = request.POST.get('email')

        # Check if the email is already registered
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect("student_login_view")

        # Generate a password for the new user
        password = generate_password()

        # Create a new user instance for authentication
        user = User.objects.create_user(username=email, password=password, first_name=firstname, last_name=lastname)
        user.save()

        # Create a new student instance
        student = Student(
            firstname=firstname,
            lastname=lastname,
            mothername=mothername,
            fathername=fathername,
            address=address,
            gender=gender,
            state=state,
            city=city,
            dob=dob,
            pincode=pincode,
            course=course,
            email=email
        )
        student.save()

        # Send a welcome email with the login credentials
        send_mail(
            'Welcome to Student Portal',
            f'Dear {firstname},\n\nYour account has been created successfully.\nYour login credentials are:\nEmail: {email}\nPassword: {password}\n\nPlease change your password after logging in for the first time.',
            'admin@example.com',
            [email],
            fail_silently=False,
        )

        messages.success(request, "Registration successful! Check your email for login details.")
        return redirect("student_login_view")  # Redirect to the login page after successful registration

    return render(request, 'Accounts/student_signup.html')  # Render the registration form


# Login view
def student_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to the home page
        else:
            if User.objects.filter(username=email).exists():
                messages.error(request, "Invalid password.")
            else:
                messages.error(request, "Invalid email or password.")

    return render(request, "Accounts/student_login.html")  # Render the login form


# Custom password reset view
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(username=email).first()
        print(f'user is  :- {user} and for password reset enter email:-  {email}')
        if user:
            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build password reset URL
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )

            print(reset_url)
            # Send password reset email
            subject = "Password Reset Request"
            message = render_to_string("Accounts/Passwords/password_reset_email.html", {"reset_url": reset_url})
            send_mail(subject, "", "admin@example.com", [email], fail_silently=False,html_message=message )
            print("Email sent successfully")
            messages.success(request, "A password reset link has been sent to your email.")
        else:
            messages.error(request, "No user found with this email address.")

    return render(request, "Accounts/Passwords/password_reset_form.html")  # Render the password reset form





# Password reset confirm view
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("student_login_view")  # Redirect to login page
            else:
                messages.error(request, "Passwords do not match.")
        
        return render(request, "Accounts/Passwords/password_reset_confirm.html")  # Render form to set new password

    messages.error(request, "The password reset link is invalid or has expired.")
    return redirect("password_reset")  # Redirect back to the password reset form




def logout_view(request):
    logout(request)
    return redirect('home')