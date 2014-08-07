django-lost-views
=================

Some useful Django views to supplement the existing class based views.

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

Example:

class BookDetailView(DetailViewWithForm):
    template_name = "books/book_detail.html"
    model = Book
    form_class = ContactForm
    
    def form_valid(self, form):
        return HttpResponseRedirect(reverse('homepage'))


### DetailViewWithMultipleForms

Example:

class BookDetailWithLoginOrRegisterView(DetailViewWithMultipleForms):
    template_name = "books/book_detail.html"
    model = Book
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


### FormsetView

Example:

class ManagementView(FormsetView):
    template_name = 'accounts/manage.html'
    formset_class = ManagementFormset


### DetailViewWithFormset

Example:

class OpeningHoursView(DetailViewWithFormset):
    template_name = 'shops/update_opening_hours.html'
    model = Shop
    formset_class = OpeningHoursFormset


### FormWithFormsetView

Example:

class SomeView(DetailViewWithFormAndFormset):
    template_name = 'template.html'
    form_class = SomeForm
	formset_class = SomeFormset
    
    def form_valid(self, form, formset):       
        return HttpResponseRedirect(self.get_success_url())


### DetailViewWithFormAndFormset

Example:

class ShopView(DetailViewWithFormAndFormset):
    template_name = 'template.html'
    model = Shop
    form_class = ShopUpdateForm
	formset_class = OpeningHoursFormset
    
    def form_valid(self, form, formset):       
        return HttpResponseRedirect(self.get_success_url())


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
