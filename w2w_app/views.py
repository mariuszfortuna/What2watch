from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from w2w_app.forms import AddPersonModelForm
from w2w_app.models import Person


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, template_name='home.html')


class PersonView(View):
    def get(self, request, person_id):
        person = Person.objects.get(pk=person_id)
        if person is not None:
            return render(request, 'person.html', {'person': person})
        else:
            raise Http404('Person does not exist')


class AddPersonModelFormView(View):

    def get(self, request):
        form = AddPersonModelForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = AddPersonModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('persons_list')
        return render(request, 'form.html', {'form': form})


class PersonsGenericListView(ListView):
    model = Person
    template_name = 'persons_list.html'