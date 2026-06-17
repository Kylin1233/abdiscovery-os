import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import ELISA_DATA, SPR_DATA, EXPRESSION_DATA, ENTITY_ANTIBODIES, ENTITY_CELL_LINES
from utils import render_sidebar, plot_dose_response, kd_color, verdict_color

st.set_page_config(page_title="实验数据管理 | AbDiscovery OS", page_icon="🧪", layout="wide")

render_sidebar(
    page_name="实验数据管理",
    biomap_module="BioMap OS · 实验数据记录模块",
    benchling_module="Benchling Notebook + Structured Tables",
    related_stages=[3, 4, 5],
)

st.title("🧪 实验数据管理")
st.markdown("结构化实验数据表 — 对标 **Benchling Structured Tables**（结合活性/动力学/表达）")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("ELISA记录", f"{len(ELISA_DATA)}条")
c2.metric("SPR记录", f"{len(SPR_DATA)}条")
c3.metric("表达数据", f"{len(EXPRESSION_DATA)}条")
best_kd = min(s["kd_nm"] for s in SPR_DATA)
c4.metric("最优KD", f"{best_kd} nM")

st.divider()

# ── Structured Tables ──
tab_elisa, tab_spr, tab_expr = st.tabs(["🔴 ELISA 结合活性", "📈 SPR 动力学", "🧫 细胞表达"])

# ─── ELISA ───
with tab_elisa:
    st.markdown("### ELISA 结合活性检测")
    st.markdown("**Structured Table**: 抗原包被 → 梯度抗体 → HRP标记二抗 → TMB显色 → OD450读取")

    elisa_display = []
    for e in ELISA_DATA:
        elisa_display.append({
            "抗体ID": e["antibody_id"],
            "名称": e["name"],
            "靶点": e["target"],
            "抗原浓度 (μg/mL)": e["antigen_conc_ug_ml"],
            "OD450": e["od450"],
            "EC50 (nM)": e["ec50_nm"],
            "最大结合率 (%)": e["max_binding_pct"],
            "判定": f"{verdict_color(e['verdict'])} {e['verdict']}",
        })
    df_elisa = pd.DataFrame(elisa_display)
    st.dataframe(df_elisa, hide_index=True, use_container_width=True)

    st.markdown("#### 📊 剂量-响应曲线")
    sel_elisa = st.multiselect(
        "选择抗体对比",
        [e["name"] for e in ELISA_DATA],
        default=[ELISA_DATA[0]["name"], ELISA_DATA[-1]["name"]],
        key="elisa_sel",
    )
    if sel_elisa:
        selected = [e for e in ELISA_DATA if e["name"] in sel_elisa]
        fig_dr = plot_dose_response(selected)
        st.plotly_chart(fig_dr, key="dose_response", use_container_width=True)

# ─── SPR ───
with tab_spr:
    st.markdown("### SPR / Biacore 动力学检测")
    st.markdown("**Structured Table**: 抗体固定 → 梯度抗原流过 → 实时监测结合/解离 → 动力学拟合")

    spr_display = []
    for s in SPR_DATA:
        spr_display.append({
            "抗体ID": s["antibody_id"],
            "名称": s["name"],
            "ka (1/Ms)": f"{s['ka_per_ms']:.2e}",
            "kd (1/s)": f"{s['kd_per_s']:.2e}",
            "KD (nM)": s["kd_nm"],
            "亲和力": kd_color(s["kd_nm"]),
            "Chi²": s["chi2"],
            "判定": f"{verdict_color(s['verdict'])} {s['verdict']}",
        })
    df_spr = pd.DataFrame(spr_display)
    st.dataframe(df_spr, hide_index=True, use_container_width=True)

    abnormal = [s for s in SPR_DATA if s["chi2"] > 0.4]
    if abnormal:
        st.warning(f"⚠️ 异常预警：{len(abnormal)}条记录Chi²拟合度偏高（>0.4），建议检查实验条件")

    st.markdown("#### 📊 亲和力演进趋势")
    st.markdown("从噬菌体展示到AI优化，观察KD逐步改善的过程（PD-L1靶点为例）")

    pdl1_spr = [s for s in SPR_DATA if "PDL1" in s["name"]]
    if pdl1_spr:
        import plotly.graph_objects as go
        fig_trend = go.Figure()
        names = [s["name"] for s in pdl1_spr]
        kds = [s["kd_nm"] for s in pdl1_spr]
        sources = []
        for s in pdl1_spr:
            ab = next((a for a in ENTITY_ANTIBODIES if a["id"] == s["antibody_id"]), None)
            sources.append(ab["source"] if ab else "")

        bar_colors = ["#EF553B" if "AI" not in src else "#636EFA" for src in sources]

        fig_trend.add_trace(go.Bar(
            x=names, y=kds,
            marker_color=bar_colors,
            text=[f"{kd}nM" for kd in kds],
            textposition="outside",
        ))
        fig_trend.update_layout(
            title="PD-L1抗体亲和力成熟过程",
            yaxis_title="KD (nM)",
            yaxis_type="log",
            height=350,
            margin=dict(l=60, r=20, t=40, b=40),
            annotations=[
                dict(x=0.5, y=-0.15, xref="paper", yref="paper",
                     text="🔴 传统筛选  🔵 AI设计/优化", showarrow=False, font=dict(size=12)),
            ],
        )
        st.plotly_chart(fig_trend, key="kd_trend", use_container_width=True)

