from django.conf.urls import include, url
from django.contrib import admin
from start import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'djangoStart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('start.urls')),
]

#url(r'^start/', include('start.urls')), # ADD THIS NEW TUPLE!
