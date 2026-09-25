from pathlib import Path
from html import escape

# Coordinates in the supplied 816 × 1926 reference. Only artwork is reused;
# navigation, headings, course content, links and forms remain semantic HTML.
def art(x,y,w,h,label='',cls='',eager=False):
 return f'<span class="ref-art {cls}" style="--x:{x};--y:{y};--w:{w};--h:{h}"'+(f' role="img" aria-label="{escape(label)}"' if label else ' aria-hidden="true"')+f'><img src="/assets/design-reference.png" alt="" width="816" height="1926" loading="{"eager" if eager else "lazy"}" draggable="false"></span>'

def photo(name, width, height, alt='', cls='', widths=(), sizes='100vw', eager=False):
 src=f'/assets/{name}{"-"+str(width) if widths else ""}.webp'
 responsive=(f' srcset="'+', '.join(f'/assets/{name}-{w}.webp {w}w' for w in widths)+f'" sizes="{sizes}"') if widths else ''
 if name.startswith('letter-example-'):
  src=src.replace('.webp','.png')
 priority=' fetchpriority="high"' if eager else ''
 return f'<img class="site-photo {cls}" src="{src}"{responsive} width="{width}" height="{height}" alt="{escape(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}>'

def icon(name, cls=''):
 paths={
  'laptop':'<rect x="4" y="4" width="16" height="12" rx="1.5"/><path d="M2 20h20M8 16l-1 4m9-4 1 4"/>',
  'application':'<path d="M13 3H5a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-5M8 7h4M8 11h2"/><path d="m12 15 7-7 3 3-7 7-4 1zM17 10l3 3"/>',
  'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m3 6 9 7 9-7"/>',
  'play':'<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m10 8 6 4-6 4z"/>',
  'certificate':'<path d="M13 3H5a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h5M8 7h5M8 11h3"/><circle cx="17" cy="12" r="4"/><path d="m14 15-1 7 4-2 4 2-1-7"/>',
  'users':'<circle cx="12" cy="7" r="3"/><path d="M6 21v-3a6 6 0 0 1 12 0v3zM5 4a3 3 0 0 0 0 6m14-6a3 3 0 0 1 0 6M4 14a5 5 0 0 0-3 5v2h2m18 0h2v-2a5 5 0 0 0-3-5"/>',
  'globe':'<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4" ry="10"/><path d="M3 8h18M2 12h20M3 16h18"/>',
  'headset':'<path d="M3 13v-2a9 9 0 0 1 18 0v2M21 17v2a3 3 0 0 1-3 3h-3"/><rect x="2" y="11" width="4" height="8" rx="2"/><rect x="18" y="11" width="4" height="8" rx="2"/><path d="M12 22h3"/>'
 }
 return f'<svg class="ui-icon {cls}" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>'

