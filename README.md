# railway-visualization
数据结构作业5，铁路可视化及最短路径
# 城市间铁路连接及A*路径可视化

## 简介

本项目利用A*算法和Dash框架，实现了中国前500城市之间铁路连接的最短路径求解和可视化。用户可以在界面中选择起点和终点，实时计算并显示最短路径，同时展示各个城市的铁路连接情况。
<div style="display:flex; justify-content:center;">
    <img src="picture/image1.png" alt="Image text" style="width:300px;">
</div>

## 功能

1. **数据爬取**：爬取中国前500城市的火车站台经纬度及其铁路连接数据。
2. **图结构表示**：将城市和铁路数据表示为图结构，城市作为节点，铁路连接作为边。
3. **A*算法实现**：实现A*算法，用于求解最短路径。
4. **可视化展示**：使用Dash框架进行数据的可视化展示，实时显示最短路径和城市间的铁路连接。

## 依赖

- Python 3.x
- NetworkX
- Geopandas
- Geopy
- Dash
- Dash Bootstrap Components
- Dash Leaflet
- Matplotlib
- Pandas
- Scikit-learn

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/Yuki-zik/railway-visualization.git
cd railway-visualization
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用

### 数据爬取和图数据生成

1. 运行 `graph_create.py`，生成图结构数据，保存节点和边的数据到CSV文件。

```bash
python graph_create.py
```

### A*算法实现

1.  `astar.py` 文件，包含A*算法的实现。

### 可视化互动界面

1. 运行 `grapy.py` 文件，启动Dash应用，进行数据的可视化展示。

```bash
python grapy.py
```

## 文件结构

- **astar.py**: 实现A*算法，用于求解最短路径。
- **edges.csv、node.csv**: 保存城市间铁路连接的边数据，包括起点、终点和距离。
- **graph_create.py**: 爬取数据并创建图结构，导出节点和边数据到CSV文件。
- **grapy.py**: 创建Dash应用，进行可视化展示。

## 详细说明

### astar.py

`astar.py` 文件实现了A*算法，用于求解最短路径。该文件包含以下主要功能：

- **初始化A*算法实例**
- **启发式函数**：使用地理距离作为启发式函数。
- **搜索函数**：执行A*算法搜索从起点到目标点的最短路径。
- **路径重建**：从起点到目标点重建路径。

### graph_create.py

`graph_create.py` 文件用于爬取数据并创建图结构。该文件包含以下主要功能：

- **读取城市和铁路数据**
- **构建图结构**：将城市作为节点，铁路连接作为边。
- **保存节点和边数据**：将节点和边的数据保存到CSV文件中。
- **可视化城市铁路连接图**：使用Matplotlib可视化优化后的城市铁路连接图。

### grapy.py

`grapy.py` 文件用于创建Dash应用，进行数据的可视化展示。该文件包含以下主要功能：

- **读取节点和边数据**：从CSV文件中读取节点和边数据。
- **创建图模型**：使用NetworkX构建图模型。
- **初始化A*算法实例**：使用读取的数据初始化A*算法实例。
- **创建Dash应用**：使用Dash框架创建可视化互动界面。
- **定义回调函数**：根据用户选择的起点和终点，实时计算并展示最短路径。

## 运行示例

1. 启动应用：

```bash
python grapy.py
```

2. 在浏览器中打开 `http://127.0.0.1:8050`，即可看到可视化界面。

3. 选择起点和终点，实时计算并显示最短路径。

## 许可证

此项目采用 MIT 许可证。详情请参见 LICENSE 文件。
