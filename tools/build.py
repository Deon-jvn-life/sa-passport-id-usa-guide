#!/usr/bin/env python3
"""Build the South Africans in the USA passport and Smart ID guide into site/. Run: python3 tools/build.py"""
import json,os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
from sitelib import Site,CSS,D,esc,a,slug,href
BASE="https://sa-passport-id-usa-guide.vercel.app"
S=dict(dha="https://www.dha.gov.za/index.php/civic-services/dha-service-centres-abroad",vfs="https://services.vfsglobal.com/usa/en/zap/",
 vfsinfo="https://visa.vfsglobal.com/one-pager/southafrica/usa/passport-services/index.html",book="https://passports.vfsglobal.com/usa/en/zaf/login",
emb="https://www.saembassy.org/sa-citizens-services/",ny="https://dirco.gov.za/newyork/",la="https://dirco.gov.za/losangeles/",
 lalaunch="https://dirco.gov.za/losangeles/2026/01/29/the-launch-of-the-new-vfs-centre/",
 etc="https://www.saembassy.org/wp-content/uploads/2025/08/EMERGENCY-TRAVEL-CERTIFICATE-ETC.pdf", embadult="https://www.saembassy.org/wp-content/uploads/2026/02/ADULT-PASSPORT-CHECKLIST.pdf",
 embid="https://www.saembassy.org/wp-content/uploads/2026/02/RE-ISSUE-OF-ID-BOOK.pdf",photo="https://www.saembassy.org/wp-content/uploads/2023/09/Passport_ID_PhotoSpecifications-scaled.jpg",
 rol="https://www.saembassy.org/wp-content/uploads/2023/09/rol.pdf",finder="https://sa-smart-id-bank-finder.vercel.app",
 embbirth="https://www.saembassy.org/visas/civic_immigration/birth_registration/",
 cc="https://collections.concourt.org.za/items/a730fad7-a956-4ba3-8f39-2778134b8dfb",
 govsmart="https://www.gov.za/news/media-statements/home-affairs-milestone-one-million-smart-ids-delivered-seven-months-26-oct",
 saflii="https://www.saflii.org/za/cases/ZACC/2025/8.html",
 dhaannounce="https://www.dha.gov.za/index.php/statements-speeches/1980-restoring-dignity-through-digital-progress-home-affairs-launches-new-citizenship-portal",
 dhacit="https://www.dha.gov.za/index.php/citizenship1",
 portal="https://myhomeaffairsonline.dha.gov.za/reinstatement-of-citizenship",
 portalfaq="https://myhomeaffairsonline.dha.gov.za/faq",
 embcit="https://www.saembassy.org/visas/civic_immigration/citizenship/",
 embret="https://www.saembassy.org/wp-content/uploads/2024/02/RETETION-OF-SA-CITIZENSHIP.pdf",
 embex="https://www.saembassy.org/wp-content/uploads/2024/02/EXEMPTION-OF-SA-CITIZENSHIP.pdf",
 embren="https://www.saembassy.org/wp-content/uploads/2024/02/RENUNCIATION-OF-SA-CITIZENSHIP.pdf",
 nyciv="https://dirco.gov.za/newyork/immigration-and-civic/",
 nyimm="https://dirco.gov.za/newyork/immigration-services/",
 laimm="https://dirco.gov.za/losangeles/immigration-services/")
def src(*k): return ' <span class="src">['+', '.join(a(S[x]) for x in k)+']</span>'
C=json.load(open(os.path.join(HERE,'centres.json'))); M=json.load(open(os.path.join(HERE,'missions.json')))
CENTRE_NAV=[('centres/index.html','All centres')]+[(f'centres/{x["id"]}/index.html', x["city"]) for x in C]
GROUPS=[
 ("Find a centre", CENTRE_NAV),
 ("Documents and fees",[('what-to-bring/index.html','What to bring'),('fees/index.html','Fees'),('smart-id/index.html','Smart identity card')]),
 ("After you apply",[('tracking/index.html','Track an application'),('lost-passport/index.html','Lost passport')]),
 ("Citizenship and offices",[('citizenship/index.html','Citizenship'),('embassy-consulates/index.html','Embassy and consulates')]),
 ("Using this guide",[('faq/index.html','Common questions'),('find/index.html','All pages'),('disclaimer/index.html','Disclaimer')])]
ORDER=['what-to-bring/index.html','fees/index.html','smart-id/index.html','centres/index.html','tracking/index.html','lost-passport/index.html','embassy-consulates/index.html','citizenship/index.html']
FOOT=f'This is an unofficial, independent guide for South Africans in the United States. It is not affiliated with the Department of Home Affairs (DHA), DIRCO, the South African Embassy or consulates, VFS Global or the SA Chamber of Commerce in the USA. Facts are taken from the official pages linked on each page; always confirm on {a(S["vfs"],"the VFS Global South Africa USA site")} and {a(S["dha"],"DHA")} before you travel or pay.'
DISCLAIMER='For general information only. This independent site is not affiliated with any government, bank or agency. Information can change and may contain errors; always confirm with the official source before you act. Nothing here is legal, financial or professional advice, and we accept no liability for decisions made using it.'
# Search-console tokens. Leave a value empty and the matching meta tag is omitted.
VERIFY={"google-site-verification":"XA7XgB_UwrIRvQyNVsnWpSyTyaU6e3-v4g4RBw8RAVI","msvalidate.01":""}
RELATED=[("https://sa-refugees-usa-guide.vercel.app/","South African refugees in the USA"),("https://sa-smart-id-bank-finder.vercel.app/","SA Smart ID bank branch finder")]
BLURB={
 'centres/index.html':'Addresses, days and hours for every centre, and how to book an appointment.',
 'what-to-bring/index.html':'Forms, originals, copies and photo rules for a passport or identity document.',
 'fees/index.html':'Published fees for a passport, a lost passport, a first identity document and birth registration, and how you pay.',
 'smart-id/index.html':'A first identity document and a Smart identity card re-issue, and where the official pages do not match.',
 'lost-passport/index.html':'Replacing a lost or stolen passport, and the emergency travel certificate from the Embassy.',
 'tracking/index.html':'How to track an application, and how collection and courier delivery are described.',
 'citizenship/index.html':'The 6 May 2025 court order, who it does not cover, and the Department of Home Affairs online status check.',
 'embassy-consulates/index.html':'Addresses, hours, phone numbers and areas served for the Embassy in Washington and the consulates in New York and Los Angeles.',
 'faq/index.html':'Short sourced answers about appointments, documents, fees, a lost passport and citizenship.',
 'find/index.html':'Every page on this guide, listed by topic.',
 'disclaimer/index.html':'Accuracy, no warranty, liability, external links and how to check the official source.'}