# ─── Expression ───
with tab_expr:
    st.markdown("### 细胞表达数据")
    st.markdown("**Structured Table**: 细胞培养 → 取样 → 滴度测定(Protein A HPLC) → 活力测定(Vi-Cell)")

    expr_display = []
    for e in EXPRESSION_DATA:
        expr_display.append({
            "细胞株ID": e["cell_line_id"],
            "名称": e["name"],
            "培养天数": e["day"],
            "滴度 (mg/L)": e["titer_mg_l"],
            "活力 (%)": e["viability_pct"],
            "判定": f"{verdict_color(e['verdict'])} {e['verdict']}",
        })
    df_expr = pd.DataFrame(expr_display)
    st.dataframe(df_expr, hide_index=True, use_container_width=True)

    low_viability = [e for e in EXPRESSION_DATA if e["viability_pct"] < 92]
    if low_viability:
        st.warning(f"⚠️ 异常预警：{len(low_viability)}个细胞株活力偏低（<92%），建议检查培养条件")

    st.markdown("#### 📊 表达量对比")
    import plotly.graph_objects as go
    fig_expr = go.Figure()
    fig_expr.add_trace(go.Bar(
        x=[e["name"] for e in EXPRESSION_DATA],
        y=[e["titer_mg_l"] for e in EXPRESSION_DATA],
        marker_color=["#00CC96" if e["titer_mg_l"] >= 500 else "#FFA15A" if e["titer_mg_l"] >= 200 else "#EF553B" for e in EXPRESSION_DATA],
        text=[f"{e['titer_mg_l']} mg/L" for e in EXPRESSION_DATA],
        textposition="outside",
    ))
    fig_expr.add_hline(y=500, line_dash="dash", line_color="green", annotation_text="目标线: 500 mg/L")
    fig_expr.update_layout(
        title="细胞株表达量对比",
        yaxis_title="滴度 (mg/L)",
        height=350,
        margin=dict(l=60, r=20, t=40, b=40),
    )
    st.plotly_chart(fig_expr, key="expr_bar", use_container_width=True)

st.divider()

# ── Multi-candidate comparison ──
st.subheader("⚖️ 多候选抗体对比")
st.markdown("选择多个抗体进行多维对比（对标 Benchling Insights 聚合分析）")

all_names = [ab["name"] for ab in ENTITY_ANTIBODIES if ab["kd_nm"] < 15]
sel_compare = st.multiselect("选择对比抗体", all_names, default=all_names[:4], key="compare_sel")

if len(sel_compare) >= 2:
    from utils import plot_radar_chart
    categories = ["亲和力", "热稳定性", "表达量", "来源评分", "综合评分"]

    values_dict = {}
    for name in sel_compare:
        ab = next(a for a in ENTITY_ANTIBODIES if a["name"] == name)
        kd_score = max(0, 100 - ab["kd_nm"] * 5)
        tm_score = max(0, (ab["tm_celsius"] - 60) * 5)
        expr_score = (ab["expression_mg_l"] / 1.5) if ab["expression_mg_l"] else 30
        source_score = 85 if "AI" in ab["source"] else 60
        overall = (kd_score + tm_score + expr_score + source_score) / 4
        values_dict[name] = [min(100, kd_score), min(100, tm_score), min(100, expr_score), source_score, min(100, overall)]

    fig_radar = plot_radar_chart(categories, values_dict, "候选抗体多维对比")
    st.plotly_chart(fig_radar, key="compare_radar", use_container_width=True)

