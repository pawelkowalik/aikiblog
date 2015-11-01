# -*- coding: utf-8 -*-
from django.views import generic
from django.contrib.auth.models import User
from aikiblog.models import Training, User, Dojo, News, TechTren


import datetime
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from annoying.decorators import render_to
from aikiblog.forms import SaveUserDataForm, AddTrainingForm, AddTechniquesForm
from django.shortcuts import render

User = get_user_model()


class DojoList(generic.ListView):
    template_name = 'aikiblog/dojo_list.html'
    model = Dojo
    paginate_by = 10
    context_object_name = 'dojo_list'
    queryset = Dojo.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(DojoList, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class StageList(generic.ListView):
    template_name = 'aikiblog/stage_list.html'
    model = Training
    paginate_by = 10
    context_object_name = 'stage_list'
    queryset = Training.objects.filter(type="S").order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(StageList, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TrainingList(generic.ListView):
    model = Training
    paginate_by = 10
    context_object_name = 'training_list'
    queryset = Training.objects.filter(type="T").order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(TrainingList, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class NewsList(generic.ListView):
    model = News
    paginate_by = 6
    context_object_name = 'news_list'
    queryset = News.objects.order_by('-posted_date')

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class DojoDetail(generic.DetailView):
    model = Dojo

    def get_context_data(self, **kwargs):
        context = super(DojoDetail, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TrainingDetail(generic.DetailView):
    model = Training

    def get_context_data(self, **kwargs):
        context = super(TrainingDetail, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class UserDetail(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]
        context['all_user_trainings'] = Training.objects.order_by('-date')

        return context


class NewsDetail(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['all_trainings'] = Training.objects.order_by('-date')[:7]

        return context


@render_to('save_user_data.html')
def save_user_data(request, user_id):
        form = SaveUserDataForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(user_id)
            return HttpResponseRedirect('/')
        else:
            return {'save_user_data_form': form}


@render_to('add_training.html')
def add_training(request):
    form = AddTrainingForm(request.POST or None, request=request)
    if form.is_valid():
        user = request.user
        training = Training.objects.create(
            date=form.cleaned_data['date'],
            place=form.cleaned_data['place'],
            sensei=form.cleaned_data['sensei'],
            notes=form.cleaned_data['notes'],
            type='T',
            user=user
            )
        training.techniques.add(*form.cleaned_data['techniques'])

        return HttpResponseRedirect('/')
    else:
        return render(request, 'add_training.html', {'form': form})


@render_to('add_stage.html')
def add_stage(request):
    form = AddTrainingForm(request.POST or None, request=request)
    if form.is_valid():
        user = request.user
        training = Training.objects.create(
            date=form.cleaned_data['date'],
            place=form.cleaned_data['place'],
            sensei=form.cleaned_data['sensei'],
            notes=form.cleaned_data['notes'],
            type='S',
            user=user
            )
        training.techniques.add(*form.cleaned_data['techniques'])

        return HttpResponseRedirect('/')
    else:
        return render(request, 'add_stage.html', {'form': form})


@render_to('add_techniques.html')
def add_techniques(request):
    user = request.user
    form = AddTechniquesForm(request.POST or None, request=request)
    techniques = TechTren.objects.filter(user=user).order_by('-date')
    if form.is_valid():
        technique = TechTren.objects.create(
            date=form.cleaned_data['date'],
            stand=form.cleaned_data['stand'],
            attack=form.cleaned_data['attack'],
            technique=form.cleaned_data['technique'],
            mistakes=form.cleaned_data['mistakes'],
            user=user
            )

        return HttpResponseRedirect('/add_techniques#content')
    else:
        return render(request, 'add_techniques.html', {'form': form, 'techniques': techniques})