for x in C:
    BLURB[f'centres/{x["id"]}/index.html']=f'Address, days, hours, services and how to book the {x["city"]} centre.'
ALIAS={
 'centres/index.html':'vfs centre center address hours appointment booking',
 'what-to-bring/index.html':'dha-73 dha-529 dha-9 bi-529 photos documents checklist fingerprints',
 'fees/index.html':'cost price dollar maxi consular service fee money order',
 'smart-id/index.html':'smart id card identity reissue re-issue green book',
 'lost-passport/index.html':'lost stolen emergency travel certificate etc di-47 police',
 'tracking/index.html':'track status courier collection delivery',
 'citizenship/index.html':'dual citizenship retain renounce constitutional court section 6',
 'embassy-consulates/index.html':'embassy consulate washington new york los angeles phone emergency dirco',
 'faq/index.html':'questions answers faq',
 'find/index.html':'search index all pages',
 'disclaimer/index.html':'liability warranty accuracy'}
for x in C:
    ALIAS[f'centres/{x["id"]}/index.html']=' '.join([x['id'], x['city'], x['state'], x['address'], 'vfs centre'])
READ={
 'index.html':['what-to-bring/index.html','fees/index.html','centres/index.html','lost-passport/index.html'],
 'what-to-bring/index.html':['fees/index.html','smart-id/index.html','centres/index.html','citizenship/index.html'],
 'fees/index.html':['what-to-bring/index.html','smart-id/index.html','centres/index.html','citizenship/index.html'],
 'smart-id/index.html':['what-to-bring/index.html','fees/index.html','centres/index.html','citizenship/index.html'],
 'centres/index.html':['what-to-bring/index.html','fees/index.html','tracking/index.html','embassy-consulates/index.html'],
 'tracking/index.html':['centres/index.html','what-to-bring/index.html','lost-passport/index.html','fees/index.html'],
 'lost-passport/index.html':['embassy-consulates/index.html','fees/index.html','tracking/index.html','citizenship/index.html'],
 'embassy-consulates/index.html':['lost-passport/index.html','centres/index.html','citizenship/index.html','faq/index.html'],
 'citizenship/index.html':['what-to-bring/index.html','lost-passport/index.html','embassy-consulates/index.html','smart-id/index.html'],
 'faq/index.html':['what-to-bring/index.html','fees/index.html','centres/index.html','citizenship/index.html'],
 'find/index.html':['what-to-bring/index.html','centres/index.html','faq/index.html','disclaimer/index.html'],
 'disclaimer/index.html':['find/index.html','faq/index.html','what-to-bring/index.html','centres/index.html'],
 '404.html':['find/index.html','centres/index.html','what-to-bring/index.html','faq/index.html']}
for x in C:
    READ[f'centres/{x["id"]}/index.html']=['centres/index.html','what-to-bring/index.html','fees/index.html','tracking/index.html']
s=Site(ROOT,BASE,"SA Passport and ID Guide (USA)",GROUPS,ORDER,FOOT,CSS,related=RELATED,disclaimer=DISCLAIMER,verify=VERIFY)
s.summaries=BLURB
s.read_next=READ
s.aliases=ALIAS
s.long_pages={'centres/index.html','what-to-bring/index.html','fees/index.html','smart-id/index.html','lost-passport/index.html','tracking/index.html','embassy-consulates/index.html','citizenship/index.html','faq/index.html'}
s.flow_toc={'index.html','find/index.html','fees/index.html','centres/index.html'}
BOOK=f'<div class="card warn"><strong>Book an appointment online.</strong> The Department of Home Affairs lists an online booking link for every United States centre{src("dha")}. VFS Global tells you to book an appointment{src("vfsinfo")}. The New York consulate says you may use the centre that is most convenient{src("ny")}. Book only through {a(S["vfs"],"services.vfsglobal.com/usa/en/zap")}.</div>'
CONF=f'''<div class="card conf"><strong>Conflicts between official sources (as of {D})</strong><ul>
<li><strong>Processing time.</strong> VFS Global says six to eight weeks{src("vfsinfo")}. The Embassy says a minimum of 6 to 8 months for applications lodged with it{src("emb","embadult")}.</li>
<li><strong>Smart identity card re-issue at VFS Global.</strong> VFS Global lists "Smart ID - Reissue" at $12 consular plus a $60 service fee, and it publishes a re-issue checklist{src("vfsinfo")}. The Department of Home Affairs says the centres initially offer passport applications and renewals, and birth certificate applications{src("dha")}. The New York and Los Angeles consulate notices list a first identity document. They do not list a Smart identity card re-issue{src("ny","lalaunch")}. Check the VFS Global booking categories before you book.</li>
<li><strong>Washington, DC centre.</strong> The Department of Home Affairs lists a centre in Washington, DC{src("dha")}. The New York consulate says VFS Global services launched in New York and Washington, DC{src("ny")}. The Embassy page lists only Atlanta, Miami, Houston, Chicago, Los Angeles and New York{src("emb")}.</li>
<li><strong>Applying at the Embassy.</strong> The Embassy page says "No appointment required" for applications Monday to Thursday, 9:30 a.m. to 12:30 p.m. The same page says no mailed-in passport, identity document or birth registration applications will be processed, and it points those applications to VFS Global{src("emb")}.</li>
<li><strong>How far ahead to apply.</strong> VFS Global says book at least 18 months before your passport expires{src("vfsinfo")}. The Embassy says 12 months{src("emb")}.</li></ul></div>'''
def centre_card(x,link=True):
    t=f'<a href="{x["id"]}/index.html">{esc(x["city"])}</a>' if link else esc(x['city'])
    n=f'<p class="src"><span class="tag mix">Note</span> {esc(x["note"])}</p>' if x['note'] else ''
    return f'<tr><td><strong>{t}</strong></td><td>{esc(x["address"])}</td><td>{esc(x["days"])}</td><td>{esc(x["hours"])}{n}</td><td>{a(S["vfs"],"Book on VFS")}{src("dha")}</td></tr>'
TH='<div class="wrap" tabindex="0" role="region" aria-label="Centre addresses and hours"><table><tr><th>Centre</th><th>Address</th><th>Days</th><th>Hours</th><th>Booking and sources</th></tr>'
def topics_html():
    chunks=['<h2>All topics</h2>','<p>Every page on this guide, grouped by topic.</p>']
    for g,items in GROUPS:
        cards=''.join(f'<li><a class="jump" href="{p}"><span class="lt">{esc(t)}</span><span class="ls">{esc(BLURB[p])}</span></a></li>' for p,t in items)
        chunks.append(f'<section class="topic" id="{slug(g)}"><h3>{esc(g)}</h3><ul class="link-grid">{cards}</ul></section>')
    return ''.join(chunks)
