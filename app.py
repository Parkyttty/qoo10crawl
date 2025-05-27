import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin
from datetime import datetime
import io

# 페이지 설정
st.set_page_config(
    page_title="Qoo10.jp 상품 크롤러",
    page_icon="🛍️",
    layout="wide"
)

class Qoo10Crawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page_content(self, url):
        """웹페이지 내용을 가져옵니다."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            st.error(f"페이지 요청 실패: {e}")
            return None
    
    def extract_product_info(self, item_element, rank):
        """개별 상품 정보를 추출합니다."""
        try:
            # 광고 상품 체크 (PR 태그가 있으면 제외)
            ad_tag = item_element.find('span', class_='ad_cps')
            if ad_tag and ad_tag.get_text(strip=True) == 'PR':
                return None
            
            # 브랜드명 추출
            brand_element = item_element.find('a', class_='txt_brand')
            brand_name = ''
            if brand_element:
                brand_name = brand_element.get_text(strip=True)
                brand_name = re.sub(r'^公式\s*', '', brand_name)
            
            # 제품명 추출
            title_element = item_element.find('a', class_='tt')
            product_name = ''
            product_link = ''
            if title_element:
                product_name = title_element.get('title', '').strip()
                if not product_name:
                    product_name = title_element.get_text(strip=True)
                product_link = title_element.get('href', '')
                if product_link and not product_link.startswith('http'):
                    product_link = urljoin('https://www.qoo10.jp', product_link)
            
            # 가격 정보 추출
            price_section = item_element.find('div', class_='prc')
            original_price = ''
            sale_price = ''
            
            if price_section:
                del_element = price_section.find('del')
                if del_element:
                    original_price = del_element.get_text(strip=True)
                
                strong_element = price_section.find('strong')
                if strong_element:
                    sale_price = strong_element.get_text(strip=True)
            
            # 리뷰 수 추출
            review_count = ''
            review_element = item_element.find('span', class_='review_total_count')
            if review_element:
                review_text = review_element.get_text(strip=True)
                review_match = re.search(r'\((\d+)\)', review_text)
                if review_match:
                    review_count = review_match.group(1)
            
            return {
                '순위': rank,
                '브랜드명': brand_name,
                '제품명': product_name,
                '정가': original_price,
                '판매가': sale_price,
                '제품링크': product_link,
                '리뷰수': review_count
            }
        
        except Exception as e:
            st.error(f"상품 정보 추출 중 오류 발생: {e}")
            return None
    
    def crawl_products(self, url, progress_bar=None, status_text=None):
        """상품 목록을 크롤링합니다."""
        if status_text:
            status_text.text("페이지 내용을 가져오는 중...")
        
        html_content = self.get_page_content(url)
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        item_elements = soup.find_all('div', class_='item')
        
        if not item_elements:
            st.warning("상품을 찾을 수 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
            return []
        
        if status_text:
            status_text.text(f"총 {len(item_elements)}개의 상품을 처리 중...")
        
        products = []
        rank = 1
        
        for i, item in enumerate(item_elements):
            if progress_bar:
                progress_bar.progress((i + 1) / len(item_elements))
            
            product_info = self.extract_product_info(item, rank)
            if product_info:
                products.append(product_info)
                rank += 1
            
            time.sleep(0.1)
        
        return products

def convert_df_to_csv(df):
    """DataFrame을 CSV로 변환합니다."""
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8')
    return output.getvalue().encode('utf-8-sig')

def main():
    st.title("🛍️ Qoo10.jp 상품 크롤러")
    st.markdown("Qoo10.jp의 상품 정보를 크롤링하여 CSV 파일로 다운로드할 수 있습니다.")
    
    # 사이드바
    st.sidebar.header("📋 사용법")
    st.sidebar.markdown("""
    1. Qoo10.jp 카테고리 페이지 URL을 입력
    2. '크롤링 시작' 버튼 클릭
    3. 결과를 확인하고 CSV 다운로드
    
    **주의사항:**
    - 광고 상품(PR)은 제외됩니다
    - 너무 빈번한 요청은 피해주세요
    """)
    
    # URL 입력
    url = st.text_input(
        "🔗 Qoo10.jp URL을 입력하세요:",
        placeholder="https://www.qoo10.jp/cat/120000012/220000159?...",
        help="Qoo10.jp의 카테고리 페이지 URL을 입력해주세요."
    )
    
    # 크롤링 버튼
    if st.button("🚀 크롤링 시작", type="primary"):
        if not url:
            st.error("URL을 입력해주세요.")
            return
        
        if 'qoo10.jp' not in url:
            st.error("Qoo10.jp URL을 입력해주세요.")
            return
        
        # 크롤링 실행
        crawler = Qoo10Crawler()
        
        # 진행 상황 표시
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("크롤링 중입니다..."):
            products = crawler.crawl_products(url, progress_bar, status_text)
        
        # 결과 처리
        if products:
            df = pd.DataFrame(products)
            
            st.success(f"✅ 총 {len(products)}개의 상품을 크롤링했습니다!")
            
            # 결과 표시
            st.subheader("📊 크롤링 결과")
            st.dataframe(df, use_container_width=True)
            
            # 통계 정보
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 상품 수", len(products))
            with col2:
                brands = df['브랜드명'].nunique()
                st.metric("브랜드 수", brands)
            with col3:
                avg_reviews = df['리뷰수'].replace('', '0').astype(int).mean()
                st.metric("평균 리뷰 수", f"{avg_reviews:.1f}")
            with col4:
                has_discount = df['정가'].ne('').sum()
                st.metric("할인 상품 수", has_discount)
            
            # CSV 다운로드
            csv_data = convert_df_to_csv(df)
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qoo10_products_{current_time}.csv"
            
            st.download_button(
                label="📥 CSV 파일 다운로드",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                type="primary"
            )
            
        else:
            st.error("❌ 크롤링된 상품이 없습니다. URL을 확인해주세요.")
    
    # 하단 정보
    st.markdown("---")
    st.markdown(
        "ℹ️ 이 도구는 개인적인 용도로만 사용해주세요. "
        "웹사이트의 이용약관을 준수하고 과도한 요청은 피해주세요."
    )

if __name__ == "__main__":
    main()