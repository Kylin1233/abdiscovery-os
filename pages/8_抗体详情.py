import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import (ENTITY_ANTIBODIES, ENTITY_CELL_LINES, ENTITY_PLASMIDS,
                       ELISA_DATA, SPR_DATA, DEVELOPABILITY_DATA, PROJECTS)
from utils import render_sidebar, plot_radar_chart, kd_color, verdict_color

st.set_page_config(page_title="抗体详情 | AbDiscovery OS", page_icon="🧬", layout="wide")

render_sidebar(
    page_name="抗体详情（二级页面）",
    biomap_module="BioMap OS · 样本全流程管理",
    benchling_module="Benchling Registry · 实体详情视图",
    related_stages=[2, 3, 4, 5],
)

# ── Antibody Selection ──
drill_ab_id = st.session_state.get("drill_antibody", None)
ab_options = {ab["id"]: f"{ab['id']} — {ab['name']} ({ab['target']})" for ab in ENTITY_ANTIBODIES}
default_idx = list(ab_options.keys()).index(drill_ab_id) if drill_ab_id and drill_ab_id in ab_options else 0

sel_label = st.selectbox("选择抗体", list(ab_options.values()), index=default_idx, key="ab_sel_detail")
sel_id = sel_label.split(" — ")[0]
ab = next(a for a in ENTITY_ANTIBODIES if a["id"] == sel_id)

st.title(f"🧬 {ab['name']}")
st.caption(f"实体ID: {ab['id']} · 创建日期: {ab['created']} · 项目: {ab['project']}")

st.divider()

# ── Basic Info ──
st.subheader("📋 基本属性")
b1, b2, b3, b4, b5 = st.columns(5)
b1.metric("靶点", ab["target"])
b2.metric("格式", ab["format"])
b3.metric("来源", ab["source"])
b4.metric("KD (nM)", f"{ab['kd_nm']}")
b5.metric("Tm (°C)", f"{ab['tm_celsius']}")

# ── Sequence ──
st.subheader("🧪 序列信息")
with st.container(border=True):
    st.markdown(f"**VH 序列** ({len(ab['vh'])} aa)")
    st.code(ab["vh"], language=None)
    if ab["vl"]:
        st.markdown(f"**VL 序列** ({len(ab['vl'])} aa)")
        st.code(ab["vl"], language=None)
    else:
        st.markdown("**VL 序列**: *N/A — 单域抗体(VHH)无VL*")
    st.markdown(f"**CDR-H3**: `{ab['cdr_h3']}` ({len(ab['cdr_h3'])} aa)")

st.divider()

# ── Experimental Data ──
st.subheader("📊 实验数据汇总")

tab_elisa, tab_spr, tab_dev = st.tabs(["🔴 ELISA", "📈 SPR", "📋 可开发性"])

with tab_elisa:
    elisa_record = next((e for e in ELISA_DATA if e["antibody_id"] == sel_id), None)
    if elisa_record:
        ec1, ec2, ec3, ec4 = st.columns(4)
        ec1.metric("OD450", f"{elisa_record['od450']}")
        ec2.metric("EC50 (nM)", f"{elisa_record['ec50_nm']}")
        ec3.metric("最大结合率", f"{elisa_record['max_binding_pct']}%")
        ec4.metric("判定", f"{verdict_color(elisa_record['verdict'])} {elisa_record['verdict']}")
    else:
        st.info("暂无ELISA数据")

