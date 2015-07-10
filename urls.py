from django.conf.urls import patterns, url

from tenders import views

urlpatterns = patterns('',


	# Updater
	# ex: /tenders/updaters/
	url(r'^updaters/$', views.updaters, name='updaters'),
	# AJAX
	url(r'^ajax/get-updater/$', views.ajaxGetUpdater, name='ajaxGetUpdater'),
	url(r'^ajax/save-updater/$', views.ajaxSaveUpdater, name='ajaxSaveUpdater'),
	url(r'^ajax/switch-updater-state/$', views.ajaxSwitchUpdaterState, name='ajaxSwitchUpdaterState'),

	# Region
	# ex: /tenders/regions/
	url(r'^regions/$', views.regions, name='regions'),
	# AJAX
	url(r'^ajax/get-region/$', views.ajaxGetRegion, name='ajaxGetRegion'),
	url(r'^ajax/save-region/$', views.ajaxSaveRegion, name='ajaxSaveRegion'),
	url(r'^ajax/switch-region-state/$', views.ajaxSwitchRegionState, name='ajaxSwitchRegionState'),

	#PlanGraphs
	# ex: /tenders/plan-graphs/
	url(r'^plan-graphs/$', views.planGraphs, name='planGraphs'),

	#PlanGraph Positions
	# ex: /tenders/plan-graph-positions/
	url(r'^plan-graph-positions/$', views.planGraphPositions, name='planGraphPositions'),

)
