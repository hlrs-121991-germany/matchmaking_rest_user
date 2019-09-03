from django.conf.urls import url, include
from django.contrib import admin
from questions import views as quest_views
from matches import views as match_views
from likes import views as like_views
from users import views as user_views
from . import views as root_views

urlpatterns = [
    url(r'^$', root_views.api_root_list),
    url(r'^match-api$',
        root_views.api_match_list),
    url(r'^match-api/v0$',
        root_views.api_v0_list),
    url(r'^match-api/v0/questions$',
        quest_views.question_list),
    url(r'^match-api/v0/questions/(?P<pk>[0-9]+)$',
        quest_views.question_detail),
    url(r'^match-api/v0/answers$',
        quest_views.answer_list),
    url(r'^match-api/v0/answers/(?P<pk>[0-9]+)$',
        quest_views.answer_detail),
    url(r'^match-api/v0/questions-answers$',
        quest_views.question_answer_list),
    url(r'^match-api/v0/user-answers$',
        quest_views.user_answer_list),
    url(r'^match-api/v0/user-answers/(?P<pk>[0-9]+)$',
        quest_views.user_answer_detail),
    url(r'^match-api/v0/matches$',
        match_views.match_list),
    url(r'^match-api/v0/matches/(?P<pk>[0-9]+)$',
        match_views.match_detail),
    url(r'^match-api/v0/position-matches$',
        match_views.position_match_list),
    url(r'^match-api/v0/position-matches/(?P<pk>[0-9]+)$',
        match_views.position_match_detail),
    url(r'^match-api/v0/location-matches$',
        match_views.location_match_list),
    url(r'^match-api/v0/location-matches/(?P<pk>[0-9]+)$',
        match_views.location_match_detail),
    url(r'^match-api/v0/employer-matches$',
        match_views.employer_match_list),
    url(r'^match-api/v0/employer-matches/(?P<pk>[0-9]+)$',
        match_views.employer_match_detail),
    url(r'^match-api/v0/user-likes$',
        like_views.user_like_list),
    url(r'^match-api/v0/user-likes/(?P<pk>[0-9]+)$',
        like_views.user_like_detail),
    url(r'^match-api/v0/user-likes/(?P<pk>[a-zA-Z0-9_.-]+)$',
        like_views.user_like_detail),
    url(r'^match-api/v0/users$',
        user_views.user_list),
    url(r'^match-api/v0/users/(?P<pk>[0-9]+)$',
        user_views.user_detail),

    url(r'^admin101/', include(admin.site.urls)),
]
