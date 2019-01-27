# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


PO_STATUS = (
	('open', 'PO Open'),
	('completed', 'PO Closed'),
)


class third_party_data(models.Model):
	since = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=150, unique=True)
	name_id = models.CharField(
		max_length=200, 
		unique=True, 
		help_text='All lowercase and no space'
	)
	contact_person = models.CharField(max_length=100)
	address = models.TextField()
	phone = models.CharField(max_length=50)
	email = models.EmailField(max_length=150, unique=True)
	is_active = models.BooleanField(default=True, help_text='Check if active')

	class Meta:
		abstract = True

	def __str__(self):
		return self.name


class Supplier(third_party_data):
	pass


class Customer(third_party_data):
	brand_name = models.CharField(
		max_length=150, 
		blank=True, 
		help_text='If no brand, could be empty'
	)


class Product(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	no = models.CharField(
		max_length=100, 
		help_text='Unique master code for all sizes and colors, example: MSN001'
	)
	code = models.CharField(
		max_length=100, 
		unique=True, 
		help_text='Unique product code with size and color codes, example: MSN001_BLK_XL'
	)
	name = models.CharField(max_length=200, help_text='Product name')
	description = models.TextField()
	size = models.CharField(max_length=20)
	color = models.CharField(max_length=20)
	category = models.CharField(max_length=100)
	collection = models.CharField(max_length=150, blank=True)
	supplier = models.ForeignKey(Supplier, to_field='name_id')
	brand_name = models.CharField(max_length=150, blank=True)
	prod_price = models.IntegerField(default=0, help_text='Production price')
	pub_price = models.IntegerField(default=0)
	retail_price = models.IntegerField(default=0)
	is_active = models.BooleanField(default=True, help_text='Check if active')
	edited_at = models.DateTimeField(auto_now=True)
	image = models.ImageField(default='images/noimage.jpg', upload_to='images')

	class Meta:
		verbose_name = 'Master Product'
		ordering = ['code']

	def __str__(self):
		return "{} | {} - {} | {}".format(self.code, self.color, self.size, self.name)


class PoOrder(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	customer = models.ForeignKey(Customer)
	po_supplier = models.CharField(max_length=50, unique=True)
	po_customer = models.CharField(max_length=50, unique=True)
	ready_date = models.DateTimeField()
	shipment_date = models.DateTimeField()
	status = models.CharField(
		max_length=10,
		choices=PO_STATUS,
		default='open'
	)
	edited_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'PO Order'

	def __str__(self):
		return self.po_customer


class ProductPo(models.Model):
	po_order = models.ForeignKey(PoOrder)
	code = models.ForeignKey(Product)
	qty_order = models.IntegerField(blank=False)
	qty_ready = models.IntegerField(default=0)
	qty_invoice = models.IntegerField(default=0)
	qty_shipped = models.IntegerField(default=0)

	class Meta:
		verbose_name = 'Product PO'

	def __str__(self):
		return "{} | {} | {} pcs".format(
			self.po_order, self.code, self.qty_order)


class Invoice(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	invoice_no = models.IntegerField(default=0)
	po_customer = models.ForeignKey(PoOrder)
	code = models.ForeignKey(Product)
	send_to_be_shipped = models.IntegerField(default=0)

	
