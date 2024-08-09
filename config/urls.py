from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts import views as account_views

urlpatterns = [
    path('', account_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('feed/', include('apps.feed.urls', namespace='feed')),
    path('groups/', include('apps.groups.urls', namespace='groups')),
    path('messaging/', include('apps.messaging.urls', namespace='messaging')),
    path('stories/', include('apps.stories.urls', namespace='stories')),
    path('events/', include('apps.events.urls', namespace='events')),
    path('marketplace/', include('apps.marketplace.urls', namespace='marketplace')),
    path('jobs/', include('apps.jobs.urls', namespace='jobs')),
    path('confessions/', include('apps.confessions.urls', namespace='confessions')),
    path('dining/', include('apps.dining.urls', namespace='dining')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('search/', include('apps.search.urls', namespace='search')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)