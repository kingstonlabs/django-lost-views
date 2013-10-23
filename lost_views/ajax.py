from django.template.loader import render_to_string
from django.views.generic import DetailView, UpdateView, FormView

from .generic import DetailViewWithForm, FormsetView, DetailViewWithFormset, DetailViewWithFormAndFormset
from .response import JsonResponse


class AjaxDetailMixin(object):
    def get_object(self, queryset=None):
        pk = self.request.POST.get(self.pk_url_kwarg, None)
        if pk:
            self.kwargs.update({self.pk_url_kwarg: pk})
		
        slug = self.request.POST.get(self.slug_url_kwarg, None)
        if slug:
            self.kwargs.update({self.slug_url_kwarg: slug})
        return super(AjaxDetailMixin, self).get_object(queryset)


class AjaxPopupMixin(object):
    title = ''

    def get_title(self):
        return self.title
    
    def render_to_response(self, context, extra_context={}):
        output_html = render_to_string(self.template_name, context)
        response_data = {'result': 'ok', 'html': output_html, 'title': self.get_title()}
        response_data.update(extra_context)
        return JsonResponse(response_data)

    def post(self, request, *args, **kwargs):
        if 'popup' in self.request.POST:
            self.request.method = 'GET'
            return self.get(request, *args, **kwargs)
        return super(AjaxPopupMixin, self).post(request, *args, **kwargs)


class AjaxDetailView(AjaxDetailMixin, AjaxPopupMixin, DetailView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=self.object))


class AjaxDeleteView(AjaxDetailMixin, DetailView):
    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'result': 'ok'})


class AjaxUpdateView(AjaxPopupMixin, UpdateView):
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(object=self.object, form=form), {'status': 'form_invalid'})

    def form_valid(self, form):
        form.save()
        return JsonResponse({'result': 'ok', 'status': 'form_valid'})


class AjaxDetailViewWithForm(AjaxPopupMixin, DetailViewWithForm):
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(object=self.object, form=form), {'status': 'form_invalid'})

    def form_valid(self, form):
        form.save()
        return JsonResponse({'result': 'ok', 'status': 'form_valid'})

    def get_form_kwargs(self):
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT') and 'popup' not in self.request.POST \
            and self.pk_url_kwarg not in self.request.POST and self.slug_url_kwarg not in self.request.POST:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs


class AjaxDetailViewWithModelForm(AjaxDetailViewWithForm):
    def get_form_kwargs(self):
        kwargs = super(AjaxDetailViewWithModelForm, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs


class AjaxFormView(AjaxPopupMixin, FormView):
    pass


class AjaxFormsetView(AjaxPopupMixin, FormsetView):
    pass


class AjaxDetailViewWithFormset(AjaxPopupMixin, DetailViewWithFormset):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxDetailViewWithFormset, self).get(request, *args, **kwargs)
    
    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset), {'status': 'form_invalid'})

    def form_valid(self, formset):
        formset.save()
        return JsonResponse({'result': 'ok', 'status': 'form_valid'})


class AjaxDetailViewWithFormAndFormset(AjaxPopupMixin, DetailViewWithFormAndFormset):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxDetailViewWithFormAndFormset, self).get(request, *args, **kwargs)
    
    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset), {'status': 'form_invalid'})

    def form_valid(self, form, formset):
        return JsonResponse({'result': 'ok', 'status': 'form_valid'})
