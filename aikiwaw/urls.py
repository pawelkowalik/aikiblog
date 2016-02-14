from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from aikiblog.views import (TrainingList, StageList, TrainingDetail, UserDetail, DojoList, DojoDetail, NewsList,
                            NewsDetail, TechniqueList, TrainingUpdate, TechTrenUpdate, UserUpdate, month, calendar, add_stage,
                            add_training, add_techniques, add_images, save_user_data, change_avatar)

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
        url(r'^training_update/(?P<slug>[\w\-_]+)/$', TrainingUpdate.as_view(), name='training-update'),
        url(r'^technique_update/(?P<slug>[\w\-_]+)/$', TechTrenUpdate.as_view(), name='techtren-update'),
        url(r'^trainings/?$', TrainingList.as_view(), name='training-list'),
        url(r'^trainings/(?P<page>[0-9]+)/$', TrainingList.as_view(), name='training-list'),
        url(r'^technique/(?P<slug>[\w\-_]+)/(?P<page>[0-9]+)/$', TechniqueList.as_view(), name='technique-list'),
        url(r'^technique/(?P<slug>[\w\-_]+)/$', TechniqueList.as_view(), name='technique-list'),
        url(r'^user/(?P<pk>[\w\-_]+)/$', UserDetail.as_view(), name='user-detail'),
        url(r'^user_update/(?P<pk>[\w\-_]+)/$', UserUpdate.as_view(), name='user-update'),
        url(r'^accounts/', include('registration.backends.default.urls')),
        url(r'^add_techniques/$', add_techniques, name='add-techniques'),
        url(r'^add_training/$', add_training, name='add-training'),
        url(r'^add_stage/$', add_stage, name='add-stage'),
        url(r'^add_images/((?P<training_id>[\d]+))/$', add_images, name='add-images'),
        url(r'^save_user_data/(?P<user_id>[\d]+)/$', save_user_data, name='save_user_data'),
        url(r'^change_avatar/((?P<user_id>[\d]+))/$', change_avatar, name='change-avatar'),
        url(r'^calendar/(\d+)/$', calendar, name='calendar'),
        url(r'^calendar/$', calendar, name='calendar'),
        url(r"^calendar/month/(\d+)/(\d+)/(prev|next)/$", month, name='month'),
        url(r"^calendar/month/(\d+)/(\d+)/$", month, name='month'),
        url(r"^calendar/month$", month, name='month'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)