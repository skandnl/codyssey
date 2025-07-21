# team.py

import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from matplotlib import font_manager, rc

# ==============================================================================
# 📝 설정: 한글 폰트 및 파일 경로
# ==============================================================================

def set_korean_font():
    """운영체제에 맞는 한글 폰트를 설정합니다."""
    try:
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    except FileNotFoundError:
        try:
            rc('font', family='AppleGothic')
        except:
            print("한글 폰트를 찾을 수 없어 기본 폰트로 설정됩니다.")
            pass
    plt.rcParams['axes.unicode_minus'] = False

MAP_FILE = 'area_map.csv'
STRUCT_FILE = 'area_struct.csv'
CATEGORY_FILE = 'area_category.csv'

INITIAL_MAP_IMAGE = 'map.png'
FINAL_MAP_IMAGE = 'map_final.png'
PATH_CSV = 'home_to_cafe.csv'


# ==============================================================================
# 📂 1단계: 데이터 수집 및 분석 (수정된 로직)
# ==============================================================================

def analyze_and_filter_data():
    """
    실제 CSV 파일 구조에 맞게 데이터를 병합하고 area 1에 대한 데이터를 필터링합니다.
    """
    print("--- 1단계: 데이터 분석 시작 ---")
    try:
        df_map = pd.read_csv(MAP_FILE)
        df_struct = pd.read_csv(STRUCT_FILE)
        df_category = pd.read_csv(CATEGORY_FILE)
    except FileNotFoundError as e:
        print(f"오류: 필수 CSV 파일 '{e.filename}'을(를) 찾을 수 없습니다.")
        return None

    # 열 이름의 공백 제거
    df_map.columns = df_map.columns.str.strip()
    df_struct.columns = df_struct.columns.str.strip()
    df_category.columns = df_category.columns.str.strip()

    # 1. 구조물 정보(df_struct)와 카테고리 이름(df_category)을 병합합니다.
    df_category.rename(columns={'struct': 'name'}, inplace=True)
    df_full_struct = pd.merge(df_struct, df_category, on='category', how='left')

    # 2. 위 결과와 지도 정보(df_map)를 좌표(x, y) 기준으로 병합합니다.
    df_merged = pd.merge(df_full_struct, df_map, on=['x', 'y'])

    # 3. 최종 구조물 이름을 결정합니다. (건설 현장 우선)
    # ConstructionSite가 1이면 이름을 'ConstructionSite'로 강제 설정합니다.
    df_merged.loc[df_merged['ConstructionSite'] == 1, 'name'] = 'ConstructionSite'

    # 여기서 name 열의 공백을 제거합니다.
    df_merged['name'] = df_merged['name'].str.strip()

    # 4. 실제 구조물(category != 0)과 건설 현장만 필터링합니다.
    final_df = df_merged[(df_merged['category'] != 0) | (df_merged['ConstructionSite'] == 1)].copy()

    # 5. 프로젝트의 다른 코드와 호환되도록 열 이름을 변경합니다.
    final_df.rename(columns={'x': 'loc_x', 'y': 'loc_y'}, inplace=True)
    
    # 6. 필요한 열만 선택하고 area 1 데이터만 필터링합니다.
    final_df = final_df[['loc_x', 'loc_y', 'area', 'name']]
    area1_df = final_df[final_df['area'] == 1].copy().reset_index(drop=True)

    print("Area 1 데이터 필터링 완료.")
    print(area1_df)

    # (보너스) 구조물 종류별 요약 통계
    print("\n--- [보너스] 구조물 종류별 요약 통계 (Area 1) ---")
    summary = area1_df.groupby('name')[['loc_x', 'loc_y']].describe()
    print(summary)
    print("-" * 30)

    return area1_df

# ==============================================================================
# 🗺️ 2단계: 지도 시각화 (기존 코드와 동일)
# ==============================================================================

