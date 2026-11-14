#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bankwood.co.kr 정적 사이트 생성기 (표준 라이브러리만 사용)
 python3 tools/build.py  → guide/, insight/, sitemap.xml, rss.xml, llms.txt, llms-full.txt, index.html 의 최신 인사이트 블록 갱신
"""
import os, sys, json, glob, re, html
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from guides import PAGES
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
def W(path,txt):
    p=os.path.join(ROOT,path); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,"w",encoding="utf-8").write(txt)
def esc(s): return html.escape(s,quote=True)
def strip(h): return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",h))).strip()
def gtitle(slug): return next(t for s,t,_ in GUIDES if s==slug)
def gsub(slug): return next(d for s,_,d in GUIDES if s==slug)

SIDECTA=f'''<div class="sidecta"><small>사전 입소상담 접수 중</small><h3>상담실장 박민경</h3><a class="tel" href="tel:{TEL1}">{TEL1}</a><p>2027년 1월 준공 예정 · 정원 49명<br>등급 신청이 처음이어도 괜찮습니다.</p></div>'''

def crumbs(items):
    out=[]; 
    for i,(n,u) in enumerate(items):
        out.append(f'<a href="{u}">{n}</a>' if i<len(items)-1 else f'<b>{n}</b>')
    return '<nav class="crumbs wrap" aria-label="현재 위치">'+'<span>›</span>'.join(out)+'</nav>'
def bc_ld(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}
def faq_ld(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
def art_ld(title,desc,path,date,mod):
    return {"@type":"Article","headline":title,"description":desc,"datePublished":date,"dateModified":mod,"inLanguage":"ko-KR",
     "author":{"@type":"Organization","name":"은행나무요양원","url":SITE+"/"},
     "publisher":{"@type":"Organization","name":"은행나무요양원","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/assets/og-image.png"}},
     "mainEntityOfPage":SITE+path,"image":SITE+"/assets/og-image.png"}
def faq_html(faqs):
    return '<h2 id="faq">자주 묻는 질문</h2><div class="faq" style="padding:0">'+"".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faqs)+'</div>'
def toc(secs,has_faq=True):
    li="".join(f'<li><a href="#{i}">{t}</a></li>' for i,t,_ in secs)+('<li><a href="#faq">자주 묻는 질문</a></li>' if has_faq else "")
    return f'<div class="toc"><b>이 글의 차례</b><ol>{li}</ol></div>'
def related_html(items,title="함께 보면 좋은 글"):
    return f'<section class="related"><div class="wrap"><h2>{title}</h2><div class="rel-grid">'+"".join(f'<a href="{u}"><b>{esc(t)}</b><span>{esc(d)}</span></a>' for t,d,u in items)+'</div></div></section>'

def page(headhtml,body):
    return headhtml+header()+'\n<main id="main">\n'+body+'\n</main>\n'+footer()+'\n</body>\n</html>\n'

# ── 안내 페이지
def render_guide(slug,p):
    path=f"/guide/{slug}/"; bc=[("홈","/"),("이용 가이드","/guide/"),(p["h1"].split(",")[0][:30],path)]
    bc[-1]=(gtitle(slug),path)
    srcs=""
    if p.get("srcs"):
        srcs='<div class="srcs"><b>출처</b><ul>'+"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in p["srcs"])+'</ul>'+(f'<p>{esc(p["note"])}</p>' if p.get("note") else "")+'</div>'
    elif p.get("note"): srcs=f'<div class="srcs"><p>{esc(p["note"])}</p></div>'
    secs="".join(f'<h2 id="{i}">{t}</h2>{b}' for i,t,b in p["secs"])
    ld=[art_ld(p["h1"],p["desc"],path,"2026-11-13",TODAY),bc_ld(bc),faq_ld(p["faqs"])]
    h=head(p["title"],esc(p["desc"]),path,extra_ld=ld,kw=p["kw"])
    rel=[(gtitle(s),gsub(s),f"/guide/{s}/") for s in p["rel"]]
    body=f'''{crumbs(bc)}
<section class="page-hero" style="padding-top:0"><div class="wrap"><h1>{esc(p["h1"])}</h1><p class="lead">{esc(p["lead"])}</p><p class="meta">은행나무요양원 · 최종 확인 {TODAY}</p></div></section>
<div class="page-body"><div class="wrap page-grid"><article class="prose">{secs}{faq_html(p["faqs"])}{srcs}</article><aside class="side">{toc(p["secs"])}{SIDECTA}</aside></div></div>
{related_html(rel)}'''
    W(f"guide{path[6:]}index.html",page(h,body))

def render_hub():
    path="/guide/"; bc=[("홈","/"),("이용 가이드",path)]
    cards="".join(f'<a class="guide-card" href="/guide/{s}/"><b>{t}</b><span>{d}</span><em>자세히 보기 →</em></a>' for s,t,d in GUIDES)
    ld=[{"@type":"CollectionPage","name":"요양원 이용 가이드","url":SITE+path,"inLanguage":"ko-KR"},bc_ld(bc)]
    h=head("요양원 이용 가이드 | 비용·등급 신청·입소 절차·고르는 법 - 은행나무요양원","요양원 비용과 본인부담금, 장기요양등급 신청, 입소 절차와 준비물, 요양원 고르는 법, 요양원·요양병원 차이를 쉽게 정리한 이용 가이드.",path,extra_ld=ld,kw="요양원 가이드, 요양원 비용, 장기요양등급 신청, 요양원 입소 절차, 서울근교 요양원")
    body=f'''{crumbs(bc)}
<section class="page-hero" style="padding-top:0"><div class="wrap"><h1>요양원 이용 가이드</h1><p class="lead">처음 요양원을 알아보는 가족을 위해 비용, 등급 신청, 입소 준비, 고르는 법을 순서대로 정리했습니다.</p></div></section>
<div class="page-body"><div class="wrap"><div class="grid-guides">{cards}</div>
<p style="margin-top:2.618rem"><a class="btn p" href="/#calculator">본인부담금 계산해 보기</a> <a class="btn s" href="/insight/">인사이트 글 보기</a></p></div></div>'''
    W("guide/index.html",page(h,body))

# ── 인사이트
ALLOWED=set("h2 h3 p ul ol li strong em a br table thead tbody tr th td blockquote".split())
def load_posts():
    posts=[]
    for f in sorted(glob.glob(os.path.join(ROOT,"content/insight/*.json"))):
        d=json.load(open(f,encoding="utf-8")); d["_file"]=f; posts.append(d)
    posts.sort(key=lambda d:(d["date"],d["slug"]),reverse=True)
    return posts
def validate(posts):
    errs=[]; slugs=set(); titles=set()
    for d in posts:
        n=os.path.basename(d["_file"])
        for k in ("slug","title","description","date","category","summary","body","faq"):
            if k not in d: errs.append(f"{n}: '{k}' 없음")
        if errs and errs[-1].startswith(n): continue
        if not re.fullmatch(r"[a-z0-9-]+",d["slug"]): errs.append(f"{n}: slug는 영문 소문자·숫자·하이픈만")
        if d["slug"] in slugs: errs.append(f"{n}: slug 중복")
        if d["title"] in titles: errs.append(f"{n}: 제목 중복")
        slugs.add(d["slug"]); titles.add(d["title"])
        if len(re.sub(r"\s","",strip(d["body"])))<1500: errs.append(f"{n}: 본문 1,500자(공백 제외) 미만")
        if len(d["summary"])!=3: errs.append(f"{n}: summary는 3줄")
        if not 3<=len(d["faq"])<=5: errs.append(f"{n}: FAQ 3~5개")
        tags=set(re.findall(r"</?([a-z0-9]+)",d["body"]))
        if tags-ALLOWED: errs.append(f"{n}: 허용되지 않은 태그 {tags-ALLOWED}")
        if not (60<=len(d["description"])<=160): errs.append(f"{n}: description 60~160자 ({len(d['description'])})")
    return errs
def wrap_tables(b): return re.sub(r"(<table.*?</table>)",r'<div class="tbl">\1</div>',b,flags=re.S)

def render_post(d,posts):
    path=f"/insight/{d['slug']}/"; bc=[("홈","/"),("인사이트","/insight/"),(d["title"],path)]
    summ="".join(f"<li>{esc(x)}</li>" for x in d["summary"])
    srcs=""
    if d.get("sources"):
        srcs='<div class="srcs"><b>출처</b><ul>'+"".join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>' for s in d["sources"])+'</ul></div>'
    heads=re.findall(r'<h2[^>]*>(.*?)</h2>',d["body"])
    body_h=d["body"]; secs=[]
    for i,t in enumerate(heads,1):
        body_h=body_h.replace(f"<h2>{t}</h2>",f'<h2 id="s{i}">{t}</h2>',1); secs.append((f"s{i}",strip(t),""))
    others=[p for p in posts if p["slug"]!=d["slug"]][:3]
    rel=[(o["title"],o["description"],f"/insight/{o['slug']}/") for o in others]
    rel+= [(gtitle(s),gsub(s),f"/guide/{s}/") for s in ("cost","grade","choose")][:max(0,3-len(rel))]
    faqs=[(f["q"],f["a"]) for f in d["faq"]]
    ld=[art_ld(d["title"],d["description"],path,d["date"],d.get("modified",d["date"])),bc_ld(bc),faq_ld(faqs)]
    h=head(f'{d["title"]} - 은행나무요양원 인사이트',esc(d["description"]),path,extra_ld=ld,kw=", ".join(d.get("keywords",[d["category"]])))
    cta=f'<div class="callout"><p>요양원 입소와 등급 신청이 궁금하시면 편하게 문의하세요. 상담실장 박민경 <a href="tel:{TEL1}" style="white-space:nowrap">{TEL1}</a> · 은행나무요양원은 2027년 1월 준공 예정이며 사전 입소상담을 받고 있습니다.</p></div>'
    body=f'''{crumbs(bc)}
<section class="page-hero" style="padding-top:0"><div class="wrap"><span class="eyebrow">{esc(d["category"])}</span><h1>{esc(d["title"])}</h1><p class="meta">{d["date"]} · 은행나무요양원 인사이트</p></div></section>
<div class="page-body"><div class="wrap page-grid"><article class="prose"><div class="callout"><b>핵심 요약</b><ul style="margin:.382rem 0 0 1.272rem">{summ}</ul></div>{wrap_tables(body_h)}{faq_html(faqs)}{srcs}{cta}</article><aside class="side">{toc(secs)}{SIDECTA}</aside></div></div>
{related_html(rel)}'''
    W(f"insight/{d['slug']}/index.html",page(h,body))

def render_insight_index(posts):
    path="/insight/"; bc=[("홈","/"),("인사이트",path)]
    cards="".join(f'<a class="guide-card" href="/insight/{d["slug"]}/"><small style="font-weight:700;color:var(--green2)">{esc(d["category"])} · {d["date"]}</small><b>{esc(d["title"])}</b><span>{esc(d["description"])}</span></a>' for d in posts) or "<p>곧 첫 글이 올라옵니다.</p>"
    ld=[{"@type":"Blog","name":"은행나무요양원 인사이트","url":SITE+path,"inLanguage":"ko-KR","publisher":{"@type":"Organization","name":"은행나무요양원"},
         "blogPost":[{"@type":"BlogPosting","headline":d["title"],"url":SITE+f"/insight/{d['slug']}/","datePublished":d["date"]} for d in posts[:20]]},bc_ld(bc)]
    h=head("인사이트 | 요양원 선택·비용·등급·돌봄 정보 매일 업데이트 - 은행나무요양원","요양원 선택, 비용과 제도, 장기요양등급, 치매 돌봄 정보를 하루 한 편씩 정리하는 은행나무요양원 인사이트.",path,extra_ld=ld,kw="요양원 정보, 요양원 비용, 장기요양등급, 치매 돌봄, 서울근교 요양원")
    body=f'''{crumbs(bc)}
<section class="page-hero" style="padding-top:0"><div class="wrap"><h1>인사이트</h1><p class="lead">요양원을 알아보는 가족에게 도움이 되는 정보를 하루 한 편씩 정리합니다. 제도와 금액은 공식 자료를 확인해 적습니다.</p><p class="meta"><a href="/rss.xml" style="text-decoration:underline">RSS 구독</a></p></div></section>
<div class="page-body"><div class="wrap"><div class="grid-guides">{cards}</div></div></div>'''
    W("insight/index.html",page(h,body))

def inject_home(posts):
    p=os.path.join(ROOT,"index.html")
    if not os.path.exists(p): return
    s=open(p,encoding="utf-8").read()
    cards="".join(f'<a class="guide-card" href="/insight/{d["slug"]}/"><small style="font-weight:700;color:var(--green2)">{esc(d["category"])} · {d["date"]}</small><b>{esc(d["title"])}</b><span>{esc(d["description"])}</span></a>' for d in posts[:3]) or ""
    blk=f'<!--INSIGHT_START-->{cards}<!--INSIGHT_END-->'
    s2=re.sub(r"<!--INSIGHT_START-->.*?<!--INSIGHT_END-->",lambda m:blk,s,flags=re.S)
    if s2!=s: open(p,"w",encoding="utf-8").write(s2)

def write_feeds(posts):
    urls=[("/",TODAY,"1.0"),("/guide/",TODAY,"0.8"),("/insight/",posts[0]["date"] if posts else TODAY,"0.8")]
    urls+=[(f"/guide/{s}/",TODAY,"0.8") for s,_,_ in GUIDES]
    urls+=[(f"/insight/{d['slug']}/",d.get("modified",d["date"]),"0.6") for d in posts]
    x='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{SITE}{u}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for u,m,pr in urls)+"</urlset>\n"
    W("sitemap.xml",x)
    items="".join(f'<item><title>{esc(d["title"])}</title><link>{SITE}/insight/{d["slug"]}/</link><guid>{SITE}/insight/{d["slug"]}/</guid><pubDate>{datetime.strptime(d["date"],"%Y-%m-%d").strftime("%a, %d %b %Y 07:00:00 +0900")}</pubDate><description>{esc(d["description"])}</description></item>\n' for d in posts[:30])
    W("rss.xml",f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>은행나무요양원 인사이트</title><link>{SITE}/insight/</link><description>요양원 선택·비용·등급·돌봄 정보</description><language>ko-KR</language>\n{items}</channel></rss>\n')
    head_p=os.path.join(ROOT,"tools/llms_head.txt")
    base=open(head_p,encoding="utf-8").read() if os.path.exists(head_p) else "# 은행나무요양원\n"
    ll=base.rstrip()+"\n\n## 이용 가이드\n"+"".join(f"- [{t}]({SITE}/guide/{s}/): {d}\n" for s,t,d in GUIDES)
    if posts: ll+="\n## 인사이트 (최신순)\n"+"".join(f"- [{d['title']}]({SITE}/insight/{d['slug']}/): {d['description']}\n" for d in posts[:50])
    W("llms.txt",ll)
    full=ll+"\n\n---\n# 전문\n"
    for s,p in PAGES.items():
        full+=f"\n\n## {p['h1']}\n{SITE}/guide/{s}/\n"+"\n".join(strip(b) for _,_,b in p["secs"])+"\n"+"\n".join(f"Q. {q}\nA. {a}" for q,a in p["faqs"])
    for d in posts[:50]:
        full+=f"\n\n## {d['title']}\n{SITE}/insight/{d['slug']}/\n{strip(d['body'])}\n"+"\n".join(f"Q. {f['q']}\nA. {f['a']}" for f in d["faq"])
    W("llms-full.txt",full)

def main():
    posts=load_posts(); errs=validate(posts)
    if errs:
        print("검증 실패:"); [print(" -",e) for e in errs]; sys.exit(1)
    for s,p in PAGES.items(): render_guide(s,p)
    render_hub(); [render_post(d,posts) for d in posts]; render_insight_index(posts)
    inject_home(posts); write_feeds(posts)
    print(f"OK 안내 {len(PAGES)}쪽 · 인사이트 {len(posts)}편")
if __name__=="__main__": main()
