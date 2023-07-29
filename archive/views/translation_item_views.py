from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from ..models import Segment
from ..forms.translation_item_forms import SegmentForm


class TranslationUpdateItemView(LoginRequiredMixin, UpdateView):
    model = Segment
    form_class = SegmentForm
    template_name = "segment_update.html"

    def form_valid(self, form):
        updated_segment = form.save(commit=False)
        updated_segment.updated_by = self.request.user
        updated_segment.save()

        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return HttpResponseRedirect(previous_url)

        return HttpResponseRedirect(reverse_lazy("home"))

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(TranslationUpdateItemView, self).post(request, *args, **kwargs)


class TranslationDeleteItemView(LoginRequiredMixin, DeleteView):
    model = Segment
    template_name = "segment_delete.html"

    def get_success_url(self):
        if self.request.GET.get("previous_url"):
            previous_url = self.request.GET.get("previous_url")
            return previous_url
        return reverse_lazy("home")

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            if request.GET.get("previous_url"):
                previous_url = request.GET.get("previous_url")
                return HttpResponseRedirect(previous_url)
        else:
            return super(TranslationDeleteItemView, self).post(request, *args, **kwargs)
