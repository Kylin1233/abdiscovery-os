import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import (PROJECTS, ENTITY_ANTIBODIES, ELISA_DATA, SPR_DATA,
                       EXPRESSION_DATA, DEVELOPABILITY_DATA, ENTITY_CELL_LINES)
from utils import render_sidebar, plot_spr_sensorgram, plot_dose_response, kd_color, verdict_color

st.set_page_config(page_title="实验报告 | AbDiscovery OS", page_icon="📄", layout="wide")

render_sidebar(
    page_name="实验报告（二级页面）",
    biomap_module="BioMap OS · 实验数据记录",
    benchling_module="Benchling Notebook · 实验报告视图",
    related_stages=[3, 4, 5],
)

# ── Project Selection ──
drill_proj = st.session_state.get("drill_report_project", None)
proj_options = {p["id"]: f"{p['id']} — {p['name']}" for p in PROJECTS}
default_idx = list(proj_options.keys()).index(drill_proj) if drill_proj and drill_proj in proj_options else 0

sel_label = st.selectbox("选择项目", list(proj_options.values()), index=default_idx, key="report_proj")
sel_id = sel_label.split(" — ")[0]
proj = next(p for p in PROJECTS if p["id"] == sel_id)

st.title(f"📄 实验报告 · {proj['name']}")
st.caption(f"自动聚合 {proj['id']} 项目下所有实验数据，生成综合报告")

st.divider()

# ── Gather project data ──
proj_abs = [ab for ab in ENTITY_ANTIBODIES if ab.get("project") == sel_id]
proj_ab_ids = {ab["id"] for ab in proj_abs}
proj_elisa = [e for e in ELISA_DATA if e["antibody_id"] in proj_ab_ids]
proj_spr = [s for s in SPR_DATA if s["antibody_id"] in proj_ab_ids]
proj_cls = [cl for cl in ENTITY_CELL_LINES if cl.get("project") == sel_id]
proj_cl_ids = {cl["id"] for cl in proj_cls}
proj_expr = [e for e in EXPRESSION_DATA if e["cell_line_id"] in proj_cl_ids]
proj_dev = [d for d in DEVELOPABILITY_DATA if d["antibody_id"] in proj_ab_ids]

# ── Report Summary ──
st.subheader("📊 报告摘要")
r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("抗体序列", f"{len(proj_abs)}条")
r2.metric("ELISA数据", f"{len(proj_elisa)}条")
r3.metric("SPR数据", f"{len(proj_spr)}条")
r4.metric("细胞株", f"{len(proj_cls)}个")
r5.metric("可开发性", f"{len(proj_dev)}条")

if not proj_abs:
    st.warning("该项目暂无实验数据")
    st.stop()

st.divider()

# ═══════════════════════════════════
# Section 1: ELISA
# ═══════════════════════════════════
if proj_elisa:
    st.subheader("🔴 ELISA 结合活性报告")

    elisa_tbl = []
    for e in proj_elisa:
        elisa_tbl.append({
            "抗体": e["name"],
            "靶点": e["target"],
            "OD450": e["od450"],
            "EC50 (nM)": e["ec50_nm"],
            "最大结合率 (%)": e["max_binding_pct"],
            "判定": f"{verdict_color(e['verdict'])} {e['verdict']}",
        })
    st.dataframe(pd.DataFrame(elisa_tbl), hide_index=True, use_container_width=True)

    st.markdown("#### 剂量-响应曲线")
    fig_dr = plot_dose_response(proj_elisa)
    st.plotly_chart(fig_dr, key="report_dr", use_container_width=True)

    with st.container(border=True):
        best_elisa = min(proj_elisa, key=lambda x: x["ec50_nm"])
        st.markdown(f"**AI结论**: 最优结合活性候选为 **{best_elisa['name']}**（EC50 = {best_elisa['ec50_nm']} nM, 最大结合率 {best_elisa['max_binding_pct']}%）")

    st.divider()

