# -*- coding: utf-8 -*-
import json
SITE="https://bankwood.co.kr"
TEL1="010-2109-7717"; TEL2="010-2225-6775"
TODAY="2026-11-17"

GUIDES=[
 ("choose","좋은 노인요양원 고르는 법","방문 전에 확인할 12가지 체크리스트"),
 ("cost","요양원 비용 · 본인부담금 (2026)","등급별 1일 수가와 월 부담액, 감경 기준"),
 ("grade","장기요양등급 신청 방법","자격·절차·서류·점수 기준 한눈에"),
 ("admission","요양원 입소조건 · 절차","입소 전 서류, 계약, 면회 확인 사항"),
 ("vs-hospital","요양원 요양병원 차이","우리 부모님께 맞는 곳은 어디일까"),
 ("dementia","치매 요양원 · 치매등급","5등급·인지지원등급별 입소 가능 여부"),
 ("silvertown","실버타운과 요양원 차이","입소 조건과 비용 구조 비교"),
 ("home-care","방문요양 · 주야간보호 · 요양원","재가급여와 시설급여, 무엇이 맞을까"),
 ("ltc-insurance","노인장기요양보험이란","대상·급여 종류·본인부담 기초 안내"),
 ("grade-compare","장기요양등급 1~5등급 차이","등급별 점수와 요양원 입소 가능 여부"),
 ("near-seoul","서울근교 요양원 · 오는 길","강동·하남·구리에서 오는 방법"),
 ("namyangju-areas","남양주 동네별 안내","진접·별내·다산·마석에서 오는 길"),
 ("namyangju","남양주 요양원 안내","서울 동부에서 오가기 좋은 위치와 교통"),
 ("facility-rating","요양원 등급 확인하는 법","공단 평가등급 A~E의 뜻과 한계"),
 ("seoul-nursing-home","서울 요양원 찾기","자리가 없을 때 서울 근교를 보는 기준"),
 ("gangdong-songpa","강동·송파 요양원 찾기","강일IC·8호선으로 오는 길"),
 ("nowon-jungnang","노원·중랑 요양원 찾기","경춘선으로 마석역까지 오는 길"),
 ("cognitive-support-grade","인지지원등급이란","45점 미만 치매 어르신이 받는 등급과 서비스"),
 ("care-worker","요양보호사 안내","하는 일, 교육 320시간, 자격시험"),
 ("open-nursing-home","요양원 창업 · 개원 절차","토르건축 · 설치신고부터 장기요양기관 지정까지"),
]

def header():
    return '''<header>
  <div class="wrap nav">
    <a class="logo" href="/" aria-label="은행나무실버케어 홈">
      <svg viewBox="0 0 100 100" aria-hidden="true"><g transform="rotate(-26 50 56)"><path d="M50 64C43 55 25 43 7 34C11 24 21 16 33 13C37 12 41 13 44 12C46 11.5 48 13 49.5 16C50.5 13 52 11.5 55 12C59 13 62 12 67 13C79 16 89 24 93 34C75 43 57 55 50 64Z" fill="#CFA53A" stroke="#EFD58A" stroke-width="2" stroke-linejoin="round"/><path d="M50 64C50.5 73 54 83 61 91" fill="none" stroke="#CFA53A" stroke-width="3" stroke-linecap="round"/><path d="M50 62L28 26M50 62L42 18M50 62L58 18M50 62L72 26" stroke="#B88F27" stroke-width=".9" opacity=".55"/></g></svg>
      은행나무실버케어
    </a>
    <nav class="menu" aria-label="주요 메뉴">
      <a href="/#about">소개</a><a href="/#who">상황별 안내</a><a href="/guide/">이용 가이드</a><a href="/insight/">인사이트</a><a href="/#calculator">비용 계산기</a><a href="/#location">오시는 길</a><a class="menu-build" href="/#franchise">토르건축 상담</a>
    </nav>
    <div class="navr">
      <a class="call" href="tel:010-2109-7717">사전상담</a>
      <details class="mnav"><summary>메뉴</summary>
        <div class="panel">
          <a href="/#about">소개</a><a href="/#who">상황별 안내</a><a href="/#standard">시설 기준</a><a href="/#story">은행나무 이야기</a><a href="/#progress">개원 일정</a><a href="/#care">돌봄서비스</a><a href="/#admission">입소안내</a>
          <a href="/#calculator">비용 계산기</a><a href="/#faq">자주 묻는 질문</a><a href="/#location">오시는 길</a>
          <div class="sep"></div>
          <a href="/insight/">인사이트 (매일 새 글)</a><a href="/guide/">이용 가이드 전체</a><a href="/guide/cost/">비용 · 본인부담금</a><a href="/guide/grade/">등급 신청</a>
          <div class="sep"></div>
          <a href="/#franchise">토르건축 · 개원·가맹 상담</a>
        </div>
      </details>
    </div>
  </div>
</header>'''

def footer():
    links=" · ".join(f'<a href="/guide/{s}/">{t}</a>' for s,t,_ in GUIDES)
    return f'''<footer>
  <div class="wrap">
    <p><b>은행나무실버케어</b> · 노인요양시설 · 정원 49명 (2027년 1월 준공 예정)</p>
    <p>경기도 남양주시 화도읍 가곡로 97-22 (가곡리 256-9, 우 12032) · 입소상담 {TEL1} (원장 박민경)</p>
    <p><a href="/build/">건축 일지</a> · 토르건축 · 요양원 개원·건축·가맹 문의 {TEL2} · <a href="https://thorthor.co.kr/general-construction" target="_blank" rel="noopener">토르건축 홈페이지</a></p>
    <p style="margin-top:var(--s3)" class="flinks">{links}</p>
    <p style="margin-top:var(--s3)">© 2026 은행나무실버케어. All rights reserved. · bankwood.co.kr</p>
  </div>
</footer>
<div class="mcall"><a href="tel:010-2109-7717">📞 사전 상담하기</a><a href="/#location">오시는 길</a></div>'''

def head(title,desc,path,og_title=None,extra_ld=None,kw=""):
    url=SITE+path
    ld=json.dumps({"@context":"https://schema.org","@graph":extra_ld or []},ensure_ascii=False,indent=1)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="KR-41">
<meta name="geo.placename" content="남양주시 화도읍 가곡리">
<meta name="naver-site-verification" content="NAVER_CODE">
<meta name="msvalidate.01" content="D049D2BE3DCEA10800B6C8A47C4CADBF">
<meta property="og:type" content="article">
<meta property="og:site_name" content="은행나무실버케어">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ko_KR">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5B800">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{ld}
</script>
<link rel="stylesheet" href="/assets/style.css">
<link rel="stylesheet" href="/assets/fx.css">
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
'''
