import folium
import random
import matplotlib.colors as mcolors
from shapely.geometry import Polygon, Point

    # 지도 생성
m = folium.Map(location=[37.610854, 126.996131], zoom_start=30)

    # 폴리곤 좌표 정의
polygon_coords = [
        [37.611353, 126.995943],  # 첫 번째 점 (위도, 경도)
        [37.610878, 126.995501],  # 두 번째 점 (위도, 경도)
        [37.610369, 126.996375],  # 세 번째 점 (위도, 경도)
        [37.610843, 126.996811]   # 네 번째 점 (위도, 경도)
    ]

    # Shapely 폴리곤 생성
polygon = Polygon(polygon_coords)

    # 폴리곤 추가
folium.Polygon(
        locations=polygon_coords,
        color='blue',       # 외곽선 색상
    ).add_to(m)

    # 폴리곤 내의 영역을 20x15으로 나누기 위한 범위 설정
lat_min, lat_max = min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords)
lon_min, lon_max = min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords)

lat_step = (lat_max - lat_min) / 20
lon_step = (lon_max - lon_min) / 15

    # 파란색 계열의 색상 리스트 (회색 제거)
blue_colors = [
        '#B0C4DE', '#6495ED', '#4169E1'
    ]

    # 색상 그라데이션을 위한 함수
def get_average_color(colors):
        rgb_colors = [mcolors.hex2color(c) for c in colors]
        avg_rgb = [sum(x)/len(x) for x in zip(*rgb_colors)]
        return mcolors.to_hex(avg_rgb)

    # 작은 사각형들의 색상을 저장할 딕셔너리
rectangle_colors = {}

    # 폴리곤 내의 작은 사각형들 추가
for i in range(20):
        for j in range(15):
            lat_start = lat_min + i * lat_step
            lat_end = lat_start + lat_step
            lon_start = lon_min + j * lon_step
            lon_end = lon_start + lon_step

            # 사각형의 중심점이 폴리곤 내에 있는지 확인
            center_point = Point((lat_start + lat_end) / 2, (lon_start + lon_end) / 2)
            if polygon.contains(center_point):
                rectangle_coords = [
                    [lat_start, lon_start],
                    [lat_start, lon_end],
                    [lat_end, lon_end],
                    [lat_end, lon_start]
                ]

                # 주위의 색상 찾기
                surrounding_colors = []
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = (i + x, j + y)
                    if neighbor in rectangle_colors:
                        surrounding_colors.append(rectangle_colors[neighbor])
                if surrounding_colors:
                    color = get_average_color(surrounding_colors)
                else:
                    color = random.choice(blue_colors)

                rectangle_colors[(i, j)] = color

                folium.Polygon(
                    locations=rectangle_coords,
                    color=color,      # 외곽선 색상
                    fill=True,               # 내부 채움 여부
                    fill_color=color, # 내부 채움 색상
                    fill_opacity=1.0         # 내부 채움 투명도
                ).add_to(m)

    # 지도 시각화
m.save('map2.html')
m