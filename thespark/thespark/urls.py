"""thespark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


from rest_framework import routers, serializers, viewsets

from chat.views import (
    TemplateTestView,
    LatestConversationMessageView,
    ChatView,
    AddOrGetConversationView,
)

from forums.views import (
    ForumView,
    LastForumMessageView,
    SubscribeForumView,
    UnsubscribeForumView,
    ForumRequestView,
    ForumReportView,
    ForumsView,
)

from inbox.views import GetInbox

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/inbox/$',GetInbox.as_view()),
    url(r'^api/chat/messages/(?P<id>[0-9]+)/$', ChatView.as_view()),#conversation id
    url(r'^api/chat/conversation/(?P<id>[0-9]+)/$', AddOrGetConversationView.as_view()),
    url(r'^api/chat/inbox/$', LatestConversationMessageView.as_view()),
    url(r'^chat/conversation/$', TemplateTestView.as_view()),
    url(r'^api/forum/(?P<id>[0-9]+)/$',ForumView.as_view()),
    url(r'^api/forums/$',ForumsView.as_view()),
    url(r'^api/forum/inbox/$',LastForumMessageView.as_view()),
    url(r'^api/forum/subscribe/(?P<id>[0-9]+)/$',SubscribeForumView.as_view()),
    url(r'^api/forum/unsubscribe/(?P<id>[0-9]+)/$',UnsubscribeForumView.as_view()),
    url(r'^api/forum/request/$',ForumRequestView.as_view()),
    url(r'^api/forum/report/(?P<id>[0-9]+)/$',ForumReportView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
