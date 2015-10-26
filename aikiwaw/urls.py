from django.conf.urls import patterns, include, url
from django.contrib import admin
from aikiblog.views import TrainingList, StageList, TrainingDetail, UserDetail, DojoList, DojoDetail, NewsList, NewsDetail
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^/?$', NewsList.as_view(), name='news-list'),
        url(r'^(?P<page>[0-9]+)/$', NewsList.as_view(), name='news-list'),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^dojo/(?P<slug>[\w\-_]+)/$', DojoDetail.as_view(), name='dojo-detail'),
        url(r'^dojos/$', DojoList.as_view(), name='dojo-list'),
        url(r'^dojos/(?P<page>[0-9]+)/$', DojoList.as_view(), name='dojo-list'),
        url(r'^news/(?P<slug>[\w\-_]+)/$', NewsDetail.as_view(), name='news-detail'),
        url(r'^stages/$', StageList.as_view(), name='stage-list'),
        url(r'^stages/(?P<page>[0-9]+)/$', StageList.as_view(), name='stage-list'),
        url(r'^training/(?P<slug>[\w\-_]+)/$', TrainingDetail.as_view(), name='training-detail'),
        url(r'^trainings/?$', TrainingList.as_view(), name='training-list'),
        url(r'^trainings/(?P<page>[0-9]+)/$', TrainingList.as_view(), name='training-list'),
        url(r'^user/(?P<pk>[\w\-_]+)/$', UserDetail.as_view(), name='user-detail'),
        url(r'^accounts/', include('registration.backends.default.urls')),

        url(r'^dodaj_trening/$', 'aikiblog.forms.add_training'),

        url(r'^(?P<user_id>[\d]+)/save_user_data', 'aikiblog.views.save_user_data', name='save_user_data'),

)
