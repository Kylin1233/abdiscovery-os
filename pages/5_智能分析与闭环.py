import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import SPR_DATA, DEVELOPABILITY_DATA, CLOSED_LOOP_ITERATIONS, ENTITY_ANTIBODIES
from utils import render_sidebar, plot_spr_sensorgram, plot_closed_loop, plot_radar_chart, kd_color, verdict_color

st.set_page_config(page_title="智能分析与闭环 | AbDiscovery OS", page_icon="🔬", layout="wide")

render_sidebar(
    page_name="智能分析与闭环",
    biomap_module="BioMap OS · 智能分析 + 干湿闭环",
    benchling_module="Benchling Insights + Automation",
    related_stages=[3, 4, 5],
)

st.title("🔬 智能分析与干湿闭环")
st.markdown("SPR动力学分析 + 可开发性评估 + AI-实验室门控闭环 — 对标 **Benchling Insights + Automation + BioMap干湿闭环**")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
best_kd = min(s["kd_nm"] for s in SPR_DATA)
passed = sum(1 for d in DEVELOPABILITY_DATA if d["overall"] == "通过")
total_dev = len(DEVELOPABILITY_DATA)
loop_rounds = len(CLOSED_LOOP_ITERATIONS)
improvement = CLOSED_LOOP_ITERATIONS[0]["best_kd"] / CLOSED_LOOP_ITERATIONS[-1]["best_kd"]

c1.metric("最优KD", f"{best_kd} nM")
c2.metric("可开发性通过", f"{passed}/{total_dev}")
c3.metric("闭环轮次", f"{loop_rounds}轮")
c4.metric("亲和力累计提升", f"{improvement:.0f}×")

st.divider()

# ═══════════════════════════════════
# Section 1: SPR Analysis
# ═══════════════════════════════════
st.subheader("📈 SPR 动力学深度分析")

sel_spr = st.multiselect(
    "选择抗体查看Sensorgram",
    [s["name"] for s in SPR_DATA],
    default=[SPR_DATA[0]["name"], SPR_DATA[-2]["name"], SPR_DATA[-1]["name"]],
    key="spr_sel",
)

if sel_spr:
    selected_spr = [s for s in SPR_DATA if s["name"] in sel_spr]
    fig_spr = plot_spr_sensorgram(selected_spr)
    st.plotly_chart(fig_spr, key="sensorgram", use_container_width=True)

    st.markdown("#### 动力学参数对比")
    spr_compare = []
    for s in selected_spr:
        spr_compare.append({
            "抗体": s["name"],
            "ka (1/Ms)": f"{s['ka_per_ms']:.2e}",
            "kd (1/s)": f"{s['kd_per_s']:.2e}",
            "KD (nM)": s["kd_nm"],
            "亲和力等级": kd_color(s["kd_nm"]),
            "拟合度 Chi²": s["chi2"],
            "判定": f"{verdict_color(s['verdict'])} {s['verdict']}",
        })
    st.dataframe(pd.DataFrame(spr_compare), hide_index=True, use_container_width=True)

    with st.container(border=True):
        st.markdown("#### 🤖 AI分析结论")
        best = min(selected_spr, key=lambda x: x["kd_nm"])
        st.markdown(f"""
        **最优候选**: {best['name']}（KD = {best['kd_nm']} nM）

        - **结合动力学**: ka = {best['ka_per_ms']:.2e} M⁻¹s⁻¹（快速结合），kd = {best['kd_per_s']:.2e} s⁻¹（慢速解离）
        - **临床对标**: 获批PD-L1抗体Atezolizumab KD ≈ 0.4 nM，当前候选已达可比水平
        - **建议**: 结合动力学参数优秀，建议推进至可开发性评估阶段
        """)

st.divider()

# ═══════════════════════════════════
# Section 2: Developability
# ═══════════════════════════════════
st.subheader("📊 可开发性评估看板")
st.markdown("5维评估：热稳定性(Tm) · 聚集倾向(SEC%) · 粘度 · 免疫原性 · 化学稳定性")

