import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from mock_data import PIPELINE_STAGES, METHODOLOGY_MAPPING


def render_sidebar(page_name: str, biomap_module: str, benchling_module: str, related_stages: list[int] | None = None):
    with st.sidebar:
        st.markdown("## 🧬 AbDiscovery OS")
        st.caption("AI驱动的抗体研发数据平台")
        st.divider()

        st.markdown("**当前页面**")
        st.markdown(f"📍 {page_name}")

        st.markdown("**BioMap OS 映射**")
        st.info(biomap_module, icon="🔗")

        st.markdown("**Benchling 对标**")
        st.info(benchling_module, icon="🔗")

        if related_stages:
            st.divider()
            st.markdown("**管线阶段**")
            for s in PIPELINE_STAGES:
                if s["id"] in related_stages:
                    st.markdown(f"**{s['icon']} {s['name']}** ←")
                else:
                    st.caption(f"{s['icon']} {s['name']}")

        st.divider()
        st.caption("Demo for BioMap PM Interview")
        st.caption("对标 Benchling + BioMap OS")


def plot_pipeline(projects: list[dict]):
    stages = PIPELINE_STAGES
    stage_counts = {}
    for s in stages:
        stage_counts[s["id"]] = sum(1 for p in projects if p["stage_id"] == s["id"])

    fig = go.Figure()

    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#FF6692", "#B6E880"]

    for i, s in enumerate(stages):
        count = stage_counts[s["id"]]
        fig.add_trace(go.Bar(
            x=[1],
            y=[s["name"]],
            orientation="h",
            marker_color=colors[i % len(colors)],
            text=f"{s['icon']} {s['name']}  ({count}个项目)" if count > 0 else f"{s['icon']} {s['name']}",
            textposition="inside",
            textfont=dict(size=13, color="white"),
            hoverinfo="text",
            hovertext=f"{s['name']}\n{s['desc']}\n在研项目: {count}",
            showlegend=False,
        ))

    fig.update_layout(
        barmode="stack",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, autorange="reversed"),
        height=55 * len(stages),
        margin=dict(l=0, r=0, t=0, b=0),
        uniformtext_minsize=12,
        uniformtext_mode="show",
    )
    return fig


def plot_radar_chart(categories: list[str], values_dict: dict[str, list[float]], title: str = ""):
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    for idx, (name, vals) in enumerate(values_dict.items()):
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=name,
            opacity=0.6,
            line=dict(color=colors[idx % len(colors)]),
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=title,
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15),
    )
    return fig


