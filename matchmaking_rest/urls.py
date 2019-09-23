from django.conf.urls import url, include
from django.contrib import admin
from questions import views as quest_views
from matches import views as match_views
from likes import views as like_views
from users import views as user_views
from . import views as root_views
from rest_framework.schemas import get_schema_view
from rest_framework_raml.renderers import RAMLRenderer, RAMLDocsRenderer
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings

title='Matchmaking REST API'

base_schema_view = get_schema_view(title=title)

swagger_schema_view = get_swagger_view(
    title=title,
)

raml_schema_view = get_schema_view(
    title=title,
    renderer_classes=[RAMLRenderer, RAMLDocsRenderer]
)

urlpatterns = [
    #url(r'^$', base_schema_view),
    url(r'swagger^$', swagger_schema_view),
    url(r'^$', raml_schema_view),
    #url(r'^$', root_views.api_root_list),
    url(r'^match-api$',
        root_views.api_match_list),
    url(r'^match-api/v0$',
        root_views.api_v0_list),
    url(r'^match-api/v0/questions$',
            quest_views.QuestionList.as_view()),
    url(r'^match-api/v0/questions/(?P<pk>[0-9]+)$',
            quest_views.QuestionDetail.as_view()),
    url(r'^match-api/v0/answers$',
        quest_views.AnswerList.as_view()),
    url(r'^match-api/v0/answers/(?P<pk>[0-9]+)$',
        quest_views.AnswerDetail.as_view()),
    url(r'^match-api/v0/user-answers$',
        quest_views.UserAnswerList.as_view()),
    url(r'^match-api/v0/user-answers/(?P<pk>[0-9]+)$',
        quest_views.UserAnswerDetail.as_view()),
    url(r'^match-api/v0/matches$',
        match_views.MatchList.as_view()),
    url(r'^match-api/v0/matches/(?P<pk>[0-9]+)$',
        match_views.MatchDetail.as_view()),
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
        like_views.UserLikeList.as_view()),
    url(r'^match-api/v0/user-likes/(?P<pk>[a-zA-Z0-9_.-]+)$',
        like_views.UserLikeDetail.as_view()),
    url(r'^match-api/v0/users$',
        user_views.UserList.as_view()),
    url(r'^match-api/v0/users/(?P<pk>[a-zA-Z0-9_.-]+)$',
        user_views.UserDetail.as_view()),

    url(r'^admin101/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
