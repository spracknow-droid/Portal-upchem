import streamlit as st
import yaml

# 페이지 설정
st.set_page_config(
    page_title="Finance Team App Portal",
    page_icon="📊",
    layout="wide",
)

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

# --- 앱 목록을 카드 형태로 표시 ---
st.header("앱 목록")

# 컬럼 레이아웃 설정 (한 줄에 3개씩 표시)
num_columns = 3
columns = st.columns(num_columns)

for i, app in enumerate(apps):
    # 현재 앱이 위치할 컬럼 선택
    with columns[i % num_columns]:
        # 카드 디자인 (컨테이너 사용)
        with st.container(border=True):
            st.subheader(app['name'])
            st.markdown(f"<p style='color: #888; font-size: 14px;'>{app['description']}</p>", unsafe_allow_html=True)
            st.markdown("---")  # 구분선
            st.link_button("링크 바로가기", app['url'])

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
