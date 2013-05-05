
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.main'),
    # url(r'^mosaic/$','main.views.mosaic'),
    # url(r'^coshare/', include('coshare.foo.urls')),

    url(r'^open_modal_view/', 'main.views.open_modal'),
    url(r'^save_description/', 'main.views.change_description'),

    url(r'login_user/','main.views.login_user'),
    url(r'logout/','main.views.logout_user'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/','main.views.login_page'),
    url(r'^upload/','main.views.upload'),
    url(r'^add/','main.views.add'),
    url(r'^new_plist/','main.views.new_plist'),
    url(r'^browse/','main.views.browse'),
    url(r'^mobile/','main.views.mobile'),
    url(r'^ajax/add_album/','main.views.add_album'),
    url(r'^ajax/add_content/','main.views.add_content'),
    url(r'^ajax/remove_content/','main.views.remove_content'),
    url(r'^ajax/delete_content/','main.views.delete_content'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
