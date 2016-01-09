# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
import time
import calendar as calendar_library

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from annoying.decorators import render_to

from .forms import (SaveUserDataForm, AddTrainingForm, AddTechniquesForm,
                    TrainingCommentForm)
from .models import Training, User, Dojo, News, TechTren, TrainingComment, Technique
from .forms import UpdateTrainingForm

User = get_user_model()
mnames = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik',
          'Listopad', 'Grudzień']


def _get_techniques_by_user(user):
    techniques = TechTren.objects.filter(user__id=user.id).order_by('-date')
    choices = []
    for t in techniques:
        choices.append((t.id, t.slug))
    return choices


class DojoList(generic.ListView):
    template_name = 'aikiblog/dojo_list.html'
    model = Dojo
    paginate_by = 10
    context_object_name = 'dojo_list'
    queryset = Dojo.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(DojoList, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class StageList(generic.ListView):
    template_name = 'aikiblog/stage_list.html'
    model = Training
    paginate_by = 10
    context_object_name = 'stage_list'
    queryset = Training.objects.filter(type="S").order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(StageList, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TrainingList(generic.ListView):
    model = Training
    paginate_by = 10
    context_object_name = 'training_list'
    queryset = Training.objects.filter(type="T").order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(TrainingList, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class NewsList(generic.ListView):
    model = News
    paginate_by = 6
    context_object_name = 'news_list'
    queryset = News.objects.order_by('-posted_date')

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TechniqueList(generic.ListView):
    model = TechTren
    paginate_by = 20
    context_object_name = 'techtren_list'

    def get_context_data(self, **kwargs):
        context = super(TechniqueList, self).get_context_data(**kwargs)
        technique = get_object_or_404(Technique, slug=self.kwargs['slug'])
        context['technique'] = technique
        context['last_trainings'] = Training.objects.order_by('-date')[:7]
        return context

    def get_queryset(self, **kwargs):
        technique = Technique.objects.get(slug=self.kwargs['slug'])
        user = self.request.user
        return TechTren.objects.filter(technique=technique, user=user).order_by('-date')


class DojoDetail(generic.DetailView):
    model = Dojo

    def get_context_data(self, **kwargs):
        context = super(DojoDetail, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TrainingDetail(generic.FormView):
    form_class = TrainingCommentForm
    template_name = 'aikiblog/training_detail.html'

    def get_success_url(self):
        slug = self.kwargs['slug']
        url = reverse('training-detail', kwargs={'slug': slug})
        return url

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = TrainingCommentForm(request.POST or None)
        if form.is_valid():
            user = request.user
            training_comment = TrainingComment.objects.create(
                training=self.get_training(),
                posted_date=datetime.now(),
                text=form.cleaned_data['text'],
                author=user
            )
            return redirect(reverse('training-detail', kwargs={'slug': self.get_training().slug})+'#comments')
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        slug = self.kwargs['slug']
        return self.render_to_response(
            self.get_context_data(form=form, slug=slug))

    def get_context_data(self, **kwargs):
        kwargs = super(TrainingDetail, self).get_context_data(**kwargs)
        kwargs.update({'training': self.get_training()})
        kwargs['last_trainings'] = Training.objects.order_by('-date')[:7]
        return kwargs

    def get_training(self):
        slug = self.kwargs['slug']
        training = get_object_or_404(Training, slug=slug)
        return training


class UserDetail(generic.DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]
        context['all_user_trainings'] = Training.objects.order_by('-date')

        return context


class NewsDetail(generic.DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['last_trainings'] = Training.objects.order_by('-date')[:7]

        return context


class TrainingUpdate(generic.edit.UpdateView):
    model = Training
    template_name_suffix = '_update'
    form_class = UpdateTrainingForm

    def get_form(self, form_class):
        form = super(TrainingUpdate, self).get_form(form_class)
        form.fields['techniques'].choices = _get_techniques_by_user(self.request.user)
        return form


class TechTrenUpdate(generic.edit.UpdateView):
    model = TechTren
    fields = ['date', 'stand', 'attack', 'technique', 'mistakes']
    template_name_suffix = '_update'


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
        return render(request, 'add_techniques.html', {'form': form, 'techtrens': techniques})


def calendar(request, year=None):
    if year:
        year = int(year)
    else:
        year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    for y in [year-2, year-1, year]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False   # are there entry(s) for this month; current month?
            entries = Training.objects.filter(date__year=y, date__month=n+1, user=request.user)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current, entries=entries))
        lst.append((y, mlst))

    return render(request, "calendar.html", {'years': lst, 'user': request.user, 'year': year})


def month(request, year, month, change=None):
    year, month = int(year), int(month)

    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   mod = mdelta
        elif change == "prev": mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    cal = calendar_library.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    for day in month_days:
        trainings = current = False
        if day:
            trainings = Training.objects.filter(date__year=year, date__month=month, date__day=day, user=request.user)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, trainings, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render(request, "month.html", {'year': year, 'month': month, 'user': request.user,
                        'month_days': lst, 'mname': mnames[month-1]})
