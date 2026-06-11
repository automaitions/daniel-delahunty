// nav solid on scroll
const nav=document.getElementById('nav');
const navAlwaysSolid=nav.dataset.solid==='always';
const onScroll=()=>nav.classList.toggle('solid',navAlwaysSolid||window.scrollY>40);
onScroll();addEventListener('scroll',onScroll,{passive:true});
// drawer
const burger=document.getElementById('burger'),drawer=document.getElementById('drawer');
const toggle=o=>{drawer.classList.toggle('open',o);document.body.classList.toggle('nav-open',o);burger.setAttribute('aria-expanded',o)};
burger.addEventListener('click',()=>toggle(!drawer.classList.contains('open')));
drawer.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>toggle(false)));
addEventListener('keydown',e=>{if(e.key==='Escape')toggle(false)});
// reveal
const io=new IntersectionObserver((es)=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// faq
document.querySelectorAll('.acc__q').forEach(q=>{q.addEventListener('click',()=>{
  const open=q.getAttribute('aria-expanded')==='true';
  document.querySelectorAll('.acc__q').forEach(o=>{o.setAttribute('aria-expanded','false');o.nextElementSibling.style.maxHeight=null});
  if(!open){q.setAttribute('aria-expanded','true');const a=q.nextElementSibling;a.style.maxHeight=a.scrollHeight+'px'}
})});
// lead form → mailto
const leadForm=document.getElementById('leadForm');
if(leadForm){leadForm.addEventListener('submit',e=>{
  e.preventDefault();const f=e.target;
  const body=`Name: ${f.first.value} ${f.last.value}%0D%0AEmail: ${f.email.value}%0D%0APhone: ${f.phone.value}%0D%0AGoal: ${f.goal.value}`;
  window.location.href=`mailto:pt@danieldelahunty.com?subject=Free consult request — ${encodeURIComponent(f.first.value)}&body=${body}`;
});}
// expandable drawer submenus (Coaching, Shop)
document.querySelectorAll('.drawer__item[aria-controls]').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const open=btn.getAttribute('aria-expanded')==='true';
    btn.setAttribute('aria-expanded',!open);
    const sub=document.getElementById(btn.getAttribute('aria-controls'));
    sub.style.maxHeight=open?null:sub.scrollHeight+'px';
  });
});
// macro calculator
const g=id=>document.getElementById(id);
function calcMacros(){
  if(!g('m_age'))return;
  const age=+g('m_age').value,sex=g('m_sex').value,ht=+g('m_ht').value,wt=+g('m_wt').value,act=+g('m_act').value,goal=+g('m_goal').value;
  if(!age||!ht||!wt){return}
  const bmr=10*wt+6.25*ht-5*age+(sex==='m'?5:-161);
  const cals=Math.max(1200,Math.round(bmr*act*(1+goal)/10)*10);
  const pro=Math.round(wt*2.0), fat=Math.round(cals*0.25/9), carb=Math.max(0,Math.round((cals-pro*4-fat*9)/4));
  g('m_cals').textContent=cals.toLocaleString();
  g('m_pro').textContent=pro+'g'; g('m_carb').textContent=carb+'g'; g('m_fat').textContent=fat+'g';
}
['m_age','m_sex','m_ht','m_wt','m_act','m_goal'].forEach(id=>{const el=g(id);if(el){el.addEventListener('input',calcMacros);el.addEventListener('change',calcMacros)}});
calcMacros();

// sticky mobile consult CTA on every page except contact
if(!/contact\.html$/.test(location.pathname)){
  const bar=document.createElement('a');
  bar.href='contact.html'; bar.className='cta-bar'; bar.textContent='Book a free consult →';
  document.body.appendChild(bar);
}

