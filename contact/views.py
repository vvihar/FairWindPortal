import datetime

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ContactForm, ContactThreadForm
from .models import Contact, ContactItem

# Create your views here.


class ContactCreate(CreateView):
    """新規連絡"""

    model = Contact
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get_success_url(self):
        return reverse_lazy("contact:thread", kwargs={"pk": self.object.pk})


class ContactUpdate(UpdateView):

    model = Contact
    form_class = ContactForm
    template_name = "contact/contact_form.html"

    def get_success_url(self):
        return reverse_lazy("contact:thread", kwargs={"pk": self.object.pk})


class ContactList(ListView):
    """連絡一覧"""

    template_name = "contact/contact_list.html"
    model = Contact
    paginate_by = 10


class ContactThreadList(DetailView):
    """連絡スレッド一覧"""

    template_name = "contact/contact_thread.html"
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_items"] = ContactItem.objects.filter(contact=self.object)
        return context


class ContactThreadPost(CreateView):

    template_name = "contact/contact_thread_form.html"
    model = ContactItem
    form_class = ContactThreadForm

    def get_success_url(self):
        return reverse_lazy("contact:thread", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        """フォームが有効な場合"""
        contact = get_object_or_404(Contact, pk=self.kwargs["pk"])
        item = form.save(commit=False)
        item.person_updated = self.request.user
        item.contact = contact
        item.save()
        return super().form_valid(form)

    def get_initial(self):
        today = str(datetime.date.today())
        return {
            "date": today,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = ContactItem.objects.filter(contact=self.kwargs["pk"])
        senders = posts.values_list("sender", flat=True)
        recipients = posts.values_list("recipient", flat=True)
        context["datalist"] = list(senders) + list(recipients)
        context["thread"] = Contact.objects.get(pk=self.kwargs["pk"])
        return context


class ContactThreadUpdate(UpdateView):

    template_name = "contact/contact_thread_form.html"
    model = ContactItem
    form_class = ContactThreadForm

    def get_object(self):
        return get_object_or_404(ContactItem, pk=self.kwargs["id"])

    def get_success_url(self):
        return reverse_lazy("contact:thread", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        """フォームが有効な場合"""
        contact = get_object_or_404(Contact, pk=self.kwargs["pk"])
        item = form.save(commit=False)
        item.person_updated = self.request.user
        item.contact = contact
        item.save()
        return super().form_valid(form)

    def get_initial(self):
        date = str(self.get_object().date)
        return {
            "date": date,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = ContactItem.objects.filter(contact=self.kwargs["pk"])
        senders = posts.values_list("sender", flat=True)
        recipients = posts.values_list("recipient", flat=True)
        context["datalist"] = list(senders) + list(recipients)
        context["thread"] = self.get_object().contact
        return context
