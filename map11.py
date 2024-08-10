import pandas as pd
import mysql.connector
import folium
from folium import plugins

# 데이터베이스 연결 매개변수
host = "10.60.2.104"
user = "root"
password = "Dmstn0709!"
database = "test"

# 데이터베이스 연결
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# drive1_table에서 데이터 가져오기
query = "SELECT Rsrp, Latitude, Longitude FROM drive1_table"
df = pd.read_sql(query, conn)

# 데이터베이스 연결 종료
conn.close()

# 데이터 확인
print(df.head())

# 데이터 타입 변환
df['Rsrp'] = pd.to_numeric(df['Rsrp'])
df['Latitude'] = pd.to_numeric(df['Latitude'])
df['Longitude'] = pd.to_numeric(df['Longitude'])

# 히트맵을 위해 RSRP 값을 정규화
df['RSRP_norm'] = (df['Rsrp'] - df['Rsrp'].min()) / (df['Rsrp'].max() - df['Rsrp'].min())

# 지도 생성
center_lat = df['Latitude'].mean()
center_lon = df['Longitude'].mean()
print(f"Map center: Latitude {center_lat}, Longitude {center_lon}")

m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# 히트맵 데이터 준비
heat_data = [[row['Latitude'], row['Longitude'], row['RSRP_norm']] for index, row in df.iterrows()]
print(f"Heatmap data sample: {heat_data[:5]}")

# 히트맵 추가
plugins.HeatMap(heat_data, radius=15, max_zoom=20, gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1.0: 'red'}).add_to(m)

# 지도 HTML 파일로 저장
m.save('map111.html')

# 지도 Jupyter Notebook에서 시각화
m