st.divider()

# ── Data Entry Form ──
st.subheader("📝 新增实验数据")
st.markdown("直接在平台内录入实验结果（对标 Benchling Notebook 内嵌表单，科学家零切换成本）")

entry_type = st.selectbox("选择实验类型", ["ELISA 结合活性", "SPR 动力学", "细胞表达"], key="entry_type")

with st.form("data_entry_form"):
    if entry_type == "ELISA 结合活性":
        ef1, ef2 = st.columns(2)
        with ef1:
            entry_ab = st.selectbox("抗体ID", [ab["id"] + " — " + ab["name"] for ab in ENTITY_ANTIBODIES], key="entry_ab_elisa")
            entry_target = st.selectbox("靶点", ["PD-L1", "HER2", "TNFα", "IL-17A", "CD20"], key="entry_target_elisa")
            entry_conc = st.number_input("抗原浓度 (μg/mL)", value=1.0, min_value=0.01, step=0.1, key="entry_conc")
        with ef2:
            entry_od = st.number_input("OD450", value=2.0, min_value=0.0, max_value=4.0, step=0.01, key="entry_od")
            entry_ec50 = st.number_input("EC50 (nM)", value=5.0, min_value=0.01, step=0.1, key="entry_ec50")
            entry_maxb = st.number_input("最大结合率 (%)", value=90.0, min_value=0.0, max_value=100.0, step=1.0, key="entry_maxb")

    elif entry_type == "SPR 动力学":
        ef1, ef2 = st.columns(2)
        with ef1:
            entry_ab = st.selectbox("抗体ID", [ab["id"] + " — " + ab["name"] for ab in ENTITY_ANTIBODIES], key="entry_ab_spr")
            entry_ka = st.number_input("ka (1/Ms)", value=5.0e5, format="%.2e", key="entry_ka")
            entry_kd_rate = st.number_input("kd (1/s)", value=1.0e-3, format="%.2e", key="entry_kd_rate")
        with ef2:
            entry_kd_val = st.number_input("KD (nM)", value=2.0, min_value=0.001, step=0.1, key="entry_kd_val")
            entry_chi2 = st.number_input("Chi²", value=0.2, min_value=0.0, step=0.01, key="entry_chi2")

    else:
        ef1, ef2 = st.columns(2)
        with ef1:
            entry_cl = st.selectbox("细胞株ID", [cl["id"] + " — " + cl["name"] for cl in ENTITY_CELL_LINES], key="entry_cl_expr")
            entry_day = st.number_input("培养天数", value=14, min_value=1, max_value=30, key="entry_day")
        with ef2:
            entry_titer = st.number_input("滴度 (mg/L)", value=500.0, min_value=0.0, step=10.0, key="entry_titer")
            entry_viab = st.number_input("活力 (%)", value=95.0, min_value=0.0, max_value=100.0, step=0.1, key="entry_viab")

    entry_note = st.text_area("实验备注（可选）", height=68, key="entry_note")
    submitted = st.form_submit_button("📥 提交实验数据", type="primary", use_container_width=True)

    if submitted:
        st.success("✅ 数据已提交并自动写入 Structured Table（Demo模式，数据未持久化）")
        st.info("📎 系统自动关联实体ID、校验数据范围、触发异常检测规则")

st.divider()

# ── Design Philosophy ──
with st.container(border=True):
    st.markdown("### 💡 结构化数据采集设计理念")
    st.markdown("""
    > **"科学家用最好的工具做实验，企业无缝提取结构化数据"** — Benchling Structured Tables 设计哲学

    本页面的三类实验表（ELISA / SPR / 表达）均采用 **Structured Table** 设计：
    - 每种实验类型有预定义的 Schema（字段名、数据类型、取值范围、异常阈值）
    - 科学家在记录实验结果时，数据自动结构化、可查询、可聚合
    - 系统自动执行异常检测和预警（如 Chi² > 0.4、活力 < 92%）
    - 所有数据与实体注册中心的抗体/细胞株 ID 关联，实现全链路溯源
    """)
