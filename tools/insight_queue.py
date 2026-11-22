#!/usr/bin/env python3
"""키워드 순위표(tools/keywords.csv) → 인사이트 대기열(tools/INSIGHT_QUEUE.md).
글 JSON 의 "keyword" 값이 같거나 제목에 그 키워드가 들어 있으면 완료로 본다.
실행: python3 tools/insight_queue.py  (맨 위 '대기' 키워드부터 한 편씩 쓴다)"""
import csv,json,glob,os,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP={"의정부요양원","포천요양원","양평요양원","가평요양원","양주요양원","고급요양원","프리미엄요양원",  # 다른 지역·과장 표현
      "요양원한달비용","요양원입소비용","요양원가격","요양원식비","요양원상급침실비","요양원1인실","요양원면회","서울요양원비용","남양주요양원비용","요양병원비용"}  # 금액·규정 확정 전
RULES=[("창업","open-nursing-home"),("컨설팅","open-nursing-home"),("설립","open-nursing-home"),("인수","open-nursing-home"),("프랜차이즈","open-nursing-home"),
 ("요양보호사","care-worker"),("인지지원","cognitive-support-grade"),("실버타운","silvertown"),("요양병원","vs-hospital"),
 ("치매","dementia"),("방문요양","home-care"),("주야간","home-care"),("재가","home-care"),
 ("요양원등급","facility-rating"),("평가","facility-rating"),("추천","choose"),("좋은요양원","choose"),
 ("본인부담","cost"),("비용","cost"),
 ("등급신청","grade"),("인정신청","grade"),("등급판정","grade"),("받는방법","grade"),("신청방법","grade"),
 ("1등급","grade-compare"),("2등급","grade-compare"),("3등급","grade-compare"),("4등급","grade-compare"),("5등급","grade-compare"),("장기요양등급","grade-compare"),
 ("입소","admission"),("노인장기요양보험","ltc-insurance"),("시설급여","ltc-insurance"),("요양시설","ltc-insurance"),
 ("강동","gangdong-songpa"),("송파","gangdong-songpa"),("노원","nowon-jungnang"),("중랑","nowon-jungnang"),("강남","seoul-nursing-home"),("서울요양원","seoul-nursing-home"),
 ("하남","near-seoul"),("구리","near-seoul"),("근교","near-seoul"),("경기","near-seoul"),
 ("남양주","namyangju"),("화도","namyangju"),("마석","namyangju"),("천마산","namyangju")]
AREAS="진접 별내 다산 덕소 오남 수동 호평 평내 퇴계원 진건 조안 와부".split()
def guide(k):
    if any(a in k for a in AREAS): return "namyangju-areas"
    for s,g in RULES:
        if s in k: return g
    return "choose"
def main():
    posts=[json.load(open(f,encoding="utf-8")) for f in glob.glob(os.path.join(R,"content","insight","*.json"))]
    rows=sorted(((int(v),k) for k,v in csv.reader(open(os.path.join(R,"tools","keywords.csv"),encoding="utf-8"))),reverse=True)
    todo=[];done=[];skip=[]
    for v,k in rows:
        if k in SKIP: skip.append((v,k)); continue
        hit=[p for p in posts if p.get("keyword","").replace(" ","")==k or k in p["title"].replace(" ","")]
        (done if hit else todo).append((v,k,guide(k),hit[0]["slug"] if hit else ""))
    L=["# 인사이트 키워드 대기열","",f"대기 {len(todo)} · 완료 {len(done)} · 보류 {len(skip)}","","## 대기 (위에서부터 한 편씩)","","| 키워드 | 월 검색량 | 붙일 안내 페이지 |","|---|---|---|"]
    L+=[f"| {k} | {v:,} | {g} |" for v,k,g,_ in todo]
    L+=["","## 완료","","| 키워드 | 월 검색량 | 글 |","|---|---|---|"]+[f"| {k} | {v:,} | {s} |" for v,k,g,s in done]
    L+=["","## 보류 (다른 지역·과장 표현·금액 확정 전)","",", ".join(f"{k}({v:,})" for v,k in skip),""]
    open(os.path.join(R,"tools","INSIGHT_QUEUE.md"),"w",encoding="utf-8").write("\n".join(L))
    print(f"대기 {len(todo)} 완료 {len(done)} 보류 {len(skip)}"); [print("다음:",k,v,g) for v,k,g,_ in todo[:5]]
if __name__=="__main__": main()
