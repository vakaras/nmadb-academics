from django.conf.urls import patterns, url


urlpatterns = patterns(
    'nmadb_academics.views',
    url(r'^admin/import/$', 'import_academics',
        name='nmadb-academics-import-academic',),
    )
