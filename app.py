import streamlit as st
import pandas as pd
from mock_data import PROJECTS, PIPELINE_STAGES, RECENT_ACTIVITIES, ENTITY_ANTIBODIES, ENTITY_CELL_LINES, CLOSED_LOOP_ITERATIONS
from utils import render_sidebar, plot_pipeline, render_platform_mapping

st.set_page_config(page_title="AbDiscovery OS", page_icon="🧬", layout="wide")

render_sidebar(
    page_name="抗体研发管线总览",
    biomap_module="BioMap OS · 项目追踪模块",
    benchling_module="Benchling Workflows",
    related_stages=[1, 2, 3, 4, 5, 6, 7, 8],
)

# ── Header ──
st.title("🧬 AbDiscovery OS")
st.markdown("**AI驱动的抗体研发数据平台** — 对标 Benchling + BioMap OS，覆盖从靶点发现到候选分子确定的全流程")

# ── KPI Metrics ──
total_targets = len({p["target"] for p in PROJECTS})
total_sequences = len(ENTITY_ANTIBODIES)
total_cell_lines = len(ENTITY_CELL_LINES)
best_kd = min(ab["kd_nm"] for ab in ENTITY_ANTIBODIES)
loop_rounds = len(CLOSED_LOOP_ITERATIONS)
affinity_improvement = CLOSED_LOOP_ITERATIONS[0]["best_kd"] / CLOSED_LOOP_ITERATIONS[-1]["best_kd"]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("在研靶点", f"{total_targets}个")
c2.metric("注册序列", f"{total_sequences}条")
c3.metric("细胞株", f"{total_cell_lines}个")
c4.metric("最优KD", f"{best_kd} nM")
c5.metric("闭环迭代", f"{loop_rounds}轮")
c6.metric("亲和力提升", f"{affinity_improvement:.0f}×")

st.divider()

# ── Pipeline Stages ──
st.subheader("📊 抗体研发管线 · 8阶段")
fig = plot_pipeline(PROJECTS)
st.plotly_chart(fig, key="pipeline", use_container_width=True)

# ── Project Cards (clickable) ──
st.subheader("🔬 在研项目")
st.caption("点击「查看详情」进入项目二级页面")

for i in range(0, len(PROJECTS), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(PROJECTS):
            p = PROJECTS[i + j]
            with col:
                with st.container(border=True):
                    st.markdown(f"### {p['name']}")
                    st.caption(f"项目编号: {p['id']}")

                    mc1, mc2 = st.columns(2)
                    mc1.markdown(f"**靶点**: {p['target']}")
                    mc2.markdown(f"**格式**: {p['format']}")
                    mc1.markdown(f"**适应症**: {p['indication']}")
                    mc2.markdown(f"**阶段**: {p['stage']}")

                    st.progress(p["progress"] / 100, text=f"进度 {p['progress']}%")

                    if p["lead_count"] > 0:
                        st.success(f"✅ {p['lead_count']} 个Lead候选")
                    else:
                        st.info("🔍 筛选中")

                    if st.button(f"查看详情 →", key=f"proj_{p['id']}", use_container_width=True):
                        st.session_state["drill_project"] = p["id"]
                        st.switch_page("pages/7_项目详情.py")

st.divider()

# ── Stage Distribution ──
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 管线阶段分布")
    stage_data = []
    for s in PIPELINE_STAGES:
        count = sum(1 for p in PROJECTS if p["stage_id"] == s["id"])
        if count > 0:
            stage_data.append({"阶段": s["name"], "项目数": count})
    if stage_data:
        df_stage = pd.DataFrame(stage_data)
        import plotly.express as px
        fig_pie = px.pie(df_stage, names="阶段", values="项目数", hole=0.4)
        fig_pie.update_layout(height=350, margin=dict(l=20, r=20, t=10, b=10))
        st.plotly_chart(fig_pie, key="stage_pie", use_container_width=True)

with col_right:
    st.subheader("📋 最近研发动态")
    for act in RECENT_ACTIVITIES[:6]:
        with st.container(border=True):
            ac1, ac2 = st.columns([1, 5])
            ac1.markdown(f"### {act['icon']}")
            ac2.markdown(f"**{act['event']}**")
            ac2.caption(f"{act['time']} · {act['project']}")

st.divider()

# ── JD Coverage Matrix ──
st.subheader("🎯 JD 覆盖度矩阵")
st.markdown("每一条岗位核心要求，在Demo中都有对应页面回应")

jd_coverage = [
    {"JD核心要求": "样本全流程管理", "对应页面": "📋 序列注册中心", "具体体现": "抗体/细胞株/质粒 Registry + Schema定义 + Sankey关系图 + 库存状态", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "实验数据记录", "对应页面": "🧪 实验数据管理", "具体体现": "ELISA/SPR/表达 三类Structured Tables + 异常预警 + 数据录入表单", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "智能分析", "对应页面": "🔬 智能分析与闭环", "具体体现": "SPR sensorgram + 可开发性5维评估 + AI结论 + 干湿闭环4轮迭代", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "项目追踪", "对应页面": "🧬 首页管线 + 📁 项目详情", "具体体现": "8阶段管线 + 5项目KPI + 动态时间线 + 项目二级钻取", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "抗体/细胞场景理解", "对应页面": "全部页面", "具体体现": "整个Demo就是抗体发现全流程，含靶点→筛选→优化→CLD→候选确定", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "拆解复杂业务→标准化", "对应页面": "📋 序列注册中心", "具体体现": "3类实体Schema定义展示了「线下流程→标准化产品功能」的方法论", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "LIMS/ELN经验", "对应页面": "📋 注册中心 + 🧪 数据管理", "具体体现": "对标Benchling Registry(LIMS) + Notebook(ELN)，侧边栏标注对标关系", "覆盖": "✅ 完整覆盖"},
    {"JD核心要求": "AI赋能研发", "对应页面": "🤖 AI序列设计 + 💬 知识助手 + 🔬 闭环", "具体体现": "AIGP三模式(F2P/P2P/C2P) + Agent矩阵 + RAG问答 + 干湿闭环", "覆盖": "✅ 完整覆盖"},
]

df_jd = pd.DataFrame(jd_coverage)

def highlight_coverage(val):
    if "完整覆盖" in str(val):
        return "background-color: #d4edda; color: #155724"
    return ""

styled_jd = df_jd.style.map(highlight_coverage, subset=["覆盖"])
st.dataframe(styled_jd, hide_index=True, use_container_width=True, height=350)

st.divider()

# ── Platform Mapping ──
render_platform_mapping()

st.divider()

# ── Design Philosophy ──
st.subheader("💡 产品设计理念")
d1, d2, d3 = st.columns(3)
with d1:
    with st.container(border=True):
        st.markdown("### 🎯 科学家优先")
        st.markdown("系统适应工作方式，而非反过来。结构化数据采集嵌入实验记录，对科学家零额外负担。")
with d2:
    with st.container(border=True):
        st.markdown("### 🔄 干湿闭环")
        st.markdown("AI序列设计→湿实验验证→数据回传→AI再设计。门控闭环（Gated Loop），人机协同不断链。")
with d3:
    with st.container(border=True):
        st.markdown("### 🤖 AI不是功能，是交互方式")
        st.markdown("AI Agent嵌入科学家自然工作流：对话式查询、自动解析、智能推荐、主动式分析。")
