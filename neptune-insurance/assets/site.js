(() => {
  'use strict';
  const $ = (q, root=document) => root.querySelector(q);
  const $$ = (q, root=document) => [...root.querySelectorAll(q)];
  const el = (tag, text, cls) => {const n=document.createElement(tag); if(text!==undefined) n.textContent=text; if(cls) n.className=cls; return n;};
  const toastEl = $('.toast');
  let toastTimer;
  const toast = text => { if(!toastEl) return; toastEl.textContent=text; toastEl.classList.add('show'); clearTimeout(toastTimer); toastTimer=setTimeout(()=>toastEl.classList.remove('show'),3500);};
  const nav = $('.mobile-nav'); const toggle = $('.menu-toggle');
  if(toggle) toggle.addEventListener('click',()=>{ const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu'); });
  $$('[data-toast]').forEach(b=>b.addEventListener('click',()=>toast(b.dataset.toast)));
  const storeKey='neptune_insurance_demo_claims_v1';
  function getClaims(){try {const v=JSON.parse(localStorage.getItem(storeKey)||'[]');return Array.isArray(v)?v.slice(0,30):[];}catch(_){return [];}}
  function setClaims(v){try{localStorage.setItem(storeKey,JSON.stringify(v.slice(0,30)));return true;}catch(_){toast('Browser storage is unavailable. The demo reference will not persist.');return false;}}
  function claimApp(){
    const form=$('#claim-form');if(!form)return;
    let step=1;let savedRef='';
    const fields=['#claim-type','#claim-date','#claim-cause','#claim-policy','#claim-region'];
    const today=new Date();const dateField=$('#claim-date');dateField.max=today.toISOString().slice(0,10);dateField.value=today.toISOString().slice(0,10);
    const info=()=>({type:$('#claim-type').value,date:$('#claim-date').value,cause:$('#claim-cause').value,policy:$('#claim-policy').value,region:$('#claim-region').value,followup:$('input[name="followup"]:checked')?.value||''});
    function go(n){step=n;$$('.claim-step').forEach(s=>s.classList.toggle('active',Number(s.dataset.step)===step));$$('.step-node').forEach(s=>{const k=Number(s.dataset.step);s.classList.toggle('active',k===step);s.classList.toggle('done',k<step);});if(n===3)summary();$('#claim-app').scrollIntoView({behavior:'smooth',block:'start'});}
    function required(ids){for(const id of ids){const f=$(id);if(!f.value){toast('Please complete the highlighted demo field.');f.focus();return false;}if(f.validity && !f.validity.valid){toast('Please choose a valid date.');f.focus();return false;}}return true;}
    function summary(){const data=info();const labels=[['Claim type',data.type],['Sample incident',data.cause],['Sample date',data.date],['Policy example',data.policy],['Example area',data.region],['Follow-up',data.followup]];const target=$('#claim-summary');target.replaceChildren(...labels.map(([k,v])=>{const div=el('div',undefined,'review-row');div.append(el('span',k),el('strong',v));return div;}));}
    $('#claim-next-1').addEventListener('click',()=>{if(required(fields.slice(0,3)))go(2);});
    $('#claim-next-2').addEventListener('click',()=>{if(required(fields.slice(3)))go(3);});
    $('#claim-back-2').addEventListener('click',()=>go(1));$('#claim-back-3').addEventListener('click',()=>go(2));
    form.addEventListener('submit',event=>{event.preventDefault();if(!$('#claim-ack').checked){toast('Confirm that you understand this is a demonstration.');$('#claim-ack').focus();return;}
      const random=globalThis.crypto?.getRandomValues?crypto.getRandomValues(new Uint32Array(1))[0].toString(36).slice(0,6).toUpperCase():Math.random().toString(36).slice(2,8).toUpperCase();
      savedRef='NEP-DEMO-'+random;
      const entry={...info(),ref:savedRef,status:'Received · Demo',created:new Date().toISOString()};setClaims([entry,...getClaims()]);
      form.hidden=true;$('#claim-complete').hidden=false;$('#claim-reference').textContent=savedRef;$$('.step-node').forEach(x=>x.classList.add('done'));toast('Demo claim reference created locally.');
    });
    $('#copy-reference').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(savedRef);toast('Demo reference copied.');}catch(_){toast('Select and copy the reference shown above.');}});
    $('#claim-start-over').addEventListener('click',()=>{form.reset();dateField.value=new Date().toISOString().slice(0,10);$('#claim-ack').checked=false;form.hidden=false;$('#claim-complete').hidden=true;go(1);});
  }
  function estimator(){const estimate=$('#estimate-form');if(!estimate)return;
    const type=$('#estimate-type'),level=$('#estimate-level'),deduct=$('#estimate-deductible');
    const calc=()=>{const base={auto:85,home:125,renters:18}[type.value]||85;const lvl=Number(level.value);const mult={1:.72,2:1,3:1.38}[lvl]||1;const deductibleDelta={250:19,500:0,1000:-14}[Number(deduct.value)]||0;const value=Math.max(12,Math.round(base*mult+deductibleDelta));$('#estimate-value').textContent='$'+value;$('#estimate-label').textContent=['','Essential','Plus','Premier'][lvl]+' · Made-up monthly scenario';};[type,level,deduct].forEach(x=>x.addEventListener('input',calc));$('#estimate-reset').addEventListener('click',()=>{type.value='auto';level.value='2';deduct.value='500';calc();});calc();
  }
  function portalApp(){const rows=$('#portal-claim-rows');if(!rows)return;for(const c of getClaims()){const tr=el('tr');const ref=el('td',String(c.ref||''));const type=el('td',String(c.type||''));const status=el('td');status.append(el('span','Received · Demo','status-pill mint'));const action=el('td');const btn=el('button','View timeline','link-button');btn.dataset.ref=c.ref;action.append(btn);tr.append(ref,type,status,action);rows.prepend(tr);}
    const panel=$('#detail-panel'),content=$('#detail-content');
    function showDetail(title,lines){content.replaceChildren(el('span','DEMO DETAIL VIEW','eyebrow'),el('h3',title),el('p','Fictional demonstration information. No production policy or claim services are connected.'));const timeline=el('div',undefined,'timeline');for(const [a,b] of lines){const item=el('div',undefined,'timeline-item'),dot=el('span',undefined,'timeline-dot'),text=el('div');text.append(el('strong',a),el('span',b));item.append(dot,text);timeline.append(item);}content.append(timeline);panel.hidden=false;panel.scrollIntoView({behavior:'smooth',block:'center'});panel.focus({preventScroll:true});}
    $$( '[data-show-policy]').forEach(b=>b.addEventListener('click',()=>showDetail(b.dataset.showPolicy==='auto'?'Auto policy preview':'Home policy preview',[['Fictional policy','This example policy is displayed for UI training only.'],['Policy service','Real changes would require authentication and approved business APIs.'],['Next step','Use the support center to explore service journeys.']])));
    rows.addEventListener('click',e=>{const btn=e.target.closest('[data-ref]');if(!btn)return;showDetail('Claim '+btn.dataset.ref,[['Received','Example first notice of loss record.'],['Review','A claims specialist review is simulated; no real worker is assigned.'],['Status updates','Future Amazon Connect integration could support authenticated follow-up.']]);});
    $('#detail-close').addEventListener('click',()=>{panel.hidden=true;});
  }
  function supportApp(){const search=$('#faq-search');if(search){search.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();let count=0;$$('[data-faq]').forEach(item=>{const visible=item.textContent.toLowerCase().includes(q);item.hidden=!visible;if(visible)count++;});$('#faq-empty').hidden=count>0;});}
    const modal=$('#chat-shell');const open=$('#open-chat');if(!modal||!open)return;let opener;
    function close(){modal.hidden=true;document.body.style.overflow='';opener?.focus();}
    open.addEventListener('click',()=>{opener=document.activeElement;modal.hidden=false;document.body.style.overflow='hidden';$('#chat-close').focus();});
    $('#chat-close').addEventListener('click',close);modal.addEventListener('click',e=>{if(e.target===modal)close();});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!modal.hidden)close();});
    const answers={claims:['Filing a claim','Use the demo claims wizard to practice an FNOL journey. It creates a local reference only.','claims.html'],billing:['Billing question','Our target architecture routes billing intent to a billing specialist after appropriate verification.','portal.html'],policy:['Policy services','Explore fictional policy data in My Neptune. No real policies can be changed.','portal.html'],agent:['Talk to an agent','The live Amazon Connect number and agent routing are not yet enabled. This is a scripted preview only.','support.html#contact']};
    $('#chat-messages').addEventListener('click',e=>{const btn=e.target.closest('[data-chat-topic]');if(!btn)return;const [prompt,reply,href]=answers[btn.dataset.chatTopic];const messages=$('#chat-messages');messages.append(el('div',prompt,'msg user'),el('div',reply,'msg bot'));const link=el('a','Continue exploring →','text-action');link.href=href;messages.append(link);messages.scrollTop=messages.scrollHeight;});
  }
  claimApp();estimator();portalApp();supportApp();
})();