dev_display = []
for d in DEVELOPABILITY_DATA:
    dev_display.append({
        "抗体ID": d["antibody_id"],
        "名称": d["name"],
        "Tm (°C)": d["tm_celsius"],
        "聚集 (%)": d["aggregation_pct"],
        "粘度 (cP)": d["viscosity_cp"],
        "免疫原性评分": d["immunogenicity_score"],
        "化学稳定性": d["chemical_stability"],
        "综合判定": f"{verdict_color(d['overall'])} {d['overall']}",
        "建议": d["recommendation"],
    })
df_dev = pd.DataFrame(dev_display)
st.dataframe(df_dev, hide_index=True, use_container_width=True)

# Radar comparison
st.markdown("#### 可开发性雷达图对比")
dev_categories = ["热稳定性", "低聚集", "低粘度", "低免疫原性", "化学稳定性"]
dev_values = {}
for d in DEVELOPABILITY_DATA:
    tm_score = min(100, max(0, (d["tm_celsius"] - 60) * 5))
    agg_score = min(100, max(0, 100 - d["aggregation_pct"] * 15))
    visc_score = min(100, max(0, 100 - d["viscosity_cp"] * 4))
    immu_score = min(100, max(0, 100 - d["immunogenicity_score"] * 3))
    chem_score = {"优秀": 95, "良好": 75, "一般": 45}.get(d["chemical_stability"], 50)
    dev_values[d["name"]] = [tm_score, agg_score, visc_score, immu_score, chem_score]

fig_dev_radar = plot_radar_chart(dev_categories, dev_values, "可开发性多维对比")
st.plotly_chart(fig_dev_radar, key="dev_radar", use_container_width=True)

with st.container(border=True):
    st.markdown("#### 🤖 AI可开发性结论")
    st.markdown("""
    | 候选 | 决策 | 关键理由 |
    |------|------|---------|
    | **αPDL1-A03 (AB-005)** | ✅ 推荐进入CLD | Tm=76.4°C, 聚集1.2%, 粘度8.5cP, 各维度均达标 |
    | **αTNF-N02 (AB-010)** | ✅ 推荐进入CLD | VHH天然稳定性优异(Tm=78.5°C, 聚集0.8%), 粘度极低 |
    | **αIL17-H01-HC (AB-012)** | ✅ 推荐进入CLD | 人源化完成, 各指标达标 |
    | **αPDL1-A02 (AB-004)** | ⚠️ 条件通过 | 聚集2.8%偏高, 建议CDR-H2工程化降低聚集倾向 |
    | **αPDL1-A04 (AB-014)** | ❌ 退回优化 | 聚集4.5%+粘度15.8cP+免疫原性25, 建议P2P重新设计 |
    """)

st.divider()

# ═══════════════════════════════════
# Section 3: Closed Loop
# ═══════════════════════════════════
st.subheader("🔄 干湿闭环迭代")
st.markdown("AI设计 → 实验验证 → 数据回传 → AI再设计 — 对标 **Benchling Lab-in-the-Loop + BioMap干湿闭环**")

# Gated Loop Diagram — Plotly Flow
with st.container(border=True):
    st.markdown("#### 门控闭环（Gated Loop）架构")

    import plotly.graph_objects as go

    fig_flow = go.Figure()

    nodes = [
        {"label": "🤖 AI序列设计\n(xTrimo)", "x": 0.08, "color": "#636EFA"},
        {"label": "⏸️ 人工审核\n(Gate)", "x": 0.27, "color": "#FFA15A"},
        {"label": "🧪 湿实验执行\n(Lab)", "x": 0.46, "color": "#EF553B"},
        {"label": "📊 数据回传\n(Connect)", "x": 0.65, "color": "#00CC96"},
        {"label": "📈 AI分析\n(Insights)", "x": 0.84, "color": "#AB63FA"},
    ]

    for i, n in enumerate(nodes):
        fig_flow.add_trace(go.Scatter(
            x=[n["x"]], y=[0.5],
            mode="markers+text",
            marker=dict(size=60, color=n["color"], opacity=0.85, line=dict(width=2, color="white")),
            text=[n["label"]],
            textposition="bottom center",
            textfont=dict(size=11),
            showlegend=False,
            hoverinfo="skip",
        ))

    for i in range(len(nodes) - 1):
        fig_flow.add_annotation(
            x=nodes[i + 1]["x"] - 0.04, y=0.5,
            ax=nodes[i]["x"] + 0.04, ay=0.5,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=3, arrowsize=1.5, arrowwidth=2,
            arrowcolor="#555",
        )

    fig_flow.add_annotation(
        x=nodes[0]["x"], y=0.72,
        ax=nodes[-1]["x"], ay=0.72,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True,
        arrowhead=3, arrowsize=1.5, arrowwidth=2,
        arrowcolor="#2E86AB",
    )
    fig_flow.add_annotation(
        x=0.46, y=0.78, text="🔄 下一轮迭代（Loop Back）",
        showarrow=False, font=dict(size=12, color="#2E86AB"),
    )

    fig_flow.update_layout(
        xaxis=dict(range=[-0.05, 1.05], visible=False),
        yaxis=dict(range=[0.1, 0.9], visible=False),
        height=220,
        margin=dict(l=10, r=10, t=10, b=60),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_flow, key="gated_loop_flow", use_container_width=True)
    st.caption("每轮迭代在「人工审核」节点暂停（Gate），科学家确认后继续——AI不会跳过人类判断")

