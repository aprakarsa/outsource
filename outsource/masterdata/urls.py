from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^polist/', views.po_list, name='polist'),
	url(r'^all-invoices/', views.all_invoices, name='all_invoices'),
	url(r'^yearly-report/', views.yearly_report, name='yearly_report'),
	url(r'^detail/(?P<pk>\d+)$', views.po_detail, name='detail'),
	url(r'^barcode/(?P<pk>\d+)$', views.barcode, name='barcode'),
	url(r'^invoice/(?P<pk>\d+)$', views.create_invoice, name='invoice'),
	url(r'^display-invoice/(?P<pk>\d+)$', views.display_invoice, name='display_invoice'),
	url(r'^$', views.index, name='index'),
]
