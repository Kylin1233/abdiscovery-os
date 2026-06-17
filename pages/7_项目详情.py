import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import (PROJECTS, PIPELINE_STAGES, ENTITY_ANTIBODIES, ENTITY_CELL_LINES,
                       ENTITY_PLASMIDS, ELISA_DATA, SPR_DATA, EXPRESSION_DATA,
                       DEVELOPABILITY_DATA, RECENT_ACTIVITIES, CLOSED_LOOP_ITERATIONS)
from utils import render_sidebar, kd_color, verdict_color

st.set_page_config(page_title="项目详情 | AbDiscovery OS", page_icon="📁", layout="wide")

render_sidebar(
    page_name="项目详情（二级页面）",
    biomap_module="BioMap OS · 项目追踪",
    benchling_module="Benchling Workflows · 项目视图",
    related_stages=[1, 2, 3, 4, 5, 6, 7, 8],
)

# ── Project Selection ──
drill_id = st.session_state.get("drill_project", None)

project_options = {p["id"]: f"{p['id']} — {p['name']}" for p in PROJECTS}
default_idx = list(project_options.keys()).index(drill_id) if drill_id and drill_id in project_options else 0

sel_proj_label = st.selectbox("选择项目", list(project_options.values()), index=default_idx, key="proj_sel_detail")
sel_proj_id = sel_proj_label.split(" — ")[0]
proj = next(p for p in PROJECTS if p["id"] == sel_proj_id)

st.title(f"📁 {proj['name']}")
st.caption(f"项目编号: {proj['id']} · 启动日期: {proj['start_date']}")

st.divider()

# ── Project KPI ──
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("靶点", proj["target"])
k2.metric("格式", proj["format"])
k3.metric("阶段", proj["stage"])
k4.metric("进度", f"{proj['progress']}%")
k5.metric("Lead候选", f"{proj['lead_count']}个")

# ── Pipeline Progress ──
st.subheader("📊 管线推进状态")
stage_colors = []
for s in PIPELINE_STAGES:
    if s["id"] < proj["stage_id"]:
        stage_colors.append("#00CC96")
    elif s["id"] == proj["stage_id"]:
        stage_colors.append("#636EFA")
    else:
        stage_colors.append("#E0E0E0")

fig_progress = go.Figure(go.Bar(
    x=[s["name"] for s in PIPELINE_STAGES],
    y=[1] * len(PIPELINE_STAGES),
    marker_color=stage_colors,
    text=[s["icon"] for s in PIPELINE_STAGES],
    textposition="inside",
    textfont=dict(size=16),
    hovertext=[f"{s['name']}\n{'✅ 已完成' if s['id'] < proj['stage_id'] else '🔵 进行中' if s['id'] == proj['stage_id'] else '⬜ 待开始'}" for s in PIPELINE_STAGES],
    hoverinfo="text",
))
fig_progress.update_layout(
    height=80, margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
    yaxis=dict(visible=False),
    bargap=0.05,
)
st.plotly_chart(fig_progress, key="proj_pipeline", use_container_width=True)
st.caption("🟢 已完成  🔵 进行中  ⬜ 待开始")

st.divider()

# ── Project Antibodies ──
proj_abs = [ab for ab in ENTITY_ANTIBODIES if ab.get("project") == sel_proj_id]
st.subheader(f"🧬 项目抗体序列 ({len(proj_abs)}条)")