// ---- review marquee: auto-drift + arrows + user takeover ----
document.querySelectorAll('.rmq').forEach(rmq=>{
  const track=rmq.querySelector('.rmq__track'); if(!track)return;
  const shell=document.createElement('div'); shell.className='rmq-shell';
  rmq.parentNode.insertBefore(shell,rmq); shell.appendChild(rmq);
  rmq.classList.add('rmq--js');
  const half=()=>track.scrollWidth/2;
  let auto=!matchMedia('(prefers-reduced-motion:reduce)').matches, idle;
  const pause=ms=>{auto=false;clearTimeout(idle);idle=setTimeout(()=>auto=true,ms||4000)};
  (function tick(){
    if(auto)rmq.scrollLeft+=.6;
    if(rmq.scrollLeft>=half())rmq.scrollLeft-=half();
    requestAnimationFrame(tick);
  })();
  ['pointerdown','wheel','touchstart'].forEach(ev=>rmq.addEventListener(ev,()=>pause(),{passive:true}));
  const arrow=dir=>{
    const b=document.createElement('button');
    b.className='rmq__arrow rmq__arrow--'+(dir>0?'next':'prev');
    b.setAttribute('aria-label',dir>0?'Next reviews':'Previous reviews');
    b.innerHTML=dir>0
      ?'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
      :'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';
    b.addEventListener('click',()=>{
      pause(6000);
      const card=track.querySelector('.quote');
      const step=(card?card.offsetWidth:330)+20;
      if(dir<0&&rmq.scrollLeft<step)rmq.scrollLeft+=half();
      rmq.scrollBy({left:dir*step,behavior:'smooth'});
    });
    return b;
  };
  shell.appendChild(arrow(-1)); shell.appendChild(arrow(1));
});

