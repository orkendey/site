from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).parent
SOURCE = json.loads((ROOT / 'data/lms-catalog.json').read_text())
SLUGS = [
 'school-inclusion-kk','preschool-conflicts-kk','preschool-conflict-prevention',
 'school-inclusion','preschool-licensing-documents-kk','preschool-licensing-documents',
 'industrial-safety-healthcare','inclusive-preschool-kk','inclusive-preschool',
 'occupational-safety-kk','bullying-prevention-kk','early-pregnancy-prevention-kk',
 'antiterror-education-kk','fire-safety-kk','antiterror-healthcare-kk','anticorruption-kk',
 'bullying-8-kk','sanitary-minimum-kk','digital-literacy-kk','conciliation-committee-kk',
 'gambling-prevention-kk','state-symbols-kk','inclusion-24-kk','preschool-conflicts',
 'early-pregnancy-prevention','digital-literacy','conciliation-committee','inclusion-24',
 'occupational-safety','antiterror-healthcare','bullying-prevention','fire-safety',
 'bullying-8','state-symbols','gambling-prevention','anticorruption','sanitary-minimum',
 'antiterror-education'
]
SECTORS = {'education':'Образование','healthcare':'Здравоохранение',
           'business':'Бизнес и организации','documents':'Комплекты документов'}
BUSINESS = {9,13,15,18,19,21,25,26,28,31,33,35}
HEALTHCARE = {6,14,29,36}
DOCUMENTS = {4,5}
# Source discrepancies stay in the raw snapshot; no guessed duration is published.
REVIEW = {
 'preschool-conflicts-kk':'В казахской карточке — 120 часов; в русской — 8 часов.',
 'inclusion-24':'В названии — 24 часа, в поле продолжительности LMS — 8 часов.',
 'antiterror-education':'В утверждённом макете — 80 часов, в текущей LMS — 8 часов.'
}
SHORT_TITLES = {
 'school-inclusion-kk':'Заманауи мектептегі инклюзия',
 'school-inclusion':'Инклюзия в современной школе',
 'inclusive-preschool':'Инклюзивная образовательная среда в ДОУ',
 'inclusive-preschool-kk':'Мектепке дейінгі ұйымдардағы инклюзивті білім беру',
 'antiterror-healthcare-kk':'Денсаулық сақтау объектілерін терроризмге қарсы қорғау',
 'antiterror-education-kk':'Білім беру объектілерін антитеррористік қорғау',
}

def catalog_courses():
    result=[]
    assert len(SOURCE['courses']) == len(SLUGS)
    for i,(row,slug) in enumerate(zip(SOURCE['courses'],SLUGS)):
        item=dict(row)
        item['slug']=slug
        item['id']=row['href'].rsplit('/',1)[1]
        item['title']=' '.join(row['title'].split())
        item['short_title']=SHORT_TITLES.get(slug,item['title'])
        item['sector']='documents' if i in DOCUMENTS else 'healthcare' if i in HEALTHCARE else 'business' if i in BUSINESS else 'education'
        match=re.search(r'(\d+) часов',row['meta'])
        item['hours']=int(match.group(1)) if match and slug not in REVIEW else None
        item['language_label']='Қазақша' if row['language']=='kk' else 'Русский'
        result.append(item)
    return result

def duration(c):
    if c['sector']=='documents':return 'Комплект документов'
    return f'{c["hours"]} часов' if c['hours'] else 'Часы уточняются'

def cover(c,cls='',eager=False):
    ident=c['id']
    path=ROOT/'dist/assets/courses'/f'{ident}-960.webp'
    if not path.exists():
        return '<div class="course-cover-empty">Өркендеу</div>'
    return f'<img class="{cls}" src="/assets/courses/{ident}-960.webp" srcset="/assets/courses/{ident}-480.webp 480w, /assets/courses/{ident}-960.webp 960w" sizes="(max-width:640px) 92vw, (max-width:1000px) 46vw, 30vw" alt="{escape(c["short_title"])}" width="960" height="600" loading="{"eager" if eager else "lazy"}">'

def clean_text(text):
    return '\n'.join(line.rstrip() for line in text.replace('**','').splitlines()).strip()

def description_html(text,lang):
    if not text:
        return '<p>Содержание и условия обучения уточнит специалист центра.</p>'
    paras=re.split(r'\n\s*\n',clean_text(text))
    return ''.join('<p lang="'+lang+'">'+escape(p.strip()).replace('\n','<br>')+'</p>' for p in paras if p.strip())

