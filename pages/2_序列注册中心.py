import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import ENTITY_ANTIBODIES, ENTITY_CELL_LINES, ENTITY_PLASMIDS, PROJECTS
from utils import render_sidebar, plot_entity_network, kd_color

st.set_page_config(page_title="序列注册中心 | AbDiscovery OS", page_icon="📋", layout="wide")

render_sidebar(
    page_name="序列注册中心",
    biomap_module="BioMap OS · 样本全流程管理",
    benchling_module="Benchling Registry + Inventory",
    related_stages=[2, 3, 4, 6],
)

st.title("📋 序列注册中心")
st.markdown("统一管理抗体序列、细胞株、质粒等生物实体 — 对标 **Benchling Registry + Inventory**")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("抗体序列", f"{len(ENTITY_ANTIBODIES)}条")
c2.metric("细胞株", f"{len(ENTITY_CELL_LINES)}个")
c3.metric("质粒", f"{len(ENTITY_PLASMIDS)}个")
ai_count = sum(1 for ab in ENTITY_ANTIBODIES if "AI" in ab["source"])
c4.metric("AI生成序列", f"{ai_count}条")

st.divider()

# ── Schema Definition ──
st.subheader("🏗️ 实体Schema定义")
st.markdown("每类生物实体有标准化数据结构（对标 Benchling Schema 配置），确保全组织数据一致性")

s1, s2, s3 = st.columns(3)
with s1:
    with st.container(border=True):
        st.markdown("#### 🧬 抗体序列 Schema")
        schema_ab = {
            "字段": ["实体ID", "名称", "靶点", "抗体格式", "VH序列", "VL序列", "CDR-H3", "来源", "KD (nM)", "Tm (°C)", "表达量 (mg/L)", "状态", "关联项目"],
            "类型": ["自动生成", "文本", "关联(靶点)", "枚举", "序列", "序列(可空)", "序列", "枚举", "数值", "数值", "数值", "枚举", "关联(项目)"],
            "示例": ["AB-001", "αPDL1-H01", "PD-L1", "IgG4", "EVQLVES...", "DIQMTQ...", "ARDRGYTF...", "噬菌体展示", "12.5", "68.2", "—", "活跃", "PRJ-001"],
        }
        st.dataframe(pd.DataFrame(schema_ab), hide_index=True, height=490)
with s2:
    with st.container(border=True):
        st.markdown("#### 🔬 细胞株 Schema")
        schema_cl = {
            "字段": ["实体ID", "名称", "宿主细胞", "抗体ID", "质粒ID", "传代数", "滴度 (mg/L)", "倍增时间 (h)", "活力 (%)", "状态", "存储位置"],
            "类型": ["自动生成", "文本", "枚举", "关联(抗体)", "关联(质粒)", "整数", "数值", "数值", "数值", "枚举", "文本"],
            "示例": ["CL-001", "CHO-PDL1-P01", "CHO-K1", "AB-005", "PL-001", "15", "850", "22", "96.5", "生产株", "A区-R3C2"],
        }
        st.dataframe(pd.DataFrame(schema_cl), hide_index=True, height=430)
with s3:
    with st.container(border=True):
        st.markdown("#### 🧪 质粒 Schema")
        schema_pl = {
            "字段": ["实体ID", "名称", "载体骨架", "插入基因", "抗性标记", "启动子", "构建日期", "关联项目"],
            "类型": ["自动生成", "文本", "枚举", "文本", "枚举", "枚举", "日期", "关联(项目)"],
            "示例": ["PL-001", "pCHO1.0-HC", "pCHO1.0", "AB-005 HC", "Puromycin", "hEF1α-HTLV", "2026-04-25", "PRJ-001"],
        }
        st.dataframe(pd.DataFrame(schema_pl), hide_index=True, height=340)

st.divider()

# ── Entity Browser ──
st.subheader("🔍 实体注册浏览器")

tab_ab, tab_cl, tab_pl = st.tabs(["🧬 抗体序列", "🔬 细胞株", "🧪 质粒"])