// ---- ebook cart (client-side, localStorage) ----
(function(){
  const KEY='dd_cart';
  const read=()=>{try{return JSON.parse(localStorage.getItem(KEY))||[]}catch(e){return[]}};
  const write=c=>{localStorage.setItem(KEY,JSON.stringify(c));render()};
  const navEl=document.querySelector('.nav'); if(!navEl)return;
  const cta=navEl.querySelector('.nav__cta');
  const btn=document.createElement('button');
  btn.className='cart-btn'; btn.setAttribute('aria-label','Cart');
  btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 7h12l1 13H5zM9 7a3 3 0 016 0"/></svg><span class="cart-badge" id="cartBadge"></span>';
  navEl.insertBefore(btn, cta||null);
  const ov=document.createElement('div'); ov.className='cart-ov';
  const panel=document.createElement('div'); panel.className='cart-panel';
  panel.innerHTML='<div class="cart-head"><h3>Your cart</h3><button class="cart-x" aria-label="Close">&times;</button></div><div class="cart-items" id="cartItems"></div><div class="cart-foot" id="cartFoot"></div>';
  document.body.appendChild(ov); document.body.appendChild(panel);
  const open=o=>{panel.classList.toggle('open',o);ov.classList.toggle('open',o)};
  btn.addEventListener('click',()=>open(true));
  ov.addEventListener('click',()=>open(false));
  panel.querySelector('.cart-x').addEventListener('click',()=>open(false));
  document.querySelectorAll('.add-cart').forEach(b=>b.addEventListener('click',()=>{
    const t=b.dataset.title,p=parseFloat(b.dataset.price);
    const c=read();const ex=c.find(i=>i.t===t);if(ex)ex.q++;else c.push({t,p,q:1});
    write(c);open(true);const o=b.textContent;b.textContent='Added ✓';setTimeout(()=>b.textContent=o,1200);
  }));
  document.querySelectorAll('.add-bundle').forEach(b=>b.addEventListener('click',()=>{
    const c=read();
    document.querySelectorAll('.add-cart').forEach(a=>{const t=a.dataset.title,p=parseFloat(a.dataset.price);const ex=c.find(i=>i.t===t);if(ex)ex.q++;else c.push({t,p,q:1});});
    write(c);open(true);const o=b.textContent;b.textContent='Added ✓';setTimeout(()=>b.textContent=o,1200);
  }));
  // single source of truth for cart maths: 2 singles = 10% off singles, 3+ = 20%; bundle excluded
  const isBundle=i=>/bundle/i.test(i.t);
  function pricing(c){
    const singles=c.filter(i=>!isBundle(i));
    const nSingles=singles.reduce((s,i)=>s+i.q,0);
    const rate=nSingles>=3?.2:nSingles>=2?.1:0;
    const singlesSub=singles.reduce((s,i)=>s+i.p*i.q,0);
    const sub=c.reduce((s,i)=>s+i.p*i.q,0);
    const disc=singlesSub*rate;
    return {nSingles,rate,sub,disc,total:sub-disc,hasBundle:c.some(isBundle)};
  }
  function nudgeFor(pr){
    if(pr.hasBundle)return 'Best value unlocked — the full 7-guide library is in your cart.';
    if(pr.nSingles===1)return 'Add one more guide and save 10% on both — applied automatically.';
    if(pr.nSingles===2)return 'Add a third guide and save 20% on all of them.';
    if(pr.nSingles>=3){
      const gap=129-pr.total;
      if(gap<=0)return 'The full 7-guide bundle is $129 — cheaper than your cart right now. Switch and get everything.';
      return `You're at $${(pr.total/pr.nSingles).toFixed(2)} a guide. The full library (all 7) is $129 — just $${gap.toFixed(2)} more for everything.`;
    }
    return '';
  }
  function render(){
    const c=read();const badge=document.getElementById('cartBadge');
    const n=c.reduce((s,i)=>s+i.q,0);
    if(badge){badge.textContent=n;badge.classList.toggle('show',n>0);}
    const items=document.getElementById('cartItems'),foot=document.getElementById('cartFoot');if(!items)return;
    if(!c.length){items.innerHTML='<div class="cart-empty">Your cart is empty.<br><br><a href="ebooks.html" class="btn btn--ghost">Browse ebooks</a></div>';foot.innerHTML='';return;}
    items.innerHTML=c.map((i,ix)=>`<div class="cart-row"><div class="cart-row__t">${i.t}<span class="cart-rm" data-rm="${ix}">remove</span></div><div class="cart-qty"><button data-dec="${ix}">−</button><span>${i.q}</span><button data-inc="${ix}">+</button></div><div class="cart-row__p">$${(i.p*i.q).toFixed(2)}</div></div>`).join('');
    const pr=pricing(c);
    const nudge=nudgeFor(pr);
    foot.innerHTML=
      (nudge?`<div class="cart-nudge">${nudge}</div>`:'')+
      (pr.disc>0?`<div class="cart-sub"><span>Subtotal</span><span>$${pr.sub.toFixed(2)}</span></div><div class="cart-disc"><span>Multi-guide discount (${Math.round(pr.rate*100)}%)</span><span>−$${pr.disc.toFixed(2)}</span></div>`:'')+
      `<div class="cart-total"><span>Total</span><span>$${pr.total.toFixed(2)} AUD</span></div><button class="btn btn--primary" id="cartCo">Checkout</button><p class="cart-note">Secure card checkout coming soon — for now your order goes straight to Daniel to complete &amp; send your downloads.</p>`;
    items.querySelectorAll('[data-inc]').forEach(b=>b.onclick=()=>{const c=read();c[+b.dataset.inc].q++;write(c)});
    items.querySelectorAll('[data-dec]').forEach(b=>b.onclick=()=>{const c=read();if(--c[+b.dataset.dec].q<=0)c.splice(+b.dataset.dec,1);write(c)});
    items.querySelectorAll('[data-rm]').forEach(b=>b.onclick=()=>{const c=read();c.splice(+b.dataset.rm,1);write(c)});
    document.getElementById('cartCo').onclick=()=>{
      const c=read();const pr=pricing(c);
      let lines=c.map(i=>`${i.q} x ${i.t} - $${(i.p*i.q).toFixed(2)}`).join('%0D%0A');
      if(pr.disc>0)lines+=`%0D%0ASubtotal: $${pr.sub.toFixed(2)}%0D%0AMulti-guide discount (${Math.round(pr.rate*100)}%25): -$${pr.disc.toFixed(2)}`;
      location.href=`mailto:pt@danieldelahunty.com?subject=Ebook order - $${pr.total.toFixed(2)} AUD&body=I'd like to order:%0D%0A${lines}%0D%0A%0D%0ATotal: $${pr.total.toFixed(2)} AUD%0D%0A%0D%0AName:%0D%0A(Daniel will reply with payment + download links)`;
    };
  }
  render();
})();

