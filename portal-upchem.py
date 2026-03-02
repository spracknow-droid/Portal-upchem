import streamlit as st
import yaml

# 페이지 설정
st.set_page_config(
    page_title="Finance Team App Portal",
    page_icon="📊",
    layout="wide",
)

# --- 스타일 설정 (카드 높이 균형을 위한 간단한 CSS) ---
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:contains("바로가기") {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 포털 페이지 제목 및 부제 ---
st.title("📊 Finance Team App Portal")
st.markdown("회사 실무에 유용한 App을 한눈에 확인하고, 필요한 페이지에 빠르게 접근하세요.")

# --- YAML 파일에서 앱 목록 불러오기 ---
def load_apps_from_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            apps_data = yaml.safe_load(f)
        return apps_data['apps']
    except FileNotFoundError:
        st.error("앱 목록을 담은 'apps.yaml' 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        st.error(f"YAML 파일을 읽는 중 오류가 발생했습니다: {e}")
        return []

apps = load_apps_from_yaml('apps.yaml')

# --- 앱 목록 영역 ---
if apps:
    # 1. 카테고리 추출 및 '전체' 추가
    # category 키가 없는 경우를 대비해 .get() 사용
    unique_categories = sorted(list(set(app.get('category', '기타') for app in apps)))
    categories = ["전체"] + unique_categories

    # 2. 탭 생성
    tabs = st.tabs(categories)

    # 3. 각 탭별로 콘텐츠 구성
    for idx, tab in enumerate(tabs):
        with tab:
            current_category = categories[idx]
            
            # 필터링 로직
            if current_category == "전체":
                display_apps = apps
            else:
                display_apps = [app for app in apps if app.get('category', '기타') == current_category]
            
            # 컬럼 레이아웃 설정 (한 줄에 3개씩)
            num_columns = 3
            cols = st.columns(num_columns)

            for i, app in enumerate(display_apps):
                with cols[i % num_columns]:
                    # 카드 디자인 (컨테이너 사용)
                    with st.container(border=True):
                        # 전체 탭일 때만 카테고리 뱃지 표시
                        if current_category == "전체":
                            st.caption(f"📁 {app.get('category', '기타')}")
                        
                        st.subheader(app['name'])
                        
                        # 설명 부분 (최소 높이를 주어 카드 크기를 일정하게 유지)
                        st.markdown(f"""
                            <div style="min-height: 60px;">
                                <p style="color: #888; font-size: 14px; line-height: 1.5;">
                                    {app['description']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.divider() # 구분선
                        
                        # 버튼을 컨테이너 너비에 맞춤
                        st.link_button(f"링크 바로가기", app['url'], use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <p style='text-align: center; color: #888;'>
    문의사항은 박성규 과장에게 연락 바랍니다.
    </p>
    """,
    unsafe_allow_html=True
)
