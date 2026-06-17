import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import TARGET_RESEARCH
from utils import render_sidebar, plot_radar_chart

st.set_page_config(page_title="靶点研究 | AbDiscovery OS", page_icon="🎯", layout="wide")

render_sidebar(
    page_name="靶点研究",
    biomap_module="BioMap OS · xTrimo发现助手",
    benchling_module="Benchling Deep Research Agent",
    related_stages=[1],
)

st.title("🎯 靶点研究")
st.markdown("多源靶点情报聚合 + AI可药性评估 — 对标 **Benchling Deep Research Agent + BioMap发现助手**")

# ── Target Selection ──
targets = list(TARGET_RESEARCH.keys())
sel_target = st.selectbox("选择靶点", targets, key="target_sel")
data = TARGET_RESEARCH[sel_target]

st.divider()

# ── Target Info Card ──
st.subheader(f"📋 {sel_target} 靶点基本信息")
ic1, ic2, ic3, ic4 = st.columns(4)
ic1.metric("基因名", data["gene"])
ic2.metric("UniProt ID", data["uniprot"])
ic3.metric("蛋白家族", data["protein_family"][:12])
ic4.metric("分子量", data["molecular_weight"])

with st.container(border=True):
    tc1, tc2 = st.columns(2)
    tc1.markdown(f"**PDB结构**: {', '.join(data['pdb_ids'])}")
    tc1.markdown(f"**组织表达**: {data['tissue_expression']}")
    tc2.markdown(f"**作用机制**: {data['mechanism']}")

st.divider()

# ── Competitor Landscape ──
st.subheader("💊 已上市/在研竞品")
comp_data = []
for c in data["competitors"]:
    comp_data.append({
        "药物": c["drug"],
        "公司": c["company"],
        "适应症": c["indication"],
        "获批年份": c["year"],
        "2025年销售额": c["sales_2025"],
    })
df_comp = pd.DataFrame(comp_data)
st.dataframe(df_comp, hide_index=True, use_container_width=True)

fig_sales = go.Figure()
fig_sales.add_trace(go.Bar(
    x=[c["drug"].split(" (")[0] for c in data["competitors"]],
    y=[float(c["sales_2025"].replace("~", "").replace("亿美元", "").replace("亿元", "").strip()) for c in data["competitors"]],
    marker_color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA"][:len(data["competitors"])],
    text=[c["sales_2025"] for c in data["competitors"]],
    textposition="outside",
))
fig_sales.update_layout(
    title="竞品年销售额对比",
    yaxis_title="销售额",
    height=300,
    margin=dict(l=60, r=20, t=40, b=40),
)
st.plotly_chart(fig_sales, key="sales_bar", use_container_width=True)

st.divider()

# ── Druggability Assessment ──
st.subheader("🧪 AI可药性评估")

drug = data["druggability"]
categories = list(k for k in drug.keys() if k != "overall")
labels_cn = {
    "surface_accessibility": "表面可及性",
    "conformational_stability": "构象稳定性",
    "known_epitopes": "已知表位",
    "safety_profile": "安全性信号",
}

rc1, rc2 = st.columns([2, 1])
with rc1:
    fig_drug = plot_radar_chart(
        [labels_cn.get(c, c) for c in categories],
        {sel_target: [drug[c] for c in categories]},
        "可药性评估雷达图",
    )
    st.plotly_chart(fig_drug, key="drug_radar", use_container_width=True)

with rc2:
    st.metric("综合可药性评分", f"{drug['overall']}/100")
    for c in categories:
        label = labels_cn.get(c, c)
        val = drug[c]
        color = "🟢" if val >= 80 else "🟡" if val >= 60 else "🔴"
        st.markdown(f"{color} **{label}**: {val}/100")

st.divider()

# ── Literature Insights ──
st.subheader("📚 文献情报摘要")
st.markdown("AI自动从PubMed/bioRxiv/专利数据库提取关键结论（模拟RAG检索结果）")

for i, insight in enumerate(data["literature_insights"], 1):
    with st.container(border=True):
        st.markdown(f"**[{i}]** {insight}")

st.divider()

# ── AI Conclusion ──
st.subheader("🤖 AI立项建议")
conclusion = data["ai_conclusion"]

score_color = "🟢" if conclusion["score"] >= 80 else "🟡" if conclusion["score"] >= 60 else "🔴"

with st.container(border=True):
    cc1, cc2 = st.columns([1, 3])
    with cc1:
        st.markdown(f"### {score_color}")
        st.metric("AI评分", f"{conclusion['score']}/100")
        st.markdown(f"**建议**: {conclusion['verdict']}")
    with cc2:
        st.markdown("**竞争风险**:")
        for risk in conclusion["risks"]:
            st.markdown(f"- ⚠️ {risk}")

        st.markdown(f"**差异化策略**: {conclusion['strategy']}")

        st.markdown("**建议下一步**:")
        for step in conclusion["next_steps"]:
            st.markdown(f"- ✅ {step}")
