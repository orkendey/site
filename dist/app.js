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
