from django.conf.urls import url

import tenders.views

urlpatterns = [

	url(r'^updaters/$', tenders.views.updaters),

	url(r'^regions/$', tenders.views.regions),
	url(r'^regionkeys/$', tenders.views.regionkeys),

	url(r'^essences/(?P<model_name>[a-zA-Z0-9_-]+)$', tenders.views.essences),

	# AJAX
	url(r'^ajax/get/(?P<model_name>[a-zA-Z0-9_-]+)/$',                                        tenders.views.ajax_get),
	url(r'^ajax/save/(?P<model_name>[a-zA-Z0-9_-]+)/$',                                       tenders.views.ajax_save),
	url(r'^ajax/switch-state/(?P<model_name>[a-zA-Z0-9_-]+)/$',                               tenders.views.ajax_switch_state),
	url(r'^ajax/delete/(?P<model_name>[a-zA-Z0-9_-]+)/$',                                     tenders.views.ajax_delete),
	url(r'^ajax/link/(?P<model_name>[a-zA-Z0-9_-]+)/same/(?P<foreign_name>[a-zA-Z0-9_-]+)/$', tenders.views.ajax_link_same_foreign),

]
