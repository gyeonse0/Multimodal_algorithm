import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

# 인구 데이터를 DataFrame으로 생성
population_data = {
    'district': ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', 
                 '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', 
                 '관악구', '서초구', '강남구', '송파구', '강동구'],
    'population': [72394, 65273, 104187, 133233, 170469, 173903, 188664, 197371, 143075, 138849,
                   218369, 216345, 147312, 181651, 180679, 274010, 184097, 121223, 192064, 187662,
                   286338, 170464, 245046, 287380, 205956]
}
df_population = pd.DataFrame(population_data)

# 인구수를 구별로 매핑
population_dict = dict(zip(df_population['district'], df_population['population']))

# 인구수 기반으로 색상 지정
norm = mcolors.Normalize(vmin=min(df_population['population']), vmax=max(df_population['population']))
colormap = plt.get_cmap('YlGn')  # Yellow to Green colormap

def get_color(population):
    rgba = colormap(norm(population))
    return mcolors.to_hex(rgba)

# GeoJSON 데이터 가공
features = []
for gu_data in gu_json:
    gu_name = gu_data['response']['result']['featureCollection']['features'][0]['properties']['sig_kor_nm']
    geometry = gu_data['response']['result']['featureCollection']['features'][0]['geometry']
    population = population_dict.get(gu_name, 0)
    fill_color = get_color(population)
    
    feature = {
        "type": "Feature",
        "id": gu_name,
        "geometry": geometry,
        "properties": {
            "name": gu_name,
            "population": population,
            "fill": fill_color,
            "fill-opacity": 0.7
        }
    }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# GeoJSON 파일로 저장
with open(r"C:\Users\User\OneDrive\바탕 화면\seoul_population_data.geojson", 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=4)
