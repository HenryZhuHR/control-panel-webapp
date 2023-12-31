# 控制面板


## 技术栈

- 前端: vue3 + ts + scss + [TDesign](https://tdesign.tencent.com/mobile-vue/getting-started) 
- 后端: flask

## 前端

### 前端页面设计

![控制面板页面设计](./images/panel-design.png)


## 后端

### 后端数据设计


数据按照以下进行分组，包含数据
- `state`: [车辆状态数据](#车辆状态数据)
  - `speed`: [车辆速度数据](#车辆速度数据)

#### 车辆状态数据
车辆状态数据 (`state`) 记录状态，包含以下数据
- `speed`: [车辆速度数据](#车辆速度数据)

##### 车辆速度数据
车辆速度数据 `speed` 属于 `state` 数据的子数据(`state.speed`)，包含以下数据
| 数据名称  |  类型   | 默认值 |      范围       | 数据描述               |
| :-------: | :-----: | :----: | :-------------: | :--------------------- |
| `speed.x` | `float` | `0.0`  |  `[-1.0, 1.0]`  | x 方向速度，单位 m/s   |
| `speed.y` | `float` | `0.0`  |  `[-1.0, 1.0]`  | y 方向速度，单位 m/s   |
| `speed.z` | `float` | `0.0`  | `[-3.14, 3.14]` | z 方向速度，单位 rad/s |

需要说明的是，ROS应用层中 限制了速度范围，因此前端应该能够修改速度范围，以限制机器人移动的最大速度。因此设计数据的时候需要考虑 **「速度」** 和 **「范围」**