import folium
import pandas as pd
import numpy as np
from folium import plugins
from shapely.geometry import Polygon, Point

# 폴리곤 좌표 정의 (운동장 범위)
polygon_coords = [
    [37.611353, 126.995943],  # 첫 번째 점 (위도, 경도)
    [37.610878, 126.995501],  # 두 번째 점 (위도, 경도)
    [37.610369, 126.996375],  # 세 번째 점 (위도, 경도)
    [37.610843, 126.996811]   # 네 번째 점 (위도, 경도)
]

# Shapely 폴리곤 생성
polygon = Polygon(polygon_coords)

# 지도 생성 (운동장 중심 좌표)
center = [37.610854, 126.996131]
m = folium.Map(location=center, zoom_start=20)

# 운동장 범위 내에서 임의의 좌표 데이터 생성
np.random.seed(0)
num_points = 20000

lat_min, lat_max = min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords)
lon_min, lon_max = min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords)

latitudes = []
longitudes = []

# 네 꼭짓점 추가
for coord in polygon_coords:
    latitudes.append(coord[0])
    longitudes.append(coord[1])

# 클러스터 기반으로 데이터 생성
num_clusters = 30

# 모서리에 클러스터 추가
corners = polygon_coords
for corner in corners:
    cluster_center_lat = corner[0]
    cluster_center_lon = corner[1]
    num_points_in_cluster = np.random.randint(500, 700)
    for _ in range(num_points_in_cluster):
        lat = np.random.normal(cluster_center_lat, 0.00005)
        lon = np.random.normal(cluster_center_lon, 0.00005)
        point = Point(lat, lon)
        if polygon.contains(point):
            latitudes.append(lat)
            longitudes.append(lon)

# 중앙에 클러스터 추가
center_clusters = [(37.6111, 126.996), (37.6107, 126.9965)]
for cluster_center in center_clusters:
    cluster_center_lat = cluster_center[0]
    cluster_center_lon = cluster_center[1]
    num_points_in_cluster = np.random.randint(1000, 1500)
    for _ in range(num_points_in_cluster):
        lat = np.random.normal(cluster_center_lat, 0.0001)
        lon = np.random.normal(cluster_center_lon, 0.0001)
        point = Point(lat, lon)
        if polygon.contains(point):
            latitudes.append(lat)
            longitudes.append(lon)

# 기타 클러스터 추가
for _ in range(num_clusters - len(corners) - len(center_clusters)):
    cluster_center_lat = np.random.uniform(lat_min, lat_max)
    cluster_center_lon = np.random.uniform(lon_min, lon_max)
    num_points_in_cluster = np.random.randint(300, 600)
    for _ in range(num_points_in_cluster):
        lat = np.random.normal(cluster_center_lat, 0.0001)
        lon = np.random.normal(cluster_center_lon, 0.0001)
        point = Point(lat, lon)
        if polygon.contains(point):
            latitudes.append(lat)
            longitudes.append(lon)

location_data = pd.DataFrame({'LAT': latitudes, 'LON': longitudes})

# 히트맵 추가
heat_data = [[row['LAT'], row['LON']] for index, row in location_data.iterrows()]

# 사용자 정의 그라데이션 설정
gradient = {
    0.2: 'blue',
    0.4: 'lime',
    0.6: 'yellow',
    0.8: 'orange',
    1.0: 'red'
}

plugins.HeatMap(heat_data, gradient=gradient, radius=15, max_zoom=20).add_to(m)

# 네 꼭짓점에 마커 추가
for coord in polygon_coords:
    folium.Marker(location=coord).add_to(m)

# 지도 시각화
m.save('knu_heatmap.html')

# Jupyter Notebook에서 결과를 확인하려면 다음 코드를 실행
m
m.save('map1.html')