with tab_spr:
    spr_record = next((s for s in SPR_DATA if s["antibody_id"] == sel_id), None)
    if spr_record:
        sc1, sc2, sc3, sc4, sc5 = st.columns(5)
        sc1.metric("ka (1/Ms)", f"{spr_record['ka_per_ms']:.2e}")
        sc2.metric("kd (1/s)", f"{spr_record['kd_per_s']:.2e}")
        sc3.metric("KD (nM)", f"{spr_record['kd_nm']}")
        sc4.metric("Chi²", f"{spr_record['chi2']}")
        sc5.metric("判定", f"{verdict_color(spr_record['verdict'])} {spr_record['verdict']}")

        st.markdown("**SPR Sensorgram（模拟）**")
        import numpy as np
        t_assoc = np.linspace(0, 300, 300)
        t_dissoc = np.linspace(300, 600, 300)
        conc = 50e-9
        kobs = spr_record["ka_per_ms"] * conc + spr_record["kd_per_s"]
        req = 100 * (spr_record["ka_per_ms"] * conc) / kobs
        r_assoc = req * (1 - np.exp(-kobs * t_assoc))
        r_at_end = r_assoc[-1]
        r_dissoc = r_at_end * np.exp(-spr_record["kd_per_s"] * (t_dissoc - 300))

        fig_spr = go.Figure()
        fig_spr.add_trace(go.Scatter(
            x=np.concatenate([t_assoc, t_dissoc]),
            y=np.concatenate([r_assoc, r_dissoc]),
            mode="lines", line=dict(width=3, color="#636EFA"),
            name=ab["name"],
        ))
        fig_spr.add_vline(x=300, line_dash="dash", line_color="gray")
        fig_spr.update_layout(
            xaxis_title="时间 (s)", yaxis_title="Response (RU)",
            height=300, margin=dict(l=60, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_spr, key="ab_spr", use_container_width=True)
    else:
        st.info("暂无SPR数据")

with tab_dev:
    dev_record = next((d for d in DEVELOPABILITY_DATA if d["antibody_id"] == sel_id), None)
    if dev_record:
        dc1, dc2, dc3, dc4, dc5 = st.columns(5)
        dc1.metric("Tm (°C)", f"{dev_record['tm_celsius']}")
        dc2.metric("聚集 (%)", f"{dev_record['aggregation_pct']}")
        dc3.metric("粘度 (cP)", f"{dev_record['viscosity_cp']}")
        dc4.metric("免疫原性", f"{dev_record['immunogenicity_score']}")
        dc5.metric("综合", f"{verdict_color(dev_record['overall'])} {dev_record['overall']}")

        st.markdown(f"**AI建议**: {dev_record['recommendation']}")

        categories = ["热稳定性", "低聚集", "低粘度", "低免疫原性", "化学稳定性"]
        tm_score = min(100, max(0, (dev_record["tm_celsius"] - 60) * 5))
        agg_score = min(100, max(0, 100 - dev_record["aggregation_pct"] * 15))
        visc_score = min(100, max(0, 100 - dev_record["viscosity_cp"] * 4))
        immu_score = min(100, max(0, 100 - dev_record["immunogenicity_score"] * 3))
        chem_score = {"优秀": 95, "良好": 75, "一般": 45}.get(dev_record["chemical_stability"], 50)

        fig_radar = plot_radar_chart(categories, {ab["name"]: [tm_score, agg_score, visc_score, immu_score, chem_score]})
        st.plotly_chart(fig_radar, key="ab_dev_radar", use_container_width=True)
    else:
        st.info("暂无可开发性评估数据")

st.divider()

# ── Related Entities ──
st.subheader("🔗 关联实体")

related_cls = [cl for cl in ENTITY_CELL_LINES if cl["antibody_id"] == sel_id]
related_pls = [pl for pl in ENTITY_PLASMIDS if sel_id in pl.get("insert", "")]

r1, r2 = st.columns(2)
with r1:
    st.markdown(f"**关联细胞株** ({len(related_cls)}个)")
    if related_cls:
        for cl in related_cls:
            with st.container(border=True):
                st.markdown(f"**{cl['name']}** ({cl['id']})")
                st.caption(f"{cl['host']} · 滴度 {cl['titer_mg_l']} mg/L · 活力 {cl['viability_pct']}% · {cl['status']}")
    else:
        st.caption("暂无关联细胞株")

with r2:
    st.markdown(f"**关联质粒** ({len(related_pls)}个)")
    if related_pls:
        for pl in related_pls:
            with st.container(border=True):
                st.markdown(f"**{pl['name']}** ({pl['id']})")
                st.caption(f"骨架: {pl['backbone']} · 启动子: {pl['promoter']} · 抗性: {pl['selection']}")
    else:
        st.caption("暂无关联质粒")

st.divider()

# ── Affinity Evolution Context ──
same_target_abs = sorted(
    [a for a in ENTITY_ANTIBODIES if a["target"] == ab["target"]],
    key=lambda x: x["kd_nm"], reverse=True,
)

if len(same_target_abs) >= 2:
    st.subheader(f"📈 {ab['target']}靶点亲和力进化")
    fig_evo = go.Figure()
    fig_evo.add_trace(go.Bar(
        x=[a["name"] for a in same_target_abs],
        y=[a["kd_nm"] for a in same_target_abs],
        marker_color=[("#2E86AB" if a["id"] == sel_id else "#636EFA" if "AI" in a["source"] else "#EF553B") for a in same_target_abs],
        text=[f"{a['kd_nm']}nM" for a in same_target_abs],
        textposition="outside",
    ))
    fig_evo.update_layout(
        yaxis_title="KD (nM)", yaxis_type="log",
        height=300, margin=dict(l=60, r=20, t=10, b=60),
        annotations=[
            dict(x=0.5, y=-0.22, xref="paper", yref="paper",
                 text="🔵 当前抗体  🔵 AI生成  🔴 传统筛选", showarrow=False, font=dict(size=11)),
        ],
    )
    st.plotly_chart(fig_evo, key="ab_evo", use_container_width=True)

# ── Back button ──
st.divider()
proj_info = next((p for p in PROJECTS if p["id"] == ab.get("project")), None)
if proj_info:
    if st.button(f"← 返回项目 {proj_info['name']}", key="back_to_proj"):
        st.session_state["drill_project"] = proj_info["id"]
        st.switch_page("pages/7_项目详情.py")
