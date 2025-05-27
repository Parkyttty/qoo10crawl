# 🛍️ Qoo10.jp 상품 크롤러

Qoo10.jp의 상품 정보를 크롤링하여 CSV 파일로 다운로드할 수 있는 웹 애플리케이션입니다.

## 🌟 주요 기능

- **웹 기반 인터페이스**: 별도 설치 없이 브라우저에서 사용
- **실시간 크롤링**: URL 입력 후 즉시 크롤링 실행
- **CSV 다운로드**: 결과를 CSV 파일로 다운로드
- **광고 필터링**: PR(광고) 상품 자동 제외
- **진행률 표시**: 크롤링 진행 상황을 실시간으로 확인

## 📊 추출 데이터

- 순위 (광고 제외한 실제 순위)
- 브랜드명
- 제품명
- 정가
- 판매가
- 제품 링크
- 리뷰 수

## 🚀 로컬 실행

```bash
# 저장소 클론
git clone https://github.com/your-username/qoo10-crawler.git
cd qoo10-crawler

# 라이브러리 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 🌐 온라인 버전

[여기서 바로 사용하기](https://your-app-name.streamlit.app)

## 📝 사용법

1. Qoo10.jp 카테고리 페이지 URL 입력
2. '크롤링 시작' 버튼 클릭
3. 결과 확인 후 CSV 다운로드

## ⚠️ 주의사항

- 개인적인 용도로만 사용해주세요
- 웹사이트의 이용약관을 준수해주세요
- 과도한 요청은 피해주세요
- 광고 상품(PR)은 자동으로 제외됩니다

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **크롤링**: BeautifulSoup4, Requests
- **데이터 처리**: Pandas

## 📄 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request