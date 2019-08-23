from django.conf.urls import url
from questions import views

urlpatterns = [
    url(r'^questions/$', views.question_list),
    url(r'^questions/(?P<pk>[0-9]+)$', views.question_detail),
    url(r'^quest_answers/$', views.question_list),
    url(r'^quest_answers/(?P<pk>[0-9]+)$', views.question_list),
    url(r'^answers/$', views.answer_list),
    url(r'^answers/(?P<pk>[0-9]+)$', views.answer_detail),
    url(r'^user_answers/$', views.user_answer_list),
    url(r'^user_answers/(?P<pk>[0-9]+)$', views.user_answer_detail),
]
