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

INITIAL_MAP_IMAGE = 'map.png' # 모든 area를 포함하는 초기 맵 파일명 변경
FINAL_MAP_IMAGE = 'map_final.png' # 모든 area를 포함하는 최종 맵 파일명 변경
PATH_CSV = 'home_to_cafe.csv' # 모든 area를 포함하는 경로 CSV 파일명 변경


# ==============================================================================
# 📂 1단계: 데이터 수집 및 분석 (수정된 로직)
# ==============================================================================

def analyze_and_filter_data():
    """
    실제 CSV 파일 구조에 맞게 데이터를 병합하고 모든 area 데이터를 필터링합니다.
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

    # name 열의 공백을 제거합니다.
    df_merged['name'] = df_merged['name'].str.strip()

    # 4. 실제 구조물(category != 0)과 건설 현장만 필터링합니다. (모든 area 포함)
    final_df = df_merged[(df_merged['category'] != 0) | (df_merged['ConstructionSite'] == 1)].copy().reset_index(drop=True)

    # 5. 프로젝트의 다른 코드와 호환되도록 열 이름을 변경합니다.
    final_df.rename(columns={'x': 'loc_x', 'y': 'loc_y'}, inplace=True)
    
    # 6. 필요한 열만 선택합니다. (이제 area 1으로 필터링하지 않습니다)
    final_df = final_df[['loc_x', 'loc_y', 'area', 'name']]

    print("모든 Area 데이터 필터링 완료.")
    print(final_df.head()) # 모든 area 포함된 데이터 확인
    
    # (보너스) 구조물 종류별 요약 통계
    print("\n--- [보너스] 구조물 종류별 요약 통계 (전체 Area) ---")
    summary = final_df.groupby(['area', 'name'])[['loc_x', 'loc_y']].describe()
    print(summary)
    print("-" * 30)

    return final_df # 모든 area 데이터 반환

# ==============================================================================
# 🗺️ 2단계: 지도 시각화 (모든 area를 포함하도록 수정)
# ==============================================================================

def draw_map(data_df, output_filename, title='전체 지도', path_coords=None): # 제목 변경
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

    # 모든 area 데이터 기준으로 최대 x, y를 설정
    max_x = data_df['loc_x'].max() + 2
    max_y = data_df['loc_y'].max() + 2
    ax.set_xlim(0.5, max_x - 0.5)
    ax.set_ylim(max_y - 0.5, 0.5)
    ax.set_xticks(range(1, max_x))
    ax.set_yticks(range(1, max_y))
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_aspect('equal')

    # 모든 area의 구조물을 그립니다.
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
# 🚶 3단계: 최단 경로 탐색 (모든 area를 고려하도록 수정)
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

def find_and_save_shortest_path(all_data_df): # 모든 area 데이터를 받도록 변경
    print("--- 3단계: 최단 경로 탐색 시작 ---")
    if all_data_df is None or all_data_df.empty:
        print("오류: 경로 탐색을 위한 데이터가 없습니다.")
        return

    # 이제 area 필터링 없이 'MyHome'과 'BandalgomCoffee'를 찾습니다.
    # 여러 개가 있을 경우 첫 번째 것을 사용합니다.
    start_nodes = all_data_df[all_data_df['name'] == 'MyHome']
    end_nodes = all_data_df[all_data_df['name'] == 'BandalgomCoffee']
    
    # 장애물은 모든 area의 ConstructionSite를 포함합니다.
    obstacles = set(tuple(x) for x in all_data_df[all_data_df['name'] == 'ConstructionSite'][['loc_x', 'loc_y']].to_numpy())

    if start_nodes.empty or end_nodes.empty:
        print("오류: 'MyHome' 또는 'BandalgomCoffee' 위치를 데이터에서 찾을 수 없습니다.")
        # 디버깅을 위해 현재 데이터에 어떤 구조물이 있는지 출력
        print("찾은 'MyHome' 노드:\n", start_nodes)
        print("찾은 'BandalgomCoffee' 노드:\n", end_nodes)
        return

    # 첫 번째 'MyHome'과 'BandalgomCoffee'를 시작/종료 지점으로 사용
    start_pos = (start_nodes.iloc[0]['loc_x'], start_nodes.iloc[0]['loc_y'])
    end_pos = (end_nodes.iloc[0]['loc_x'], end_nodes.iloc[0]['loc_y'])
    
    # 그리드 크기는 모든 데이터의 최대 x, y 값을 기준으로 설정합니다.
    grid_size = (all_data_df['loc_x'].max() + 2, all_data_df['loc_y'].max() + 2)

    print(f"시작 위치 (MyHome): {start_pos}")
    print(f"도착 위치 (BandalgomCoffee): {end_pos}")
    print(f"건설 현장 (장애물 수): {len(obstacles)}개")
    print(f"그리드 크기: {grid_size[0]-1}x{grid_size[1]-1}")

    path = bfs_shortest_path(grid_size, obstacles, start_pos, end_pos)

    if not path:
        print("경고: 'MyHome'에서 'BandalgomCoffee'까지의 경로를 찾지 못했습니다.")
        return

    path_df = pd.DataFrame(path, columns=['loc_x', 'loc_y'])
    path_df.to_csv(PATH_CSV, index=False)
    print(f"✔️ '{PATH_CSV}' 파일 저장 완료.")

    # 경로 시각화 시에도 모든 area 데이터를 기반으로 지도에 그립니다.
    draw_map(all_data_df, FINAL_MAP_IMAGE, title='전체 지도 및 최단 경로', path_coords=path)

# ==============================================================================
# 🚀 메인 실행 로직
# ==============================================================================

if __name__ == '__main__':
    set_korean_font()
    # analyze_and_filter_data는 이제 모든 area 데이터를 반환합니다.
    all_struct_data = analyze_and_filter_data() 
    
    if all_struct_data is not None and not all_struct_data.empty:
        # 초기 맵은 모든 area에 대한 데이터를 사용하여 그립니다.
        draw_map(all_struct_data, INITIAL_MAP_IMAGE, title='전체 초기 지도') 
        # find_and_save_shortest_path는 이제 전체 데이터를 받아 그 안에서 경로를 찾습니다.
        find_and_save_shortest_path(all_struct_data)
        print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
    elif all_struct_data is not None and all_struct_data.empty:
        print("\n분석 결과 구조물 데이터가 없습니다.")
    else:
        print("\n데이터 분석 단계에서 오류가 발생하여 작업을 중단합니다.")