if proj_abs:
    ab_data = []
    for ab in proj_abs:
        ab_data.append({
            "ID": ab["id"],
            "名称": ab["name"],
            "来源": ab["source"],
            "CDR-H3": ab["cdr_h3"],
            "KD (nM)": ab["kd_nm"],
            "亲和力": kd_color(ab["kd_nm"]),
            "Tm (°C)": ab["tm_celsius"],
            "表达量": f"{ab['expression_mg_l']:.0f}" if ab["expression_mg_l"] else "—",
            "创建日期": ab["created"],
        })
    df_proj_ab = pd.DataFrame(ab_data)
    st.dataframe(df_proj_ab, hide_index=True, use_container_width=True)

    for ab in proj_abs:
        if st.button(f"查看 {ab['name']} 详情 →", key=f"ab_detail_{ab['id']}"):
            st.session_state["drill_antibody"] = ab["id"]
            st.switch_page("pages/8_抗体详情.py")

    # Affinity ranking
    if len(proj_abs) >= 2:
        st.markdown("#### 📈 亲和力排名")
        sorted_abs = sorted(proj_abs, key=lambda x: x["kd_nm"])
        fig_rank = go.Figure(go.Bar(
            x=[ab["name"] for ab in sorted_abs],
            y=[ab["kd_nm"] for ab in sorted_abs],
            marker_color=[("#00CC96" if ab["kd_nm"] < 1 else "#FFA15A" if ab["kd_nm"] < 10 else "#EF553B") for ab in sorted_abs],
            text=[f"{ab['kd_nm']}nM" for ab in sorted_abs],
            textposition="outside",
        ))
        fig_rank.update_layout(
            yaxis_title="KD (nM)", yaxis_type="log",
            height=300, margin=dict(l=60, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_rank, key="proj_ab_rank", use_container_width=True)
else:
    st.info("该项目暂无已注册抗体序列")

st.divider()

# ── Project Cell Lines ──
proj_cls = [cl for cl in ENTITY_CELL_LINES if cl.get("project") == sel_proj_id]
st.subheader(f"🔬 项目细胞株 ({len(proj_cls)}个)")

if proj_cls:
    cl_data = []
    for cl in proj_cls:
        cl_data.append({
            "ID": cl["id"],
            "名称": cl["name"],
            "宿主": cl["host"],
            "滴度 (mg/L)": cl["titer_mg_l"],
            "活力 (%)": cl["viability_pct"],
            "状态": cl["status"],
            "位置": cl["location"],
        })
    st.dataframe(pd.DataFrame(cl_data), hide_index=True, use_container_width=True)
else:
    st.info("该项目暂无已构建细胞株")

st.divider()

# ── Experiment Summary ──
proj_ab_ids = {ab["id"] for ab in proj_abs}
proj_elisa = [e for e in ELISA_DATA if e["antibody_id"] in proj_ab_ids]
proj_spr = [s for s in SPR_DATA if s["antibody_id"] in proj_ab_ids]

st.subheader("🧪 项目实验数据汇总")
e1, e2, e3 = st.columns(3)
e1.metric("ELISA记录", f"{len(proj_elisa)}条")
e2.metric("SPR记录", f"{len(proj_spr)}条")

proj_dev = [d for d in DEVELOPABILITY_DATA if d["antibody_id"] in proj_ab_ids]
e3.metric("可开发性评估", f"{len(proj_dev)}条")

if proj_elisa:
    st.markdown("**ELISA 结合活性**")
    elisa_tbl = []
    for e in proj_elisa:
        elisa_tbl.append({
            "抗体": e["name"],
            "EC50 (nM)": e["ec50_nm"],
            "最大结合率": f"{e['max_binding_pct']}%",
            "判定": f"{verdict_color(e['verdict'])} {e['verdict']}",
        })
    st.dataframe(pd.DataFrame(elisa_tbl), hide_index=True, use_container_width=True)

if proj_spr:
    st.markdown("**SPR 动力学**")
    spr_tbl = []
    for s in proj_spr:
        spr_tbl.append({
            "抗体": s["name"],
            "KD (nM)": s["kd_nm"],
            "亲和力": kd_color(s["kd_nm"]),
            "判定": f"{verdict_color(s['verdict'])} {s['verdict']}",
        })
    st.dataframe(pd.DataFrame(spr_tbl), hide_index=True, use_container_width=True)

    if st.button("查看完整实验报告 →", key="to_exp_report"):
        st.session_state["drill_report_project"] = sel_proj_id
        st.switch_page("pages/9_实验报告.py")

st.divider()

# ── Recent Activities ──
proj_activities = [a for a in RECENT_ACTIVITIES if a["project"] == sel_proj_id]
st.subheader(f"📋 项目动态 ({len(proj_activities)}条)")
if proj_activities:
    for act in proj_activities:
        with st.container(border=True):
            ac1, ac2 = st.columns([1, 8])
            ac1.markdown(f"### {act['icon']}")
            ac2.markdown(f"**{act['event']}**")
            ac2.caption(act['time'])
else:
    st.info("暂无动态")
