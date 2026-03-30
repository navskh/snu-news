from fpdf import FPDF
import os

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

    def cover_page(self):
        self.add_page()
        self.ln(25)

        # 상단 장식선
        self.set_draw_color(26, 42, 74)
        self.set_line_width(1.2)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(8)

        # 제목
        self.set_font("PB", size=22)
        self.set_text_color(26, 42, 74)
        self.multi_cell(0, 12, "서울대학교 핵심가치 & 최근 이슈\n조사 자료", align="L")
        self.ln(4)

        # 부제목
        self.set_font("PR", size=12)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 8, "지원 문항 [조직이해] 답변 준비를 위한 대학신문 기사 자료 모음", align="L")
        self.ln(2)

        self.set_font("PL", size=10)
        self.set_text_color(120, 120, 120)
        self.multi_cell(0, 7, "출처: 대학신문 (snunews.com) | 수집일: 2026년 3월 30일", align="L")
        self.ln(8)

        # 하단 장식선
        self.set_draw_color(26, 42, 74)
        self.set_line_width(0.5)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(10)

        # 지원 문항 박스
        self.set_fill_color(240, 244, 251)
        x = self.get_x()
        y = self.get_y()
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
        self.ln(10)

        # 목차
        self.set_font("PB", size=13)
        self.set_text_color(26, 42, 74)
        self.cell(0, 10, "수집 기사 목록", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(220, 220, 220)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(4)

        toc_items = [
            ("1", "이제는 진짜 민주주의로 갈 때다 — 서울대인부터 엘리트주의 극복해야", "특별기고 | 정병설 교수", "핵심가치·역할"),
            ("2", "다시 돌아온 계절, 파면이 남긴 궤적과 못다 한 이야기", "기획 | 대학신문", "최근 이슈·역할"),
            ("3", "외국인·청각장애인 교육 여건 개선 위해 강의 실시간 번역 서비스 도입", "캠퍼스 취재", "핵심가치·이슈"),
            ("4", "'일방적 주장 포함된 경우 제한'… 홍보물 게시 기준에 학생사회 우려", "캠퍼스 취재", "최근 이슈"),
            ("5", "장기화되는 학생식당 공실 문제, 본부는 적극적으로 대응해야", "사설 | 오피니언", "최근 이슈"),
        ]

        for num, title, meta, tag in toc_items:
            self.set_font("PB", size=10)
            self.set_text_color(26, 42, 74)
            self.cell(8, 7, f"{num}.", new_x="RIGHT", new_y="LAST")
            self.set_font("PR", size=10)
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 7, title)
            self.set_x(33)
            self.set_font("PL", size=8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, f"{meta}  |  [{tag}]", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def add_article(self, num, title, meta, url, body_paragraphs, insight):
        self.add_page()

        # 기사 번호 + 카테고리 태그
        self.set_font("PB", size=10)
        self.set_text_color(26, 42, 74)
        self.cell(0, 8, f"기사 {num}", new_x="LMARGIN", new_y="NEXT")

        # 제목
        self.set_font("PB", size=15)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 9, title)
        self.ln(2)

        # 메타 정보
        self.set_x(self.l_margin)
        self.set_font("PL", size=9)
        self.set_text_color(130, 130, 130)
        self.multi_cell(0, 6, meta)
        self.set_x(self.l_margin)
        self.set_font("PL", size=8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 6, url, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        # 구분선
        self.set_draw_color(200, 200, 200)
        self.line(25, self.get_y(), 185, self.get_y())
        self.ln(5)

        # 본문
        self.set_font("PR", size=10)
        self.set_text_color(50, 50, 50)
        for para in body_paragraphs:
            if para.strip():
                self.multi_cell(0, 7, para.strip())
                self.ln(3)

        self.ln(3)

        # 인사이트 박스
        self.set_x(self.l_margin)
        self.set_font("PB", size=9)
        self.set_text_color(26, 42, 74)
        self.cell(0, 7, "핵심가치 / 이슈 연관 분석", new_x="LMARGIN", new_y="NEXT")
        self.set_x(self.l_margin)
        self.set_font("PR", size=9)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, insight)


