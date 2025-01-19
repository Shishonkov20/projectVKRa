from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import FormMixin

from .forms import *
from .models import *


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user, type(self.request.user))
        if str(self.request.user) == "AnonymousUser":
            context['warning'] = 'Зарегистрируйтесь или войдите, чтобы посмотреть свои проекты'
            return context
        else:
            context['projects'] = WorkerInProject.objects.filter(worker=self.request.user)
            context['user'] = self.request.user
            context['ddd'] = AdvUser.objects.get(username=self.request.user)
            return context


class ProjectDetailView(DetailView, FormMixin):
    model = Project
    template_name = 'workonproject.html'
    context_object_name = 'project'
    form_class = WorkOnProjectForm
    success_url = reverse_lazy('main_page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.get_object()
        self.object.worker = self.request.user
        self.object.save()
        return super().form_valid(form)


def project_detail_view(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == "POST":
        workForm = WorkOnProjectForm(request.POST)
        print(project.pk)
        if workForm.is_valid():
            #instance = workForm.save(commit=False)
            workForm.worker = request.user
            workForm.save()
            return HttpResponseRedirect(reverse('main_page'))
        else:
            context = {
                'project': project,
                'workForm': workForm
            }
            return render(request, 'workonproject.html', context)
    else:
        workForm = WorkOnProjectForm()
        context = {
            'project': project,
            'workForm': workForm
        }
        return render(request, 'workonproject.html', context)


def works_by_project(request, pk):
    wokrs = WorkOnProject.objects.filter(project_id=pk)
    project = Project.objects.get(pk=pk)
    context = {
        "works": wokrs,
        "project": project,
    }
    return render(request, 'works_by_project.html', context)


class RegistrationFormView(CreateView):
    model = AdvUser
    form_class = AdvUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = AdvUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['films'] = Project.objects.all()
        return context


class MainLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('main_page')

    def get_success_url(self):
        return self.success_url


class MainLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'