TASKS=f'''<h2>Start here</h2>
<p>Top tasks on this guide.</p>
<ul class="tasks">
<li><a class="jump" href="what-to-bring/index.html"><span class="lt">What to bring:</span><span class="ls"> forms DHA-73, DHA-529 and DHA-9, originals plus copies, four photos.</span></a></li>
<li><a class="jump" href="fees/index.html"><span class="lt">Fees:</span><span class="ls"> adult or child renewal $127 in total at VFS ($67 consular + $60 VFS), card only{src("vfsinfo")}.</span></a></li>
<li><a class="jump" href="smart-id/index.html"><span class="lt">Smart ID:</span><span class="ls"> first ID and re-issue options and what is still unclear.</span></a></li>
<li><a class="jump" href="lost-passport/index.html"><span class="lt">Lost passport and emergency travel certificate.</span></a></li>
<li><a class="jump" href="citizenship/index.html"><span class="lt">Citizenship:</span><span class="ls"> the 6 May 2025 Constitutional Court ruling, who is excluded, and the DHA online status check.</span></a></li>
<li><a class="jump" href="tracking/index.html"><span class="lt">Tracking your application.</span></a></li>
<li><a class="jump" href="embassy-consulates/index.html"><span class="lt">Embassy and consulates:</span><span class="ls"> areas, hours and emergency numbers.</span></a></li>
<li><a class="jump" href="faq/index.html"><span class="lt">FAQ.</span></a></li>
</ul>'''
body=f'''<h1>Renew a South African passport or ID in the USA</h1>
<p>A plain-language guide for South Africans living in the United States. Since late 2025 and January 2026, Department of Home Affairs passport, first identity document and birth registration applications are taken by appointment at {len(C)} VFS Global centres in the United States{src("dha","ny")}. This guide lists every centre with days and hours, what to bring, fees exactly as published, tracking, and what to do about a lost passport or urgent travel.</p>
{BOOK}
{TASKS}
{topics_html()}
<h2>VFS Global centres in the USA</h2>{TH}{''.join(centre_card(x).replace('href="','href="centres/',1) for x in C)}</table></div>
<p>Saturday only: Atlanta and Miami. Weekdays: Chicago, Houston, Los Angeles, New York and Washington, DC{src("dha")}.</p>
{CONF}
<div class="card note"><strong>Not eligible at VFS centres:</strong> The Department of Home Affairs says applicants aged 16 and above (including those 15 turning 16 that year) must first get an identity document before a passport, and citizens born abroad whose birth is not yet registered cannot be served at the centres. They must go to a South African mission{src("dha")}. The VFS Global service list does not include the Emergency Travel Certificate{src("vfsinfo")}.</div>
<p>Need to know which South African banks let you apply for a Smart ID in South Africa? See the separate {a(S["finder"],"SA Smart ID bank branch finder")}.</p>'''
s.page('index.html',"South African passport and Smart ID renewal in the USA",
 "Unofficial guide for South Africans in the USA: VFS centres, documents, fees, tracking, lost passports, emergency travel and citizenship.",body)
b=f'<h1>VFS Global centres for South African passports in the USA</h1><p>All {len(C)} centres listed by the Department of Home Affairs on {D}{src("dha")}. Hours are for both submission and collection.</p>{BOOK}{TH}{"".join(centre_card(x) for x in C)}</table></div><p class="src">An automated check of the VFS Global booking site {a(S["vfs"],"services.vfsglobal.com/usa/en/zap")} on {D} returned 403 Forbidden. The consular services page was readable. Confirm the booking page in your own browser before you travel.</p>'
s.page('centres/index.html',"South African passport centre addresses and hours at VFS","Addresses, days and hours for every South African passport and ID centre in the USA, and how to book an appointment at VFS.",b)
for x in C:
    n=f'<div class="card conf">{esc(x["note"])}{src("dha","ny","emb")}</div>' if x['note'] else ''
    b=f'''<h1>South African passport and ID at VFS {esc(x["city"])}</h1>
<div class="card"><p><strong>Address:</strong> {esc(x["address"])}{src("dha")}</p><p><strong>Days:</strong> {esc(x["days"])}</p><p><strong>Hours:</strong> {esc(x["hours"])}{src("dha")}</p><p><strong>Booking:</strong> online, through {a(S["vfs"],"VFS Global for South Africa in the USA")}. The Department of Home Affairs lists an online booking link for this centre{src("dha","vfsinfo")}.</p><p><strong>Who can use it:</strong> the New York consulate says you may submit at the centre most convenient to you{src("ny")}.</p></div>{n}
<h2>Services</h2><ul><li>Passport applications and renewals, adult and child{src("dha","lalaunch")}</li><li>First identity document for a child turning 16 in the year, or for anyone 16 or older who has not applied for a first identity document{src("lalaunch","vfsinfo")}</li><li>Birth registration within 30 days of birth. VFS Global does not take late registration. Late registration goes to a South African mission{src("vfsinfo")}</li><li>Not on the VFS Global list: Emergency Travel Certificate{src("vfsinfo")}</li></ul>
<div class="card conf"><strong>Birth registration conflict.</strong> VFS Global accepts a birth registration within 30 days of birth{src("vfsinfo")}. The Department of Home Affairs says a citizen born abroad whose birth is not on the population register cannot be served at these centres and must go to a mission{src("dha")}.</div>
<h2>Before you go</h2><p>Bring every form and document on the {a("../../what-to-bring/index.html","what to bring")} checklist, and a credit or debit card: VFS accepts card only{src("vfsinfo")}. See {a("../../fees/index.html","fees")}.</p>'''
    CT={"atlanta":"Atlanta passport centre address, days and hours at VFS","chicago":"Chicago passport centre address, days and hours at VFS","houston":"Houston passport centre address, days and hours at VFS","los-angeles":"Los Angeles passport centre address, days and hours at VFS","miami":"Miami Coral Gables passport centre address and hours at VFS","new-york":"New York passport centre address, days and hours at VFS","washington-dc":"Washington, DC passport centre address and hours at VFS"}
    s.page(f'centres/{x["id"]}/index.html',CT[x["id"]],f"{x['city']} centre for a South African passport or ID: address, days, hours, services offered, and how to book an appointment at VFS.",b,crumb=x["city"])
