from django.http import HttpResponseRedirect
from django.views.generic import DetailView, FormView


class MultipleFormView(FormView):
    form_class = None
    form_name = None
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(forms=self.get_forms()))
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(forms=self.get_forms())) 

    def form_valid(self, form):
        return getattr(self, "%s_form_valid" % self.form_name)(form)

    def get_forms(self):
        forms = {}
        for form_name, form_class in self.get_form_classes().items():
            forms[form_name] = self.get_form(form_class)
        return forms
    
    def get_form_classes(self):
        return self.form_classes

    def get_form_class(self):
        if self.request.method in ('POST', 'PUT'):
            if not self.form_class:
                for form_name, form_class in self.get_form_classes().items():
                    if form_name in self.request.POST:
                        self.form_class = form_class
                        self.form_name = form_name
                        break
                if not self.form_class:
                    raise Exception("Button name does not match any items in form_classes.")
            return self.form_class

    def get_form(self, form_class):
        if form_class == self.get_form_class():
            return form_class(**self.get_form_kwargs())
        else:
            return form_class()


class DetailViewWithForm(DetailView, FormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class) 
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context) 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DetailViewWithForm, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(DetailViewWithForm, self).get_context_data(*args, **kwargs)
        context.update(kwargs)
        return context

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class DetailViewWithMultipleForms(DetailView, MultipleFormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, forms=self.get_forms())
        return self.render_to_response(context) 


class FormsetView(FormView):
    def get(self, request, *args, **kwargs):
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())
    
    def get_formset_kwargs(self):
        return self.get_form_kwargs()

    def post(self, request, *args, **kwargs):
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)


class DetailViewWithFormset(FormsetView, DetailView):
    def get_context_data(self, **kwargs):
        kwargs['object'] = self.object
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            kwargs[context_object_name] = self.object
        return kwargs
    
    def get_formset_kwargs(self):
        kwargs = super(DetailViewWithFormset, self).get_formset_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs 
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DetailViewWithFormset, self).post(request, *args, **kwargs)


class FormWithFormsetView(FormView):
    def get_formset_class(self):
        return self.formset_class 

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs()) 

    def get_formset_kwargs(self):
        return self.get_form_kwargs()

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def form_valid(self, form, formset):
        return HttpResponseRedirect(self.get_success_url()) 

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)


class DetailViewWithFormAndFormset(FormWithFormsetView, DetailView):
    def get_context_data(self, **kwargs):
        kwargs['object'] = self.object
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            kwargs[context_object_name] = self.object
        return kwargs
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DetailViewWithFormAndFormset, self).post(request, *args, **kwargs)
