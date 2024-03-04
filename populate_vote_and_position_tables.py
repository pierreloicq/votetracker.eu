# run populate_mep_table.py and then this one

import json, os
from django.core.wsgi import get_wsgi_application
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yvm_site.settings")
application = get_wsgi_application()

from yvm.models import Mep, Vote, Position

# delete previous content
# DELETE FROM public.yvm_vote;
# DELETE FROM public.yvm_position;
Vote.objects.all().delete()
Position.objects.all().delete()


# the model of a voteidList is :
# [number, 
# id that you can also see on mepwatch.eu, 
# classification that you will find in the news, 
# link to a summary, preferably a news or the summary found on the oeil page,
# debate link]

voteidListList = [
    # 12.07.2023 - 336/300/13
    [1,
     '157420',
     _("Implement measures for ecosystem restoration on 20&#37; of all land and sea areas by 2030, in order to meet the international commitments, with exemptions for renewable energy, housing construction and national defence projects or if food production/price has changed too much") , 
     'Environment', 
     'https://www.europarl.europa.eu/news/en/press-room/20230707IPR02433/nature-restoration-law-meps-adopt-position-for-negotiations-with-council', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2022/0195(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-07-11-ITM-003_EN.html'
     ],
    # 13.09.2023 - 62prcnt in favor
    [2,
     '157953', 
     _('Improve and harmonise air quality monitoring and consider more realistic air pollution thresholds, to be met by 2035, while intermediate threshold must be met by 2030'), 
     'Environment', 
     'https://www.europarl.europa.eu/news/en/press-room/20230911IPR04915/air-pollution-meps-want-stricter-limits-to-achieve-zero-pollution-by-2050', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2022/0347(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-09-12-ITM-009_EN.html'
     ],
    # 22.11.2023 - 77prcnt in favor
    [3,
     '160802', 
     _("Propose several targets to reduce the quantity of overall and plastic packaging and require them to be recyclable (with exemptions), while increasing the quantity of recycled plastic in new packages. Ban the use of the “forever chemicals” (PFAS) and Bisphenol A in food contact packaging"), 
     'Environment', 
     'https://www.europarl.europa.eu/news/en/press-room/20231117IPR12213/parliament-adopts-revamped-rules-to-reduce-reuse-and-recycle-packaging', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2022/0396(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-11-21-ITM-010_EN.html',
     ],
    # 14.09.2021 - 71prcnt in favor (removed because too old)
    #['135214', 'Defend and push on LGBTIQ rights in all EU countries ?', 'Human rights', 'https://oeil.secure.europarl.europa.eu/oeil/popups/summary.do?id=1674986&t=e&l=en', 'https://www.europarl.europa.eu/doceo/document/TA-9-2021-0366_EN.html'],
    # 30.03.2023, 427/79/76
    [4,
     '154076', 
     _('Require companies to disclose information that makes it easier for employees to compare salaries and to expose existing gender pay gaps'), 
     'Equality', 
     'https://www.europarl.europa.eu/news/en/press-room/20230327IPR78545/gender-pay-gap-parliament-adopts-new-rules-on-binding-pay-transparency-measures', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2021/0050(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-03-30-ITM-002_EN.html',
     ],
    # 22.11.2023, 524/85/21
    [5,
     '161196', 
     _('Remove most trade tariffs between EU and New Zealand while protecting sensitive EU agricultural sectors (like beef and dairy products) with tariff rate quotas. All EU geographical indications (GIs) are protected for wines and spirits as well as 163 famous EU foodstuff GIs'), 
     'International trade', 
     'https://www.europarl.europa.eu/news/en/press-room/20231117IPR12221/parliament-approves-eu-new-zealand-free-trade-agreement', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2023/0038M(NLE)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-11-21-ITM-009_EN.html',
     ],
    # 14.06.2023, 404/78/130 
    [6,
     '155946', 
     _('Set minimum quality standards for traineeships regarding duration, remuneration, access to social protection, and make them more accessible to persons with disabilities and to those from vulnerable backgrounds'), 
     'Employment and social affairs', 
     'https://www.europarl.europa.eu/news/en/press-room/20230609IPR96206/meps-call-for-new-rules-to-avoid-the-exploitation-of-trainees-across-the-eu', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2020/2005(INL)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-06-13-ITM-018_EN.html',
     # to check after 6 feb: 'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2024/2515(RSP)&l=en'
     ],
    # 20.04.2023, 391/140/25
    [7,
     '154562', 
     _('Facilitate the obtainment of the EU long-term resident status for foreigners who have been living in EU for more than 3 years'), 
     'Civil Liberties, justice and home affairs', 
    #  'https://www.europarl.europa.eu/news/en/press-room/20230419IPR80906/asylum-and-migration-parliament-confirms-key-reform-mandates', # too many things here
     'https://oeil.secure.europarl.europa.eu/oeil/popups/summary.do?id=1740310&t=e&l=en',
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2022/0134(COD)&l=en',
     ''],
    # 14.02.2023, 340/279/21 
    [8,
     '152544',
     _("Push carmakers to produce zero- and low-emission vehicles with the target of 100&#37; of zero emissions cars by 2035, while using a CO₂ computing methodology throughout the full life-cycle"), 
     'Environment', 
     'https://www.europarl.europa.eu/news/en/press-room/20230210IPR74715/fit-for-55-zero-co2-emissions-for-new-cars-and-vans-in-2035', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2021/0197(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-02-14-ITM-003_EN.html',
     ],

    # 09.05.2023, 499/73/55
    [9,
     '154711', 
     _('Ban methane flaring and venting for EU and non-EU companies (through rules on importations)'), 
     'Environment', 
     'https://www.europarl.europa.eu/news/en/press-room/20230505IPR84920/fit-for-55-meps-boost-methane-emission-reductions-from-the-energy-sector', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2021/0423(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-05-08-ITM-011_EN.html',
     ],
    # 12.09.2023, 530/66/32 
    [10,
     '157800', 
     _('Allow a short-term funding for the reinforcement of the European defence industry through joint procurement by member states, with bonuses for projects supporting Ukraine, Moldova and SMEs'), 
     'Security and defence', 
     'https://www.europarl.europa.eu/news/en/press-room/20230911IPR04908/meps-vote-to-strengthen-eu-defence-industry-through-common-procurement',
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2022/0219(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-09-11-ITM-017_EN.html',
     ],
    # 15.06.2323, 425/38/42 
    [11,
     '156440', 
     _('Calls on NATO members to invite Ukraine to join the alliance, support Ukraine on its path to EU accession, and put increased pressure on Russia through further sanctions'), 
     'Foreign affairs', 
     'https://www.europarl.europa.eu/news/en/press-room/20230609IPR96214/parliament-calls-on-nato-to-invite-ukraine-to-join-the-alliance', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2023/2739(RSP)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-06-13-ITM-002_EN.html',
     ],
    # 15.06.2023, 411/97/37 
    [12,
     '156258', 
     _('Launch investigations and implement safeguards to prevent abuse in the use of spyware (e.g. by police, EU or imported from/exported to non-EU governments)'), 
     'Liberty', 
     'https://www.europarl.europa.eu/news/en/press-room/20230609IPR96217/spyware-meps-call-for-full-investigations-and-safeguards-to-prevent-abuse', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2022/2077(INI)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-06-14-ITM-014_EN.html'],
    # 13: 13.07.2023, 441/70/71
    [13,
     '157621', 
     _("Following the Qatargate corruption affair, call to implement effective systems to detect foreign interference in European Parliament activity and enforce sanctions on offending countries. Call for a rapid review of the MEP's Code of Conduct and monitor the activity of former MEPs"), 
     'Democracy', 
     'https://www.europarl.europa.eu/news/en/press-room/20230707IPR02440/defending-democratic-institutions-and-ep-s-integrity-against-malign-interference', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2023/2034(INI)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-07-12-ITM-020_EN.html'],
    # 14: 14.12.2023, 366/154/15 
    [14,
     '162797', 
     _("Increase capacity of the Frontex european agency to search and rescue migrants at sea, and to fight against criminal smugglers and human traffickers. The voted text also give feedback regarding specific situations in Greece, Lithuania and Hungary"), 
     'Civil liberties, justice and home affairs', 
     'https://www.europarl.europa.eu/news/en/press-room/20231208IPR15787/frontex-meps-want-an-effective-border-agency-compliant-with-fundamental-rights', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2023/2729(RSP)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-12-13-ITM-021_EN.html'],
    # 15: 18.04.2023, 463/117/64
    [15,
     '154167', 
     _('Regarding the EU CO₂ emissions trading system, phase out the free allowances to the aviation sector by 2026 while promoting the use of sustainable aviation fuels'), 
     'Environment', 
    #  'https://www.europarl.europa.eu/news/en/press-room/20230414IPR80120/fit-for-55-parliament-adopts-key-laws-to-reach-2030-climate-target', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/summary.do?id=1741160&t=e&l=en', # put this as abstract as the news talk of other things too
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?reference=2021/0207(COD)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-04-17-ITM-015_EN.html'],
    # 16: 12.12.2023, 409/173/31 
    [16,
     '162205', 
     _('Foster the development of small modular reactors (SMRs) for nuclear electricity production'), 
     'Environment', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/summary.do?id=1769966&t=e&l=en', 
     'https://oeil.secure.europarl.europa.eu/oeil/popups/ficheprocedure.do?lang=en&reference=2023/2109(INI)',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-12-11-ITM-015_EN.html'],
    # 12.12.2023, 232/331/49 (amendment n°2)
    [17,
     '162327', 
     _('Calls on Member States to introduce solidarity taxes on high levels of wealth to provide for funding to mitigate the major challenges of our times; supports calls to start international-level discussions to establish a progressive wealth tax'), 
     'Economy', 
     'https://www.europarl.europa.eu/doceo/document/A-9-2023-0336-AM-002-003_EN.pdf', 
     'https://oeil.secure.europarl.europa.eu/oeil//popups/ficheprocedure.do?reference=2023/2058(INI)&l=en',
     'https://www.europarl.europa.eu/doceo/document/CRE-9-2023-12-11-ITM-014_EN.html'],
    # date, votes
    # [17, 'id', 'title', 'category', 'url_press', ''],
    # date, 
]


stanceDict = {'+':'for', '-': 'ag', '0':'abs'}

for voteidList in voteidListList:
    voteid = voteidList[1]
    voteabstract = voteidList[2]
    print(voteabstract)
    with open("parltrack_data/ep_votes.json", 'r', encoding='utf-8') as file:
        for line in file:
            if voteid in line:
                oneline = json.loads(line[1:])

                # Create a Vote instance
                vote = Vote(
                    vote_number = voteidList[0],
                    vote_id = oneline['voteid'],
                    vote_date = oneline['ts'][:10],
                    xml_url = oneline['url'],
                    title = oneline['title'],
                    text_id = oneline['doc'],
                    epref = oneline['epref'][0],
                    total_for = oneline['votes']['+']['total'],
                    total_against = oneline['votes']['-']['total'],
                    total_abs = oneline['votes']['0']['total'],
                    short_desc = voteidList[2],
                    topic = voteidList[3],
                    summary_url = voteidList[4],
                    procedure_url = voteidList[5],
                    debate_url = voteidList[6],
                )
                vote.save()
                
                for stance in ['+', '-', '0']:
                    print(stance)
                    mepIdsList = [list(mepDict.values())[0] for listofMepDict in oneline['votes'][stance]['groups'].values() 
                                for mepDict in listofMepDict]
                    for mep_id in mepIdsList:
                        try:
                            mep = Mep.objects.get(mep_id=mep_id)
                        except Mep.DoesNotExist:
                            print(f"{mep_id} not active")
                            continue
                        
                        try:
                            position = Position(
                                mep = mep,
                                vote = vote,
                                stance = stanceDict[stance],
                                comment = '',
                            )
                        except IntegrityError as e:
                            # should not occur
                            print(e)
                            print(Position.objects.get(mep_id=mep_id, vote_id=voteid))
                        position.save()
        print()



