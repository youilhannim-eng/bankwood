/* fx: 스크롤 등장 · 숫자 카운트 · 히어로 캔버스 · 안내 도우미 (외부 라이브러리 없음) */
(function(){
  "use strict";
  var me=document.currentScript, theme=(me&&me.dataset.theme)||"ginkgo";
  var tel=(me&&me.dataset.tel)||"", brand=(me&&me.dataset.brand)||document.title;
  var root=document.documentElement, calm=matchMedia("(prefers-reduced-motion:reduce)").matches;
  var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  /* 1. 헤더 그림자 (스크롤 위치 표시) */
  var tick=false;
  function onScroll(){ if(tick) return; tick=true; requestAnimationFrame(function(){ root.classList.toggle("fx-scrolled",(scrollY||0)>24); tick=false; }); }
  addEventListener("scroll",onScroll,{passive:true}); onScroll();

  /* 2. 움직임은 두 곳만: 입소 절차 경로, 상황별 안내 짚기. 화면에 들어오면 한 번 재생.
        내용은 처음부터 다 보이고, 움직임은 그 위에 얹는 강조일 뿐이다. */
  if(!calm && "IntersectionObserver" in window){
    var once=new IntersectionObserver(function(en){ en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add("go"); once.unobserve(x.target); } }); },{threshold:.35});
    $$(".route, .route-steps, .pick").forEach(function(e){ once.observe(e); });
  }

  /* 5. 히어로 캔버스: 은행잎 / 금빛 연결선 / 은은한 빛망울 */
  var hero=document.querySelector(".hero");
  if(hero && !calm && hero.offsetHeight>0){
    var cv=document.createElement("canvas"); cv.className="fx-canvas"; cv.setAttribute("aria-hidden","true"); hero.insertBefore(cv,hero.firstChild);
    var cx=cv.getContext("2d"), W=0,H=0,dpr=Math.min(2,devicePixelRatio||1), P=[], run=false, raf=0;
    var small=innerWidth<=600;
    function size(){W=hero.clientWidth;H=hero.clientHeight;cv.width=W*dpr;cv.height=H*dpr;cx.setTransform(dpr,0,0,dpr,0,0)}
    function rnd(a,b){return a+Math.random()*(b-a)}
    function seed(){
      P=[]; var n= theme==="gold" ? (small?26:58) : theme==="pearl" ? (small?7:12) : (small?5:9);
      for(var i=0;i<n;i++){
        if(theme==="gold") P.push({x:rnd(0,W),y:rnd(0,H),vx:rnd(-.18,.18),vy:rnd(-.18,.18),r:rnd(1,2.2)});
        else if(theme==="pearl") P.push({x:rnd(0,W),y:rnd(0,H),vx:rnd(-.1,.1),vy:rnd(-.08,.08),r:rnd(38,110),a:rnd(.05,.12)});
        else P.push({x:rnd(0,W),y:rnd(-H,H),vy:rnd(.25,.7),sw:rnd(.4,1.2),ph:rnd(0,6.28),r:rnd(7,15),rot:rnd(0,6.28),vr:rnd(-.012,.012),a:rnd(.35,.8)});
      }
    }
    function leaf(p){ /* 부채꼴 은행잎 */
      cx.save(); cx.translate(p.x,p.y); cx.rotate(p.rot); cx.globalAlpha=p.a; var r=p.r;
      cx.beginPath(); cx.moveTo(0,r*1.1); cx.bezierCurveTo(-r*1.5,r*.2,-r*1.2,-r,-r*.12,-r*.62); cx.lineTo(0,-r*.3); cx.lineTo(r*.12,-r*.62); cx.bezierCurveTo(r*1.2,-r,r*1.5,r*.2,0,r*1.1); cx.closePath();
      cx.fillStyle="#F5B800"; cx.fill(); cx.strokeStyle="rgba(138,106,0,.5)"; cx.lineWidth=1; cx.stroke();
      cx.beginPath(); cx.moveTo(0,r*1.1); cx.lineTo(0,r*1.9); cx.stroke(); cx.restore();
    }
    function draw(t){
      cx.clearRect(0,0,W,H);
      if(theme==="gold"){
        var lim=small?92:138;
        for(var i=0;i<P.length;i++){var p=P[i]; p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>W)p.vx*=-1; if(p.y<0||p.y>H)p.vy*=-1;
          for(var j=i+1;j<P.length;j++){var q=P[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.sqrt(dx*dx+dy*dy);
            if(d<lim){cx.strokeStyle="rgba(201,162,39,"+(.34*(1-d/lim))+")";cx.lineWidth=1;cx.beginPath();cx.moveTo(p.x,p.y);cx.lineTo(q.x,q.y);cx.stroke()}}
          cx.fillStyle="rgba(232,212,138,.85)";cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);cx.fill();}
      }else if(theme==="pearl"){
        P.forEach(function(p){p.x+=p.vx;p.y+=p.vy; if(p.x<-p.r)p.x=W+p.r; if(p.x>W+p.r)p.x=-p.r; if(p.y<-p.r)p.y=H+p.r; if(p.y>H+p.r)p.y=-p.r;
          var g=cx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r); g.addColorStop(0,"rgba(150,160,180,"+p.a+")"); g.addColorStop(1,"rgba(150,160,180,0)");
          cx.fillStyle=g;cx.beginPath();cx.arc(p.x,p.y,p.r,0,6.28);cx.fill();});
      }else{
        P.forEach(function(p){p.y+=p.vy; p.x+=Math.sin(t/1000*p.sw+p.ph)*.5; p.rot+=p.vr; if(p.y>H+24){p.y=-24;p.x=rnd(0,W)} leaf(p)});
      }
      if(run) raf=requestAnimationFrame(draw);
    }
    function start(){if(!run){run=true;raf=requestAnimationFrame(draw)}}
    function stop(){run=false;cancelAnimationFrame(raf)}
    size(); seed();
    var rt; addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(function(){var w=W;size();if(Math.abs(w-W)>40)seed()},180)});
    if("IntersectionObserver" in window) new IntersectionObserver(function(e){e[0].isIntersecting&&!document.hidden?start():stop()}).observe(hero); else start();
    document.addEventListener("visibilitychange",function(){document.hidden?stop():(hero.getBoundingClientRect().bottom>0&&start())});
  }

  /* 6. 안내 도우미: 이 사이트의 '자주 묻는 질문'에서 답을 찾아 보여 줌 (외부로 아무것도 보내지 않음) */
  function faqFrom(doc){
    return $$(".faq details, #faq details",doc).map(function(d){
      var s=d.querySelector("summary"), a=d.cloneNode(true); var ss=a.querySelector("summary"); if(ss) ss.remove();
      return s?{q:s.textContent.trim(),a:a.textContent.trim().replace(/\s+/g," ")}:null;
    }).filter(function(x){return x&&x.a});
  }
  function grams(s){s=s.toLowerCase().replace(/[^0-9a-z가-힣]/g,"");var o={};for(var i=0;i<s.length-1;i++)o[s.substr(i,2)]=1;return o}
  function best(text,faq){
    var g=grams(text),top=null,sc=0;
    faq.forEach(function(f){var q=grams(f.q),a=grams(f.a),n=0;for(var k in g){if(q[k])n+=2;else if(a[k])n+=1} n=n/Math.max(3,Object.keys(g).length); if(n>sc){sc=n;top=f}});
    return sc>=.5?top:null;
  }
  function ask(faq){
    if(faq.length<2) return;
    var btn=document.createElement("button"); btn.className="fx-ask"; btn.type="button"; btn.setAttribute("aria-expanded","false"); btn.innerHTML="<i></i>궁금한 점 물어보기";
    var pn=document.createElement("div"); pn.className="fx-panel"; pn.setAttribute("role","dialog"); pn.setAttribute("aria-label","안내 도우미");
    pn.innerHTML='<header><div><b>안내 도우미</b><small>자주 묻는 질문에서 답을 찾아 드립니다</small></div><button type="button" aria-label="닫기">×</button></header><div class="fx-log" aria-live="polite"></div><form class="fx-form"><input type="text" placeholder="예: 비용은 얼마인가요?" aria-label="질문 입력" maxlength="80"><button type="submit">보내기</button></form>';
    document.body.appendChild(btn); document.body.appendChild(pn);
    var log=pn.querySelector(".fx-log"), inp=pn.querySelector("input");
    function say(cls,html){var m=document.createElement("div");m.className="fx-msg "+cls;m.innerHTML=html;log.appendChild(m);log.scrollTop=log.scrollHeight;return m}
    function esc(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
    function chips(list){var w=document.createElement("div");w.className="fx-chips";list.forEach(function(f){var b=document.createElement("button");b.type="button";b.textContent=f.q;b.onclick=function(){reply(f.q,f)};w.appendChild(b)});log.appendChild(w);log.scrollTop=log.scrollHeight}
    function contact(){return tel?'<a href="tel:'+tel+'">'+tel+'</a>로 전화 주시면 바로 안내해 드립니다.':'자세한 내용은 홈페이지 안내를 확인해 주세요.'}
    function reply(text,hit){
      say("q",esc(text)); hit=hit||best(text,faq);
      setTimeout(function(){
        if(hit) say("a",esc(hit.a)+"<small>출처: "+esc(brand)+" 자주 묻는 질문</small>");
        else { say("a","이 질문은 준비된 답변에 없습니다. "+contact()); chips(faq.slice(0,4)); }
      },382);
    }
    var opened=false;
    function toggle(on){pn.classList.toggle("on",on);btn.setAttribute("aria-expanded",on);
      if(on&&!opened){opened=true;say("a","안녕하세요. "+esc(brand)+" 안내 도우미입니다. 아래 질문을 누르거나 직접 입력해 보세요.");chips(faq.slice(0,5))}
      if(on&&innerWidth>600) inp.focus();}
    btn.onclick=function(){toggle(!pn.classList.contains("on"))};
    pn.querySelector("header button").onclick=function(){toggle(false);btn.focus()};
    document.addEventListener("keydown",function(e){if(e.key==="Escape"&&pn.classList.contains("on"))toggle(false)});
    pn.querySelector("form").onsubmit=function(e){e.preventDefault();var v=inp.value.trim();if(v){reply(v);inp.value=""}};
  }
  function initAsk(){
    var f=faqFrom(document);
    if(f.length>=2) return ask(f);
    if(location.pathname!=="/"&&window.fetch&&window.DOMParser)
      fetch("/").then(function(r){return r.text()}).then(function(h){ask(faqFrom(new DOMParser().parseFromString(h,"text/html")))}).catch(function(){});
  }
  if("requestIdleCallback" in window) requestIdleCallback(initAsk,{timeout:2000}); else setTimeout(initAsk,600);
})();
