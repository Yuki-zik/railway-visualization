import geopandas as gpd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# 设置字体以支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决坐标轴负号显示问题

# 读取shapefile文件
shapefile_path = "data/火车站.shp"
gdf = gpd.read_file(shapefile_path)

# 提取城市名字并去掉"市"字
gdf['城市名'] = gdf['火车站'].str.extract(r'(.+?)(?:火车站|站)')[0].str.replace('市', '')

# 您提供的城市列表
selected_cities = [
    "北京", "上海", "广州", "深圳", "成都", "重庆", "杭州", "西安", "武汉", "苏州", "郑州", "南京", "天津", "长沙",
    "东莞", "宁波", "佛山", "合肥", "青岛", "昆明", "沈阳", "济南", "无锡", "厦门", "福州", "温州", "金华", "哈尔滨",
    "大连", "贵阳", "南宁", "泉州", "石家庄", "长春", "南昌", "惠州", "常州", "嘉兴", "徐州", "南通", "太原", "保定",
    "珠海", "中山", "兰州", "临沂", "潍坊", "烟台", "绍兴", "台州", "海口", "乌鲁木齐", "洛阳", "廊坊", "汕头",
    "湖州", "咸阳", "盐城", "济宁", "呼和浩特", "扬州", "赣州", "阜阳", "唐山", "镇江", "邯郸", "银川", "南阳", "桂林",
    "泰州", "遵义", "江门", "揭阳", "芜湖", "商丘", "连云港", "新乡", "淮安", "淄博", "绵阳", "菏泽", "漳州", "周口",
    "沧州", "信阳", "衡阳", "湛江", "三亚", "上饶", "邢台", "莆田", "柳州", "宿迁", "九江", "襄阳", "驻马店", "宜昌",
    "岳阳", "肇庆", "滁州", "威海", "德州", "泰安", "安阳", "荆州", "运城", "安庆", "潮州", "清远", "开封", "宿州",
    "株洲", "蚌埠", "许昌", "宁德", "六安", "宜春", "聊城", "渭南", "宜宾", "鞍山", "南充", "秦皇岛", "亳州", "常德",
    "晋中", "孝感", "丽水", "平顶山", "黄冈", "吉林", "龙岩", "枣庄", "郴州", "日照", "马鞍山", "衢州", "鄂尔多斯",
    "包头", "邵阳", "玉林", "榆林", "西宁", "德阳", "泸州", "临汾", "南平", "焦作", "宣城", "毕节", "淮南", "黔南",
    "滨州", "黔东南", "茂名", "三明", "湘潭", "梅州", "乐山", "黄石", "韶关", "衡水", "怀化", "张家口", "永州", "十堰",
    "曲靖", "大庆", "舟山", "宝鸡", "景德镇", "北海", "娄底", "吉安", "汕尾", "锦州", "咸宁", "大同", "恩施", "营口",
    "长治", "赤峰", "抚州", "漯河", "眉山", "东营", "铜仁", "拉萨", "汉中", "黄山", "阳江", "大理", "盘锦", "达州",
    "吕梁", "承德", "红河", "百色", "丹东", "益阳", "濮阳", "河源", "铜陵", "鄂州", "内江", "梧州", "淮北", "安顺",
    "晋城"
]

# 过滤数据集以仅保留所选城市
filtered_gdf = gdf[gdf['城市名'].isin(selected_cities)]

# 输出过滤后的数据检查
print(filtered_gdf[['城市名', '火车站']])

# 筛选出独特的城市名字及其坐标
unique_cities = filtered_gdf.dropna(subset=['城市名']).drop_duplicates(subset=['城市名'])
city_coords = unique_cities[['WGS84_Lat', 'WGS84_Lng']].values

# 使用最近邻算法找到每个城市的最近邻居
nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(city_coords)
distances, indices = nbrs.kneighbors(city_coords)

# 初始化一个图模型
G_optimized = nx.Graph()

# 添加节点（城市）
for idx, row in unique_cities.iterrows():
    city_name = row["城市名"]
    if pd.notna(city_name):
        G_optimized.add_node(city_name, pos=(row["WGS84_Lng"], row["WGS84_Lat"]))

# 添加边（铁路连接及其距离）
for i, (distance_row, index_row) in enumerate(zip(distances, indices)):
    city1 = unique_cities.iloc[i]["城市名"]
    for j, dist in zip(index_row, distance_row):
        if i != j:
            city2 = unique_cities.iloc[j]["城市名"]
            if pd.notna(city1) and pd.notna(city2):
                G_optimized.add_edge(city1, city2, weight=dist)

# 导出节点数据
nodes = pd.DataFrame({
    "城市名": list(G_optimized.nodes),
    "经度": [G_optimized.nodes[node]['pos'][0] for node in G_optimized.nodes],
    "纬度": [G_optimized.nodes[node]['pos'][1] for node in G_optimized.nodes]
})
nodes.to_csv("nodes.csv", index=False, encoding='utf-8-sig')

# 导出边数据
edges = pd.DataFrame([(u, v, d['weight']) for u, v, d in G_optimized.edges(data=True)],
                     columns=["起点", "终点", "距离"])
edges.to_csv("edges.csv", index=False, encoding='utf-8-sig')

# 显示优化后的城市铁路连接图
pos_optimized = nx.get_node_attributes(G_optimized, 'pos')
weights_optimized = nx.get_edge_attributes(G_optimized, 'weight')

plt.figure(figsize=(20, 15))
nx.draw_networkx_nodes(G_optimized, pos_optimized, node_size=50, node_color="skyblue")
nx.draw_networkx_edges(G_optimized, pos_optimized, alpha=0.3)
nx.draw_networkx_labels(G_optimized, pos_optimized, font_size=8, font_weight="bold")

# 添加边权重标签
edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G_optimized.edges(data=True)}
nx.draw_networkx_edge_labels(G_optimized, pos_optimized, edge_labels=edge_labels, font_size=6)

plt.title("Optimized Railway Connections Between Selected Cities")
plt.show()