b=f'''<h1>What to bring to VFS for a South African passport</h1><p>Summarised from the VFS Global consular services information page{src("vfsinfo")}. Complete all forms in black ink, no correction fluid, and write N/A rather than leaving blanks.</p>
<h2>Adult passport (16 and older)</h2><div class="card"><ul>
<li>Form DHA-73 passport application: complete section A and sign section E. Section B is completed at your appointment.</li>
<li>DHA-529 Determination of Citizenship Status: required for every passport application made outside South Africa. Questions A9 and A10 must be answered and section E signed.</li>
<li>DHA-9 fingerprint form: not downloadable at VFS; you complete it at the appointment.</li>
<li>DI-47 loss report plus a police report, if your passport was lost or stolen.</li>
<li>Originals and copies of: current SA passport, SA ID (green ID book or Smart ID card), SA birth certificate, marriage certificate if a married surname is to appear in the passport. The centre can certify copies if you show the original.</li>
<li>Dual citizens: proof of how and when you acquired the other nationality, such as a naturalization certificate and retention certificate. A foreign passport or ID is not proof of how and when you acquired it. The February 2026 Embassy adult checklist still asks for a copy of a retention certificate if applicable{src("embadult")}. For the 6 May 2025 ruling and the DHA online check, see {a('../citizenship/index.html','citizenship')}.</li>
<li>Foreign-language documents need a sworn English translation; foreign birth, marriage and divorce documents must be legalised or apostilled.</li>
<li>Four colour photos, 35 mm x 45 mm, head and shoulders. Photos can be taken at the centre for a fee. Do not attach them to the form.</li></ul>{src("vfsinfo")}</div>
<div class="card note"><strong>First adult passport (turning 16):</strong> apply for the first ID card first or together with the passport, and both parents and the child must attend{src("vfsinfo")}.</div>
<h2>Child passport (under 16)</h2><div class="card"><ul><li>DHA-73 and BI-529 (section E signed by a parent); parental consent on page 2 section C is signed in the office, and both parents must be present for applicants under 18.</li><li>If one parent is not in the USA, consent must be obtained from Home Affairs in South Africa or a South African embassy where that parent lives.</li><li>Originals and copies: child's current passport, SA birth certificate, both parents' SA IDs and passports.</li><li>Under 15 and a half: no fingerprints required. Four photos, 35 x 45 mm.</li></ul>{src("vfsinfo")}</div>
<h2>First ID</h2><div class="card"><ul><li>BI-529, DHA-9 (at appointment), certified unabridged birth certificate and both parents' ID and passport first pages, certifications not older than 3 months. Four photos.</li></ul>{src("vfsinfo")}</div>
<h2>Embassy checklist (for comparison)</h2><p>The Embassy adult checklist also asks for a copy of a retention certificate if applicable, and a divorce decree or written request where you change or keep a surname{src("embadult")}. Embassy photo specification: {a(S["photo"],"official image")}.</p>'''
s.page('what-to-bring/index.html',"What to bring for a South African passport or ID in the USA","Forms DHA-73, DHA-529 and DHA-9, documents, copies and photo rules for a South African passport or ID at VFS in the USA.",b)
rows=[("Passport renewal, adult","$67","$60","$127"),("Passport renewal, adult MAXI","$133","$60","$193"),("Passport lost, adult","$134","$60","$194"),("Passport lost MAXI, adult","$266","$60","$326"),("Passport renewal, child","$67","$60","$127"),("Passport renewal, MAXI child","$133","$60","$193"),("Passport lost, child","$134","$60","$194"),("Passport lost MAXI, child","$266","$60","$326"),("First ID issuance / Smart ID first issuance","$0","$60","$60"),("Smart ID re-issue","$12","$60","$72"),("Birth registration","$6","$60","$66")]
b=f'''<h1>Fees for South African passports and ID at VFS in the USA</h1><p>As published by VFS Global on {D}{src("vfsinfo")}. Pay at the centre by credit or debit card only; other payment methods are not accepted. The VFS service fee is $60 on top of the consular fee.</p>
<div class="wrap" tabindex="0" role="region" aria-label="Published fees"><table><tr><th>Service</th><th>Consular fee (USD)</th><th>VFS service fee (USD)</th><th>Total (USD)</th></tr>{''.join(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in rows)}</table></div>
<p class="src">MAXI is the larger passport; the Embassy checklist describes Regular as 32 pages and MAXI as 48 pages{src("embadult")}. Photos at the centre carry a separate fee that VFS does not state on the page we checked{src("vfsinfo")}.</p>
<h2>Embassy fees (money order, no cards)</h2><div class="card"><ul><li>Passport: $67 regular (32 pages), $133 MAXI (48 pages), $134 regular lost/damaged/stolen, $266 MAXI lost/damaged/stolen, by money order payable to SA Embassy{src("embadult")}.</li><li>Re-issue of ID book: $12 by money order{src("embid")}.</li><li>Emergency Travel Certificate: $12 by money order{src("etc")}.</li><li>The Embassy accepts the exact fee in cash or money order, no card payments{src("emb")}.</li></ul></div>
<div class="card note"><strong>Citizenship.</strong> The DHA reinstatement FAQ does not state a fee. The Embassy citizenship page still publishes $25 for a section 6(2) retention application made before foreign citizenship is taken, and $25 for a section 26(4) exemption for foreign citizenship taken before 6 October 1995{src("dhacit","embcit")}. See {a('../citizenship/index.html','citizenship')}.</div>'''
s.page('fees/index.html',"South African passport fees in the USA (VFS and Embassy)","Published VFS Global and SA Embassy fees for South African passport renewal, lost passport, MAXI, child, ID and birth registration in the USA.",b)
b=f'''<h1>South African Smart ID in the USA</h1>
<div class="card"><p><strong>First ID (16 and older):</strong> VFS takes first ID applications for children aged 15 turning 16 in the year and for anyone 16 or older who never applied for a first ID. Fee $60 (consular $0 + VFS $60){src("vfsinfo","lalaunch")}.</p>
<p><strong>Re-issue:</strong> VFS publishes a "Re-Issue ID Card" checklist and a Smart ID re-issue fee of $72 ($12 + $60){src("vfsinfo")}. Required: BI-529, DHA-9 at the appointment, certified unabridged birth certificate (and name change approval if relevant), certified unabridged marriage certificate for female applicants, and four photos{src("vfsinfo")}.</p></div>
{CONF}
<p>The Embassy re-issue checklist lists DHA-9, BI-529, copy of passport, marriage certificate if changing surname, 2 photos and a $12 money order, with a minimum 6 to 8 months processing{src("embid")}. It also says no mailed-in applications will be processed from 1 March 2026.</p>
<p>Planning a visit to South Africa? On 26 October 2026 the Department of Home Affairs said a replacement Smart identity card is available at 669 bank branches in South Africa, and that you can apply there without a prior booking. The same statement says production of the green identity book stops on 31 March 2027, and recognition of that book as a valid identity document ends by 31 March 2028. It also says passport applications, a first Smart identity card, and home delivery will be added at those branches. It does not give a start date for those extra services. VFS Global in the United States still lists a green identity book as a document you can bring{src("govsmart","vfsinfo")}. See the separate {a(S["finder"],"SA Smart ID bank branch finder")}.</p>'''
s.page('smart-id/index.html',"South African Smart ID in the USA: first ID and re-issue","What official sources say about applying for a first South African ID or re-issuing a Smart ID card from the USA, with conflicts flagged.",b)
EMC=''.join('<li>'+esc(m['name'])+': '+esc(m['phone'])+' <span class="src">['+a(m['url'])+']</span></li>' for m in M)
b=f'''<h1>Lost South African passport in the USA and emergency travel</h1>
<h2>Replacing a lost or stolen passport</h2><div class="card"><ul><li>Report the loss to the police and complete form DI-47 (loss of passport report); bring both to VFS with your other documents{src("vfsinfo")}.</li><li>Fees at VFS: lost adult or child passport $194 ($134 + $60); lost MAXI $326 ($266 + $60){src("vfsinfo")}.</li><li>The Embassy also publishes a {a(S["rol"],"report of lost travel document form")}{src("emb")}.</li></ul></div>
<h2>Emergency Travel Certificate</h2><div class="card warn"><p>The VFS Global service list does not include an Emergency Travel Certificate{src("vfsinfo")}. The certificate is handled by the Embassy. It is a one-way travel document to South Africa only, valid for a maximum of three months from issue{src("etc")}.</p>
<ul><li>Completed DHA-73 and DHA-9 (a copy of the original DHA-9 can be used; prints must be clear)</li><li>2 photos (colour, no smile, mouth closed, no glasses)</li><li>Copy of passport, South African birth certificate or identity document</li><li>Proof of travel arrangements and a written reason for urgent travel to South Africa</li><li>Fee $12 money order payable to the South African Embassy, plus a prepaid envelope for collection</li><li>The Embassy form says the minimum processing period is 7 business days. Submit or mail the application to the South African Embassy, 3051 Massachusetts Avenue NW, Washington, DC 20008.</li></ul>{src("etc")}
<p>The Department of Home Affairs says an Emergency Travel Certificate issued abroad usually takes 3 to 5 working days{src("dhacit")}.</p>
<p>The New York and Los Angeles immigration pages use the same sentence. They say the embassy is open for this certificate Monday to Friday, 9:00 a.m. to 12:00 p.m. and 1:30 p.m. to 3:30 p.m., without an appointment, and that the process takes 2 to 5 days. They say "the embassy". Those hours are not the consular hours on the New York or Los Angeles home pages, so this guide does not use 2 to 5 days as the timing at those consulates{src("nyimm","laimm")}.</p>
<p>Home Affairs will not approve an Emergency Travel Certificate for applicants eligible for a first identity document (turning 16 and above) who have not applied for it{src("etc")}.</p>
<p>DHA says a South African living abroad who still holds South African citizenship needs a valid South African passport to travel to South Africa, and that proof of a passport application is not accepted for travel. See {a('../citizenship/index.html','citizenship')}{src("dhacit")}.</p></div>
<h2>Emergency contacts</h2><ul>{EMC}</ul>'''
s.page('lost-passport/index.html',"Lost South African passport and emergency travel in the USA","What to do if you lose your South African passport in the USA: police report, DI-47, VFS fees and Embassy Emergency Travel Certificate requirements.",b)
b=f'''<h1>Track a South African passport or ID application from the USA</h1><div class="card"><ul>
<li><strong>VFS tracking:</strong> use the "Track your application" option in the menu of the {a(S["vfs"],"VFS Global South Africa USA site")}{src("vfs")}. The address visatracking.vfsglobal.com/Global returned 404 Not Found on {D}, so this guide does not link it.</li>
<li><strong>Collection:</strong> DHA says that from 1 November 2025 service centres offer optional secure courier delivery to an address you choose{src("dha")}. Centre hours include collection times{src("dha")}.</li>
<li><strong>Embassy applications:</strong> follow up on status through the Home Affairs contact centre at hacc@dha.gov.za. Send your prepaid collection envelope only once the Embassy tells you the document is ready (postage not less than $10){src("emb")}.</li>
<li><strong>Los Angeles Consulate:</strong> to have a passport returned by post, bring a prepaid self-addressed USPS or UPS envelope; FedEx is not accepted{src("la")}.</li></ul></div>
<div class="card note">Expected timing differs by official source: six to eight weeks on the VFS Global page, and at least 6 to 8 months at the Embassy{src("vfsinfo","emb")}.</div>'''
s.page('tracking/index.html',"Track a South African passport application in the USA","How to track a South African passport or ID application made at VFS or the Embassy in the USA, and how collection and courier delivery work.",b)
b='<h1>South African Embassy and consulates in the USA</h1><p>VFS centres now take most passport, first ID and birth registration applications. The missions still handle emergency travel certificates, late birth registration and other civic matters. The Embassy citizens services page links to the DHA citizenship reinstatement portal. See '+a('../citizenship/index.html','citizenship')+src("emb","portal")+'.</p>'+''.join(f'<div class="card"><h2>{esc(m["name"])}</h2><p><strong>Address:</strong> {esc(m["address"])}</p><p><strong>Phone:</strong> {esc(m["phone"])}</p><p><strong>Email:</strong> {esc(m["email"])}</p><p><strong>Hours:</strong> {esc(m["hours"])}</p><p><strong>Area served:</strong> {esc(m["area"])}</p><p class="src">[{a(m["url"],"official page")}]</p></div>' for m in M)+f'<div class="card note">Gap: no official web page for a South African consulate in Chicago could be confirmed on {D}; Chicago appears here only as a VFS centre{src("dha")}.</div>'
s.page('embassy-consulates/index.html',"South African Embassy and consulates in the USA: contacts","Addresses, hours, emergency phone numbers and areas served for the South African Embassy in Washington and consulates in New York and Los Angeles.",b)
faq=[("Can I walk in at a VFS centre?",f"Book an appointment online. The Department of Home Affairs lists an online booking link for every United States centre{src('dha')}. VFS Global tells applicants to book an appointment{src('vfsinfo')}."),
("Do I have to use the centre for my state?",f"No. The New York consulate says you may submit at the centre most convenient to you{src('ny')}."),
("Can I mail my renewal to the Embassy?",f"No. The Embassy says no mailed-in passport, ID or birth registration applications will be processed{src('emb')}."),
("How do I pay at VFS?",f"Credit or debit card only{src('vfsinfo')}."),
("How much is an adult renewal?",f"$127 at VFS: $67 consular fee plus $60 VFS service fee. MAXI is $193{src('vfsinfo')}."),
("How many photos?",f"Four colour photos, 35 x 45 mm, for passports and IDs at VFS{src('vfsinfo')}."),
("My child is 15 and turns 16 this year. Can they renew a passport?",f"They must apply for a first ID first or together with the first adult passport; both parents and the child must attend{src('vfsinfo','dha')}."),
("I am travelling to South Africa in a few days and my passport is lost.",f"Contact the Embassy about an Emergency Travel Certificate. The Embassy form says a minimum of 7 business days{src('etc')}. The Department of Home Affairs says the usual time abroad is 3 to 5 working days{src('dhacit')}. VFS Global does not list the certificate as a service{src('vfsinfo')}. The Department of Home Affairs says proof of a passport application is not accepted for travel to South Africa{src('dhacit')}."),
("I became a US citizen. Did I lose my South African citizenship?",f"The Constitutional Court declared the automatic-loss rule in section 6(1)(a) invalid from 6 October 1995, and DHA says people who lost citizenship under that rule are considered to have retained it. Voluntary renunciation, and loss before 6 October 1995, are excluded. Check your own record on the DHA portal. See {a('../citizenship/index.html','citizenship')}{src('cc','dhacit')}."),
("When should I apply?",f"VFS recommends booking at least 18 months before expiry; the Embassy suggests 12 months{src('vfsinfo','emb')}."),
("Can I renew my Smart ID card at VFS?",f"Sources disagree. VFS Global lists a Smart identity card re-issue fee. The Department of Home Affairs and the consulate notices do not list that re-issue. See {a('../smart-id/index.html','Smart ID')}.")]
s.page('faq/index.html',"FAQ: South African passports and Smart ID in the USA","Short sourced answers about South African passport renewal, Smart ID, VFS appointments, citizenship and emergency travel in the USA.",'<h1>FAQ: South African passports and ID in the USA</h1>'+''.join(f'<h2>{q}</h2><div class="card"><p>{x}</p></div>' for q,x in faq),faq=faq)
b=f'''<h1>Retaining South African citizenship when you take another citizenship</h1>
<p>For South Africans in the United States who have taken US citizenship, or another citizenship, or who are about to. This page summarises the Constitutional Court order of 6 May 2025 and the Home Affairs pages that implement it. It is not legal advice. Confirm your own record before you travel or pay.</p>
<h2>What the Court decided</h2>
<div class="card"><p>On 6 May 2025 the Constitutional Court confirmed the Supreme Court of Appeal's order in <em>Democratic Alliance v Minister of Home Affairs</em> (CCT 184/23). It declared section 6(1)(a) of the South African Citizenship Act 88 of 1995 inconsistent with the Constitution and invalid from 6 October 1995. Citizens who lost their citizenship by operation of that section are deemed not to have lost it{src("cc","saflii")}. DHA's 24 November 2025 statement says the judgment took immediate effect and that affected people are deemed never to have lost their citizenship{src("dhaannounce")}.</p>
<p>The struck-down section applied to a citizen who, whilst not a minor, by a voluntary and formal act other than marriage, acquired the citizenship or nationality of another country. The old rule removed South African citizenship unless the Minister had given permission to retain it beforehand. The Court held that this ministerial power, in section 6(2), did not save section 6(1)(a){src("saflii","cc")}. The order does not say that every other loss-of-citizenship rule in the Act was struck down.</p></div>
<h2>Who DHA says is covered</h2>
<div class="card"><ul>
<li>Anyone who lost citizenship under section 6(1)(a) is considered to have retained it. DHA tells those people to check their status on the official portal and, if needed, start reinstatement there{src("dhacit","portal")}.</li>
<li>If your second nationality was acquired after 6 October 1995 and you did not obtain ministerial permission, DHA says you are automatically covered and considered to have retained South African citizenship. DHA still says you may use the portal to confirm your status{src("dhacit")}.</li>
<li>The portal FAQ says the ruling covers both citizens by birth and people who obtained citizenship through naturalisation, if the naturalised citizenship was lost after acquiring another country's citizenship{src("portalfaq")}.</li>
<li>Children born while a parent was incorrectly recorded as having lost citizenship may have affected statuses. DHA says the system will advise if dependants need further steps. It does not list those steps{src("dhacit")}.</li>
</ul>
<p>The portal is {a(S["portal"],"myhomeaffairsonline.dha.gov.za/reinstatement-of-citizenship")}. The Embassy citizens services page links to My Home Affairs Online for citizenship reinstatement{src("emb")}.</p></div>
<h2>Who is not covered</h2>
<div class="card warn"><ul>
<li><strong>Voluntary renunciation.</strong> DHA says the ruling does not apply to people who voluntarily renounced South African citizenship, which DHA describes as a common requirement when obtaining citizenship in another country{src("dhacit")}.</li>
<li><strong>Before 6 October 1995.</strong> People who lost citizenship through conversion before 6 October 1995 are not eligible for reinstatement under this judgment{src("dhacit")}.</li>
</ul>
<p>Neither the judgment nor the DHA FAQ says whether the United States naturalization oath counts as voluntary renunciation of South African citizenship. This page does not decide that. Use the portal to check the record in your name.</p></div>
<h2>Check or confirm your status</h2>
<p>DHA's reinstatement FAQ, checked on this date, describes this process. Do it yourself. Someone may help you, but you must be the person verified by the selfie or passport upload{src("dhacit")}.</p>
<div class="card"><ol>
<li>Create a profile at {a("https://myhomeaffairsonline.dha.gov.za/","My Home Affairs Online")}. DHA emails a verification link. Log in with that email and password{src("dhacit")}.</li>
<li>Check your citizen status. You need your ID number{src("dhaannounce","dhacit")}.</li>
<li>Take a selfie in a well-lit place with a white background. If the selfie is not enough, scan a passport. A South African or foreign passport is accepted, including an expired passport. Do not cover the page with your fingers, and avoid overhead light on the page{src("dhacit")}.</li>
<li>If your citizenship is still valid, DHA confirms it and says reinstatement is not necessary{src("dhacit")}.</li>
<li>If your citizenship may have been revoked, complete the application. DHA says most details are pre-filled from its records. Submit it. You are told by email when it is finalised. Track it under My Applications, at the top right of the homepage{src("dhacit")}.</li>
</ol></div>
<div class="card"><ul>
<li><strong>From the USA:</strong> yes. The platform is global. You may use a foreign passport if you do not have a valid South African passport{src("dhacit","portalfaq")}.</li>
<li><strong>Time:</strong> allow 8 to 10 weeks for DHA to review a reinstatement application. If the record already shows you as a citizen, DHA says you are notified immediately{src("dhacit","dhaannounce")}.</li>
<li><strong>Fee:</strong> the DHA reinstatement FAQ does not state a fee. Do not assume it is free, and do not pay a figure from the older Embassy retention forms unless you are filing one of those forms.</li>
<li><strong>Documents:</strong> a selfie, a passport (South African or foreign, even if expired), and further documents only if the review asks for them{src("dhacit")}.</li>
<li><strong>Invalid ID number:</strong> DHA says this can happen if the number does not match its records, including where the ID format changed after 1986, or if it was typed wrong. The FAQ gives the contact as HACC on +27800 601 190{src("dhacit")}. The portal FAQ gives the email hacc@dha.gov.za{src("portalfaq")}.</li>
<li><strong>Passport:</strong> reinstatement does not issue a passport. You apply separately. DHA says that application is at a Home Affairs office or a South African mission abroad{src("dhacit")}. In the USA, VFS takes passport applications. See {a("../what-to-bring/index.html","what to bring")} and {a("../fees/index.html","fees")}.</li>
</ul></div>
<div class="card conf"><strong>Conflicts on the official pages (as of {D})</strong><ul>
<li><strong>Must you go to an office?</strong> The DHA FAQ says the process is fully online, and that in rare cases DHA may tell you to visit a Home Affairs office. It does not say a mission in the United States can finish that rare case{src("dhacit")}. The portal FAQ answers "Do I need to visit a Home Affairs office or a South African mission abroad?" with no, and says the entire process is completed online{src("portalfaq")}.</li>
<li><strong>Is there a certificate?</strong> The DHA FAQ says the outcome is sent electronically, and that you will be told if a certificate is added later{src("dhacit")}. The portal FAQ says you will not receive a certificate of reinstatement. The result is by email, and you can check the updated status on the portal{src("portalfaq")}.</li>
<li><strong>"Instantly" and 8 to 10 weeks.</strong> The Minister's 24 November 2025 statement describes correcting the population register from anywhere in the world, and says a person whose citizenship is still valid is notified immediately{src("dhaannounce")}. The same department's FAQ says a submitted reinstatement application takes 8 to 10 weeks because of risk checks{src("dhacit")}.</li>
</ul></div>
<h2>Passport applications still ask for a retention certificate</h2>
<div class="card note"><p>The Embassy adult passport checklist dated in the file path February 2026, after the judgment and after the portal launch, still asks for a "Copy of Retention Certificate (if applicable)"{src("embadult")}. The checklist does not say when it is applicable, and it does not say that a portal email replaces it.</p>
<p>The VFS Global consular services page, read on {D}, asks dual citizens for proof of how and when the other nationality was acquired. It gives a naturalization certificate and a retention or registration certificate as examples. It says a foreign passport or identity document is not that proof{src("vfsinfo")}. The page does not say that an email from the citizenship portal replaces a retention certificate. Open the VFS Global page yourself before you book.</p></div>
<h2>Travelling to South Africa</h2>
<div class="card"><ul>
<li>DHA says South Africans living and working abroad must have a valid South African passport to travel to South Africa. If you still hold South African citizenship, DHA says you will be penalised for entering on a foreign passport. The FAQ does not state the penalty amount{src("dhacit")}.</li>
<li>Proof that you have applied for a South African passport is not accepted for travel. In an emergency, DHA says you may apply for an Emergency Travel Certificate at your local mission. See {a("../lost-passport/index.html","lost passport and the ETC")}{src("dhacit")}.</li>
<li>A minor who has dual citizenship also needs a valid South African passport to enter South Africa. DHA's answer is "Yes"{src("dhacit")}.</li>
<li>A child who was never registered as a South African citizen may travel on a foreign passport, subject to visa requirements. To register that child, DHA says you apply for foreign birth registration at the mission or a local office{src("dhacit")}. Where that application is lodged is in conflict: the Embassy birth registration page still describes mailing it in{src("embbirth")}; the citizens services page says no mailed-in birth registration will be processed and points birth registration to VFS{src("emb")}; DHA says a citizen born abroad whose birth is not on the population register cannot be served at the VFS centres and must go to a mission{src("dha")}. This site does not yet have a full birth-registration page.</li>
</ul></div>
<div class="card conf"><strong>Same FAQ, two answers on a foreign passport.</strong> One answer says you may not travel to South Africa on a foreign passport if you have no valid South African passport. A later answer says that if the Court reinstated your citizenship without an application, and you did not intend to resume citizenship or obtain a South African passport, you may travel on your foreign passport if the other country allows dual citizenship. If you do not want South African citizenship, that answer says you may apply for renunciation{src("dhacit")}. Read both answers on the FAQ before you travel. This guide cannot tell you which one an official will apply to you.</div>
<h2>If you do not want South African citizenship</h2>
<div class="card"><p>DHA says you may apply for renunciation{src("dhacit")}. The Embassy still publishes a renunciation requirements PDF, linked from the citizens services page{src("emb","embren")}:</p>
<ul>
<li>DHA-246 renunciation form and BI-529</li>
<li>Copy of birth certificate or passport, if available</li>
<li>Original South African passport, ID book or card</li>
<li>Copy of the US naturalization certificate, or other foreign citizenship</li>
<li>Minimum processing period 6 to 8 months</li>
<li>The PDF says to mail the application to the South African Embassy, 3051 Massachusetts Avenue NW, Washington, DC 20008</li>
</ul>
<p>The PDF does not state a fee{src("embren")}. The citizens services notice that no mailed-in applications will be processed names passport, identity document and birth registration. It does not name renunciation{src("emb")}. Confirm with the Embassy before you post original documents.</p></div>
<h2>Older Embassy and consulate pages</h2>
<p>These pages are still online. They describe the pre-judgment retention and exemption process. They do not mention the 6 May 2025 order.</p>
<div class="card conf"><ul>
<li><strong>Embassy citizenship page, section 6(2).</strong> It says a citizen who intends to retain citizenship must apply before foreign citizenship is taken, and should have the exemption certificate in hand first. It lists BI-529E, BI-1664, a valid passport, proof of South African citizenship, a notarized letter that the foreign citizenship has not been taken up, proof of current status in that country, a fee of $25, and 4 to 6 weeks{src("embcit")}.</li>
<li><strong>Embassy retention PDF</strong> (file path February 2024): DHA-1664, BI-529, copy of the South African passport, copy of the US permanent residence card, a notarized affidavit that you have not yet taken up US citizenship, $25 money order payable to the SA Embassy, 30 business days, mailed to the Embassy{src("embret")}.</li>
<li><strong>Before 6 October 1995.</strong> The Embassy still publishes a section 26(4) exemption for foreign citizenship taken before that date: BI-529, proof of the foreign citizenship, copy of the South African passport, $25, and 30 business days, mailed to the Embassy. The citizenship page calls the form BI-1666. The PDF and the New York forms list call it DHA-1666{src("embcit","embex","nyciv")}. DHA says this judgment does not reinstate that group{src("dhacit")}.</li>
<li><strong>New York.</strong> The consulate's civic forms list still includes retention on DHA-1664 and a section 26(4) exemption on DHA-1666. That list gives no fee and no processing time{src("nyciv")}. The New York and Los Angeles immigration pages still list retention of citizenship, determination of citizenship, and renunciation. They do not mention the 2025 judgment or the portal{src("nyimm","laimm")}.</li>
</ul>
<p>If you already hold another citizenship, or you are about to take one, start with the DHA portal. The section that used to remove citizenship for that act is invalid from 6 October 1995{src("cc","dhacit")}. If VFS or the Embassy still asks for a retention certificate with a passport application, the February 2026 checklist shows that request is still in print{src("embadult")}.</p></div>
<h2>Sources checked</h2>
<ul>
<li>{a(S["cc"],"Constitutional Court case record, judgment and media summary, 6 May 2025")}</li>
<li>{a(S["saflii"],"Full judgment, SAFLII, [2025] ZACC 8")}</li>
<li>{a(S["dhaannounce"],"DHA statement, 24 November 2025, citizenship portal launch")}</li>
<li>{a(S["dhacit"],"DHA citizenship reinstatement FAQ")}</li>
<li>{a(S["portal"],"My Home Affairs Online, reinstatement")}</li>
<li>{a(S["portalfaq"],"My Home Affairs Online FAQ")}</li>
<li>{a(S["emb"],"SA Embassy, Washington, citizens services")} (links to the portal)</li>
<li>{a(S["embcit"],"SA Embassy citizenship page")} (section 6(2) and section 26(4) still published)</li>
<li>{a(S["embadult"],"SA Embassy adult passport checklist, February 2026")}</li>
<li>{a(S["embret"],"SA Embassy retention PDF")}, {a(S["embex"],"exemption PDF")}, {a(S["embren"],"renunciation PDF")}</li>
<li>{a(S["nyciv"],"Consulate General, New York, civic forms")}, {a(S["nyimm"],"New York immigration services")}, {a(S["laimm"],"Los Angeles immigration services")}</li>
</ul>'''
s.page('citizenship/index.html',"Keep South African citizenship after another nationality","What the May 2025 Constitutional Court ruling and Home Affairs say about South Africans in the USA who take another citizenship.",b,lastmod="2026-10-26")
b=f'''<h1>Disclaimer</h1>
<p>{esc(DISCLAIMER)}</p>
<h2>Accuracy</h2>
<p>Pages on this site summarise public information for South Africans in the United States. They can be incomplete, out of date, or wrong. A date on a page is the date that page was last checked, not a promise that the underlying rule is still current.</p>
<h2>No warranty</h2>
<p>The site is provided as is and as available. There is no warranty of accuracy, completeness, fitness for a particular purpose, or uninterrupted access.</p>
<h2>Limitation of liability</h2>
<p>To the extent the law allows, the people who publish this site accept no liability for any loss, cost, delay, or decision that results from using it or relying on it. That includes travel, fees, citizenship, identity documents, and appointments.</p>
<h2>External links are not endorsements</h2>
<p>Links to the Department of Home Affairs, DIRCO, the South African Embassy and consulates, VFS Global, the SA Chamber of Commerce in the USA, courts, and other sites are there so you can read the source. This site does not control those sites and does not endorse them. Their pages can change or disagree with each other.</p>
<h2>Not affiliated</h2>
<p>This independent site is not affiliated with any government, bank, or agency. It is not a site of the Department of Home Affairs, DIRCO, the South African Embassy or consulates, VFS Global, or any bank.</p>
<h2>Check official sources</h2>
<p>Always confirm with the official source before you act, pay, travel, book, or send documents. If a sentence here disagrees with the official page it cites, follow the official page.</p>
<h2>Contact and corrections</h2>
<p>This site has no contact form, no advice line, and no user accounts. It does not answer personal questions or check an individual case. For a correction, compare the sentence with the official page linked beside it and follow that official page.</p>'''
s.page('disclaimer/index.html',"Disclaimer for this South African passport guide in the USA","Accuracy, no warranty, liability limits, external links, affiliation and corrections for this unofficial South African passport guide.",b,lastmod="2026-10-26",crumb="Disclaimer")
find='<h1>All pages</h1><p>Type in the search box at the top of this page. The list below stays complete if search is not available.</p><p id="index-status" class="index-status" aria-live="polite">Showing every page.</p><div id="page-index">'
for g,items in GROUPS:
    find+=f'<section><h2>{esc(g)}</h2><ul class="index-list">'+''.join(
        f'<li data-keywords="{esc(ALIAS.get(p,""))}"><a class="jump" href="{href(p)}"><span class="lt">{esc(t)}</span><span class="ls">{esc(BLURB[p])}</span></a></li>'
        for p,t in items)+'</ul></section>'
