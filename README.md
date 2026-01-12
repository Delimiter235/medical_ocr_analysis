# 🏥 Medical Report Analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://www.python.org/)
[![OCR](https://img.shields.io/badge/Model-PaddleOCR-green?style=flat-square)](https://github.com/PaddlePaddle/PaddleOCR)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)]()

## 📖 Introduction

**Medical Report Analysis Pipeline** 是一个基于 Python 的自动化数据处理工具，旨在解决纸质医疗化验单（如血清铁蛋白检测）的**非结构化数据提取**难题。

在面对大量纸质或图片格式的医疗记录时，人工录入效率低下且容易出错。本项目利用 **PaddleOCR** 进行文字识别，结合**语义锚点算法**进行数据清洗与结构化，最终生成可视化的病情趋势图表，为家庭健康监控提供数据支持。

> **核心价值：** 将“死”的图片数据转化为“活”的可视化洞察 (Data Insights)。

## ✨ Key Features (核心功能)

- **📄 批量 OCR 处理:** 自动遍历目录，支持断点续传，将图片转为 JSON 数据。
- **🔍 智能语义提取:** 不依赖绝对坐标，基于关键字锚点（Anchor-based）提取特定指标（如铁蛋白、白细胞等）。
- **📊 自动化报表:** 自动聚合数据生成 CSV 格式的标准化报表。
- **📈 趋势可视化:** 基于 Matplotlib/Seaborn 生成带有医学参考范围（Reference Range）的时间序列折线图。

## 🛠 Tech Stack (技术栈)

- **Environment:** Arch Linux (WSL2) / Python 3.12
- **Core Engine:** PaddleOCR (PP-Structure)
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Utils:** Tqdm, Python-dotenv

## 📂 Directory Structure (目录结构)

```
text
medical-ocr-pipeline/
├── data/                  # [GitIgnored] Local data storage
│   ├── raw/               # Original images
│   └── processed/         # Generated JSONs and CSVs
├── src/                   # Source code
│   ├── config.py          # Path configuration (Single Source of Truth)
│   ├── ocr_engine.py      # OCR wrapper
│   └── extractor.py       # Data extraction logic
├── output/                # [GitIgnored] Visualization results
├── tests/                 # Unit tests & dummy data
├── requirements.txt       # Dependency lock file
└── README.md              # Project documentation
```

## 🚀 Quick Start (快速开始)
1. Installation
Clone the repository and install dependencies:

```
git clone https://github.com/YourUsername/medical-ocr-analysis.git
cd medical-ocr-analysis

# Create virtual environment (Recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

2. Prepare Data
Place your medical report images in data/raw/images/.
(Note: Real medical data is not included in this repo for privacy reasons.)

3. Run Pipeline
Execute the main script to process images and generate charts:

```
# Run batch OCR and extraction
python scripts/run_pipeline.py

# Generate visualization
python scripts/visualize.py
```

4. Check Results
Structured Data: data/processed/report.csv
Charts: output/trend_chart.png

## 📊 Result Preview (效果展示)
![alt text](output/trend_chart.png)

## 🔒 Privacy & Compliance (隐私声明)
本项目严格遵守数据隐私原则：
数据隔离： 所有真实的医疗数据（图片、JSON、CSV）均存储在本地 data/ 目录，并已被 .gitignore 排除。
脱敏测试： 仓库中的测试数据均为人工生成的虚构数据（Dummy Data）。

## 📝 Roadmap (路线图)

完成基础 OCR 流程与 CSV 导出。

实现血清铁蛋白趋势可视化。

[Refactor] 将硬编码提取逻辑重构为通用配置化规则 (Config-driven extraction)。

增加对血常规 (Blood Routine) 复杂表格的解析支持。

集成 LLM (Local/API) 用于更复杂的非结构化文本清洗。

## 🤝 Contribution
Contributions are welcome! Please open an issue or submit a PR.
