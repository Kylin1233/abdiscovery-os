import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from mock_data import KNOWLEDGE_QA
from utils import render_sidebar

st.set_page_config(page_title="AI知识助手 | AbDiscovery OS", page_icon="💬", layout="wide")

render_sidebar(
    page_name="AI知识助手",
    biomap_module="BioMap OS · xTrimo知识助手/发现助手",
    benchling_module="Benchling AI Agents (Ask/Research)",
    related_stages=None,
)

st.title("💬 AI知识助手")
st.markdown("抗体研发领域RAG问答系统 — 对标 **Benchling AI Agents + BioMap xTrimo知识助手**")

st.divider()

# ── Agent Matrix ──
st.subheader("🤖 AI Agent 矩阵")
st.markdown("对标 Benchling AI Agent 体系 + BioMap OS 助手体系")

a1, a2, a3, a4 = st.columns(4)
with a1:
    with st.container(border=True):
        st.markdown("### 💬 Ask Agent")
        st.markdown("**功能**: 对话式查询实验数据和注册信息")
        st.markdown("**BioMap**: 知识助手")
        st.caption("\"AB-005的KD是多少？\"")
with a2:
    with st.container(border=True):
        st.markdown("### 🔍 Research Agent")
        st.markdown("**功能**: 跨数据集深度综合分析")
        st.markdown("**BioMap**: 发现助手")
        st.caption("\"比较所有PD-L1候选的可开发性\"")
with a3:
    with st.container(border=True):
        st.markdown("### 🧬 Design Agent")
        st.markdown("**功能**: AI驱动序列设计")
        st.markdown("**BioMap**: AIGP (F2P/P2P/C2P)")
        st.caption("\"设计KD<1nM的PD-L1抗体\"")
with a4:
    with st.container(border=True):
        st.markdown("### 📄 Data Entry Agent")
        st.markdown("**功能**: 自动解析实验报告")
        st.markdown("**BioMap**: 数据整合")
        st.caption("\"上传SPR报告自动提取数据\"")

st.divider()

# ── RAG Architecture ──
st.subheader("🏗️ RAG 检索增强生成架构")
with st.container(border=True):
    r1, r2, r3, r4, r5 = st.columns(5)
    r1.markdown("### 📚\n**知识库**\nUniProt\nPDB\nPubMed\n内部数据")
    r2.markdown("### 🔗\n**向量化**\nEmbedding\n分块索引\n语义检索")
    r3.markdown("### 🔍\n**检索**\nTop-K召回\n重排序\n相关性过滤")
    r4.markdown("### 🤖\n**生成**\nxTrimo LLM\n上下文注入\n专业回答")
    r5.markdown("### 📎\n**引用溯源**\n来源标注\n原文链接\n置信度评分")

st.divider()

# ── Knowledge QA ──
st.subheader("💡 抗体研发知识问答")
st.markdown("预设专业问答（模拟知识助手RAG检索 + 大模型生成效果）")

for i, qa in enumerate(KNOWLEDGE_QA):
    with st.expander(f"❓ {qa['question']}", expanded=(i == 0)):
        st.markdown(qa["answer"])
        st.divider()
        st.markdown("**📚 参考来源**:")
        for src in qa["sources"]:
            st.caption(f"📎 {src}")

st.divider()

# ── Custom Question ──
st.subheader("🔤 自定义问题")
user_q = st.text_input("输入你的问题（抗体研发相关）", placeholder="例如：如何提高抗体的表达量？", key="custom_q")

