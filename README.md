# FitTracker - AI减肥管理应用

一个基于Python + Kivy + KivyMD的智能减肥管理移动应用，帮助用户追踪饮食、运动和制定科学的减肥计划。

## 功能特性

- **今日概览**：实时显示摄入/消耗/净热量
- **饮食记录**：手动添加每餐食物和热量
- **运动追踪**：8种运动类型，基于MET值计算消耗
- **减肥计划**：根据个人数据(BMR/TDEE)生成科学计划
- **日历视图**：查看任意日期的饮食和运动记录
- **数据管理**：本地SQLite存储，支持清除数据

## 技术栈

- Python 3.11
- Kivy 2.3.1
- KivyMD 1.2.0
- SQLite (本地数据存储)

## 快速开始

### 本地运行
```bash
# 使用conda环境
D:\Miniconda\envs\my_env_python\python.exe main.py

# 或激活环境后运行
conda activate my_env_python
python main.py
```

### 打包APK (Google Colab)
1. 打开 `build_apk_colab.ipynb`
2. 上传项目文件到Colab
3. 运行所有cell生成APK
4. 下载生成的APK文件

## 项目结构

```
fittracker/
├── main.py                 # 主应用入口
├── database.py             # 数据库模块
├── buildozer.spec          # Buildozer配置
├── build_apk_colab.ipynb   # Colab打包脚本
├── .gitignore
└── README.md
```

## 数据库表结构

- `user_profile` - 用户个人信息(身高/体重/年龄/性别/目标体重)
- `meals` - 饮食记录(日期/餐次/食物/热量/营养素)
- `exercises` - 运动记录(日期/类型/时长/消耗)
- `daily_logs` - 每日汇总(摄入/消耗/净热量)
- `plans` - 减肥计划(目标/周期/每日热量)

## 运动类型

| 类型 | MET值 | 说明 |
|------|-------|------|
| 快走 | 3.5 | 5km/h |
| 慢跑 | 8.0 | 8km/h |
| 中速跑 | 9.8 | 10km/h |
| 骑行 | 6.0 | 中等强度 |
| 游泳 | 7.0 | 中等强度 |
| 力量训练 | 5.0 | 中等强度 |
| 瑜伽 | 3.0 | 中等强度 |
| 跳绳 | 12.0 | 中等强度 |

## 待实现功能

- [ ] AI食物识别(集成视觉API)
- [ ] 步数计数器
- [ ] 体重趋势图表
- [ ] 数据导出功能
- [ ] 多语言支持

## License

MIT