# Iteration Timeline
st.markdown("#### 📅 4轮迭代详情")
for it in CLOSED_LOOP_ITERATIONS:
    with st.expander(f"Round {it['round']}: {it['phase']} — {it['key_metric']}", expanded=(it['round'] == 1)):
        ic1, ic2 = st.columns(2)
        with ic1:
            st.markdown(f"**🤖 AI动作**: {it['ai_action']}")
            st.markdown(f"**🧪 湿实验**: {it['wet_action']}")
        with ic2:
            st.markdown(f"**📊 结果**: {it['result']}")
            st.markdown(f"**⏱️ 周期**: {it['duration_days']}天")
            st.markdown(f"**输入→输出**: {it['sequences_in']} → {it['sequences_out']}条")
            st.markdown(f"**最优KD**: {it['best_kd']} nM")

# Closed Loop Chart
fig_loop = plot_closed_loop(CLOSED_LOOP_ITERATIONS)
st.plotly_chart(fig_loop, key="closed_loop", use_container_width=True)

# Efficiency Summary
st.markdown("#### ⚡ 效率对比")
eff1, eff2, eff3 = st.columns(3)
with eff1:
    with st.container(border=True):
        st.markdown("**传统方法**")
        st.markdown("- 筛选: ~10,000序列/年")
        st.markdown("- 优化: 12-18个月")
        st.markdown("- 成功率: ~1%")
with eff2:
    with st.container(border=True):
        st.markdown("**AI + 干湿闭环**")
        st.markdown("- 筛选: ~10,000序列/天")
        st.markdown("- 优化: 2-4个月")
        st.markdown("- 命中率: ~8%")
with eff3:
    with st.container(border=True):
        st.markdown("**提升倍数**")
        st.markdown("- 筛选通量: **365×**")
        st.markdown("- 优化周期: **4-6×**")
        st.markdown("- 命中率: **8×**")

total_days = sum(it["duration_days"] for it in CLOSED_LOOP_ITERATIONS)
with st.container(border=True):
    st.markdown(f"#### 🤖 AI闭环总结")
    st.markdown(f"""
    经过 **{loop_rounds}轮** 干湿闭环迭代（共 **{total_days}天**），从初始100条AI生成序列中：
    - Round 1 (F2P): 100条 → 8个Hit（命中率8%），最优KD={CLOSED_LOOP_ITERATIONS[0]['best_kd']}nM
    - Round 2 (P2P): 80条变体 → 3个Lead，KD提升至{CLOSED_LOOP_ITERATIONS[1]['best_kd']}nM（**{CLOSED_LOOP_ITERATIONS[0]['best_kd']/CLOSED_LOOP_ITERATIONS[1]['best_kd']:.1f}×**提升）
    - Round 3 (P2P精细化): 30条 → 1个Lead，KD={CLOSED_LOOP_ITERATIONS[2]['best_kd']}nM（**{CLOSED_LOOP_ITERATIONS[0]['best_kd']/CLOSED_LOOP_ITERATIONS[2]['best_kd']:.0f}×**累计提升）
    - Round 4 (C2P可开发性): 5条工程化变体 → 最终候选AB-005确定

    **总亲和力提升: {improvement:.0f}×** | 传统方法同等效果需要 12-18个月，AI闭环仅需 **{total_days}天**
    """)
