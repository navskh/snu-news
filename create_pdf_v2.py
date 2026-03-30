from fpdf import FPDF
import os
import json

# 폰트 경로
FONT_DIR = os.path.expanduser("~/Library/Fonts/")

class KoreanPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.add_font("PR", "", FONT_DIR + "Pretendard-Regular.otf")
        self.add_font("PB", "", FONT_DIR + "Pretendard-Bold.otf")
        self.add_font("PL", "", FONT_DIR + "Pretendard-Light.otf")
        self.add_font("PSB", "", FONT_DIR + "Pretendard-SemiBold.otf")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(25, 20, 25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("PL", size=8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 8, "서울대학교 핵심가치 & 최근 이슈 조사 자료 | 출처: 대학신문 (snunews.com)", align="R")
            self.ln(2)
            self.set_draw_color(200, 200, 200)
            self.line(25, self.get_y(), 185, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("PL", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"{self.page_no()}", align="C")

    def cover_page(self, toc_items):
        self.add_page()
        self.ln(15)

        self.set_draw_color(26, 42, 74)
        self.set_line_width(1.2)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(8)

        self.set_font("PB", size=22)
        self.set_text_color(26, 42, 74)
        self.multi_cell(0, 12, "서울대학교 핵심가치 & 최근 이슈\n조사 자료", align="L")
        self.ln(3)

        self.set_font("PR", size=12)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, "지원 문항 [조직이해] 답변 준비를 위한 대학신문 기사 자료 모음", align="L")
        self.ln(2)

        self.set_font("PL", size=10)
        self.set_text_color(120, 120, 120)
        self.multi_cell(0, 7, "출처: 대학신문 (snunews.com) | 수집일: 2026년 3월 30일 | 수집 기사: 58편 (2025.03~2026.03)", align="L")
        self.ln(6)

        self.set_draw_color(26, 42, 74)
        self.set_line_width(0.5)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(8)

        # 지원 문항 박스
        self.set_font("PB", size=10)
        self.set_text_color(26, 42, 74)
        self.cell(0, 8, "[조직이해] 지원 문항", new_x="LMARGIN", new_y="NEXT")
        self.set_font("PR", size=10)
        self.set_text_color(50, 50, 50)
        question = (
            "지원자가 생각하는 서울대학교의 핵심가치는 무엇인지 기술하고, "
            "최근 대학을 둘러싼 다양한 이슈 중 하나를 선택하여 이에 대한 "
            "지원자의 견해와 서울대학교의 역할에 대하여 기술하여 주십시오."
        )
        self.multi_cell(0, 7, question)
        self.ln(8)

        # 목차
        self.set_font("PB", size=13)
        self.set_text_color(26, 42, 74)
        self.cell(0, 10, f"수집 기사 목록 (총 {len(toc_items)}편)", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(220, 220, 220)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(4)

        for num, title, meta, date, tag in toc_items:
            self.set_font("PB", size=9)
            self.set_text_color(26, 42, 74)
            self.cell(10, 6, f"{num}.", new_x="RIGHT", new_y="LAST")
            self.set_font("PR", size=9)
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 6, title)
            self.set_x(35)
            self.set_font("PL", size=7.5)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, f"{date}  |  {meta}  |  [{tag}]", new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

    def add_section_header(self, section_name, count):
        self.add_page()
        self.ln(10)
        self.set_fill_color(26, 42, 74)
        self.set_font("PB", size=16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 14, f"  {section_name}  ({count}편)", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(5)

    def add_article(self, num, title, meta, date, url, body_paragraphs, summary, topic):
        self.add_page()

        # 주제 태그
        self.set_font("PB", size=8)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(26, 42, 74)
        self.cell(0, 6, f"  기사 {num:02d}  |  {topic}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(4)

        # 제목
        self.set_font("PB", size=14)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 9, title)
        self.ln(2)

        # 메타 정보
        self.set_font("PL", size=9)
        self.set_text_color(130, 130, 130)
        self.multi_cell(0, 6, f"{date}  |  {meta}")
        self.set_font("PL", size=8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 6, url, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        self.set_draw_color(200, 200, 200)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(4)

        # 요약
        if summary:
            self.set_fill_color(245, 247, 252)
            self.set_font("PSB", size=8.5)
            self.set_text_color(26, 42, 74)
            self.cell(0, 6, "  요약", new_x="LMARGIN", new_y="NEXT", fill=True)
            self.set_font("PR", size=9)
            self.set_text_color(60, 60, 60)
            self.set_fill_color(245, 247, 252)
            self.multi_cell(0, 6, "  " + summary, fill=True)
            self.ln(4)

        # 본문
        self.set_font("PR", size=9.5)
        self.set_text_color(50, 50, 50)
        for para in body_paragraphs:
            if para.strip():
                self.multi_cell(0, 6.5, para.strip())
                self.ln(2)


def split_body(body_text, chunk_size=400):
    """Split body text into paragraphs"""
    if not body_text:
        return []
    # Split on newlines first
    parts = [p.strip() for p in body_text.split('\n') if p.strip()]
    if not parts:
        parts = [body_text]

    # If we have very long parts, split them further
    result = []
    for part in parts:
        if len(part) > chunk_size:
            # Split at sentence boundaries
            sentences = []
            current = ""
            for ch in part:
                current += ch
                if ch in ('다', '요', '까', '죠') and len(current) > 150:
                    if current.strip():
                        sentences.append(current.strip())
                    current = ""
            if current.strip():
                sentences.append(current.strip())

            # Group sentences into paragraphs
            para = ""
            for s in sentences:
                para += s + " "
                if len(para) > 300:
                    result.append(para.strip())
                    para = ""
            if para.strip():
                result.append(para.strip())
        else:
            result.append(part)

    return result[:20]  # Max 20 paragraphs


# Load collected articles
with open('/Users/younghoonsung/Projects/snu-news/snu_articles_final.json', 'r', encoding='utf-8') as f:
    raw_articles = json.load(f)

raw_articles.sort(key=lambda x: x.get('date', ''), reverse=True)

# Manual summaries and insights for key articles
manual_data = {
    35079: {
        'summary': '윤석열 전 대통령 탄핵·파면 1주년 기획. 비상계엄(2024.12.3)부터 헌재 만장일치 인용(2025.4.4)까지 과정과 서울대 캠퍼스 내 학생총회·시국선언·대자보 활동 기록.',
        'topic': '민주주의 / 탄핵 / 대학의 사회적 역할',
    },
    35080: {
        'summary': 'AI 기반 실시간 강의 번역·자막 서비스 TransLive 도입(2026.3~). 80개 언어 지원, 청각장애인·외국인 학생 학습권 보장. 이번 학기 27개 강좌 도입.',
        'topic': 'AI / 기술 / 글로벌화 / 포용성',
    },
    35064: {
        'summary': '국어국문학과 정병설 교수 특별기고. 한국 사회의 권력 집중·위계 문화를 비판하며, 서울대인부터 엘리트주의를 극복하고 시민 결정권을 확대해 진정한 민주주의를 실현해야 한다고 주장.',
        'topic': '민주주의 / 대학의 역할 / 핵심가치',
    },
    35063: {
        'summary': '학생처 홍보물 게시 기준에 "일방적 주장 제한" 등 표현의 자유 침해 우려 조항 포함. 학소위·비서공 등 학생단체 반발. 학생처장 자의적 판단 가능성 지적.',
        'topic': '표현의 자유 / 학생 자치 / 민주주의',
    },
    35065: {
        'summary': '관정도서관 2층 리모델링 완료 후 특정 자리 사유화(장시간 점거)와 소음 문제 불거짐. 이용 학생들의 반응 엇갈려.',
        'topic': '학생 복지 / 캠퍼스 환경',
    },
    35078: {
        'summary': '시대의 아픔을 품는 따뜻한 지성이 돼야 한다는 주제의 인터뷰. 서울대의 지적·사회적 역할에 대한 논의.',
        'topic': '대학의 역할 / 핵심가치',
    },
    35068: {
        'summary': '철학자 하버마스(1929~2026) 타계 추모 특별기고. 공론장 이론, 의사소통적 합리성, 민주주의 철학적 유산을 되새기며 대학의 공론장 역할 강조.',
        'topic': '학술 / 민주주의 / 대학의 역할',
    },
    35061: {
        'summary': '아리랑이 특정 정치 세력의 집회 음악으로 전용되는 현상을 비판. 문화의 자율성과 독립성을 보호해야 한다는 칼럼.',
        'topic': '문화 / 표현의 자유 / 사회',
    },
    35058: {
        'summary': '서울대병원 노인진료센터 취재. 질병 치료를 넘어 환자의 삶 전체를 돌보는 통합적 진료 방식 소개. 서울대의 사회적 기여 사례.',
        'topic': '사회적 역할 / 의료 / 복지',
    },
    35056: {
        'summary': '제4식당(76동) 2024년 7월 계약 해지 후 공실 장기화. 인문대·사범대 인근 구성원 식생활 불편. 본부의 적극적 해결 촉구.',
        'topic': '학생 복지 / 캠퍼스 행정',
    },
    35051: {
        'summary': '성과 중심 연구 경쟁 속에서 연구의 진정한 목적과 방향성을 묻는 기사. 양적 지표 추구 문화에 대한 비판.',
        'topic': '학술 / 연구 / 대학 정책',
    },
    35038: {
        'summary': '중동 정세 안정에도 원/달러 환율 1,500원대가 지속되는 이유를 구조적으로 분석. 미국 통화정책, 한국 경상수지 등 복합 요인 설명.',
        'topic': '사회 / 경제',
    },
    35040: {
        'summary': '광화문 현판의 한글·한자 논쟁을 통해 문화재 정책과 역사 인식 문제를 다룸.',
        'topic': '사회 / 문화 / 역사',
    },
    35075: {
        'summary': "힙합 아티스트 '하공안' 11집이 타입비트(저작권 있는 비트) 사용으로 음원 삭제 조치를 받은 사건을 보도. 저작권 문제와 창작 문화 논의.",
        'topic': '문화 / 저작권 / 사회',
    },
    35023: {
        'summary': '한국 쉬었음 청년 50만 명 돌파(2025). 덴마크 플렉시큐리티 모델 해외취재를 통해 노동시장 유연성+사회안전망 결합 해법 탐구.',
        'topic': '사회 / 청년 / 교육개혁',
    },
    34640: {
        'summary': '유홍림 총장 단독 인터뷰(2025.11). 종합화 50주년 성과 평가, "경계를 넘어·지역을 잇고·세계를 향해" 비전 제시. 글로벌 대학으로의 전환 논의.',
        'topic': '글로벌화 / 대학 비전 / 핵심가치',
    },
    34520: {
        'summary': '서울대 외국인 학생 비율 4.4%(연세대 17.2%, 고려대 16.8% 대비 현저히 낮음). 글로벌인재학부 신설 논의, 할랄·채식 식당 부재, 행정 한국어 편향 등 문제 제기.',
        'topic': '글로벌화 / 국제화 / 포용성',
    },
    34360: {
        'summary': '서울대 교수들의 홍콩과기대 등 해외 이직 증가. 연봉 격차(최대 4배), 연구 환경 열악, 카운터오퍼 문화 부재가 원인. 글로벌 인재 경쟁 대응 촉구.',
        'topic': '대학 정책 / 인재 유출 / 글로벌화',
    },
    34900: {
        'summary': '학과 간 칸막이가 높아 융합 연구와 교육이 어렵다는 문제 제기. 학제 간 협력을 위한 제도적 개선 방안 논의.',
        'topic': '대학 구조 / 교육 개혁',
    },
    34910: {
        'summary': '학부 신설·정원 증원 시 교원 확보, 공간 부족, 재정 문제 등 예상되는 문제에 대학 본부가 사전 대비해야 한다는 오피니언.',
        'topic': '대학 정책 / 구조조정 / 학령인구',
    },
    34950: {
        'summary': '한국 ODA(공적개발원조) 정책이 전환점을 맞이한 배경과 서울대의 국제 개발협력 역할을 분석.',
        'topic': '글로벌화 / 사회적 역할 / ODA',
    },
    34750: {
        'summary': 'LnL(Liberal education and Leadership) 사업 확대를 둘러싼 논란. 기초교양 교육 강화 정책의 실효성과 부작용 논의.',
        'topic': '대학 교육 / 교육과정',
    },
    34570: {
        'summary': '자연대 신입생이 수학·과학 기초과목 시험을 통해 수강 면제받는 제도 도입 여부 논의. 교육 기회 형평성 문제 제기.',
        'topic': '교육 과정 / 학생 자치',
    },
    34690: {
        'summary': '컴퓨터공학과 개론·실습(컴개실) 전용 분반 개설을 논의한 자연대 교육공청회 결과 보도.',
        'topic': '교육 과정 / AI / 학과 정책',
    },
    34600: {
        'summary': '2024~2025학년도 단과대학생회 공약 이행률 점검. 공약 달성률, 소통 방식, 예산 집행 등 평가.',
        'topic': '학생 자치 / 거버넌스',
    },
    34160: {
        'summary': '관악사(기숙사) 입주 학생들과 관장 간의 운영 체계 개선 대화. 비용, 시설, 규정 등 현안 논의.',
        'topic': '학생 복지 / 주거',
    },
    34120: {
        'summary': '학생단체 Signal(시그널)이 구설수 반복으로 총학생회 운영위원회에서 불신임 가결됨. 학생 자치 거버넌스 문제 논의.',
        'topic': '학생 자치 / 민주주의',
    },
    34200: {
        'summary': '서울대 마르크스주의 경제학 스터디가 제도권 밖 정치경제학 강의로 부활. 학문의 자유와 비판적 교육의 공간 논의.',
        'topic': '학술 / 학문의 자유',
    },
    34560: {
        'summary': '학생회 회계 불투명 문제가 반복되는 상황. 제도적 감사 체계 강화와 회계 투명성 확보 촉구.',
        'topic': '학생 자치 / 거버넌스',
    },
    34540: {
        'summary': 'SPC그룹 불매운동 관련, 허영인 회장이 받은 서울대 발전공로상 박탈을 촉구하는 학내 연서명 발표.',
        'topic': '사회적 역할 / 윤리',
    },
    34650: {
        'summary': '학생 자치 언론기금 감사 결과 공개. 운영 현황과 문제점 보도.',
        'topic': '학생 자치 / 언론',
    },
    34380: {
        'summary': '수능 중심 고교 교육 체계의 한계를 지적하며 대학 입시와 교육 개혁이 고3만의 문제가 아닌 전 교육 시스템 개혁 문제임을 주장.',
        'topic': '교육 개혁 / 학령인구',
    },
    34440: {
        'summary': '학부대학(신입생 대상 교양 교육기관) 신입생 세미나 교과목 강화의 필요성 주장. 비판적 사고와 글쓰기 교육 중요성 강조.',
        'topic': '교육 개혁 / 핵심가치',
    },
    34000: {
        'summary': '서울대입구역 인근 옥외 전광판의 빛공해로 인근 주민들이 수면 방해를 겪는 문제. 현행 빛공해 규제법의 허점과 행정 절차 문제 취재.',
        'topic': '사회 / 환경 / 주거',
    },
    34280: {
        'summary': '2025년 이스라엘-이란 12일 무력 충돌의 경과, 원인, 국제 질서에 대한 함의를 분석.',
        'topic': '국제 / 사회',
    },
    34040: {
        'summary': '나와 다르다는 이유로 차별받는 사회 문제를 다룬 기사. 다양성과 포용을 서울대 핵심가치로 연결.',
        'topic': '인권 / 표현의 자유 / 다양성',
    },
    34180: {
        'summary': '정치에서 감정의 역할을 분석한 칼럼. 이성적 토론과 감정적 반응의 관계, 민주주의적 소통 방식 논의.',
        'topic': '민주주의 / 오피니언',
    },
    35030: {
        'summary': '중앙도서관 편의점 공사 완료 후 메뉴·가격·위치에 대한 학생 반응이 엇갈림.',
        'topic': '학생 복지 / 캠퍼스',
    },
    34710: {
        'summary': '급발진·페달 오인 사고의 심리·인지적 원인 분석. 긴급 상황에서의 인간 반응과 자동화 시스템 설계 문제 논의.',
        'topic': 'AI / 기술 / 사회',
    },
    34670: {
        'summary': '도시재생 사업으로 문을 닫게 된 구도심 골목 상권. 재개발의 긍정적 의도와 실제 주민 삶에 미치는 영향 사이의 괴리를 취재.',
        'topic': '사회적 역할 / 지역사회',
    },
    34730: {
        'summary': '서울대 대학신문 창간 역사와 역대 기사들을 통해 본 시대별 서울대의 모습. 학보의 사회적 역할과 언론의 자유 논의.',
        'topic': '대학신문 / 언론 / 역사',
    },
}

# Topic groupings for section organization
sections = [
    ("민주주의 / 탄핵 / 정치", [35079, 35064, 35068, 34120, 34180]),
    ("표현의 자유 / 학생 자치", [35063, 34040, 34560, 34600, 34650, 34540]),
    ("AI / 기술 / 글로벌화", [35080, 34640, 34520, 34360, 34950, 34710]),
    ("대학 정책 / 구조조정 / 교육", [34900, 34910, 34750, 34570, 34690, 34380, 34440]),
    ("학생 복지 / 캠퍼스 환경", [35065, 35056, 34160, 35030]),
    ("사회적 역할 / 지역사회", [35058, 35051, 34670, 34000, 35023, 34280]),
    ("학술 / 연구 / 문화", [35061, 35038, 35040, 35075, 34200, 34730]),
]

# Build article lookup
article_map = {a['idxno']: a for a in raw_articles}

# Generate ordered article list for TOC
ordered_articles = []
for section_name, ids in sections:
    for id_ in ids:
        if id_ in article_map:
            a = article_map[id_]
            manual = manual_data.get(id_, {})
            ordered_articles.append({
                'idxno': id_,
                'title': a['title'],
                'date': a['date'][:10],
                'url': a['url'],
                'meta': a.get('author', '') or a.get('section', '') or '대학신문',
                'body': a.get('body', ''),
                'summary': manual.get('summary', a.get('summary_manual', '')),
                'topic': manual.get('topic', a.get('topic', '기타')),
                'section_name': section_name,
            })

# Create TOC items
toc_items = [(str(i+1), a['title'], a['meta'][:30] if a['meta'] else '-', a['date'], a['topic'][:20])
             for i, a in enumerate(ordered_articles)]

# Generate PDF
pdf = KoreanPDF()
pdf.cover_page(toc_items)

# Add articles organized by section
article_num = 1
current_section = None

for a in ordered_articles:
    if a['section_name'] != current_section:
        current_section = a['section_name']
        count = sum(1 for x in ordered_articles if x['section_name'] == current_section)
        pdf.add_section_header(current_section, count)

    body_paras = split_body(a['body'])

    pdf.add_article(
        num=article_num,
        title=a['title'],
        meta=a['meta'][:50] if a['meta'] else '대학신문',
        date=a['date'],
        url=a['url'],
        body_paragraphs=body_paras,
        summary=a['summary'],
        topic=a['topic'],
    )
    article_num += 1

output_path = "/Users/younghoonsung/Projects/snu-news/SNU_뉴스_종합_자료_v2.pdf"
pdf.output(output_path)
print(f"PDF 생성 완료: {output_path}")
print(f"총 기사 수: {len(ordered_articles)}편")