def build_home(D,modal,courses):
 links='<a href="/courses/">Курсы</a><a href="/organizations/">Для организаций</a><a href="/about/">О центре</a><a href="/materials/">Материалы</a><a href="/contacts/">Контакты</a>'
 logo='<a class="brand" href="/">Өркендеу<span>Учебно-методический центр</span></a>'
 pics=[(60,369,228,134),(306,369,228,134),(552,369,228,134)]
 cards=''
 for c,rect in zip(courses,pics):
  duration='Часы уточняются' if c['slug']=='antiterror-education' else str(c['hours'])+' часов'
  cards+=f'<article class="home-course"><a class="home-course-photo" href="/courses/{c["slug"]}/">'+art(*rect,label=c['title'])+f'<span class="home-course-duration">{duration}</span></a><div class="home-course-copy"><h3><a href="/courses/{c["slug"]}/">{c["title"]}</a></h3><div class="home-course-meta"><span>Онлайн · РУ / ҚАЗ</span><a href="/courses/{c["slug"]}/">Подробнее <span aria-hidden="true">→</span></a></div></div></article>'
 steps=[('Выберите курс','Найдите программу<br> под свои задачи.','laptop'),('Оставьте заявку','Заполните простую<br> форму','application'),('Получите доступ','Мы отправим вам<br> данные для входа','mail'),('Пройдите обучение','Изучайте материалы<br> в удобном темпе','play'),('Получите сертификат','После успешного<br> завершения','certificate')]
 journey=''.join(f'<li><span class="step-visual"><span class="step-number" aria-hidden="true">{i}</span><span class="step-circle">{icon(symbol)}</span></span><h3>{t}</h3><p>{d}</p></li>' for i,(t,d,symbol) in enumerate(steps,1))
 letters=''
 for i,(w,h) in enumerate([(308,357),(306,354),(304,354)],1):
  letters+=f'<button class="home-letter" data-document="Благодарственное письмо — образец {i}" data-document-image="/assets/letter-example-{i}.png">'+photo(f'letter-example-{i}',w,h,alt=f'Образец благодарственного письма {i}',cls='letter-image')+'<span>Благодарственное письмо <span aria-hidden="true">⌕</span></span></button>'
 materials=''
 for i,(title,tag,rect) in enumerate([('Методические рекомендации','СТАТЬИ',(60,1589,228,99)),('Материалы для воспитателей','ДЛЯ ВОСПИТАТЕЛЕЙ',(306,1589,228,99)),('Практика безопасной школы','БЕЗОПАСНОСТЬ',(552,1589,228,99))],1):
  materials+=f'<a class="home-material" href="/materials/article-{i}/"><span class="home-material-picture">'+art(*rect,label=title)+f'<span class="sr-only">{tag}</span></span><span class="material-title">{title}<span aria-hidden="true">→</span></span></a>'
 content=f'''<div class="site-frame"><div class="ornament-rail" aria-hidden="true"></div><a class="skip" href="#main">Перейти к содержанию</a>
<header class="home-header"><div class="home-header-inner">{logo}<nav aria-label="Основное меню">{links}</nav><span class="languages" aria-label="Обучение на русском и казахском языках"><b>РУ</b> / ҚАЗ</span><a class="login" href="https://lms.orkendey.kz/" target="_blank" rel="noopener">Войти в LMS</a><button class="menu" aria-label="Открыть меню" aria-expanded="false">☰</button></div></header>
<main id="main">
<section class="home-hero"><div class="hero-copy"><p class="eyebrow">ОБУЧЕНИЕ, КОТОРОЕ ПОМОГАЕТ В РАБОТЕ</p><h1>Учитесь новому.<br>Растите в профессии.</h1><p class="hero-description">Повышение квалификации для специалистов и команд в образовании, здравоохранении и частном секторе.</p><div class="hero-actions"><a class="btn gold" href="/courses/">Выбрать курс</a><a class="btn outline" href="/organizations/">Обучить коллектив</a></div><div class="hero-features"><span>{icon('laptop')}Онлайн-обучение</span><span>{icon('globe')}Русский и қазақша</span></div></div>{photo('hero-classroom',1536,1024,'Педагоги на обучении: на ноутбуке открыта платформа Өркендеу','hero-art',(768,1024,1536),'(max-width:620px) 100vw, 55vw',True)}</section>
<section class="home-courses content"><div class="section-heading"><h2>Актуальные курсы</h2><a href="/courses/">Смотреть все курсы <span aria-hidden="true">⟶</span></a></div><div class="home-course-grid">{cards}</div></section>
<section class="organization-band"><div class="band-background mountain-art">{photo('mountains-sharp',2172,724)}</div><div class="organization-content">{icon('users','organization-icon')}<div><h2>Обучение для вашей организации</h2><p>Подберём программы для вашего коллектива</p></div><button class="btn gold" data-apply="Обучение коллектива">Получить предложение</button></div></section>
<section class="home-process"><div class="content"><h2>Как проходит обучение</h2><ol class="journey">{journey}</ol></div><a class="learning-art" href="https://lms.orkendey.kz/" target="_blank" rel="noopener" aria-label="Перейти на платформу обучения">{photo('learning-platform',2048,727,'Личный кабинет Өркендеу: видеолекция, список уроков и учебные материалы',widths=(768,1280,2048),sizes='96vw')}</a></section>
<section class="home-documents"><div><h2>Документы, которым доверяют</h2><p>Сертификат с возможностью<br>проверки подлинности</p><a class="btn outline" href="/certificate/">Проверить сертификат</a></div><div class="certificate-composition"><button class="certificate-preview certificate-preview-1" data-document="Инклюзивное образование · 80 часов" data-document-format="landscape" data-document-image="/assets/certificate-inclusion-2400.webp" data-document-pdf="/documents/certificate-inclusion.pdf" data-document-note="Сертификат учебно-методического центра «Өркендеу»." aria-label="Увеличить сертификат: Инклюзивное образование · 80 часов"><img src="/assets/certificate-inclusion-960.webp" srcset="/assets/certificate-inclusion-960.webp 960w, /assets/certificate-inclusion-2400.webp 2400w" sizes="(max-width:620px) 45vw, 28vw" width="2400" height="1699" loading="lazy" alt="Инклюзивное образование · 80 часов"></button><button class="certificate-preview certificate-preview-2" data-document="Профилактика буллинга · 72 часа" data-document-format="landscape" data-document-image="/assets/certificate-bullying-2400.webp" data-document-pdf="/documents/certificate-bullying.pdf" data-document-note="Сертификат учебно-методического центра «Өркендеу»." aria-label="Увеличить сертификат: Профилактика буллинга · 72 часа"><img src="/assets/certificate-bullying-960.webp" srcset="/assets/certificate-bullying-960.webp 960w, /assets/certificate-bullying-2400.webp 2400w" sizes="(max-width:620px) 45vw, 28vw" width="2400" height="1699" loading="lazy" alt="Профилактика буллинга · 72 часа"></button></div></section>
<section class="home-letters"><div class="letters-decoration">{photo('letters-background',2048,724,widths=(1024,2048),sizes='100vw')}</div><div class="content"><div class="section-heading"><h2>Нам доверяют организации и специалисты</h2><a href="/letters/">Все письма <span aria-hidden="true">⟶</span></a></div><p class="letters-subtitle">Благодарственные письма наших клиентов</p><div class="home-letters-grid">{letters}</div></div></section>
<section class="home-materials content"><div class="section-heading"><h2>Полезные материалы</h2><a href="/materials/">Все материалы <span aria-hidden="true">⟶</span></a></div><div class="home-material-grid">{materials}</div></section>
<section class="home-consult"><div class="consult-decoration">{photo('mountains-sharp',2172,724)}</div><div class="consult-content">{icon('headset','consult-icon')}<div><h2>Поможем выбрать программу</h2><p>Оставьте заявку — мы проконсультируем вас<br> и подберём подходящие курсы</p></div><form id="quick-application" aria-label="Заявка на консультацию"><label class="sr-only" for="quick-name">Ваше имя</label><input id="quick-name" name="name" required autocomplete="given-name" placeholder="Ваше имя"><label class="sr-only" for="quick-phone">Телефон</label><input id="quick-phone" name="phone" required type="tel" autocomplete="tel" pattern="[0-9+\\s\\x28\\x29\\x2D]{{10,20}}" placeholder="Телефон"><button class="btn gold" type="submit">Получить консультацию</button></form></div></section>
</main><footer class="home-footer">{art(680,1844,135,81,cls='footer-art')}<div class="footer-inner">{logo}<nav aria-label="Меню в подвале">{links}</nav><div class="footer-contact">Алматы · Астана<br><a href="mailto:edu@orkendey.kz">edu@orkendey.kz</a></div></div><p class="demo-caption">Демоверсия · Документы — образцы · Заявки не отправляются</p></footer></div>'''
 html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Өркендеу — профессиональное обучение и повышение квалификации</title><meta name="description" content="Повышение квалификации специалистов и обучение команд в образовании, здравоохранении и частном секторе по всему Казахстану."><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230e3148'/%3E%3Ctext x='32' y='46' text-anchor='middle' font-size='46' fill='%23c2a05c'%3EӨ%3C/text%3E%3C/svg%3E"><link rel="preload" as="image" href="/assets/hero-classroom-1536.webp" imagesrcset="/assets/hero-classroom-768.webp 768w, /assets/hero-classroom-1024.webp 1024w, /assets/hero-classroom-1536.webp 1536w" imagesizes="(max-width:620px) 100vw, 55vw"><link rel="stylesheet" href="/home.css"><script defer src="/app.js"></script></head><body class="reference-home">{content}{modal}</body></html>'''
 (D/'index.html').write_text(html)