find+='</div>'
s.page('find/index.html',"Full page list for this South African passport guide","Search or browse every page in this unofficial guide to South African passports and identity documents in the United States.",find)
hub="".join(f'<li><a href="{p}">{esc(t)}</a></li>' for g,items in GROUPS for p,t in items)
s.page('404.html',"Page not found: South African passport guide in the USA","That page is not on this guide. Open the VFS centres, documents, fees, Smart ID, lost passport, citizenship, tracking or FAQ pages.",f'<h1>Page not found</h1><p>That address is not a page on this guide.</p><ul>{hub}</ul>',sitemap=False,article=False,robots="noindex",crumb="Page not found")
s.finish()
facts=["100 Peachtree Street, Suite 225, 2nd Floor, Atlanta, GA 30303","$127","6 May 2025","XA7XgB_UwrIRvQyNVsnWpSyTyaU6e3-v4g4RBw8RAVI","Last checked: 26 Oct 2026","3051 Massachusetts Avenue NW","(212) 692-2401","Independent guide. Not a government website.","services.vfsglobal.com/usa/en/zap"]
blob="\n".join(open(os.path.join(s.out,p),encoding="utf-8").read() for p in s.pages)
missing=[fact for fact in facts if fact not in blob]
if missing: raise SystemExit("Missing facts after build: "+"; ".join(missing))
print(len(s.pages),'pages',len(s.indexable),'in sitemap',len(C),'centres',len(M),'missions')
