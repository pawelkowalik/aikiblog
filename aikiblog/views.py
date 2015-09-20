# -*- coding: utf-8 -*-
from django.views import generic
from django.contrib.auth.models import User

from aikiblog.models import Training, User, Dojo, News


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
    paginate_by = 10
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