with tab_ab:
    fc1, fc2, fc3 = st.columns(3)
    targets = ["全部"] + sorted({ab["target"] for ab in ENTITY_ANTIBODIES})
    formats = ["全部"] + sorted({ab["format"] for ab in ENTITY_ANTIBODIES})
    sources = ["全部"] + sorted({ab["source"] for ab in ENTITY_ANTIBODIES})

    sel_target = fc1.selectbox("靶点筛选", targets, key="ab_target")
    sel_format = fc2.selectbox("格式筛选", formats, key="ab_format")
    sel_source = fc3.selectbox("来源筛选", sources, key="ab_source")

    filtered = ENTITY_ANTIBODIES
    if sel_target != "全部":
        filtered = [ab for ab in filtered if ab["target"] == sel_target]
    if sel_format != "全部":
        filtered = [ab for ab in filtered if ab["format"] == sel_format]
    if sel_source != "全部":
        filtered = [ab for ab in filtered if ab["source"] == sel_source]

    display_data = []
    for ab in filtered:
        display_data.append({
            "ID": ab["id"],
            "名称": ab["name"],
            "靶点": ab["target"],
            "格式": ab["format"],
            "来源": ab["source"],
            "CDR-H3": ab["cdr_h3"],
            "KD (nM)": ab["kd_nm"],
            "亲和力": kd_color(ab["kd_nm"]),
            "Tm (°C)": ab["tm_celsius"],
            "表达量": f"{ab['expression_mg_l']:.0f}" if ab["expression_mg_l"] else "—",
            "项目": ab["project"],
        })

    df_ab = pd.DataFrame(display_data)
    st.dataframe(df_ab, hide_index=True, use_container_width=True, height=min(400, 35 * len(display_data) + 38))

    st.caption(f"共 {len(filtered)} 条记录 | 🟢 KD<1nM  🟡 1-10nM  🔴 >10nM")

    with st.expander("📄 展开查看序列详情"):
        sel_ab_id = st.selectbox("选择抗体", [ab["id"] + " — " + ab["name"] for ab in filtered], key="ab_detail")
        if sel_ab_id:
            ab_id = sel_ab_id.split(" — ")[0]
            ab = next(a for a in ENTITY_ANTIBODIES if a["id"] == ab_id)
            dc1, dc2 = st.columns(2)
            with dc1:
                st.markdown(f"**VH序列**: `{ab['vh'][:60]}...`")
                if ab["vl"]:
                    st.markdown(f"**VL序列**: `{ab['vl'][:60]}...`")
                else:
                    st.markdown("**VL序列**: *N/A (单域抗体)*")
                st.markdown(f"**CDR-H3**: `{ab['cdr_h3']}`")
            with dc2:
                st.markdown(f"**KD**: {ab['kd_nm']} nM {kd_color(ab['kd_nm'])}")
                st.markdown(f"**Tm**: {ab['tm_celsius']}°C")
                st.markdown(f"**来源**: {ab['source']}")
                st.markdown(f"**创建日期**: {ab['created']}")

            related_cls = [cl for cl in ENTITY_CELL_LINES if cl["antibody_id"] == ab["id"]]
            if related_cls:
                st.markdown("**关联细胞株**:")
                for cl in related_cls:
                    st.markdown(f"- {cl['id']} ({cl['name']}) — {cl['host']}, 滴度 {cl['titer_mg_l']} mg/L")

            if st.button(f"查看 {ab['name']} 完整详情 →", key=f"to_ab_{ab['id']}"):
                st.session_state["drill_antibody"] = ab["id"]
                st.switch_page("pages/8_抗体详情.py")

with tab_cl:
    cl_data = []
    for cl in ENTITY_CELL_LINES:
        cl_data.append({
            "ID": cl["id"],
            "名称": cl["name"],
            "宿主": cl["host"],
            "抗体": cl["antibody_id"],
            "质粒": cl["plasmid_id"],
            "传代": cl["passage"],
            "滴度 (mg/L)": cl["titer_mg_l"],
            "倍增 (h)": cl["doubling_h"],
            "活力 (%)": cl["viability_pct"],
            "状态": cl["status"],
            "位置": cl["location"],
        })
    df_cl = pd.DataFrame(cl_data)
    st.dataframe(df_cl, hide_index=True, use_container_width=True)

with tab_pl:
    pl_data = []
    for pl in ENTITY_PLASMIDS:
        pl_data.append({
            "ID": pl["id"],
            "名称": pl["name"],
            "骨架": pl["backbone"],
            "插入基因": pl["insert"],
            "抗性": pl["selection"],
            "启动子": pl["promoter"],
            "构建日期": pl["created"],
            "项目": pl["project"],
        })
    df_pl = pd.DataFrame(pl_data)
    st.dataframe(df_pl, hide_index=True, use_container_width=True)

st.divider()

# ── Entity Relationship Network ──
st.subheader("🔗 实体关系网络")
st.markdown("全链路溯源：靶点 → 抗体序列 → 质粒 → 细胞株（对标 Benchling Registry 关联追踪）")

fig_net = plot_entity_network(ENTITY_ANTIBODIES, ENTITY_CELL_LINES, ENTITY_PLASMIDS)
st.plotly_chart(fig_net, key="entity_net", use_container_width=True)

st.divider()

# ── Inventory Panel ──
st.subheader("📦 库存状态")
inv_data = []
for cl in ENTITY_CELL_LINES:
    inv_data.append({
        "实体ID": cl["id"],
        "名称": cl["name"],
        "类型": "细胞株",
        "存储位置": cl["location"],
        "状态": cl["status"],
        "活力": f"{cl['viability_pct']}%",
    })
df_inv = pd.DataFrame(inv_data)

def highlight_status(val):
    if val == "生产株":
        return "background-color: #d4edda"
    elif val == "瞬转株":
        return "background-color: #fff3cd"
    return ""

styled = df_inv.style.map(highlight_status, subset=["状态"])
st.dataframe(styled, hide_index=True, use_container_width=True)