# 기사 데이터
articles = [
    {
        "title": "이제는 진짜 민주주의로 갈 때다 — 서울대인부터 엘리트주의 극복해야",
        "meta": "특별기고 | 정병설 교수(국어국문학과) | 2026.03.29",
        "url": "https://www.snunews.com/news/articleView.html?idxno=35064",
        "body": [
            "한국은 권력의 집중과 위계화에 익숙한 나라다. 시민의 결정 폭을 넓혀야 좋은 민주주의를 이룰 수 있으며, 서울대인부터 엘리트주의를 극복해야 한다.",
            "현대 정치에서 민주주의만큼 자주 사용되는 말은 없을 것이다. 그런데 민주주의를 모르는 사람도 없지만 그것을 제대로 아는 사람도 많지 않다. 서울대 중앙도서관 앞의 넓은 계단 정원은 오랫동안 아크로폴리스라고 불렸다. 1980년대 이후 대규모 학생 집회에 자주 사용됐는데, 민주주의 발상지로 알려진 고대 아테네의 유명 지명으로 장소의 의미를 나타내려고 했던 듯하다.",
            "천 년 이상 왕정과 독재 속에 살았던 한국인에게 민주주의가 쉽게 이해된다면 그것이 도리어 이상한 일이다. 대통령·대법원·대검찰청 등 권력자들은 모두 이름에 '대', '중앙', '고등' 등 위압적인 접두사를 붙일 뿐만 아니라, 그 건물들은 멀리서도 권력을 느낄 수 있는 위치와 높이를 갖추고 있다. 이렇게 권력의 집중과 위계화에 익숙한 나라에서 민주주의에 대한 감각을 갖추기는 쉽지 않다.",
            "서울대인부터 엘리트주의를 극복해야 한다는 것이 필자의 주장이다. 서울대를 비롯한 명문 대학에 다닌다는 것은 곧 사회 엘리트 집단에 속한다는 인식이 강하다. 그러나 진정한 민주주의를 위해서는 이러한 엘리트 의식을 극복하고 시민 모두의 결정 폭을 넓혀야 한다. 좋은 민주주의는 소수 엘리트의 통치가 아니라, 다양한 시민들이 실질적으로 참여하는 공론장에서 만들어진다.",
        ],
        "insight": "이 기고문은 서울대가 한국 사회에서 지식·권력 위계를 재생산하는 기관이 될 것인지, 아니면 민주적 가치와 개방성을 선도하는 기관이 될 것인지를 정면으로 묻는다. '개방성', '사회적 책임', '비판적 사고'가 서울대의 핵심가치와 연결되며, '서울대인부터 엘리트주의 극복'이라는 메시지는 지원 답변에서 서울대의 사회적 역할을 논할 때 직접 인용·활용할 수 있다.",
    },
    {
        "title": "다시 돌아온 계절, 파면이 남긴 궤적과 못다 한 이야기",
        "meta": "기획 | 학사사회문화부 차장, 김태연 기자 | 2026.03.29",
        "url": "https://www.snunews.com/news/articleView.html?idxno=35079",
        "body": [
            "지난해 4월 4일, 헌법재판소는 윤석열 전 대통령 탄핵소추안을 만장일치로 인용했다. 2024년 12월 3일 비상계엄 선포로 촉발된 헌정 위기는 넉 달여 만에 일단락됐지만, 그 여파는 아직 사회 곳곳에 남아 있다.",
            "파면 1주년을 맞은 지금, 한국 사회는 민주주의의 회복력을 확인하는 동시에 극단적 지지 세력의 폭력, 정서적 양극화, 정치적 피로감이라는 새로운 과제에 직면해 있다.",
            "서울대 캠퍼스에서도 계엄 선포 직후 학생총회와 시국선언, 대자보 게시가 잇따랐고, 교수·학생·직원·동문이 함께 목소리를 높였다. 그러나 당시의 관심과 참여가 일상 속에서 지속되고 있는지는 물음표로 남는다.",
            "대학신문은 파면 1주년을 맞아 청년 사회와 캠퍼스가 그 시간을 어떻게 통과했는지, 그리고 아직 끝나지 않은 얘기는 무엇인지 되짚어 봤다. 비상계엄 해제 요구 결의안은 재석의원 190인 만장일치로 통과됐고, 이후 두 차례의 탄핵소추안 발의 끝에 2024년 12월 14일 가결됐다.",
        ],
        "insight": "비상계엄과 탄핵이라는 헌정 위기 속에서 서울대 구성원들이 어떤 역할을 했는지 보여주는 기사다. 서울대는 단순한 교육기관을 넘어 사회적 공론장이자 민주주의 수호의 공간으로 기능했다. '사회적 책임을 다하는 대학', '민주주의의 보루로서의 서울대'라는 핵심가치와 직결된다. 최근 대학 이슈로 이 사안을 선택한다면, 서울대의 역할을 '사회 비판·각성·연대의 장'으로 서술할 수 있다.",
    },
    {
        "title": "외국인·청각장애인 교육 여건 개선 위해 강의 실시간 번역 서비스 도입",
        "meta": "보도·취재 | 캠퍼스 | 2026.03",
        "url": "https://www.snunews.com/news/articleView.html?idxno=35080",
        "body": [
            "올해 3월부터 실시간 강의 자동 번역·자막 제공 서비스 'TransLive'(트랜스라이브)가 도입됐다. 트랜스라이브는 인공지능(AI)으로 교수자의 강의 내용을 음성 인식해 강의 대본과 번역 자막을 실시간으로 제공하는 LMS(eTL) 기반 서비스다.",
            "정보화기획과 이정현 담당관은 '외국인 학생의 한국어 강의 수강과 내국인 학생의 외국어 강의 수강을 모두 원활하게 하고, 청각장애 학생들의 학습권을 보장하기 위한 시스템'이라며 '서울대 학생 모두에게 언어 장벽이 없는 교육 환경을 제공하고자 도입했다'고 그 취지를 밝혔다.",
            "80개 언어를 지원하는 트랜스라이브는 대면·비대면 강의에서 모두 활용될 수 있고, 강의별 도입 여부는 교수자가 결정한다. 이번 학기 기준 27개 강좌에 도입됐으며, 실사용자들은 캠퍼스 내 언어 장벽 완화에 도움이 됐다고 말한다.",
            "교수자가 서비스를 사용할 과목에 트랜스라이브 설정을 예약하고 예정된 시각에 강의를 시작하면, 수강생은 초대 링크나 QR코드로 접속한다. 강의 진행 중 실시간 음성을 텍스트로 변환한 원어 대본과 번역 자막을 수강생이 화면으로 확인할 수 있다.",
        ],
        "insight": "'포용성', '다양성', '접근성'의 가치를 실현하는 대표적인 최근 사례다. 소수자(청각장애인, 외국인 학생)의 학습권 보장이라는 측면에서 서울대가 추구하는 '모두를 위한 교육'의 가치를 보여준다. AI 기술을 활용한 교육 혁신이라는 점에서 서울대의 '혁신'과 '개방' 가치와도 연결된다. 최근 대학 이슈로 선택 시 '포용적 교육환경 구축'의 사례로 활용 가능하다.",
    },
    {
        "title": "'일방적 주장 포함된 경우 제한'… 홍보물 게시 기준에 학생사회 우려",
        "meta": "보도·취재 | 캠퍼스 | 2026.03.24",
        "url": "https://www.snunews.com/news/articleView.html?idxno=35063",
        "body": [
            "학생처 홈페이지에 게시된 학내 홍보물 승인 기준에 표현의 자유 침해가 우려되는 항목이 일부 포함돼 있다는 의문이 제기됐다. 지난 23일 기준 논란이 됐던 부분은 △사실관계가 확인되지 않은 일방적인 주장이 포함된 경우 △소송 등 법적 다툼이 진행되고 있는 사안과 관련된 경우 △학생처장이 광고물의 게시가 부적절하다고 인정하는 경우 등 6개 조건이다.",
            "여러 학내 학생단체는 홍보물 승인 기준이 모호해 공론장을 통한 자유로운 비판과 의견 개진이 위축될 여지가 있다고 지적했다. 비정규직없는서울대만들기공동행동 이재현 전 학생대표는 '특정 대상을 비방한다는 조항은 합리적인 비판에도 무분별하게 적용될 수 있다'고 우려를 표했다.",
            "학소위 엄지나 위원장은 '특히 학생처장이 부적절하다고 인정하는 홍보물을 제한하는 것은 판단의 주체가 학생처장이라는 점에서 자의적일 수밖에 없다'고 주장했다.",
            "학생지원과는 '해당 기준은 한정된 홍보 공간을 나눠 쓰고 캠퍼스 미관을 지키기 위한 최소한의 업무 처리 기준'이라며 '학생처 홈페이지를 새로 열면서 정보 제공 차원에서 게시한 것'이라고 설명했다.",
        ],
        "insight": "'표현의 자유'와 '학문의 자유'라는 대학의 핵심가치가 행정 기준에 의해 위협받을 수 있다는 이슈다. 대학이 자유로운 공론장을 어떻게 보장해야 하는지에 대한 논의이며, 서울대의 역할로 '학내 민주주의 강화'와 '표현의 자유 보장'을 제시할 수 있다. 이 이슈를 선택할 경우, 대학 본부와 학생 자치 간 균형이라는 관점에서 서울대의 역할을 논할 수 있다.",
    },
    {
        "title": "장기화되는 학생식당 공실 문제, 본부는 적극적으로 대응해야",
        "meta": "사설 | 오피니언 | 2026.03",
        "url": "https://www.snunews.com/news/articleView.html?idxno=35056",
        "body": [
            "지난 2024년부터 운영이 중지된 제4식당(76동)이 현재까지도 공실 상태다. 임대료 미납으로 2024년 7월 20일 계약이 해지됐으며, 같은 해 11월 입찰이 진행됐지만 업체 선정 실패로 신규 입점이 무산됐다.",
            "학생식당은 강의실 인근에 위치해 짧은 시간 동안 식사를 해결하기에 용이하고, 저렴한 가격으로 부담 없이 이용할 수 있어 구성원들의 수요가 높은 시설이다. 제4식당은 인문대, 사범대, 기숙사와 맞닿아 있어 접근성이 높고 가격도 저렴해 많은 구성원이 이용하던 식당이었다.",
            "단과대별 식당 개수, 메뉴 다양성 등에서 나타나고 있는 큰 편차는 구성원들의 불만을 야기할 수밖에 없다. 캠퍼스 중심부와 달리 제4식당 주변에서 생활하는 구성원은 상대적으로 학내 식생활에 큰 제약을 받고 있다.",
            "본부는 공실 장기화 문제에 대해 보다 적극적으로 해결 방안을 모색해야 한다. 자산관리팀은 새 업체 입점을 위한 입찰 절차를 신속하게 추진하고, 단기적으로는 임시 운영 방안을 마련해야 한다. 학생식당은 단순한 편의시설이 아니라 구성원의 기본적인 생활 여건과 직결되는 복지 시설이다.",
        ],
        "insight": "서울대 구성원의 기본적인 생활 여건(복지) 문제다. '구성원 모두를 위한 공동체'라는 서울대의 가치 실현 여부를 점검하는 사례로 활용 가능하다. 특히 접근성 불평등(단과대별 편차) 문제는 서울대가 내부적으로 형평성을 어떻게 실현하고 있는지를 보여주며, 대학 본부의 책임 있는 행정과 구성원 복지라는 관점에서 서울대의 역할을 논할 수 있다.",
    },
]

# PDF 생성 실행
pdf = KoreanPDF()
pdf.cover_page()
for i, art in enumerate(articles, 1):
    pdf.add_article(
        num=i,
        title=art["title"],
        meta=art["meta"],
        url=art["url"],
        body_paragraphs=art["body"],
        insight=art["insight"],
    )

output_path = "/Users/younghoonsung/Projects/snu-news/SNU_뉴스_조직이해_자료.pdf"
pdf.output(output_path)
print(f"PDF 생성 완료: {output_path}")
