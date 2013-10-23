django-lost-views
=================

Some useful Django views...

## Generic Views
### MultipleFormView
Define your form names and classes in the dictionary `form_classes`. The button names in the template should match your form names.

Example view:

    from lost_views import MultipleFormView

	class LoginOrRegisterView(MultipleFormView):
		template_name = 'accounts/login_or_register.html'
		form_classes = {
			'login': LoginForm,
			'registration': RegistrationForm,
		}

		def login_form_valid(self, form):
			login(self.request, form.authed_user)
			return HttpResponseRedirect(self.get_success_url())

		def registration_form_valid(self, form):
			form.save()
			login(self.request, form.authed_user)
			return HttpResponseRedirect(self.get_success_url())

		def get_success_url(self):
			return self.request.GET.get("next", reverse('homepage'))

Example template:

	<h2>Log In</h2>
	<form id='login' method='post'>
		{% csrf_token %}
		{{ forms.login }}
		<button name='login'>Log In</button>
	</form>

	<h2>Register</h2>
	<form id='register' method='post'>
		{% csrf_token %}
		{{ forms.registration }}
		<button name='registration'>Register</button>
	</form>

### DetailViewWithForm
### DetailViewWithMultipleForms
### FormsetView
### DetailViewWithFormset
### FormWithFormsetView
### DetailViewWithFormAndFormset


## Ajax Views
### AjaxDetailView
### AjaxDeleteView  
### AjaxUpdateView  
### AjaxDetailViewWithForm  
### AjaxDetailViewWithModelForm  
### AjaxFormView  
### AjaxFormsetView  
### AjaxDetailViewWithFormset  
### AjaxDetailViewWithFormAndFormset
