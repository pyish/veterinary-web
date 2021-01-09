from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, reverse

from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView
#from django.views.generic import View

from django.contrib.auth import get_user_model

from django.contrib.auth import login, authenticate
from .models import User, Sick_Approach_Form
from django.contrib.auth.forms import AuthenticationForm   



User = get_user_model()

class VetOfficerSignUpView(CreateView):
	def get_success_url(form):
		return reverse('login')
    
	model = User
	form_class = forms.VetOfficerSignUpForm
	template_name = 'user/register.html'

	def get_context_data(form, **kwargs):
		context = super(VetOfficerSignUpView, form).get_context_data(**kwargs)
		context['form'] = form.form_class
		return context
    

class FarmerSignUpView(CreateView):
	def get_success_url(form):
		return reverse('login')
	model = User
	form_class = forms.FarmerSignUpForm
	template_name = 'user/register.html'

	def get_context_data(form, **kwargs):
		context = super(FarmerSignUpView, form).get_context_data(**kwargs)
		context['form'] = form.form_class
		return context


class StudentSignUpView(CreateView):
	def get_success_url(form):
		return reverse('login')
        
	model = User
	template_name = 'user/register.html'
	form_class = forms.StudentSignUpForm
	
	def get_context_data(form, **kwargs):
		context = super(StudentSignUpView, form).get_context_data(**kwargs)
		context['form'] = form.form_class
		return context
		

def user_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_authenticated and user.is_vet_officer:
               return redirect('vet-portal')
            elif user.is_authenticated and user.is_farmer:
                return redirect('farmer-portal')
            elif user.is_authenticated and user.is_student:
                return redirect('student-portal')    
        else:
            messages.error(request, 'invalid Credentials')
    
    return render(request, 'user/login.html', {'form':form})



def clinical_approach(request):
    return render(request, 'user/clinical_approach.html') 


def sick_approach(request):
    if request.method == "POST":
        form = forms.SickApproachForm(request.POST)

        if form.is_valid():
            form.is_sick_approach_form = True
            form.farm_name = form.cleaned_data.get('farm_name')
            form.species_affected = form.cleaned_data.get('species_affected')            
            form.num_of_species_affected = form.cleaned_data.get('num_of_species_affected')
            form.form = Sick_Approach_Form.objects.create(form=form)
            form.disease_nature = form.cleaned_data.get('nature_of_disease')
            form.clinical_sign = form.cleaned_data.get('clinical_sign')
            form.disease_diagnosis = form.cleaned_data.get('disease_diagnosis')
            form.differential_diagnosis = form.cleaned_data.get('differential_diagnosis')
            form.final_diagnosis = form.cleaned_data.get('final_diagnosis')
            form.sickness_duration = form.cleaned_data.get('sickness_duration')
            form.sickness_history = form.cleaned_data.get('sickness_history')
            form.drug_choices = form.cleaned_data.get('drug_choice')
            form.treatment_duration = form.cleaned_data.get('treatment_duration')
            form.start_dose_date = form.cleaned_data.get('start_dose_date')
            form.prognosis = form.cleaned_data.get('prognosis')
            form.harmony_with_clinic_signs_and_lab = form.cleaned_data.get('pathological_conditions_in_harmony_with_the_clinic_signs_and_lab_reports')
            form.cause_of_death_if_in_no_harmony = form.cleaned_data.get('cause_of_the_death_if_no')
            form.disease_one_of_the_zoonotic = form.cleaned_data.get('disease_zoonotic')
            form.advice_given_if_zoonotic = form.cleaned_data.get('advice_given_if_zoonotic')
            form.relapse = form.cleaned_data.get('relapse')
            form.cause_if_relapse = form.cleaned_data.get('cause_if_relapse')
            form.save()
            

        # if form.is_valid():
        #     form.save()
        #     farm_name = form.cleaned_data.get('username')
        #     messages.success(request,f'Details for {farm_name} Succesfully Saved')
        #     return redirect('clinical-approach')

    else:
        form = forms.SickApproachForm()

    context = {
        'sick_approach_form':form
        }
    return render(request, 'user/sick_approach.html', context) 







# class SickApproachFormView(CreateView):
# 	def get_success_url(form):
# 		return reverse('vet-portal')
        
# 	model = Sick_Approach_Form
# 	template_name = 'user/sick_approach.html'
# 	form_class = forms.SickApproachForm
	
# 	def get_context_data(form, **kwargs):
# 		context = super(SickApproachFormView, form).get_context_data(**kwargs)
# 		context['sick_approach_form'] = form.form_class
# 		return context

def dead_approach(request):
    if request.method == "POST":
        form = forms.DeadApproachForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('farm_name')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('clinical-approach')

    else:
        form = forms.DeadApproachForm()

    context = {
        'dead_approach_form':form
    }
    return render(request, 'user/dead_approach.html', context)  

def surgical_approach(request):
    if request.method == "POST":
        form = forms.SurgicalApproachForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('farm_name')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('clinical-approach')

    else:
        form = forms.SurgicalApproachForm()

    context = {
        'surgical_approach_form':form
    }
    return render(request, 'user/surgical_approach.html', context)  


def deworming(request):
    if request.method == "POST":
        form = forms.DewormingForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {deworming} Succesfully Saved')
            return redirect('deworming')

    else:
        form = forms.DewormingForm()

    context = {
        'deworming_form':form
    }
    return render(request, 'user/deworming.html', context) 

    
def vaccination(request):
    if request.method == "POST":
        form = forms.vaccination_form(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {vaccination} Succesfully Saved')
            return redirect('vaccination')

    else:
        form = forms.vaccination_form()

    context = {
        'vaccination_form':form
    }
    return render(request, 'user/vaccination.html', context)


def breeding_record(request):
    return render(request, 'user/breeding_record.html')

def artificial_insemination(request):
    if request.method == "POST":
        form = forms.ArtificialInseminationForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('artificial-insemination')

    else:
        form = forms.ArtificialInseminationForm()

    context = {
        'artificial_insemination_form':form
    }
    return render(request, 'user/artificial_insemination.html', context) 


def calf_registration(request):
    if request.method == "POST":
        form = forms.CalfRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('calf-registration')

    else:
        form = forms.CalfRegistrationForm()

    context = {
        'calf_registration_form':form
    }
    return render(request, 'user/calf_registration.html', context)


def livestock_inventory(request):
    if request.method == "POST":
        form = forms.LivestockInventoryForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('livestock-inventory')

    else:
        form = forms.LivestockInventoryForm()

    context = {
        'livestock_inventory_form':form
    }
    return render(request, 'user/livestock_inventory.html', context)


def pregnancy_diagnosis(request):
    if request.method == "POST":
        form = forms.PregnancyDiagnosisForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {farm_name} Succesfully Saved')
            return redirect('pregnancy_diagnosis')

    else:
        form = forms.PregnancyDiagnosisForm()

    context = {
        'pregnancy_diagnosis_form':form
    }
    return render(request, 'user/pregnancy_diagnosis.html', context)
    

def consultation(request):
    if request.method == "POST":
        form = forms.FarmConsultationForm(request.POST)

        if form.is_valid():
            form.save()
            farm_name = form.cleaned_data.get('username')
            messages.success(request,f'Details for {consultation} Succesfully Saved')
            return redirect('consultation')

    else:
        form = forms.FarmConsultationForm()

    context = {
        'consultation_form':form
    }
    return render(request, 'user/consultation.html', context)



