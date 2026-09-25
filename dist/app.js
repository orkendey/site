const $=s=>document.querySelector(s);const $$=s=>document.querySelectorAll(s);
$('.menu').addEventListener('click',()=>{const n=$('header nav'),open=n.classList.toggle('open');$('.menu').setAttribute('aria-expanded',String(open));$('.menu').setAttribute('aria-label',open?'Закрыть меню':'Открыть меню')});
$$('[data-apply]').forEach(b=>b.addEventListener('click',()=>{$('#application').reset();$('#form-result').textContent='';$('#apply-context').textContent=b.dataset.apply;$('#apply-dialog').showModal()}));
$$('dialog .close').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
$$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}}));
$('#application').addEventListener('submit',e=>{e.preventDefault();$('#form-result').textContent='Форма заполнена корректно. Это демоверсия: заявка не отправлена. Для связи с центром: edu@orkendey.kz.'});
$$('[data-document]').forEach(b=>b.addEventListener('click',()=>{
 $('#document-title').textContent=b.dataset.document;
 $('#document-dialog').classList.toggle('wide-document',b.dataset.documentFormat==='landscape');
 $('#document-note').textContent=b.dataset.documentNote||'Демонстрационный образец. Здесь можно разместить ваш оригинал.';
 if(b.dataset.documentImage){
  const image=document.createElement('img');
  image.src=b.dataset.documentImage;image.alt=b.dataset.document;
  image.className='document-image'+(b.dataset.documentFormat==='landscape'?' landscape':'');
  $('#document-content').replaceChildren(image);
  if(b.dataset.documentPdf){
   const link=document.createElement('a');
   link.href=b.dataset.documentPdf;link.target='_blank';link.rel='noopener';
   link.className='document-pdf';link.textContent='Открыть сертификат в PDF ↗';
   $('#document-content').append(link);
  }
 }else if(b.dataset.artView){
  const [x,y,w,h]=b.dataset.artView.split(',').map(Number);
  const frame=document.createElement('div');frame.className='ref-art document-art'+(w<h?' portrait':'');
  frame.style.cssText=`--x:${x};--y:${y};--w:${w};--h:${h};aspect-ratio:${w}/${h};position:relative;overflow:hidden;max-width:680px;margin:auto`;
  const image=document.createElement('img');image.src='/assets/design-reference.png';image.alt=b.dataset.document;
  image.style.cssText=`display:block;position:absolute;max-width:none;width:${816/w*100}%;height:auto;left:${-x/w*100}%;top:${-y/h*100}%`;
  frame.append(image);$('#document-content').replaceChildren(frame);
 }else{
  const node=(b.classList.contains('certificate')?b:b.querySelector('.letter')).cloneNode(true);
  node.removeAttribute('data-document');node.removeAttribute('aria-label');
  if(node.tagName==='BUTTON'){const div=document.createElement('div');div.className=node.className;div.innerHTML=node.innerHTML;$('#document-content').replaceChildren(div)}else $('#document-content').replaceChildren(node);
 }
 $('#document-dialog').showModal();
}));
$('#quick-application')?.addEventListener('submit',e=>{
 e.preventDefault();$('#application').reset();
 $('#application [name="name"]').value=$('#quick-name').value;
 $('#application [name="phone"]').value=$('#quick-phone').value;
 $('#apply-context').textContent='Консультация по программе обучения';
 $('#form-result').textContent='Форма заполнена. В демоверсии заявки не отправляются. Для связи с центром: edu@orkendey.kz.';
 $('#apply-dialog').showModal();
});
let currentFilter='all';function filter(){let count=0;const term=($('#course-search')?.value||'').trim().toLowerCase();$$('#catalog .course').forEach(c=>{const visible=(currentFilter==='all'||c.querySelector('.eyebrow').textContent===currentFilter)&&c.textContent.toLowerCase().includes(term);c.hidden=!visible;if(visible)count++});if($('#no-results'))$('#no-results').hidden=count>0}
$('#course-search')?.addEventListener('input',filter);$$('[data-filter]').forEach(b=>b.addEventListener('click',()=>{currentFilter=b.dataset.filter;$$('[data-filter]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b))});filter()}));

// Imported LMS catalog: language, sector, duration and text filters work together.
if ($('#catalog-search')) {
 let sector = 'all';
 const search = $('#catalog-search'), language = $('#catalog-language'), hours = $('#catalog-hours');
 const cards = [...$$('.catalog-card')];
 function applyCatalogFilters() {
  const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let total = 0;
  for (const card of cards) {
   const durationMatches = hours.value === 'all' || (hours.value === 'review' ? !card.dataset.hours && card.dataset.sector !== 'documents' : card.dataset.hours === hours.value);
   const visible = (sector === 'all' || card.dataset.sector === sector) && (language.value === 'all' || card.dataset.language === language.value) && durationMatches && terms.every(term => card.dataset.search.toLocaleLowerCase().includes(term));
   card.hidden = !visible;
   if (visible) total++;
  }
  $('#catalog-count').textContent = `Найдено: ${total}`;
  $('#catalog-empty').hidden = total > 0;
 }
 search.addEventListener('input', applyCatalogFilters);
 language.addEventListener('change', applyCatalogFilters);
 hours.addEventListener('change', applyCatalogFilters);
 $$('[data-sector-filter]').forEach(button => button.addEventListener('click', () => {
  sector = button.dataset.sectorFilter;
  $$('[data-sector-filter]').forEach(item => { const active = item === button; item.classList.toggle('active', active); item.setAttribute('aria-pressed', String(active)); });
  applyCatalogFilters();
 }));
 $('#catalog-reset').addEventListener('click', () => {
  search.value = ''; language.value = 'all'; hours.value = 'all'; sector = 'all';
  $$('[data-sector-filter]').forEach(item => { const active = item.dataset.sectorFilter === 'all'; item.classList.toggle('active', active); item.setAttribute('aria-pressed', String(active)); });
  applyCatalogFilters();
 });
}

// The public catalog is read from Supabase. If it is temporarily unavailable,
// the bundled catalog remains visible so visitors can still choose a course.
(async () => {
 const config = window.ORKENDEY_SUPABASE || {
  restUrl: 'https://nzllxcwfelieokqqoqqm.supabase.co/rest/v1',
  publishableKey: 'sb_publishable_hu9060B6OWyXPAKRXlLPmQ_iSH7FmNW'
 };
 if (!config?.restUrl || !config?.publishableKey) return;
 try {
  const response = await fetch(`${config.restUrl}/website_courses?select=slug,title,description,language,sector,hours,duration_review,cover_url,lms_url&order=title.asc`, {
   headers: { apikey: config.publishableKey }
  });
  if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
  const courses = await response.json();
  if (!Array.isArray(courses) || !courses.length) return;
  const bySlug = new Map(courses.map(course => [course.slug, course]));
  const languageName = language => language === 'kk' ? 'Қазақша' : 'Русский';
  const sectorName = sector => ({education:'Образование', healthcare:'Здравоохранение', business:'Бизнес и организации', documents:'Комплекты документов'})[sector] || 'Обучение';
  const duration = course => course.sector === 'documents' ? 'Комплект документов' : course.hours ? `${course.hours} часов` : 'Часы уточняются';
  const excerpt = text => (text || 'Содержание и условия обучения уточнит специалист центра.').replace(/\s+/g, ' ').trim();

  $$('.catalog-card').forEach(card => {
   const slug = card.querySelector('a[href*="/courses/"]')?.getAttribute('href')?.split('/').filter(Boolean).pop();
   const course = bySlug.get(slug);
   if (!course) return;
   card.dataset.sector = course.sector;
   card.dataset.language = course.language;
   card.dataset.hours = course.hours || '';
   card.dataset.search = `${course.title} ${sectorName(course.sector)} ${excerpt(course.description)}`;
   const image = card.querySelector('img');
   if (image && course.cover_url) { image.src = course.cover_url; image.srcset = ''; image.alt = course.title; }
   const meta = card.querySelectorAll('.catalog-meta span');
   if (meta[0]) meta[0].textContent = languageName(course.language);
   if (meta[1]) meta[1].textContent = duration(course);
   const title = card.querySelector('h2 a');
   if (title) { title.textContent = course.title; title.closest('h2').lang = course.language; }
   const cardLink = card.querySelector('.catalog-cover');
   if (cardLink) cardLink.setAttribute('aria-label', course.title);
   const description = card.querySelector('.catalog-excerpt');
   if (description) { description.textContent = excerpt(course.description); description.lang = course.language; }
  });

  const path = location.pathname.split('/').filter(Boolean);
  const slug = path[0] === 'courses' && path[1] ? path[1] : null;
  const course = bySlug.get(slug);
  if (!course) return;
  const title = document.querySelector('.course-intro h1');
  if (title) { title.textContent = course.title; title.lang = course.language; }
  const eyebrow = document.querySelector('.course-intro .eyebrow');
  if (eyebrow) eyebrow.textContent = `${sectorName(course.sector)} · ${languageName(course.language)}`;
  const tags = document.querySelectorAll('.course-intro-tags span');
  if (tags[0]) tags[0].textContent = languageName(course.language);
  if (tags[1]) tags[1].textContent = duration(course);
  const cover = document.querySelector('.course-intro-cover img');
  if (cover && course.cover_url) { cover.src = course.cover_url; cover.srcset = ''; cover.alt = course.title; }
  const facts = document.querySelector('.course-facts dl');
  if (facts) facts.innerHTML = `<div><dt>${course.sector === 'documents' ? 'Тип материала' : 'Продолжительность'}</dt><dd>${duration(course)}</dd></div><div><dt>Язык</dt><dd>${languageName(course.language)}</dd></div><div><dt>Стоимость</dt><dd>Уточните у специалиста</dd></div>`;
  const reading = document.querySelector('.course-description');
  if (reading && course.description) {
   const heading = reading.querySelector('h2');
   const eyebrow = reading.querySelector('.eyebrow');
   reading.querySelectorAll('p:not(.eyebrow)').forEach(p => p.remove());
   const paragraphs = course.description.replace(/\r\n/g, '\n').split(/\n\s*\n/).filter(Boolean);
   paragraphs.forEach(text => { const p=document.createElement('p'); p.lang=course.language; p.textContent=text.trim(); reading.append(p); });
   if (heading) heading.textContent = course.sector === 'documents' ? 'О комплекте документов' : 'Содержание обучения';
   if (eyebrow) eyebrow.textContent = course.sector === 'documents' ? 'МАТЕРИАЛЫ ДЛЯ РАБОТЫ' : 'О ПРОГРАММЕ';
  }
 } catch (error) {
  console.warn('Supabase catalog is unavailable; showing bundled catalog.', error);
 }
})();
