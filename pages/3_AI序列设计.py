import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import ENTITY_ANTIBODIES, PROJECTS
from utils import render_sidebar, plot_radar_chart, kd_color

st.set_page_config(page_title="AI序列设计 | AbDiscovery OS", page_icon="🤖", layout="wide")

render_sidebar(
    page_name="AI序列设计",
    biomap_module="BioMap OS · xTrimo / AIGP平台",
    benchling_module="Benchling Model Hub + Biologics",
    related_stages=[2, 3, 4],
)

st.title("🤖 AI序列设计")
st.markdown("AI驱动的抗体序列生成与优化 — 直接对标 **百图生科AIGP平台（F2P / P2P / C2P）**")

st.divider()

# ── AIGP Mode Selection ──
st.subheader("🎯 设计模式选择")
st.markdown("三种设计模式映射百图生科AIGP核心范式：")

mode_tab1, mode_tab2, mode_tab3 = st.tabs([
    "🆕 F2P（Function → Protein）",
    "🔄 P2P（Protein → Protein）",
    "📝 C2P（Context → Protein）",
])

# ═════════════════════════════════
# F2P Mode
# ═════════════════════════════════
with mode_tab1:
    st.markdown("### 🆕 从功能需求生成全新抗体序列")
    st.markdown("输入靶点和期望属性，AI从零设计抗体序列（de novo生成）")

    with st.container(border=True):
        fc1, fc2 = st.columns(2)
        with fc1:
            f2p_target = st.selectbox("靶点", ["PD-L1", "HER2", "TNFα", "CD20", "IL-17A"], key="f2p_target")
            f2p_format = st.selectbox("抗体格式", ["IgG4", "IgG1", "sdAb(VHH)", "scFv"], key="f2p_format")
            f2p_kd = st.slider("期望KD范围 (nM)", 0.1, 50.0, (0.5, 10.0), key="f2p_kd")
        with fc2:
            f2p_tm = st.slider("期望Tm (°C)", 60, 85, 70, key="f2p_tm")
            f2p_count = st.slider("生成候选数", 3, 10, 5, key="f2p_count")
            f2p_optimize = st.multiselect("优化目标", ["亲和力", "稳定性", "低免疫原性", "高表达"], default=["亲和力", "稳定性"], key="f2p_opt")

    if st.button("🚀 启动F2P序列生成", key="f2p_btn", type="primary"):
        with st.spinner("xTrimo F2P模型生成中..."):
            import time
            time.sleep(1.5)

        st.success(f"✅ 已生成 {f2p_count} 条候选序列")

        f2p_abs = [ab for ab in ENTITY_ANTIBODIES if ab["source"] == "AI生成(F2P)" and ab["target"] == f2p_target]
        if not f2p_abs:
            f2p_abs = [ab for ab in ENTITY_ANTIBODIES if "AI" in ab["source"]][:f2p_count]

        results = []
        for i, ab in enumerate(f2p_abs[:f2p_count]):
            results.append({
                "排名": i + 1,
                "序列ID": ab["id"],
                "名称": ab["name"],
                "CDR-H3": ab["cdr_h3"],
                "预测KD (nM)": ab["kd_nm"],
                "亲和力": kd_color(ab["kd_nm"]),
                "预测Tm (°C)": ab["tm_celsius"],
                "置信度": f"{90 - i * 5}%",
            })
        st.dataframe(pd.DataFrame(results), hide_index=True, use_container_width=True)

# ═════════════════════════════════
# P2P Mode
# ═════════════════════════════════
with mode_tab2:
    st.markdown("### 🔄 基于已有序列优化改进")
    st.markdown("输入已有抗体序列，AI进行亲和力成熟、稳定性提升、去免疫原性等优化")

    with st.container(border=True):
        parent_abs = [ab for ab in ENTITY_ANTIBODIES if ab["kd_nm"] > 5]
        p2p_parent = st.selectbox(
            "选择亲本序列",
            [f"{ab['id']} — {ab['name']} (KD={ab['kd_nm']}nM)" for ab in parent_abs],
            key="p2p_parent",
        )
        p2p_goal = st.selectbox("优化目标", ["亲和力提升", "热稳定性提升", "降低免疫原性", "提高表达量"], key="p2p_goal")
        p2p_rounds = st.selectbox("优化轮次", [1, 2, 3], index=1, key="p2p_rounds")

    if st.button("🚀 启动P2P序列优化", key="p2p_btn", type="primary"):
        with st.spinner("xTrimo P2P模型优化中..."):
            import time
            time.sleep(1.5)

        parent_id = p2p_parent.split(" — ")[0]
        parent = next(ab for ab in ENTITY_ANTIBODIES if ab["id"] == parent_id)

        optimized = [ab for ab in ENTITY_ANTIBODIES if "P2P" in ab.get("source", "") and ab["target"] == parent["target"]]
        if not optimized:
            optimized = [ab for ab in ENTITY_ANTIBODIES if ab["kd_nm"] < parent["kd_nm"]][:3]

        st.success(f"✅ 从 {parent['name']}(KD={parent['kd_nm']}nM) 优化生成 {len(optimized)} 条变体")

        st.markdown("#### 优化轨迹")
        fig_opt = go.Figure()
        all_trace = [parent] + optimized
        fig_opt.add_trace(go.Scatter(
            x=[ab["name"] for ab in all_trace],
            y=[ab["kd_nm"] for ab in all_trace],
            mode="lines+markers+text",
            text=[f"{ab['kd_nm']}nM" for ab in all_trace],
            textposition="top center",
            marker=dict(size=12),
            line=dict(width=3),
        ))
        fig_opt.update_layout(
            title=f"P2P优化轨迹: {parent['name']} → 优化变体",
            yaxis_title="KD (nM)", yaxis_type="log",
            height=350, margin=dict(l=60, r=20, t=40, b=40),
        )
        st.plotly_chart(fig_opt, key="p2p_trace", use_container_width=True)

        opt_data = []
        for ab in optimized:
            improvement = parent["kd_nm"] / ab["kd_nm"]
            opt_data.append({
                "ID": ab["id"],
                "名称": ab["name"],
                "CDR-H3": ab["cdr_h3"],
                "KD (nM)": ab["kd_nm"],
                "提升倍数": f"{improvement:.1f}×",
                "Tm (°C)": ab["tm_celsius"],
            })
        st.dataframe(pd.DataFrame(opt_data), hide_index=True, use_container_width=True)

