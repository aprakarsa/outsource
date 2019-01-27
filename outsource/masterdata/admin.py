# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Supplier, Customer, Product, PoOrder, ProductPo, Invoice
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class ProductPoInline(admin.TabularInline):
    model = ProductPo
    extra = 1


class ProductResource(resources.ModelResource):
	
	class Meta:
   		model = Product
   		exclude = ('created_at', 'is_active', 'edited_at', 'image',)


class PoOrderResource(resources.ModelResource):

	class Meta:
		model = PoOrder


class ProductPoResource(resources.ModelResource):

	class Meta:
		model = ProductPo


class SupplierAdmin(admin.ModelAdmin):
	model_fields = [
		'name',
		'id',
		'name_id',
		'contact_person',
		'address',
		'phone',
		'email',
		'is_active',
		'since',
	]
	list_display = model_fields
	search_fields = model_fields
	list_per_page = 25


class CustomerAdmin(admin.ModelAdmin):
	model_fields = [
		'name',
		'id',
		'name_id',
		'brand_name',
		'contact_person',
		'address',
		'phone',
		'email',
		'is_active',
		'since',
	]
	list_display = model_fields
	search_fields = model_fields
	list_per_page = 25


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ProductResource

	model_fields = [
		'no',
		'code',
		'id',
		'name',
		'category',
		'collection',
		'prod_price',
		'pub_price',
		'retail_price',
		'supplier',
		'brand_name',
		'is_active',
		'image',
	]

	list_display = model_fields
	search_fields = [
		'no',
		'code',
		'id',
		'name',
		'description',
		'size',
		'color',
		'category',
		'collection',
		'brand_name',
		'supplier__name',
	]
	list_per_page = 25
	list_editable = ['is_active']


class PoOrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = PoOrderResource

	model_fields = [
		'created_at',
		'id',
		'po_customer',
		'customer',
		'ready_date',
		'shipment_date',
		'status',
		'edited_at',
	]

	list_display = model_fields
	search_fields = [
		'id',
		'po_supplier',
		'po_customer',
		'status',
		'customer__name',
	]
	list_per_page = 25
	list_editable = ['status']

	inlines = [ProductPoInline]


class ProductPoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = ProductPoResource

	model_fields = [
		'po_order',
		'code',
		'qty_order',
		'qty_ready',
		'qty_shipped',
	]

	list_display = model_fields
	search_fields = [
		'po_order__po_customer',
		'code__code',
		'code__name',
	]
	list_per_page = 25
	list_editable = ['qty_ready', 'qty_shipped']


class InvoiceAdmin(admin.ModelAdmin):
	model_fields = [
		'invoice_no',
		'po_customer',
		'code',
		'send_to_be_shipped',
		'created_at',
	]
	list_display = model_fields
	search_fields = [
		'invoice_no',
		'po_customer__po_customer',
		'code__code',
		'send_to_be_shipped',
	]
	list_per_page = 25


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PoOrder, PoOrderAdmin)
admin.site.register(ProductPo, ProductPoAdmin)
admin.site.register(Invoice, InvoiceAdmin)
