# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import CheckForm, YearsForm
from .models import PoOrder, ProductPo, Invoice, Product

import random
import barcode


def index(request):
	check_form = CheckForm()

	context = {
		'page_title': 'PO Status',
		'check_form': check_form,
	}

	if request.method == 'POST':
		check_form = CheckForm(request.POST)

		if check_form.is_valid():
			context['po_customer'] = request.POST['po_customer']
			po_customer = context['po_customer']

			status = get_object_or_404(PoOrder, po_customer=po_customer)

			context['po_status'] = status.status
			context['po_id'] = status.id
			context['po_name'] = status.customer.name
			context['po_supplier'] = status.po_supplier
			context['po_ready'] = status.ready_date
			context['po_shipment'] = status.shipment_date

			return render(request, 'masterdata/po_status.html', context)

		else:
			check_form = CheckForm()

	return render(request, 'masterdata/index.html', context)


@login_required
def select_years(request):
	pass


def barcode(request, pk):
    import mybarcode

    barcode = ''
    retail_price = 0
    desc = ''
    size = ''
    color = ''
    po_product = ProductPo.objects.filter(code=pk)
    for product in po_product:
		barcode = product.code.code
		retail_price = product.code.retail_price
		desc = product.code.description
		size = product.code.size
		color = product.code.color

    d = mybarcode.MyBarcodeDrawing(barcode).save(formats=['png'],outDir='./media/barcodes/',fnRoot=barcode)
    # return HttpResponseRedirect('/media/barcodes/{}.pdf'.format(barcode))

    context = {
    	'barcode': barcode,
    	'retail_price': retail_price,
	    'desc': desc,
	    'size': size,
	    'color': color,
    }

    return render(request, 'masterdata/print_barcode.html', context)


@login_required
def po_list(request):
	po_list = PoOrder.objects.all().order_by('-id')

	context = {
		'page_title': 'PO List',
		'po_list': po_list,
	}
	return render(request, 'masterdata/po_list.html', context)


def po_detail(request, pk):
	po_products = ProductPo.objects.filter(po_order=pk)

	total_qty_order = 0
	total_qty_ready = 0
	total_qty_invoice = 0
	total_qty_shipped = 0
	total_amount_order = 0
	total_amount_ready = 0
	total_amount_invoice = 0
	total_amount_shipped = 0
	total_amount_profit = 0
	po_numbers = ''
	po_customer = ''
	ready_date = ''
	shipment_date = ''
	po_supplier = ''
	po_status = ''
	for product in po_products:
		total_qty_order += product.qty_order
		total_qty_ready += product.qty_ready
		total_qty_invoice += product.qty_invoice
		total_qty_shipped += product.qty_shipped
		po_numbers = product.po_order.po_customer
		po_customer = product.po_order.customer.name
		ready_date = product.po_order.ready_date
		shipment_date = product.po_order.shipment_date
		po_supplier = product.po_order.po_supplier
		po_status = product.po_order.status
		total_amount_order += (product.code.pub_price * product.qty_order)
		total_amount_ready += (product.code.pub_price * product.qty_ready)
		total_amount_invoice += (product.code.pub_price * product.qty_invoice)
		total_amount_shipped += (product.code.pub_price * product.qty_shipped)
		total_amount_profit += (product.code.prod_price * product.qty_shipped)

	context = {
		'page_title': 'PO Detail',
		'po_products': po_products,
		'total_qty_order': total_qty_order,
		'total_qty_ready': total_qty_ready,
		'total_qty_invoice': total_qty_invoice,
		'total_qty_shipped': total_qty_shipped,
		'total_amount_profit': total_amount_profit,
		'prod_id': pk,
		'po_numbers': po_numbers,
		'po_customer': po_customer,
		'ready_date': ready_date,
		'shipment_date': shipment_date,
		'po_supplier': po_supplier,
		'po_status': po_status,
		'total_amount_order': total_amount_order,
		'total_amount_ready': total_amount_ready,
		'total_amount_invoice': total_amount_invoice,
		'total_amount_shipped': total_amount_shipped,

	}
	return render(request, 'masterdata/po_detail.html', context)


@login_required
def create_invoice(request, pk):
	# udpate qty ready and qty to be shipped
	po_products = ProductPo.objects.filter(po_order=pk)

	qty_in_ready = 0
	qty_in_invoice = 0
	qty_in_shipped = 0
	new_qty_ready = 0
	new_qty_shipped = 0
	po_customer = ''
	po_code = ''

	check_record = Invoice.objects.all()
	invoice_no = 0
	if check_record.exists():
		check_record = Invoice.objects.latest('id')
		invoice_no = int(check_record.invoice_no) + 1
	else:
		invoice_no = 101

	for product in po_products:
		qty_in_ready = product.qty_ready
		qty_in_invoice = product.qty_invoice
		qty_in_shipped = product.qty_shipped
		new_qty_ready = product.qty_ready - product.qty_invoice
		new_qty_shipped = qty_in_shipped + product.qty_invoice

		query = ProductPo.objects.get(pk=product.id)
		query.qty_ready = new_qty_ready
		query.qty_invoice = 0
		query.qty_shipped = new_qty_shipped
		query.save()

		po_customer = PoOrder(id=product.po_order.id)
		po_code = Product(id=product.code.id)

		if qty_in_invoice != 0:
			query_insert = Invoice(
				invoice_no=invoice_no,
				po_customer=po_customer,
				code = po_code,
				send_to_be_shipped = qty_in_invoice
			)
			query_insert.save()

	return HttpResponseRedirect('/masterdata/display-invoice/{}'.format(invoice_no))


@login_required
def display_invoice(request, pk):
	invoice = Invoice.objects.filter(invoice_no=pk).order_by('-id')

	total_price = 0
	total_qty = 0
	created_at = ''
	invoice_no = ''
	po_customer = ''

	for item in invoice:
		total_qty += item.send_to_be_shipped
		total_price += (item.code.pub_price * item.send_to_be_shipped)
		created_at = item.created_at
		invoice_no = item.invoice_no
		po_customer = item.po_customer

	cust_details = PoOrder.objects.get(po_customer=po_customer)
	name = cust_details.customer.name
	address = cust_details.customer.address
	phone = cust_details.customer.phone
	email = cust_details.customer.email

	context = {
		'page_title': 'Invoices',
		'invoice': invoice,
		'total_qty': total_qty,
		'total_price': total_price,
		'created_at': created_at,
		'invoice_no': invoice_no,
		'po_customer': po_customer,
		'name': name,
		'address': address,
		'phone': phone,
		'email': email,
	}

	return render(request, 'masterdata/display_invoice.html', context)


@login_required
def all_invoices(request):
	all_invoices = Invoice.objects.all().values('invoice_no', 'po_customer').order_by('-invoice_no').distinct()

	context = {
		'page_title': 'Invoices',
		'all_invoices': all_invoices,
	}

	return render(request, 'masterdata/all_invoices.html', context)	


@login_required
def yearly_report(request):	
	years_form = YearsForm()

	context = {
		'page_title': 'Reports',
		'years_form': years_form,
	}

	if request.method == 'POST':
		years_form = YearsForm(request.POST)

		if years_form.is_valid():
			context['year'] = request.POST['year']
			year = context['year']

			po_order = PoOrder.objects.filter(ready_date__year=year)

			print(year)

			context['po_order'] = po_order

			return render(request, 'masterdata/yearly_report.html', context)

		else:
			years_form = YearsForm()

	return render(request, 'masterdata/yearly_report.html', context)



















