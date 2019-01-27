from django import forms

from . import models


YEARS_CHOICES = [
	('2019', '2019'),
	('2020', '2020'),
	('2021', '2021'),
	('2022', '2022'),
	('2023', '2023'),
	('2024', '2025'),
]


class CheckForm(forms.Form):
	po_customer = forms.CharField(
		label='PO Numbers',
		max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control',
				'placeholder': 'Enter Your PO Numbers here',
			}
		),
	)


class YearsForm(forms.Form):
	year = forms.CharField(
		label='Select Years', 
		widget=forms.Select(
			choices=YEARS_CHOICES,
			attrs={
				'class': 'form-control',
			}
		),
	)
