from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,VerifyCodeForm,UserLoginForm
import random
from utils import send_Otp_Code
from .models import OtpCode,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


class UserRegisterView (View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'


    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})  #send form to register page

    def post(self,request):
        form =self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)  #create random code
            send_Otp_Code(form.cleaned_data['phone_number'],random_code) #send phone number and code random to utils
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'],code=random_code)
            request.session['user_registration_info'] = {
                'phone_number' : form.cleaned_data['phone_number'],
                'full_name' : form.cleaned_data['full_name'],
                'password' : form.cleaned_data['password'],
            }
            messages.success(request,'we send for you a code','success')
            return redirect('accounts:verify_code')
        return render(request,self.template_name,{'form':form})




class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/verify.html',{'form':form})

    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'],
                                         user_session['full_name'],user_session['password'])
                code_instance.delete()
                messages.success(request,'you registered.','success')
                return redirect('home:home')

            else:
                messages.error(request,'this code is wrong...','danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')



class UserLoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number=cd['phone_number'],password=cd['password'])
            if user is not None:
                    login(request,user)
                    messages.success(request,'you login successfully...','success')
                    return redirect('home:home')

            messages.error(request, 'phone or password is wrong...', 'warning')

        return render(request,self.template_name,{'form':form})

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')