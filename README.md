# AbDiscovery OS

AI驱动的抗体研发数据平台原型，覆盖从靶点发现到候选分子确定的全流程。产品架构对标 **Benchling + BioMap OS** 双平台。

## 产品概览

AbDiscovery OS 围绕抗体发现 8 个核心阶段构建：靶点发现与验证 → 抗体库构建与筛选 → 命中确认 → 先导优化 → 可开发性评估 → 细胞株构建 → 工艺开发 → 候选分子确定。

平台包含 6 个功能模块 + 3 个二级钻取页面：

| 模块 | 功能 | 对标 |
|------|------|------|
| 靶点研究 | 多源情报聚合 + AI可药性评估 | Benchling Research Agent / BioMap 发现助手 |
| 序列注册中心 | 抗体/细胞株/质粒 Registry + Schema + 关系网络 | Benchling Registry / BioMap 样本管理 |
| AI序列设计 | AIGP 三模式（F2P / P2P / C2P） | Benchling Model Hub / BioMap xTrimo |
| 实验数据管理 | ELISA/SPR/表达 Structured Tables + 数据录入 | Benchling Notebook / BioMap 实验记录 |
| 智能分析与闭环 | SPR sensorgram + 可开发性评估 + 4轮干湿闭环 | Benchling Insights / BioMap 干湿闭环 |
| AI知识助手 | Agent矩阵 + RAG问答 + 多轮对话 | Benchling AI Agents / BioMap 知识助手 |
| 项目详情 | 项目钻取：管线进度 + 抗体列表 + 实验汇总 | 二级页面 |
| 抗体详情 | 抗体全属性：序列 + SPR + 可开发性 + 关联实体 | 二级页面 |
| 实验报告 | 项目维度实验综合报告 + AI结论 | 二级页面 |

## 技术栈

- **Streamlit** — 多页面应用框架
- **Plotly** — 交互式图表（Bar / Scatter / Radar / Sankey / Pie）
- **Pandas** — 数据表展示与样式
- **NumPy** — SPR sensorgram 曲线模拟

全部数据为 Mock 数据，基于真实抗体研发流程和公开文献构建。

## 快速启动

```bash
pip install streamlit plotly pandas numpy
cd abdiscovery-os
streamlit run app.py --server.port 8504
```

浏览器访问 http://localhost:8504

## 项目结构

```
abdiscovery-os/
├── app.py                 # 首页：管线总览 + 项目卡片 + JD覆盖度矩阵
├── mock_data.py           # 14个数据集（5个项目 / 15条抗体 / 6个细胞株 / 8个质粒...）
├── utils.py               # 10个通用组件（图表 + 侧边栏 + 颜色编码）
├── pages/
│   ├── 1_靶点研究.py
│   ├── 2_序列注册中心.py
│   ├── 3_AI序列设计.py
│   ├── 4_实验数据管理.py
│   ├── 5_智能分析与闭环.py
│   ├── 6_AI知识助手.py
│   ├── 7_项目详情.py       # 二级页面
│   ├── 8_抗体详情.py       # 二级页面
│   └── 9_实验报告.py       # 二级页面
├── .streamlit/config.toml  # 主题配置
└── 设计说明文档.md          # 详细设计说明
```

## Mock 数据亮点

- **15条抗体序列**覆盖 5 种来源（噬菌体展示 / 杂交瘤 / 免疫驼 / AI生成 / 人源化），呈现传统方法与 AI 方法的对比
- **PD-L1 项目**展示完整亲和力成熟过程：KD 从 12.5nM 经 4 轮闭环优化至 0.3nM
- **5 种抗体格式**（IgG4 / IgG1 / sdAb / scFv / ADC）体现抗体工程多样性
- **竞品数据**使用真实药物名称和公开销售额

## 设计理念

- **科学家优先** — 系统适应工作方式，结构化数据采集嵌入实验记录，零额外负担
- **干湿闭环** — AI序列设计 → 湿实验验证 → 数据回传 → AI再设计，门控闭环人机协同
- **AI是交互方式，不是功能** — Agent嵌入自然工作流：对话查询、自动解析、智能推荐、主动分析

## License

本项目为面试展示用途的产品原型 Demo。