def plot_spr_sensorgram(antibodies: list[dict]):
    fig = go.Figure()
    t_assoc = np.linspace(0, 300, 300)
    t_dissoc = np.linspace(300, 600, 300)

    colors = px.colors.qualitative.Plotly
    for idx, ab in enumerate(antibodies):
        ka = ab["ka_per_ms"]
        kd_rate = ab["kd_per_s"]
        rmax = 100

        conc = 50e-9
        kobs = ka * conc + kd_rate
        req = rmax * (ka * conc) / kobs

        r_assoc = req * (1 - np.exp(-kobs * t_assoc))
        r_at_end = r_assoc[-1]
        r_dissoc = r_at_end * np.exp(-kd_rate * (t_dissoc - 300))

        t_full = np.concatenate([t_assoc, t_dissoc])
        r_full = np.concatenate([r_assoc, r_dissoc])

        fig.add_trace(go.Scatter(
            x=t_full, y=r_full,
            mode="lines",
            name=f"{ab['name']} (KD={ab['kd_nm']}nM)",
            line=dict(color=colors[idx % len(colors)], width=2),
        ))

    fig.add_vline(x=300, line_dash="dash", line_color="gray", annotation_text="解离开始")

    fig.update_layout(
        title="SPR Sensorgram（模拟）",
        xaxis_title="时间 (s)",
        yaxis_title="Response (RU)",
        height=400,
        margin=dict(l=60, r=20, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    return fig


def plot_dose_response(antibodies: list[dict]):
    fig = go.Figure()
    concs = np.logspace(-2, 3, 100)
    colors = px.colors.qualitative.Plotly

    for idx, ab in enumerate(antibodies):
        ec50 = ab["ec50_nm"]
        emax = ab["max_binding_pct"]
        response = emax * concs / (ec50 + concs)

        fig.add_trace(go.Scatter(
            x=concs, y=response,
            mode="lines",
            name=f"{ab['name']} (EC50={ec50}nM)",
            line=dict(color=colors[idx % len(colors)], width=2),
        ))

    fig.update_layout(
        title="ELISA 剂量-响应曲线",
        xaxis_title="抗体浓度 (nM)",
        yaxis_title="结合率 (%)",
        xaxis_type="log",
        height=400,
        margin=dict(l=60, r=20, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    )
    return fig


def plot_entity_network(antibodies, cell_lines, plasmids):
    labels = []
    sources = []
    targets = []
    values = []
    colors = []

    target_set = sorted({ab["target"] for ab in antibodies})
    for t in target_set:
        labels.append(f"靶点: {t}")

    ab_start = len(labels)
    for ab in antibodies:
        labels.append(ab["id"])
        t_idx = target_set.index(ab["target"])
        sources.append(t_idx)
        targets.append(ab_start + antibodies.index(ab))
        values.append(1)
        colors.append("rgba(99, 110, 250, 0.4)")

    pl_start = len(labels)
    for pl in plasmids:
        labels.append(pl["id"])

    cl_start = len(labels)
    for cl in cell_lines:
        labels.append(cl["id"])

    for cl in cell_lines:
        ab_id = cl["antibody_id"]
        pl_id = cl["plasmid_id"]
        ab_idx = next((ab_start + i for i, ab in enumerate(antibodies) if ab["id"] == ab_id), None)
        pl_idx = next((pl_start + i for i, pl in enumerate(plasmids) if pl["id"] == pl_id), None)
        cl_idx = cl_start + cell_lines.index(cl)
        if ab_idx is not None:
            sources.append(ab_idx)
            targets.append(cl_idx)
            values.append(1)
            colors.append("rgba(0, 204, 150, 0.4)")
        if pl_idx is not None:
            sources.append(pl_idx)
            targets.append(cl_idx)
            values.append(1)
            colors.append("rgba(255, 161, 90, 0.4)")

    for pl in plasmids:
        insert = pl.get("insert", "")
        for ab in antibodies:
            if ab["id"] in insert:
                sources.append(ab_start + antibodies.index(ab))
                targets.append(pl_start + plasmids.index(pl))
                values.append(1)
                colors.append("rgba(171, 99, 250, 0.4)")

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15, thickness=20,
            label=labels,
            color=["#636EFA"] * len(target_set) +
                  ["#EF553B"] * len(antibodies) +
                  ["#AB63FA"] * len(plasmids) +
                  ["#00CC96"] * len(cell_lines),
        ),
        link=dict(source=sources, target=targets, value=values, color=colors),
    ))

    fig.update_layout(
        title="实体关系网络 (靶点 → 抗体 → 质粒 → 细胞株)",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_closed_loop(iterations):
    rounds = [f"Round {it['round']}" for it in iterations]
    kd_values = [it["best_kd"] for it in iterations]
    seq_in = [it["sequences_in"] for it in iterations]
    seq_out = [it["sequences_out"] for it in iterations]
    days = [it["duration_days"] for it in iterations]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=rounds, y=seq_in,
        name="输入序列数", marker_color="#636EFA", opacity=0.6,
        yaxis="y",
    ))
    fig.add_trace(go.Bar(
        x=rounds, y=seq_out,
        name="输出序列数", marker_color="#00CC96", opacity=0.6,
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=rounds, y=kd_values,
        name="最优KD (nM)", mode="lines+markers",
        line=dict(color="#EF553B", width=3),
        marker=dict(size=10),
        yaxis="y2",
    ))

    fig.update_layout(
        title="干湿闭环迭代进展",
        yaxis=dict(title="序列数量", side="left"),
        yaxis2=dict(title="最优KD (nM)", side="right", overlaying="y", type="log"),
        barmode="group",
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
    )
    return fig


def render_platform_mapping():
    st.markdown("### 📋 平台方法论映射")
    cols_header = st.columns([1.5, 2, 2, 2, 2])
    headers = ["维度", "本Demo", "Benchling", "BioMap OS", "产品价值"]
    for col, h in zip(cols_header, headers):
        col.markdown(f"**{h}**")

    for m in METHODOLOGY_MAPPING:
        cols = st.columns([1.5, 2, 2, 2, 2])
        cols[0].write(m["dimension"])
        cols[1].write(m["demo"])
        cols[2].write(m["benchling"])
        cols[3].write(m["biomap"])
        cols[4].write(m["value"])


def kd_color(kd_nm):
    if kd_nm < 1:
        return "🟢"
    elif kd_nm < 10:
        return "🟡"
    else:
        return "🔴"


def verdict_color(verdict):
    mapping = {
        "优秀": "🟢", "合格": "🟡", "活性": "🟢",
        "弱活性": "🟡", "达标": "🟢", "瞬转正常": "🟡",
        "偏低": "🔴", "通过": "🟢", "条件通过": "🟡", "不通过": "🔴",
    }
    return mapping.get(verdict, "⚪")
