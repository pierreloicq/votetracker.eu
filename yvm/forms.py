from django import forms
from django.utils.translation import gettext_lazy as _

class CountrySelectionForm(forms.Form):
    # just the values on the left are useful here, since the display form is in the html
    # which was easier to style it with css and maybe to get instant country translations
    country_choices = [
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

    country = forms.ChoiceField(choices=country_choices, required=True)


