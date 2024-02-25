from django import forms
from django.utils.translation import gettext as _

class CountrySelectionForm(forms.Form):
    country_choices = [
        ('', _('Select a country')),
        ('Austria', _('Austria')),
        ('Belgium', _('Belgium')),
        ('Bulgaria', _('Bulgaria')),
        ('Croatia', _('Croatia')),
        ('Cyprus', _('Cyprus')),
        ('Czechia', _('Czechia')),
        ('Denmark', _('Denmark')),
        ('Estonia', _('Estonia')),
        ('Finland', _('Finland')),
        ('France', _('France')),
        ('Germany', _('Germany')),
        ('Greece', _('Greece')),
        ('Hungary', _('Hungary')),
        ('Ireland', _('Ireland')),
        ('Italy', _('Italy')),
        ('Latvia', _('Latvia')),
        ('Lithuania', _('Lithuania')),
        ('Luxembourg', _('Luxembourg')),
        ('Malta', _('Malta')),
        ('Netherlands', _('Netherlands')),
        ('Poland', _('Poland')),
        ('Portugal', _('Portugal')),
        ('Romania', _('Romania')),
        ('Slovakia', _('Slovakia')),
        ('Slovenia', _('Slovenia')),
        ('Spain', _('Spain')),
        ('Sweden', _('Sweden'))
    ]

    country = forms.ChoiceField(choices=country_choices, required=True, 
                                widget=forms.Select(attrs={#'class': 'form-select w-100', 
                                                           'aria-label': 'select the country where you vote'})
                                )


