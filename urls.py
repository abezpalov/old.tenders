from django.conf.urls import url

import tenders.views

urlpatterns = [

	url(r'^updaters/$', tenders.views.updaters),

#	url(r'^ajax/get-updater/$', views.ajaxGetUpdater, name='ajaxGetUpdater'),
#	url(r'^ajax/save-updater/$', views.ajaxSaveUpdater, name='ajaxSaveUpdater'),
#	url(r'^ajax/switch-updater-state/$', views.ajaxSwitchUpdaterState, name='ajaxSwitchUpdaterState'),


#	url(r'^regions/$', views.regions, name='regions'),
#	url(r'^ajax/get-region/$', views.ajaxGetRegion, name='ajaxGetRegion'),
#	url(r'^ajax/save-region/$', views.ajaxSaveRegion, name='ajaxSaveRegion'),
#	url(r'^ajax/switch-region-state/$', views.ajaxSwitchRegionState, name='ajaxSwitchRegionState'),


#	url(r'^ajax/get-organisation/$', views.ajaxGetOrganisation, name='ajaxGetOrganisation'),


#	url(r'^plan-graphs/$', views.planGraphs, name='planGraphs'),


#	url(r'^plan-graph-positions(/query/(?P<query>[0-9]+)){0,1}(/page/(?P<page>[0-9]+)){0,1}/$', views.planGraphPositions, name='planGraphPositions'),
#	url(r'^ajax/get-plan-graph-position/$', views.ajaxGetPlanGraphPosition, name='ajaxGetPlanGraphPosition'),

#	url(r'^query-filters/$', views.queryFilters, name='queryFilters'),
#	url(r'^ajax/get-queryfilter/$',           views.ajaxGetQueryFilter,          name='ajaxGetQueryFilter'),
#	url(r'^ajax/save-queryfilter/$',          views.ajaxSaveQueryFilter,         name='ajaxSaveQueryFilter'),
#	url(r'^ajax/switch-queryfilter-state/$',  views.ajaxSwitchQueryFilterState,  name='ajaxSwitchQueryFilterState'),
#	url(r'^ajax/switch-queryfilter-public/$', views.ajaxSwitchQueryFilterPublic, name='ajaxSwitchQueryFilterPublic'),

#	url(r'^essences/$',      views.essences, name='essences'),

#	url(r'^essence/okpd/$',             views.OKPDs,                 name='OKPDs'),
#	url(r'^ajax/get-okpd-childrens/$',  views.ajaxGetOKPDChildrens,  name='ajaxGetOKPDChildrens'),
#	url(r'^ajax/get-okpd-thread/$',     views.ajaxGetOKPDThread,     name='ajaxGetOKPDThread'),
#	url(r'^ajax/search-okpds/$',        views.ajaxSearchOKPDs,       name='ajaxSearchOKPDs'),

#	url(r'^essence/okved/$',            views.OKVEDs,                name='OKVEDs'),
#	url(r'^ajax/get-okved-childrens/$', views.ajaxGetOKVEDChildrens, name='ajaxGetOKVEDChildrens'),
#	url(r'^ajax/get-okved-thread/$',    views.ajaxGetOKVEDThread,    name='ajaxGetOKVEDThread'),
#	url(r'^ajax/search-okveds/$',       views.ajaxSearchOKVEDs,      name='ajaxSearchOKVEDs'),

#	url(r'^essence/okei/$',             views.OKEIs,                 name='OKEIs'),
#	url(r'^ajax/get-okei/$',            views.ajaxGetOKEI,           name='ajaxGetOKEI'),
#	url(r'^ajax/search-okeis/$',        views.ajaxSearchOKEIs,       name='ajaxSearchOKEIs'),

#	url(r'^essence/organisations/$',    views.organisations,         name='organisations'),

]