// ---- macro calculator: email-gated results (Suby HVCO lead gen) ----
(function(){
  const unlock=document.getElementById('m_unlock'); if(!unlock)return;
  const gate=document.getElementById('macroGate'), res=document.getElementById('macroResults'), email=document.getElementById('m_email');
  const reveal=()=>{gate.style.display='none';res.style.display='block';};
  if(localStorage.getItem('dd_macro_unlocked'))reveal();
  unlock.addEventListener('click',()=>{
    const em=(email.value||'').trim();
    if(!/.+@.+\..+/.test(em)){email.style.borderColor='var(--accent)';email.focus();return;}
    localStorage.setItem('dd_macro_unlocked','1'); reveal();
    const cals=document.getElementById('m_cals').textContent,pro=document.getElementById('m_pro').textContent,
          carb=document.getElementById('m_carb').textContent,fat=document.getElementById('m_fat').textContent;
    location.href=`mailto:pt@danieldelahunty.com?subject=Macro lead + free starter guide&body=New lead from the macro calculator.%0D%0AEmail: ${encodeURIComponent(em)}%0D%0A%0D%0ATheir macros:%0D%0ACalories: ${cals}%0D%0AProtein: ${pro}%0D%0ACarbs: ${carb}%0D%0AFat: ${fat}%0D%0A%0D%0APlease send the free starter guide.`;
  });
})();

// ---- homepage quiz (scorecard) ----
(function(){
  const quiz=document.getElementById('ddquiz'); if(!quiz)return;
  const steps=[...quiz.querySelectorAll('.quiz__step')], fill=document.getElementById('qfill');
  const ans={}; let i=0;
  const R={
    rise:{n:'Rise Above — 8 Weeks',c:"An 8-week reset is your fastest honest start — custom training, your foods, and weekly check-ins to lock in the habits.",a:[['Book a free consult','contact.html','btn--primary'],['See Rise Above','rise-above.html','btn--ghost']]},
    lean:{n:'Lean For Life',c:"You've got momentum — ongoing coaching keeps it off for good, with a weekly check-in so you never rebound.",a:[['Book a free consult','contact.html','btn--primary'],['See Lean For Life','lean-for-life.html','btn--ghost']]},
    guide:{n:'Start With A Guide',c:"Not ready to invest in coaching yet? Start with a guide ($25.99) or the full bundle ($129) and build the basics.",a:[['Browse the guides','ebooks.html','btn--primary'],['Book a free consult','contact.html','btn--ghost']]}
  };
  function show(n){steps.forEach((s,ix)=>s.classList.toggle('on',ix===n));fill.style.width=((n+1)/(steps.length+1)*100)+'%';}
  function pick(){
    if(ans.barrier==='budget')return 'guide';
    if(ans.now==='stuck'||ans.now==='advanced'||ans.barrier==='accountability')return 'lean';
    return 'rise';
  }
  quiz.querySelectorAll('.quiz__opt').forEach(b=>b.addEventListener('click',()=>{
    ans[b.dataset.k]=b.dataset.v;
    if(i<steps.length-1){i++;show(i);}
    else{
      const r=R[pick()];
      document.getElementById('qrname').textContent=r.n;
      document.getElementById('qrcopy').textContent=r.c;
      document.getElementById('qractions').innerHTML=r.a.map(x=>`<a href="${x[1]}" class="btn ${x[2]}">${x[0]}</a>`).join('');
      steps.forEach(s=>s.classList.remove('on'));
      document.getElementById('qresult').classList.add('on');
      fill.style.width='100%';
    }
  }));
  document.getElementById('qretake').addEventListener('click',()=>{for(const k in ans)delete ans[k];i=0;document.getElementById('qresult').classList.remove('on');show(0);});
  const qsend=document.getElementById('qsend');
  if(qsend)qsend.addEventListener('click',()=>{const em=(document.getElementById('qemail')||{}).value||'';const plan=document.getElementById('qrname').textContent;location.href=`mailto:pt@danieldelahunty.com?subject=My starting point: ${encodeURIComponent(plan)}&body=Email: ${encodeURIComponent(em)}%0D%0AMy quiz match: ${encodeURIComponent(plan)}%0D%0A%0D%0APlease send my plan + free starter guide.`;});
})();