# ═════════════════════════════════
# C2P Mode
# ═════════════════════════════════
with mode_tab3:
    st.markdown("### 📝 基于上下文信息设计")
    st.markdown("输入表位信息、竞品序列、可开发性约束等上下文，AI设计差异化序列")

    with st.container(border=True):
        c2p_target = st.selectbox("靶点", ["PD-L1", "HER2"], key="c2p_target")
        c2p_context = st.text_area(
            "设计上下文（自然语言描述）",
            value="设计一个针对PD-L1的IgG4抗体，要求：\n1. 结合表位与Atezolizumab不同（差异化竞争）\n2. KD < 1 nM\n3. Tm > 75°C\n4. 免疫原性评分 < 15\n5. 适合CHO细胞高表达（>50 mg/L瞬转）",
            height=150,
            key="c2p_ctx",
        )

    if st.button("🚀 启动C2P上下文设计", key="c2p_btn", type="primary"):
        with st.spinner("xTrimo C2P模型解析上下文中..."):
            import time
            time.sleep(2)

        c2p_abs = [ab for ab in ENTITY_ANTIBODIES if "C2P" in ab.get("source", "")]
        if not c2p_abs:
            c2p_abs = [ab for ab in ENTITY_ANTIBODIES if ab["kd_nm"] < 1][:2]

        st.success(f"✅ C2P模型生成 {len(c2p_abs)} 条满足上下文约束的候选")

        for ab in c2p_abs:
            with st.container(border=True):
                st.markdown(f"#### {ab['name']} ({ab['id']})")
                cc1, cc2 = st.columns(2)
                cc1.markdown(f"**KD**: {ab['kd_nm']} nM {kd_color(ab['kd_nm'])}")
                cc1.markdown(f"**Tm**: {ab['tm_celsius']}°C")
                cc2.markdown(f"**CDR-H3**: `{ab['cdr_h3']}`")
                cc2.markdown(f"**表达量**: {ab['expression_mg_l']} mg/L")
                st.markdown("**AI设计说明**: 通过上下文约束优化，CDR-H3区域引入差异化残基，预测结合表位与Atezolizumab部分重叠但存在独特接触位点")

st.divider()

# ── Model Info Card ──
st.subheader("🧠 AI模型信息")
with st.container(border=True):
    mi1, mi2 = st.columns(2)
    with mi1:
        st.markdown("#### xTrimo 蛋白质设计引擎")
        st.markdown("""
        | 属性 | 参数 |
        |------|------|
        | 基础模型 | xTrimo V3 |
        | 参数量 | **2100亿** |
        | 架构 | MoE + GLM |
        | 覆盖模态 | 7大生物模态 |
        | 训练数据 | UniProt + PDB + 专有数据 |
        | 蛋白质理解 | 200+任务SOTA |
        """)
    with mi2:
        st.markdown("#### AIGP 三大范式")
        st.markdown("""
        | 范式 | 输入 | 输出 | 典型场景 |
        |------|------|------|---------|
        | **F2P** | 功能需求 | 全新序列 | de novo抗体设计 |
        | **P2P** | 已有序列 | 优化变体 | 亲和力成熟/人源化 |
        | **C2P** | 上下文约束 | 定制序列 | 差异化/可开发性优化 |
        """)

    st.markdown("""
    > **与Benchling Model Hub的差异**: Benchling集成第三方模型（AlphaFold/Chai-1），定位为"模型集市"。
    > 百图生科xTrimo是**自研**的2100亿参数生命科学大模型，可以做真正的"AI序列设计"而非"AI辅助分析"，
    > 这是更深的技术壁垒。
    """)