# ═══════════════════════════════════
# Section 2: SPR
# ═══════════════════════════════════
if proj_spr:
    st.subheader("📈 SPR 动力学报告")

    spr_tbl = []
    for s in proj_spr:
        spr_tbl.append({
            "抗体": s["name"],
            "ka (1/Ms)": f"{s['ka_per_ms']:.2e}",
            "kd (1/s)": f"{s['kd_per_s']:.2e}",
            "KD (nM)": s["kd_nm"],
            "亲和力": kd_color(s["kd_nm"]),
            "Chi²": s["chi2"],
            "判定": f"{verdict_color(s['verdict'])} {s['verdict']}",
        })
    st.dataframe(pd.DataFrame(spr_tbl), hide_index=True, use_container_width=True)

    st.markdown("#### Sensorgram 叠加")
    fig_spr = plot_spr_sensorgram(proj_spr)
    st.plotly_chart(fig_spr, key="report_spr", use_container_width=True)

    st.markdown("#### 亲和力排名")
    sorted_spr = sorted(proj_spr, key=lambda x: x["kd_nm"])
    fig_rank = go.Figure(go.Bar(
        x=[s["name"] for s in sorted_spr],
        y=[s["kd_nm"] for s in sorted_spr],
        marker_color=[("#00CC96" if s["kd_nm"] < 1 else "#FFA15A" if s["kd_nm"] < 10 else "#EF553B") for s in sorted_spr],
        text=[f"{s['kd_nm']}nM" for s in sorted_spr],
        textposition="outside",
    ))
    fig_rank.update_layout(
        yaxis_title="KD (nM)", yaxis_type="log",
        height=300, margin=dict(l=60, r=20, t=10, b=40),
    )
    st.plotly_chart(fig_rank, key="report_rank", use_container_width=True)

    with st.container(border=True):
        best_spr = min(proj_spr, key=lambda x: x["kd_nm"])
        st.markdown(f"""
        **AI结论**: 最优亲和力候选为 **{best_spr['name']}**
        - KD = {best_spr['kd_nm']} nM {kd_color(best_spr['kd_nm'])}
        - ka = {best_spr['ka_per_ms']:.2e} M⁻¹s⁻¹（快速结合）
        - kd = {best_spr['kd_per_s']:.2e} s⁻¹（慢速解离，药效持久）
        - 拟合质量 Chi² = {best_spr['chi2']}（{verdict_color(best_spr['verdict'])} {best_spr['verdict']}）
        """)

    st.divider()

# ═══════════════════════════════════
# Section 3: Expression
# ═══════════════════════════════════
if proj_expr:
    st.subheader("🧫 细胞表达报告")

    expr_tbl = []
    for e in proj_expr:
        expr_tbl.append({
            "细胞株": e["name"],
            "培养天数": e["day"],
            "滴度 (mg/L)": e["titer_mg_l"],
            "活力 (%)": e["viability_pct"],
            "判定": f"{verdict_color(e['verdict'])} {e['verdict']}",
        })
    st.dataframe(pd.DataFrame(expr_tbl), hide_index=True, use_container_width=True)

    fig_expr = go.Figure()
    fig_expr.add_trace(go.Bar(
        x=[e["name"] for e in proj_expr],
        y=[e["titer_mg_l"] for e in proj_expr],
        marker_color=["#00CC96" if e["titer_mg_l"] >= 500 else "#FFA15A" for e in proj_expr],
        text=[f"{e['titer_mg_l']} mg/L" for e in proj_expr],
        textposition="outside",
    ))
    fig_expr.add_hline(y=500, line_dash="dash", line_color="green", annotation_text="目标: 500 mg/L")
    fig_expr.update_layout(yaxis_title="滴度 (mg/L)", height=300, margin=dict(l=60, r=20, t=10, b=40))
    st.plotly_chart(fig_expr, key="report_expr", use_container_width=True)

    st.divider()

# ═══════════════════════════════════
# Section 4: Developability
# ═══════════════════════════════════
if proj_dev:
    st.subheader("📋 可开发性评估报告")

    dev_tbl = []
    for d in proj_dev:
        dev_tbl.append({
            "抗体": d["name"],
            "Tm (°C)": d["tm_celsius"],
            "聚集 (%)": d["aggregation_pct"],
            "粘度 (cP)": d["viscosity_cp"],
            "免疫原性": d["immunogenicity_score"],
            "综合": f"{verdict_color(d['overall'])} {d['overall']}",
            "建议": d["recommendation"],
        })
    st.dataframe(pd.DataFrame(dev_tbl), hide_index=True, use_container_width=True)

    st.divider()

# ═══════════════════════════════════
# Overall Conclusion
# ═══════════════════════════════════
st.subheader("🤖 AI综合报告结论")

with st.container(border=True):
    best_candidates = []
    if proj_spr:
        best_spr = min(proj_spr, key=lambda x: x["kd_nm"])
        best_candidates.append(f"亲和力最优: **{best_spr['name']}** (KD={best_spr['kd_nm']}nM)")
    if proj_dev:
        passed_dev = [d for d in proj_dev if d["overall"] == "通过"]
        if passed_dev:
            for d in passed_dev:
                best_candidates.append(f"可开发性通过: **{d['name']}** (Tm={d['tm_celsius']}°C)")

    st.markdown(f"**项目 {proj['name']}** 实验数据综合分析：")
    for c in best_candidates:
        st.markdown(f"- {c}")

    if not best_candidates:
        st.markdown("- 项目处于早期阶段，数据积累中")

    st.markdown(f"""

    **下一步建议**:
    - {"推进最优候选进入下一阶段" if best_candidates else "继续筛选和优化"}
    - 补充缺失的实验数据（如可开发性评估、表达优化）
    - 定期回顾项目数据，利用AI闭环加速迭代
    """)

# ── Navigation ──
st.divider()
bc1, bc2 = st.columns(2)
with bc1:
    if st.button("← 返回项目详情", key="back_proj"):
        st.session_state["drill_project"] = sel_id
        st.switch_page("pages/7_项目详情.py")
with bc2:
    if st.button("← 返回实验数据管理", key="back_exp"):
        st.switch_page("pages/4_实验数据管理.py")
