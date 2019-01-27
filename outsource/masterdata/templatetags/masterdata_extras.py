from django import template

from masterdata.models import PoOrder, Invoice, ProductPo

register = template.Library() 


@register.filter('subtract')
def subtract(value, arg):
	'''substraction of 2 numbers'''
	return value - arg


@register.filter('multiply')
def multiply(value, arg):
	'''substraction of 2 numbers'''
	return value * arg


@register.filter('get_po')
def get_po(value):
    return PoOrder.objects.get(pk=value).po_customer


@register.filter('get_cust_name')
def get_cust_name(value):
    invoices = Invoice.objects.filter(invoice_no=value)

    cust_name = ''
    for invoice in invoices:
    	cust_name = invoice.po_customer.customer.name

    return cust_name


@register.filter('get_inv_date')
def get_inv_date(value):
    invoices = Invoice.objects.filter(invoice_no=value)

    inv_date = ''
    for invoice in invoices:
    	inv_date = invoice.created_at

    return inv_date


@register.filter('get_total_qty')
def get_total_qty(value):
    invoices = Invoice.objects.filter(invoice_no=value)

    total_qty = 0
    for invoice in invoices:
    	total_qty += invoice.send_to_be_shipped

    return total_qty


@register.filter('get_total_amount')
def get_total_amount(value):
    invoices = Invoice.objects.filter(invoice_no=value)

    total_amount = 0
    for invoice in invoices:
    	total_amount += (invoice.send_to_be_shipped * invoice.code.pub_price)

    return total_amount


@register.filter('get_total_qty_detail')
def get_total_qty_detail(value):
    product_po = ProductPo.objects.filter(po_order=value)

    total_qty_detail = 0
    for product in product_po:
    	total_qty_detail += product.qty_order

    return total_qty_detail


@register.filter('get_total_amount_detail')
def get_total_amount_detail(value):
    product_po = ProductPo.objects.filter(po_order=value)

    total_amount_detail = 0
    for product in product_po:
    	total_amount_detail += (product.qty_order * product.code.pub_price)

    return total_amount_detail


@register.filter('get_total_amount_shipped')
def get_total_amount_shipped(value):
    product_po = ProductPo.objects.filter(po_order=value)

    total_amount_shipped = 0
    for product in product_po:
        total_amount_shipped += (product.qty_shipped * product.code.pub_price)

    return total_amount_shipped


@register.filter('get_total_amount_profit')
def get_total_amount_profit(value):
    product_po = ProductPo.objects.filter(po_order=value)

    total_amount_shipped = 0
    total_amount_prod = 0
    for product in product_po:
        total_amount_shipped += (product.qty_shipped * product.code.pub_price)
        total_amount_prod += (product.qty_shipped * product.code.prod_price)

    return total_amount_shipped - total_amount_prod