def build_catalog(D,page,btn):
    courses=catalog_courses()
    def write(slug,title,body,description):
        dest=D/slug/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
        html=page(escape(title),body)
        html=re.sub(r'<meta name="description" content="[^"]*">',lambda m:'<meta name="description" content="'+escape(' '.join(description.split()))+'">',html,count=1)
        html=html.replace('</head>','<link rel="stylesheet" href="/catalog.css"></head>')
        dest.write_text(html)
    cards=[]
    for c in courses:
        text=escape(clean_text(c['description']))
        cards.append(f'''<article class="catalog-card" data-sector="{c['sector']}" data-language="{c['language']}" data-hours="{c['hours'] or ''}" data-search="{escape(c['title']+' '+SECTORS[c['sector']]+' '+clean_text(c['description']))}">
<a class="catalog-cover" href="/courses/{c['slug']}/" aria-label="{escape(c['title'])}">{cover(c)}</a>
<div class="catalog-card-body"><div class="catalog-meta"><span>{c['language_label']}</span><span>{duration(c)}</span></div>
<h2 lang="{c['language']}"><a href="/courses/{c['slug']}/">{escape(c['short_title'])}</a></h2>
<p class="catalog-excerpt" lang="{c['language']}">{text}</p>
<a class="catalog-more" href="/courses/{c['slug']}/">Подробнее <span aria-hidden="true">→</span></a></div></article>''')
    filters=''.join(f'<button type="button" data-sector-filter="{key}" aria-pressed="false">{label}</button>' for key,label in SECTORS.items())
    body=f'''<div class="catalog-page"><section class="catalog-intro container"><a class="breadcrumb" href="/">Главная /</a><p class="eyebrow">ПРОФЕССИОНАЛЬНОЕ РАЗВИТИЕ</p><h1>Каталог курсов</h1><p class="catalog-lead">Выберите программу для себя или команды. Обучение на русском и казахском языках.</p></section>
<section class="catalog-content container" aria-label="Каталог программ"><div class="catalog-controls"><label class="catalog-search">Поиск курса<input id="catalog-search" type="search" placeholder="Например, инклюзия или охрана труда" autocomplete="off"></label><label>Язык обучения<select id="catalog-language"><option value="all">Все языки</option><option value="ru">Русский</option><option value="kk">Қазақша</option></select></label><label>Продолжительность<select id="catalog-hours"><option value="all">Любая</option><option value="8">8 часов</option><option value="24">24 часа</option><option value="72">72 часа</option><option value="80">80 часов</option><option value="review">Уточняется</option></select></label></div>
<div class="catalog-sectors" role="group" aria-label="Направление обучения"><button type="button" class="active" data-sector-filter="all" aria-pressed="true">Все направления</button>{filters}</div>
<div class="catalog-results"><p id="catalog-count" role="status" aria-live="polite">Найдено: {len(courses)}</p><button id="catalog-reset" type="button">Сбросить фильтры</button></div>
<div class="catalog-grid">{''.join(cards)}</div><div id="catalog-empty" hidden><h2>Подходящих программ не найдено</h2><p>Попробуйте другое название или измените фильтры.</p></div>
<div class="catalog-help"><div><h2>Поможем подобрать обучение</h2><p>Расскажите о своей задаче — подберём программу для вас или вашей команды.</p></div>{btn('Получить консультацию','Подбор программы')}</div></section></div>'''
    write('courses','Каталог курсов',body,'Курсы Өркендеу для образования, здравоохранения и организаций. Каталог программ на русском и казахском языках, описание и условия обучения.')
    for c in courses:
        is_docs=c['sector']=='documents'
        desc=clean_text(c['description'])
        if c['hours']: hours=f'{c["hours"]} часов'
        else:hours='Уточняется при обращении'
        facts=(f'<div><dt>Продолжительность</dt><dd>{hours}</dd></div>' if not is_docs else '<div><dt>Тип материала</dt><dd>Комплект документов</dd></div>')
        body=f'''<article class="course-page"><section class="course-intro container"><a class="breadcrumb" href="/courses/">← Каталог курсов</a><div class="course-intro-grid"><div><p class="eyebrow">{SECTORS[c['sector']]} · {c['language_label']}</p><h1 lang="{c['language']}">{escape(c['title'])}</h1><div class="course-intro-tags"><span>{c['language_label']}</span><span>{duration(c)}</span></div><div class="actions">{btn('Уточнить условия',c['title'])}<a class="text-link" href="https://lms.orkendey.kz{c['href']}" target="_blank" rel="noopener">Открыть в LMS ↗</a></div></div><div class="course-intro-cover">{cover(c,eager=True)}</div></div></section>
<section class="course-reading container"><div class="course-description"><p class="eyebrow">{'МАТЕРИАЛЫ ДЛЯ РАБОТЫ' if is_docs else 'О ПРОГРАММЕ'}</p><h2>{'О комплекте документов' if is_docs else 'Содержание обучения'}</h2>{description_html(c['description'],c['language'])}</div><aside class="course-facts"><h2>Информация</h2><dl>{facts}<div><dt>Язык</dt><dd>{c['language_label']}</dd></div><div><dt>Стоимость</dt><dd>Уточните у специалиста</dd></div></dl>{btn('Узнать стоимость',c['title'])}<p class="course-facts-note">Поможем с выбором и расскажем о порядке {'получения материалов' if is_docs else 'записи на обучение'}.</p></aside></section>
<section class="course-bottom container"><a class="text-link" href="/courses/">← Посмотреть другие программы</a></section></article>'''
        write('courses/'+c['slug'],c['short_title'],body,desc[:260] or c['title'])
    return courses
