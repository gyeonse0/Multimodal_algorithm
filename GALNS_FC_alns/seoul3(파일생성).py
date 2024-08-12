import pandas as pd
import requests
import folium
import json
from shapely.geometry import Polygon, Point
import random

# 랜덤 포인트 수
a = 63

# 서울 구 데이터 가져오기
API_key = '5357464a61716b7236306b6a746b45'
service = 'SearchFAQOfGUListService'
gu_url = f'http://openapi.seoul.go.kr:8088/{API_key}/json/{service}/1/25'
gu_list = requests.get(gu_url).json()
df_gu = pd.DataFrame(gu_list['SearchFAQOfGUListService']['row'])

# GeoJSON 데이터 가져오기
gu_json = []
vworld_key = '3C36C01F-FC3D-302C-BEB6-E697864F7DF3'
for gu in df_gu['CD_DESC']:
    url_vworld = f'https://api.vworld.kr/req/data?service=data&version=2.0&request=GetFeature&format=json&errorformat=json&size=10&page=1&data=LT_C_ADSIGG_INFO&attrfilter=sig_kor_nm:like:{gu}&columns=sig_cd,full_nm,sig_kor_nm,sig_eng_nm,ag_geom&geometry=true&attribute=true&key={vworld_key}&domain=https://localhost'
    result_dict = requests.get(url_vworld).json()
    gu_json.append(result_dict)

# GeoJSON 데이터 가공
features = []
for gu_data in gu_json:
    gu_name = gu_data['response']['result']['featureCollection']['features'][0]['properties']['sig_kor_nm']
    geometry = gu_data['response']['result']['featureCollection']['features'][0]['geometry']
    feature = {
        "type": "Feature",
        "id": gu_name,
        "geometry": geometry,
        "properties": {
            "name": gu_name
        }
    }
    features.append(feature)


geojson_data = {
   "type": "FeatureCollection",
   "features": features
}

# 랜덤 포인트 생성 함수
def generate_random_points(polygon, num_points):
    points = []
    while len(points) < num_points:
        lon = random.uniform(polygon.bounds[0], polygon.bounds[2])
        lat = random.uniform(polygon.bounds[1], polygon.bounds[3])
        point = Point(lon, lat)
        
        if polygon.contains(point):
            points.append((lat, lon))
    return points

# 강남구의 랜덤 포인트 생성
def generate_gangnam_points():
    gangnam_points = []
    for feature in features:
        if feature['id'] == '강남구':  # 강남구의 id를 확인
            coords = feature['geometry']['coordinates']
            
            if feature['geometry']['type'] == 'Polygon':
                polygon = Polygon(coords[0])
                gangnam_points = generate_random_points(polygon, a)  # 'a'만큼 포인트 생성
            
            elif feature['geometry']['type'] == 'MultiPolygon':
                for coord in coords:
                    polygon = Polygon(coord[0])
                    gangnam_points.extend(generate_random_points(polygon, a))
                    break
    
    return gangnam_points

# 강남구 포인트 생성
random_points = generate_gangnam_points()

# 서울 중심에 Folium 맵 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# GeoJSON 레이어 추가
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'opacity': 0.7,
        'weight': 1,
        'color': 'white',
        'fillOpacity': 0.2,
        'dashArray': '5, 5',
    }
).add_to(m)

# 랜덤 포인트를 Marker로 추가
for point in random_points:
    folium.Marker(
        location=point,
        icon=folium.Icon(icon='circle', color='red', icon_size=(1,1))
    ).add_to(m)

# HTML 파일로 저장
m.save('C:/Users/User/OneDrive/바탕 화면/seoul_gangnam_random_points_map.html')

# 포인트를 포함한 GeoJSON 데이터 생성
points_features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "properties": {
            "marker-color": "#ff0000",  # 빨간색
            "marker-symbol": "circle"   # 원형 마커
        }
    } for lat, lon in random_points
]

# 기존 features에 points_features 추가
combined_features = features + points_features

combined_geojson_data = {
    "type": "FeatureCollection",
    "features": combined_features
}

# 포인트가 포함된 GeoJSON 파일로 저장
points_file_path = 'C:/Users/User/OneDrive/바탕 화면/gangnam_with_random_points.geojson'
with open(points_file_path, 'w', encoding='utf-8') as f:
    json.dump(combined_geojson_data, f, ensure_ascii=False, indent=4)