def draw_map(data_df, output_filename, title='Area 1 지도', path_coords=None):
    print(f"--- 지도 시각화 시작 ({output_filename}) ---")
    if data_df is None or data_df.empty:
        print('오류: 시각화할 데이터가 없습니다.')
        return

    styles = {
        'Apartment': {'marker': 'o', 'color': 'brown', 'label': '아파트/빌딩'},
        'Building': {'marker': 'o', 'color': 'brown', 'label': '아파트/빌딩'},
        'BandalgomCoffee': {'marker': 's', 'color': 'green', 'label': '반달곰 커피'},
        'MyHome': {'marker': '^', 'color': 'green', 'label': '내 집'},
        'ConstructionSite': {'marker': 's', 'color': 'gray', 'label': '건설현장', 's': 250}
    }

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(title, fontsize=18, pad=20)
    ax.set_xlabel('X 좌표', fontsize=12)
    ax.set_ylabel('Y 좌표', fontsize=12)

    max_x = data_df['loc_x'].max() + 2
    max_y = data_df['loc_y'].max() + 2
    ax.set_xlim(0.5, max_x - 0.5)
    ax.set_ylim(max_y - 0.5, 0.5)
    ax.set_xticks(range(1, max_x))
    ax.set_yticks(range(1, max_y))
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_aspect('equal')

    for name, style in styles.items():
        subset = data_df[data_df['name'] == name]
        if not subset.empty:
            ax.scatter(subset['loc_x'], subset['loc_y'],
                       marker=style['marker'], color=style['color'],
                       s=style.get('s', 150), label=style['label'], zorder=5)

    if path_coords:
        path_x, path_y = zip(*path_coords)
        ax.plot(path_x, path_y, color='red', linewidth=3, linestyle='-',
                marker='o', markersize=5, zorder=10, label='최단 경로')

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title='범례')
    
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✔️ '{output_filename}' 파일 저장 완료.")
    print("-" * 30)

# ==============================================================================
# 🚶 3단계: 최단 경로 탐색 (기존 코드와 동일)
# ==============================================================================

def bfs_shortest_path(grid_size, obstacles, start, end):
    queue = deque([[start]])
    visited = {start}
    max_x, max_y = grid_size

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for move_x, move_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (x + move_x, y + move_y)
            if (1 <= next_pos[0] < max_x and 1 <= next_pos[1] < max_y and
                    next_pos not in obstacles and next_pos not in visited):
                new_path = list(path)
                new_path.append(next_pos)
                queue.append(new_path)
                visited.add(next_pos)
    return None

def find_and_save_shortest_path(data_df):
    print("--- 3단계: 최단 경로 탐색 시작 ---")
    if data_df is None:
        return

    start_node = data_df[data_df['name'] == 'MyHome']
    end_node = data_df[data_df['name'] == 'BandalgomCoffee']
    obstacles = set(tuple(x) for x in data_df[data_df['name'] == 'ConstructionSite'][['loc_x', 'loc_y']].to_numpy())

    if start_node.empty or end_node.empty:
        print("오류: 'MyHome' 또는 'BandalgomCoffee' 위치를 데이터에서 찾을 수 없습니다.")
        # 디버깅을 위해 이 부분에 추가
        print("start_node 내용:\n", start_node)
        print("end_node 내용:\n", end_node)
        return

    start_pos = (start_node.iloc[0]['loc_x'], start_node.iloc[0]['loc_y'])
    end_pos = (end_node.iloc[0]['loc_x'], end_node.iloc[0]['loc_y'])
    grid_size = (data_df['loc_x'].max() + 2, data_df['loc_y'].max() + 2)

    path = bfs_shortest_path(grid_size, obstacles, start_pos, end_pos)

    if not path:
        print("경고: 'MyHome'에서 'BandalgomCoffee'까지의 경로를 찾지 못했습니다.")
        return

    path_df = pd.DataFrame(path, columns=['loc_x', 'loc_y'])
    path_df.to_csv(PATH_CSV, index=False)
    print(f"✔️ '{PATH_CSV}' 파일 저장 완료.")

    draw_map(data_df, FINAL_MAP_IMAGE, title='Area 1 지도 및 최단 경로', path_coords=path)

# ==============================================================================
# 🚀 메인 실행 로직
# ==============================================================================

if __name__ == '__main__':
    set_korean_font()
    area1_data = analyze_and_filter_data()
    
    if area1_data is not None and not area1_data.empty:
        draw_map(area1_data, INITIAL_MAP_IMAGE)
        find_and_save_shortest_path(area1_data)
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
    elif area1_data is not None and area1_data.empty:
        print("\n분석 결과 Area 1에 해당하는 구조물 데이터가 없습니다.")
    else:
        print("\n데이터 분석 단계에서 오류가 발생하여 작업을 중단합니다.")