if user_q:
    with st.spinner("xTrimo知识助手检索中..."):
        import time
        time.sleep(1.5)

    with st.container(border=True):
        st.markdown("### 🤖 AI回答")

        if "表达" in user_q or "产量" in user_q:
            st.markdown("""
            提高抗体表达量可以从以下几个层面优化：

            **1. 基因层面**
            - 密码子优化（针对CHO/HEK偏好密码子）
            - 优化信号肽（如IL-2 signal peptide）
            - 去除mRNA二级结构

            **2. 载体层面**
            - 使用强启动子（hEF1α-HTLV, CMV/EF1α双启动子）
            - DHFR/GS基因扩增系统
            - UCOE或MAR元件提升转录效率

            **3. 细胞工程**
            - 高通量克隆筛选（ClonePix/FACS）
            - 定点整合（Cre-loxP或CRISPR）替代随机整合
            - 添加抗凋亡基因（Bcl-2/Bcl-xL）

            **4. 培养工艺**
            - Fed-batch补料策略优化
            - 降温培养（33-34°C提升比产率）
            - 化学成分确定培养基

            当前项目中，CHO-IL17-P01已达到1200 mg/L的优秀水平。
            """)
        elif "人源化" in user_q:
            st.markdown("""
            抗体人源化是降低免疫原性的关键步骤：

            **1. CDR移植法（CDR Grafting）**
            - 将鼠源CDR移植到人源Framework上
            - 选择与鼠源Framework最接近的人源Germline模板
            - 可能需要Framework回复突变保持亲和力

            **2. 表面重塑法（Resurfacing/Veneering）**
            - 只替换表面暴露的Framework残基
            - 保留结构核心残基
            - 通常比CDR移植保留更多亲和力

            **3. AI辅助人源化**
            - xTrimo P2P模型可预测哪些Framework残基对亲和力关键
            - 自动推荐最优人源化方案
            - 同时优化人源化比例和亲和力保留
            """)
        else:
            st.markdown(f"""
            这是一个很好的问题。基于知识库检索，以下是AI助手的回答：

            关于「{user_q}」，在抗体研发领域中，这涉及到多个关键考量因素。建议结合项目具体情况，
            参考以下资源进行深入了解：

            1. **UniProt数据库** — 查询蛋白质序列和功能注释
            2. **PDB结构数据库** — 查看已解析的抗体-抗原复合物结构
            3. **PubMed文献** — 检索最新研究进展
            4. **内部实验数据** — 结合本项目历史数据分析

            *（Demo环境下为模拟回答，实际部署时将接入完整的RAG知识库）*
            """)

        st.caption("📎 来源：UniProt, PDB, PubMed, 内部知识库 | 置信度: 85%")

st.divider()

# ── Multi-turn Dialog Demo ──
st.subheader("🔄 多轮对话示例")
st.markdown("展示知识助手的上下文理解和追问能力")

dialog = [
    {"role": "user", "content": "我们的PD-L1抗体αPDL1-A03的人源化程度如何？"},
    {"role": "assistant", "content": "αPDL1-A03（AB-005）由xTrimo P2P模型生成，基于人源化Framework设计。根据注册中心数据：\n- VH Framework来源于IGHV3-23 germline（人源化比例约92%）\n- CDR-H3序列为ARDLGYTFESYVDY（14个残基）\n- 预测免疫原性评分为12（低风险，阈值<20）\n\n整体人源化程度良好，符合治疗性抗体开发标准。"},
    {"role": "user", "content": "免疫原性评分12意味着什么？有没有进一步降低的空间？"},
    {"role": "assistant", "content": "免疫原性评分12属于**低风险**范围：\n- <10：极低风险（如全人源抗体）\n- 10-20：低风险（大多数人源化抗体在此范围）\n- 20-40：中等风险（可能需要去免疫原性处理）\n- >40：高风险\n\n进一步降低的策略：\n1. **T细胞表位去除**：识别CDR区域中的MHC-II结合肽段，定向突变\n2. **CDR-H2优化**：H2区域存在一个可能的T细胞表位（H54-H62），可通过P2P模型尝试保守替换\n3. **注意权衡**：去免疫原性突变可能影响亲和力，建议通过xTrimo C2P模式同时约束KD和免疫原性\n\n建议：当前评分12已满足开发标准，如需进一步优化建议在Round 5闭环中处理。"},
    {"role": "user", "content": "好的，如果要启动Round 5优化，输入参数应该怎么设置？"},
    {"role": "assistant", "content": "建议Round 5 C2P设计参数：\n\n**输入上下文**：\n- 亲本序列：AB-005（αPDL1-A03）\n- 约束1：KD ≤ 0.5 nM（保持当前0.3nM水平）\n- 约束2：Tm ≥ 75°C（保持当前76.4°C）\n- 约束3：免疫原性评分 < 10（从当前12降至<10）\n- 约束4：聚集倾向 < 2%（保持当前1.2%）\n- 优化焦点：CDR-H2区域T细胞表位去除\n\n**预期输出**：3-5条工程化变体\n**验证实验**：SPR（确认KD保持）+ 免疫原性预测（确认降低）+ DSF（确认Tm保持）\n\n可在「AI序列设计」页面的C2P模式中直接启动。"},
]

for msg in dialog:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])
