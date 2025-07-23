import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from matplotlib import font_manager, rc


def set_korean_font():
    try:
        font_name = font_manager.FontProperties(
            fname="c:/Windows/Fonts/malgun.ttf"
        ).get_name()
        rc("font", family=font_name)
    except FileNotFoundError:
        try:
            rc("font", family="AppleGothic")
        except Exception:
            pass
    plt.rcParams["axes.unicode_minus"] = False


MAP_FILE = "area_map.csv"
STRUCT_FILE = "area_struct.csv"
CATEGORY_FILE = "area_category.csv"

INITIAL_MAP_IMAGE = "map.png"
FINAL_MAP_IMAGE = "map_final.png"
PATH_CSV = "home_to_cafe.csv"


def analyze_and_filter_data():
    try:
        df_map = pd.read_csv(MAP_FILE)
        df_struct = pd.read_csv(STRUCT_FILE)
        df_category = pd.read_csv(CATEGORY_FILE)
    except FileNotFoundError as e:
        print(f"오류: 필수 CSV 파일 '{e.filename}'을(를) 찾을 수 없습니다.")
        return None

    df_map.columns = df_map.columns.str.strip()
    df_struct.columns = df_struct.columns.str.strip()
    df_category.columns = df_category.columns.str.strip()

    df_category.rename(columns={"struct": "name"}, inplace=True)
    df_full_struct = pd.merge(df_struct, df_category, on="category", how="left")
    df_merged = pd.merge(df_full_struct, df_map, on=["x", "y"])
    df_merged.loc[df_merged["ConstructionSite"] == 1, "name"] = "ConstructionSite"
    df_merged["name"] = df_merged["name"].str.strip()

    final_df = df_merged[
        (df_merged["category"] != 0) | (df_merged["ConstructionSite"] == 1)
    ].copy()
    final_df.reset_index(drop=True, inplace=True)
    final_df.rename(columns={"x": "loc_x", "y": "loc_y"}, inplace=True)
    final_df = final_df[["loc_x", "loc_y", "area", "name"]]

    return final_df


def draw_map(data_df, output_filename, title="전체 지도", path_coords=None):
    if data_df is None or data_df.empty:
        print("오류: 시각화할 데이터가 없습니다.")
        return

    styles = {
        "Apartment": {
            "marker": "o",
            "color": "brown",
            "label": "아파트/빌딩"
        },
        "Building": {
            "marker": "o",
            "color": "brown",
            "label": "아파트/빌딩"
        },
        "BandalgomCoffee": {
            "marker": "s",
            "color": "green",
            "label": "반달곰 커피"
        },
        "MyHome": {
            "marker": "^",
            "color": "green",
            "label": "내 집"
        },
        "ConstructionSite": {
            "marker": "s",
            "color": "gray",
            "label": "건설현장",
            "s": 250
        },
    }

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(title, fontsize=18, pad=20)
    ax.set_xlabel("X 좌표", fontsize=12)
    ax.set_ylabel("Y 좌표", fontsize=12)

    max_x = data_df["loc_x"].max() + 2
    max_y = data_df["loc_y"].max() + 2
    ax.set_xlim(0.5, max_x - 0.5)
    ax.set_ylim(max_y - 0.5, 0.5)
    ax.set_xticks(range(1, max_x))
    ax.set_yticks(range(1, max_y))
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_aspect("equal")

    for name, style in styles.items():
        subset = data_df[data_df["name"] == name]
        if not subset.empty:
            ax.scatter(
                subset["loc_x"],
                subset["loc_y"],
                marker=style["marker"],
                color=style["color"],
                s=style.get("s", 150),
                label=style["label"],
                zorder=5
            )

    if path_coords:
        path_x, path_y = zip(*path_coords)
        ax.plot(
            path_x,
            path_y,
            color="red",
            linewidth=3,
            linestyle="-",
            marker="o",
            markersize=5,
            zorder=10,
            label="최단 경로"
        )

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), title="범례")

    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"'{output_filename}' 파일 저장 완료.")


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
            if (
                1 <= next_pos[0] < max_x
                and 1 <= next_pos[1] < max_y
                and next_pos not in obstacles
                and next_pos not in visited
            ):
                new_path = list(path)
                new_path.append(next_pos)
                queue.append(new_path)
                visited.add(next_pos)
    return None


def find_and_save_shortest_path(all_data_df):
    if all_data_df is None or all_data_df.empty:
        print("오류: 경로 탐색을 위한 데이터가 없습니다.")
        return

    start_nodes = all_data_df[all_data_df["name"] == "MyHome"]
    end_nodes = all_data_df[all_data_df["name"] == "BandalgomCoffee"]
    obstacles = set(
        tuple(x)
        for x in all_data_df[
            all_data_df["name"] == "ConstructionSite"
        ][["loc_x", "loc_y"]].to_numpy()
    )

    if start_nodes.empty or end_nodes.empty:
        print("오류: 시작점 또는 도착점을 찾을 수 없습니다.")
        return

    start_pos = (start_nodes.iloc[0]["loc_x"], start_nodes.iloc[0]["loc_y"])
    end_pos = (end_nodes.iloc[0]["loc_x"], end_nodes.iloc[0]["loc_y"])
    grid_size = (
        all_data_df["loc_x"].max() + 2,
        all_data_df["loc_y"].max() + 2
    )

    path = bfs_shortest_path(grid_size, obstacles, start_pos, end_pos)

    if not path:
        print("경고: 경로를 찾지 못했습니다.")
        return

    path_df = pd.DataFrame(path, columns=["loc_x", "loc_y"])
    path_df.to_csv(PATH_CSV, index=False)
    draw_map(all_data_df, FINAL_MAP_IMAGE, title="전체 지도 및 최단 경로", path_coords=path)


if __name__ == "__main__":
    set_korean_font()
    all_struct_data = analyze_and_filter_data()

    if all_struct_data is not None and not all_struct_data.empty:
        draw_map(all_struct_data, INITIAL_MAP_IMAGE, title="전체 초기 지도")
        find_and_save_shortest_path(all_struct_data)
        print("모든 작업 완료.")
    elif all_struct_data is not None and all_struct_data.empty:
        print("구조물 데이터가 없습니다.")
    else:
        print("데이터 분석 오류로 작업 중단.")
