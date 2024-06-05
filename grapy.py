import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import networkx as nx
import dash_leaflet as dl
import dash_leaflet.express as dlx
from astar import AStar

# 读取节点和边数据
nodes_df = pd.read_csv("nodes.csv", encoding="utf-8-sig")
edges_df = pd.read_csv("edges.csv", encoding="utf-8-sig")

# 初始化图模型
G = nx.Graph()

# 添加节点
for _, row in nodes_df.iterrows():
    G.add_node(row["城市名"], pos=(row["经度"], row["纬度"]))

# 添加边
for _, row in edges_df.iterrows():
    G.add_edge(row["起点"], row["终点"], weight=row["距离"])

# 获取节点的坐标字典
cities = {row["城市名"]: (row["纬度"], row["经度"]) for _, row in nodes_df.iterrows()}

# 初始化AStar实例
astar = AStar(G, cities)

# 创建Dash应用
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="城市铁路可视化"
)

# 定义应用布局
app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            brand="城市间铁路连接及A*路径可视化",
            brand_href="#",
            color="primary",
            dark=True,
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H5("选择起点和终点", className="card-title"),
                                        dbc.Label("起点:"),
                                        dcc.Dropdown(
                                            id="start-city",
                                            options=[
                                                {"label": city, "value": city}
                                                for city in cities.keys()
                                            ],
                                            value="宁波",
                                        ),
                                        html.Br(),
                                        dbc.Label("终点:"),
                                        dcc.Dropdown(
                                            id="goal-city",
                                            options=[
                                                {"label": city, "value": city}
                                                for city in cities.keys()
                                            ],
                                            value="三亚",
                                        ),
                                        html.Br(),
                                    ]
                                )
                            ],
                            className="mb-4",
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    html.Div(
                                        id="path-info",
                                        style={"whiteSpace": "pre-line"},
                                    )
                                )
                            ],
                            className="mb-4",
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        dl.Map(
                            center=[35.8617, 104.1954],
                            zoom=4,
                            children=[
                                dl.TileLayer(
                                    url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                                ),
                                dl.LayerGroup(id="layer"),
                            ],
                            style={
                                'width': '100%',
                                'height': '600px',
                                'margin': "auto",
                                "display": "block",
                            },
                        ),
                    ],
                    md=8,
                ),
            ]
        ),
    ],
    fluid=True,
)

# 定义回调函数以更新图形和路径信息
@app.callback(
    [Output("layer", "children"), Output("path-info", "children")],
    [Input("start-city", "value"), Input("goal-city", "value")],
)
def update_graph(start_city, goal_city):
    # 使用A*算法搜索最短路径
    path, cost = astar.search(start_city, goal_city)

    # 创建路径的图形数据
    path_coords = [[cities[city][0], cities[city][1]] for city in path]

    # 创建节点的图形数据
    node_markers = [
        dl.Marker(position=[lat, lon], children=dl.Tooltip(city))
        for city, (lat, lon) in cities.items()
    ]

    # 创建路径的折线图形数据
    path_polyline = dl.Polyline(positions=path_coords, color="red")

    # 添加所有的边
    edge_lines = [
        dl.Polyline(
            positions=[[cities[edge[0]][0], cities[edge[0]][1]], [cities[edge[1]][0], cities[edge[1]][1]]],
            color="black",
            opacity=0.5,
            weight=1,
        )
        for edge in G.edges()
    ]

    # 将节点和路径添加到图层中
    layer = node_markers + edge_lines + [path_polyline]

    # 更新路径信息
    path_info = [
        html.H5(f"从{start_city}到{goal_city}的最短路径为："),
        html.Div(" → ".join(path)),
        html.Br(),
        html.H5(f"旅行用时：{cost:.2f} 小时"),
    ]

    return layer, path_info


# 运行Dash应用
if __name__ == "__main__":
    app.run_server(debug=True)
