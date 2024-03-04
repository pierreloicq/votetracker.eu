from django.shortcuts import render, redirect
# from django.utils.translation import activate
# from django.http import Http404
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
from django.urls import reverse
# from .models import Mep, Vote
from .models import Position
from .forms import CountrySelectionForm
import pandas as pd
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


# not used for the moment
eu_party_dict = {
    "PPE": _("Group of the European People's Party (Christian Democrats)"),
    "S&D": _("Group of the Progressive Alliance of Socialists and Democrats"),
    "RE": _("Renew Europe Group"),
    "ECR": _("European Conservatives and Reformists Group"),
    "ID": _("Identity and Democracy Group"),
    "GUE/NGL": _("The Left group"),
    "Verts/ALE": _("Group of the Greens/European Free Alliance"),
    "NA": _("Non-Attached Members"),
}

country_codes = {
    "Austria": "1f1e6_1f1f9",
    "Belgium": "1f1e7_1f1ea",
    "Bulgaria": "1f1e7_1f1ec",
    "Croatia": "1f1ed_1f1f7",
    "Cyprus": "1f1e8_1f1fe",
    "Czechia": "1f1e8_1f1ff",
    "Denmark": "1f1e9_1f1f0",
    "Estonia": "1f1ea_1f1ea",
    "Finland": "1f1eb_1f1ee",
    "France": "1f1eb_1f1f7",
    "Germany": "1f1e9_1f1ea",
    "Greece": "1f1ec_1f1f7",
    "Hungary": "1f1ed_1f1fa",
    "Ireland": "1f1ee_1f1ea",
    "Italy": "1f1ee_1f1f9",
    "Latvia": "1f1f1_1f1fb",
    "Lithuania": "1f1f1_1f1f9",
    "Luxembourg": "1f1f1_1f1fa",
    "Malta": "1f1f2_1f1f9",
    "Netherlands": "1f1f3_1f1f1",
    "Poland": "1f1f5_1f1f1",
    "Portugal": "1f1f5_1f1f9",
    "Romania": "1f1f7_1f1f4",
    "Slovakia": "1f1f8_1f1f0",
    "Slovenia": "1f1f8_1f1ee",
    "Spain": "1f1ea_1f1f8",
    "Sweden": "1f1f8_1f1ea"
}

def index(request):
    countryform = CountrySelectionForm(request.GET)
    if countryform.is_valid():
        # a country has been selected
        country = countryform.cleaned_data['country']
        url = reverse('bycountryAllTexts') + f'?country={country}'
        return redirect(url)
    else:
        countryform.fields['country'].choices = sorted(countryform.fields['country'].choices, key=lambda x: x[1])
        return render(request, 'yvm/index.html', {'countryform': countryform})


def bycountryAllTexts(request):
    country = request.GET.get('country')
    language_code = get_language()
    allData = Position.objects.filter(mep__country=country).values('mep__fullname', 'mep__national_party', 
                            'vote__short_desc','stance', 'comment', 'mep__photo_url', 
                            'mep__eu_page_url', 'mep__eu_group_short',
                            'vote__summary_url', 'vote__procedure_url', 'vote__vote_id', 'vote__vote_date', 
                            'vote__vote_number', 'vote__debate_url').order_by('mep__national_party', 'mep__fullname')
    # print(type(allData))
    # print(allData)
    
    df0 = pd.DataFrame.from_records(allData)
    rows = ['mep__fullname', 'mep__national_party', 'mep__photo_url', 'mep__eu_page_url', 'mep__eu_group_short']
    cols = ['vote__short_desc', 'vote__vote_id', 'vote__summary_url', 'vote__procedure_url', 'vote__vote_date', 'vote__vote_number', 
            'vote__debate_url']
    df_stance = df0.pivot(index=rows,  columns=cols, values="stance")
    df_comm = df0.pivot(index=rows, columns=cols, values="comment")

    # merge df_stance & df_comm in df containing a tuple of both values
    df = df_stance.copy()
    for irow in range(df.shape[0]):
        for icol in range(df.shape[1]):
            df.iloc[irow, icol] =  (df_stance.iloc[irow, icol], df_comm.iloc[irow, icol])
    
    # without that the order is random
    df = df.sort_index(axis=1, level='vote__vote_number')

    # print(df[['vote__summary_url', 'vote__procedure_url']])
    # print(df.query("mep__fullname == 'mep_name'"))

    # output  {short_desc -> {mep__fullname -> comment}}
    # dict_comm = df0.pivot(index=['mep__fullname'], columns=['vote__short_desc'], values="comment").to_dict() 
    # print(dict_comm)
    # print(type(df.iloc[-1,-1]))
    
    # df_meps = df.reset_index().set_index('mep__fullname')[['mep__national_party', 'mep__photo_url', 'mep__eu_page_url', 'mep__eu_group_short','mep__eu_group_long']]
    # df_stances = df.reset_index().set_index('mep__fullname').drop(['mep__national_party', 'mep__photo_url', 'mep__eu_page_url', 'mep__eu_group_short'], axis=1)
    
    # df = df.to_html(index=True, index_names=True)
    # df_meps = df_meps.to_html(index=True, index_names=True)

    #### for dev, to see the shape of the table, output here df.to_html() instead of df and display {{ df|safe }} in summary.html 
    context = {'df':df, 'country':country, 'country_code':country_codes[country], 
               'nb_mep':df.shape[0], 'nb_votes':len(df.columns), 'eu_party_dict':eu_party_dict,
               'language_code':language_code}
    return render(request, "yvm/summary.html", context)