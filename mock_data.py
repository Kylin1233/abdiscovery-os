# AbDiscovery OS — 全部Mock数据
# 基于真实抗体研发流程构建，对标 Benchling + BioMap OS

# ══════════════════════════════════════════════
# 管线阶段定义
# ══════════════════════════════════════════════

PIPELINE_STAGES = [
    {"id": 1, "name": "靶点发现与验证", "en": "Target Discovery", "icon": "🎯", "desc": "靶点筛选、验证、可药性评估"},
    {"id": 2, "name": "抗体库构建与筛选", "en": "Library & Screening", "icon": "🧬", "desc": "噬菌体展示/AI生成，高通量筛选"},
    {"id": 3, "name": "命中确认", "en": "Hit Confirmation", "icon": "✅", "desc": "ELISA验证、初步亲和力测定"},
    {"id": 4, "name": "先导优化", "en": "Lead Optimization", "icon": "⚡", "desc": "亲和力成熟、人源化、工程化改造"},
    {"id": 5, "name": "可开发性评估", "en": "Developability", "icon": "📊", "desc": "稳定性、聚集、粘度、免疫原性"},
    {"id": 6, "name": "细胞株构建", "en": "Cell Line Dev", "icon": "🔬", "desc": "CHO/HEK转染、高表达克隆筛选"},
    {"id": 7, "name": "工艺开发", "en": "Process Dev", "icon": "🏭", "desc": "上游培养、下游纯化工艺"},
    {"id": 8, "name": "候选分子确定", "en": "Candidate Selection", "icon": "🏆", "desc": "综合评估，进入IND申报"},
]

# ══════════════════════════════════════════════
# 在研项目
# ══════════════════════════════════════════════

PROJECTS = [
    {
        "id": "PRJ-001",
        "name": "Anti-PD-L1 单克隆抗体",
        "target": "PD-L1",
        "target_gene": "CD274",
        "indication": "实体瘤（非小细胞肺癌）",
        "format": "IgG4",
        "stage": "先导优化",
        "stage_id": 4,
        "progress": 55,
        "lead_count": 3,
        "start_date": "2026-01-15",
    },
    {
        "id": "PRJ-002",
        "name": "HER2×CD3 双特异性抗体",
        "target": "HER2/CD3",
        "target_gene": "ERBB2/CD3E",
        "indication": "HER2+乳腺癌",
        "format": "双特异性(Knobs-in-Holes)",
        "stage": "抗体库构建与筛选",
        "stage_id": 2,
        "progress": 25,
        "lead_count": 0,
        "start_date": "2026-03-20",
    },
    {
        "id": "PRJ-003",
        "name": "Anti-TNFα 纳米抗体",
        "target": "TNFα",
        "target_gene": "TNF",
        "indication": "类风湿关节炎",
        "format": "sdAb (VHH)",
        "stage": "可开发性评估",
        "stage_id": 5,
        "progress": 68,
        "lead_count": 2,
        "start_date": "2025-10-08",
    },
    {
        "id": "PRJ-004",
        "name": "Anti-IL-17A 单克隆抗体",
        "target": "IL-17A",
        "target_gene": "IL17A",
        "indication": "银屑病",
        "format": "IgG1",
        "stage": "细胞株构建",
        "stage_id": 6,
        "progress": 78,
        "lead_count": 1,
        "start_date": "2025-07-12",
    },
    {
        "id": "PRJ-005",
        "name": "Anti-CD20 ADC",
        "target": "CD20",
        "target_gene": "MS4A1",
        "indication": "非霍奇金淋巴瘤",
        "format": "ADC (IgG1-MMAE)",
        "stage": "靶点发现与验证",
        "stage_id": 1,
        "progress": 10,
        "lead_count": 0,
        "start_date": "2026-05-01",
    },
]

# ══════════════════════════════════════════════
# 靶点调研数据
# ══════════════════════════════════════════════

TARGET_RESEARCH = {
    "PD-L1": {
        "gene": "CD274",
        "uniprot": "Q9NZQ7",
        "protein_family": "B7免疫球蛋白超家族",
        "pdb_ids": ["5JDR", "5X8L", "5XXY"],
        "molecular_weight": "33.3 kDa",
        "tissue_expression": "肿瘤细胞、抗原呈递细胞、T细胞（诱导表达）",
        "mechanism": "PD-L1与PD-1结合后抑制T细胞活化，肿瘤利用此机制实现免疫逃逸",
        "competitors": [
            {"drug": "Atezolizumab (Tecentriq)", "company": "Roche", "indication": "NSCLC/膀胱癌", "year": 2016, "sales_2025": "~38亿美元"},
            {"drug": "Durvalumab (Imfinzi)", "company": "AstraZeneca", "indication": "NSCLC/胆道癌", "year": 2017, "sales_2025": "~47亿美元"},
            {"drug": "Avelumab (Bavencio)", "company": "Merck/Pfizer", "indication": "尿路上皮癌/MCC", "year": 2017, "sales_2025": "~5亿美元"},
            {"drug": "Sugemalimab (舒格利单抗)", "company": "基石药业", "indication": "NSCLC", "year": 2021, "sales_2025": "~15亿元"},
        ],
        "druggability": {
            "surface_accessibility": 85,
            "conformational_stability": 78,
            "known_epitopes": 90,
            "safety_profile": 72,
            "overall": 81,
        },
        "literature_insights": [
            "PD-L1在多种实体瘤中高表达（NSCLC阳性率约50-80%），是成熟的免疫检查点靶点",
            "已有3个PD-L1抗体获FDA批准，竞争激烈，需差异化策略（如ADC、双抗、联合用药）",
            "新型表位研究表明PD-L1胞外域存在非经典结合位点，可能提供差异化机会",
            "PD-L1/VEGF双抗在临床试验中显示出协同抗肿瘤效果（Phase II数据）",
        ],
        "ai_conclusion": {
            "verdict": "谨慎推进",
            "score": 72,
            "risks": ["竞争格局饱和，已有多个成熟产品", "单靶点PD-L1抗体差异化空间有限"],
            "strategy": "建议采用双特异性抗体或ADC策略实现差异化，聚焦PD-L1高表达但现有疗法响应率低的亚群",
            "next_steps": ["完成靶点验证实验", "设计PD-L1/VEGF双特异性构型", "评估ADC payload选择"],
        },
    },
    "HER2": {
        "gene": "ERBB2",
        "uniprot": "P04626",
        "protein_family": "ErbB受体酪氨酸激酶家族",
        "pdb_ids": ["1N8Z", "3BE1", "6OGE"],
        "molecular_weight": "137.9 kDa",
        "tissue_expression": "乳腺癌（20-30%过表达）、胃癌、卵巢癌、肺癌",
        "mechanism": "HER2过表达导致信号通路持续激活，驱动肿瘤增殖和生存",
        "competitors": [
            {"drug": "Trastuzumab (Herceptin)", "company": "Roche", "indication": "乳腺癌/胃癌", "year": 1998, "sales_2025": "~28亿美元"},
            {"drug": "Pertuzumab (Perjeta)", "company": "Roche", "indication": "乳腺癌", "year": 2012, "sales_2025": "~42亿美元"},
            {"drug": "T-DXd (Enhertu)", "company": "Daiichi/AZ", "indication": "乳腺癌/NSCLC/胃癌", "year": 2019, "sales_2025": "~65亿美元"},
            {"drug": "Zanidatamab", "company": "Zymeworks", "indication": "胆道癌/胃癌", "year": 2024, "sales_2025": "~2亿美元"},
        ],
        "druggability": {
            "surface_accessibility": 92,
            "conformational_stability": 85,
            "known_epitopes": 95,
            "safety_profile": 68,
            "overall": 85,
        },
        "literature_insights": [
            "HER2是实体瘤领域验证最充分的靶点之一，T-DXd的成功开创了ADC新时代",
            "HER2×CD3双特异性抗体在HER2低表达人群中显示出潜力（传统抗HER2疗法覆盖不到的患者群体）",
            "HER2 Domain II和Domain IV存在不同表位，可用于双表位策略提升亲和力",
            "脑转移瘤穿透BBB的抗HER2策略是前沿研究方向",
        ],
        "ai_conclusion": {
            "verdict": "积极推进",
            "score": 88,
            "risks": ["竞争产品多但市场空间大", "HER2低表达人群疗效数据尚不成熟"],
            "strategy": "HER2×CD3双特异性抗体可覆盖HER2低表达人群，与现有HER2-ADC差异化竞争",
            "next_steps": ["完成CD3端亲和力优化", "HER2低表达细胞系验证", "T细胞杀伤实验"],
        },
    },
}

# ══════════════════════════════════════════════
# 实体注册中心 — 抗体序列
# ══════════════════════════════════════════════

ENTITY_ANTIBODIES = [
    {"id": "AB-001", "name": "αPDL1-H01", "target": "PD-L1", "format": "IgG4", "source": "噬菌体展示",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDRGYTFGSYIDY", "kd_nm": 12.5, "tm_celsius": 68.2, "expression_mg_l": None,
     "status": "活跃", "created": "2026-02-01", "project": "PRJ-001"},
    {"id": "AB-002", "name": "αPDL1-H02", "target": "PD-L1", "format": "IgG4", "source": "噬菌体展示",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSNYAMSWVRQAPGKGLEWVSAITSSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQGISSYLNWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDRGYTFDSYIDY", "kd_nm": 8.3, "tm_celsius": 71.5, "expression_mg_l": 45.0,
     "status": "活跃", "created": "2026-02-10", "project": "PRJ-001"},
    {"id": "AB-003", "name": "αPDL1-A01", "target": "PD-L1", "format": "IgG4", "source": "AI生成(F2P)",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYAMSWVRQAPGKGLEWVSAISGDGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSWLNWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDLGYTFGSYIDY", "kd_nm": 3.2, "tm_celsius": 73.8, "expression_mg_l": 62.0,
     "status": "活跃", "created": "2026-03-05", "project": "PRJ-001"},
    {"id": "AB-004", "name": "αPDL1-A02", "target": "PD-L1", "format": "IgG4", "source": "AI生成(P2P)",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYAMSWVRQAPGKGLEWVSAISGDGKSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSWLNWYQQKPGKAPKLLIYDASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDLGYTFESYIDY", "kd_nm": 0.8, "tm_celsius": 75.1, "expression_mg_l": 58.0,
     "status": "活跃", "created": "2026-04-01", "project": "PRJ-001"},
    {"id": "AB-005", "name": "αPDL1-A03", "target": "PD-L1", "format": "IgG4", "source": "AI生成(P2P)",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYAMSWVRQAPGKGLEWVSAISGEHKSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSWLNWYQQKPGKAPKLLIYDASNLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDLGYTFESYVDY", "kd_nm": 0.3, "tm_celsius": 76.4, "expression_mg_l": 71.0,
     "status": "活跃", "created": "2026-04-20", "project": "PRJ-001"},
    {"id": "AB-006", "name": "αHER2-H01", "target": "HER2", "format": "IgG1", "source": "杂交瘤",
     "vh": "QVQLQQSGAELARPGASVKMSCKASGYTFTRYTMHWVKQRPGQGLEWIGYINPSRGYTNYADSVKGRFTITTDTSSTAYMQLSSLTSEDSAVYYCAR",
     "vl": "DIVMTQAAPSVPVTPGESVSISCRSSKSLLHSNGNTYLYWFLQRPGQSPQLLIYRMSNLASGVPDRFSGSGSGTAFTLRISRVEAEDVGVYYC",
     "cdr_h3": "ARGGYDGYYAMDY", "kd_nm": 28.6, "tm_celsius": 65.0, "expression_mg_l": None,
     "status": "活跃", "created": "2026-03-25", "project": "PRJ-002"},
    {"id": "AB-007", "name": "αHER2-A01", "target": "HER2", "format": "IgG1", "source": "AI生成(F2P)",
     "vh": "QVQLQQSGAELARPGASVKMSCKASGYTFTDYTMHWVKQRPGQGLEWIGYINPNRGYTNYADSVKGRFTITTDTSSTAYMQLSSLTSEDSAVYYCAR",
     "vl": "DIVMTQAAPSVPVTPGESVSISCRSSKSLLHSNGNTYLYWFLQRPGQSPQLLIYRMSNLASGVPDRFSGSGSGTAFTLRISRVEAEDVGVYYC",
     "cdr_h3": "ARGGYDGYYSMDY", "kd_nm": 5.1, "tm_celsius": 70.3, "expression_mg_l": 38.0,
     "status": "活跃", "created": "2026-04-10", "project": "PRJ-002"},
    {"id": "AB-008", "name": "αCD3-H01", "target": "CD3", "format": "scFv", "source": "噬菌体展示",
     "vh": "DIKLQQSGAELARPGASVKMSCKTSGYTFTRYTMHWVKQRPGQGLEWIGYINPSRGYTNYNQKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCAR",
     "vl": "QIVLSQSPAILSASPGEKVTMTCRASSSVSYIHWFQQKPGSSPKPWIYATSNLASGVPVRFSGSGSGTSYSLTISRVEAEDAATYYCQQ",
     "cdr_h3": "ARYYDDHYCMDY", "kd_nm": 45.0, "tm_celsius": 62.5, "expression_mg_l": 25.0,
     "status": "活跃", "created": "2026-04-05", "project": "PRJ-002"},
    {"id": "AB-009", "name": "αTNF-N01", "target": "TNFα", "format": "sdAb(VHH)", "source": "免疫驼",
     "vh": "QVQLQESGGGLVQAGGSLRLSCAASGRTSRSYAMGWFRQAPGKEREFVAAINWRGDITRYADSVKGRFTISRDNAKNTVYLQMNSLKPEDTAVYYCAA",
     "vl": None,
     "cdr_h3": "AADRGQGTQVTVSS", "kd_nm": 6.8, "tm_celsius": 72.0, "expression_mg_l": 120.0,
     "status": "活跃", "created": "2025-12-01", "project": "PRJ-003"},
    {"id": "AB-010", "name": "αTNF-N02", "target": "TNFα", "format": "sdAb(VHH)", "source": "AI生成(P2P)",
     "vh": "QVQLQESGGGLVQAGGSLRLSCAASGRTSRSYAMGWFRQAPGKEREFVAAINWRGEITRYADSVKGRFTISRDNAKNTVYLQMNSLKPEDTAVYYCAA",
     "vl": None,
     "cdr_h3": "AADRGQGTQVSVSS", "kd_nm": 1.2, "tm_celsius": 78.5, "expression_mg_l": 155.0,
     "status": "活跃", "created": "2026-02-15", "project": "PRJ-003"},
    {"id": "AB-011", "name": "αIL17-H01", "target": "IL-17A", "format": "IgG1", "source": "噬菌体展示",
     "vh": "EVQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSGISWNSGSIGYADSVKGRFTISRDNAKNSLYLQMNSLRAEDTALYYCAK",
     "vl": "EIVLTQSPATLSLSPGERATLSCRASQSVSSYLAWYQQKPGQAPRLLIYDASNRATGIPARFSGSGSGTDFTLTISSLEPEDFAVYYCQQ",
     "cdr_h3": "AKDGGYSSGWYFDV", "kd_nm": 0.5, "tm_celsius": 74.2, "expression_mg_l": 85.0,
     "status": "活跃", "created": "2025-09-20", "project": "PRJ-004"},
    {"id": "AB-012", "name": "αIL17-H01-HC", "target": "IL-17A", "format": "IgG1", "source": "人源化",
     "vh": "EVQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSGISWNSGSIGYADSVKGRFTISRDNAKNSLYLQMNSLRAEDTALYYCAK",
     "vl": "EIVLTQSPATLSLSPGERATLSCRASQSVSSYLAWYQQKPGQAPRLLIYDASNRATGIPARFSGSGSGTDFTLTISSLEPEDFAVYYCQQ",
     "cdr_h3": "AKDGGYSSGWYFDV", "kd_nm": 0.4, "tm_celsius": 76.8, "expression_mg_l": 92.0,
     "status": "活跃", "created": "2025-11-15", "project": "PRJ-004"},
    {"id": "AB-013", "name": "αCD20-H01", "target": "CD20", "format": "IgG1", "source": "噬菌体展示",
     "vh": "QVQLQQPGAELVKPGASVKMSCKASGYTFTSYNMHWVKQTPGRGLEWIGAIYPGNGDTSYNQKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCAR",
     "vl": "QIVLSQSPAILSASPGEKVTMTCRASSSVSYMHWYQQKPGSSPKPWIYAPSNLASGVPVRFSGSGSGTSYSLTISRVEAEDAATYYCQQ",
     "cdr_h3": "ARVVYYSNSYWYFDV", "kd_nm": 15.2, "tm_celsius": 66.8, "expression_mg_l": None,
     "status": "活跃", "created": "2026-05-10", "project": "PRJ-005"},
    {"id": "AB-014", "name": "αPDL1-A04", "target": "PD-L1", "format": "IgG4", "source": "AI生成(C2P)",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYAMSWVRQAPGKGLEWVSAISGEHKSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSWLNWYQQKPGKAPKLLIYDASNLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDLGYTFGSYVDY", "kd_nm": 0.5, "tm_celsius": 74.9, "expression_mg_l": 65.0,
     "status": "活跃", "created": "2026-05-01", "project": "PRJ-001"},
    {"id": "AB-015", "name": "αPDL1-A05", "target": "PD-L1", "format": "IgG4", "source": "AI生成(P2P)",
     "vh": "EVQLVESGGGLVQPGGSLRLSCAASGFTFSDYAMSWVRQAPGKGLEWVSAISGEHKSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAK",
     "vl": "DIQMTQSPSSLSASVGDRVTITCRASQSISSWLNWYQQKPGKAPKLLIYDASNLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYC",
     "cdr_h3": "ARDLGYTFESYVDY", "kd_nm": 0.2, "tm_celsius": 77.3, "expression_mg_l": 74.0,
     "status": "活跃", "created": "2026-05-15", "project": "PRJ-001"},
]

# ══════════════════════════════════════════════
# 实体注册中心 — 细胞株
# ══════════════════════════════════════════════

ENTITY_CELL_LINES = [
    {"id": "CL-001", "name": "CHO-PDL1-P01", "host": "CHO-K1", "antibody_id": "AB-005", "plasmid_id": "PL-001",
     "passage": 15, "titer_mg_l": 850, "doubling_h": 22, "viability_pct": 96.5, "status": "生产株",
     "created": "2026-05-01", "project": "PRJ-001", "location": "细胞库-A区-R3C2"},
    {"id": "CL-002", "name": "CHO-PDL1-P02", "host": "CHO-K1", "antibody_id": "AB-005", "plasmid_id": "PL-002",
     "passage": 12, "titer_mg_l": 620, "doubling_h": 24, "viability_pct": 95.2, "status": "备选株",
     "created": "2026-05-05", "project": "PRJ-001", "location": "细胞库-A区-R3C3"},
    {"id": "CL-003", "name": "CHO-IL17-P01", "host": "CHO-S", "antibody_id": "AB-012", "plasmid_id": "PL-003",
     "passage": 20, "titer_mg_l": 1200, "doubling_h": 20, "viability_pct": 97.8, "status": "生产株",
     "created": "2025-12-10", "project": "PRJ-004", "location": "细胞库-B区-R1C1"},
    {"id": "CL-004", "name": "HEK-TNF-T01", "host": "HEK293T", "antibody_id": "AB-010", "plasmid_id": "PL-004",
     "passage": 8, "titer_mg_l": 180, "doubling_h": 26, "viability_pct": 93.1, "status": "瞬转株",
     "created": "2026-03-01", "project": "PRJ-003", "location": "细胞库-C区-R2C1"},
    {"id": "CL-005", "name": "CHO-TNF-P01", "host": "CHO-K1", "antibody_id": "AB-010", "plasmid_id": "PL-005",
     "passage": 18, "titer_mg_l": 950, "doubling_h": 21, "viability_pct": 96.0, "status": "生产株",
     "created": "2026-04-15", "project": "PRJ-003", "location": "细胞库-B区-R2C2"},
    {"id": "CL-006", "name": "HEK-HER2-T01", "host": "HEK293F", "antibody_id": "AB-007", "plasmid_id": "PL-006",
     "passage": 5, "titer_mg_l": 120, "doubling_h": 28, "viability_pct": 91.5, "status": "瞬转株",
     "created": "2026-04-20", "project": "PRJ-002", "location": "细胞库-C区-R1C3"},
]

# ══════════════════════════════════════════════
# 实体注册中心 — 质粒
# ══════════════════════════════════════════════

ENTITY_PLASMIDS = [
    {"id": "PL-001", "name": "pCHO1.0-αPDL1-A05-HC", "backbone": "pCHO1.0", "insert": "AB-005 Heavy Chain",
     "selection": "Puromycin", "promoter": "hEF1α-HTLV", "created": "2026-04-25", "project": "PRJ-001"},
    {"id": "PL-002", "name": "pCHO1.0-αPDL1-A05-LC", "backbone": "pCHO1.0", "insert": "AB-005 Light Chain",
     "selection": "Hygromycin", "promoter": "hEF1α-HTLV", "created": "2026-04-25", "project": "PRJ-001"},
    {"id": "PL-003", "name": "pCHO-GS-αIL17-HC/LC", "backbone": "pCHO-GS", "insert": "AB-012 HC+LC (双顺反子)",
     "selection": "MSX (GS)", "promoter": "CMV/SV40", "created": "2025-11-20", "project": "PRJ-004"},
    {"id": "PL-004", "name": "pcDNA3.4-αTNF-VHH", "backbone": "pcDNA3.4", "insert": "AB-010 VHH",
     "selection": "Geneticin", "promoter": "CMV", "created": "2026-02-20", "project": "PRJ-003"},
    {"id": "PL-005", "name": "pCHO1.0-αTNF-VHH-Fc", "backbone": "pCHO1.0", "insert": "AB-010 VHH-Fc融合",
     "selection": "Puromycin", "promoter": "hEF1α-HTLV", "created": "2026-04-01", "project": "PRJ-003"},
    {"id": "PL-006", "name": "pcDNA3.4-αHER2-HC", "backbone": "pcDNA3.4", "insert": "AB-007 Heavy Chain",
     "selection": "Geneticin", "promoter": "CMV", "created": "2026-04-08", "project": "PRJ-002"},
    {"id": "PL-007", "name": "pcDNA3.4-αHER2-LC", "backbone": "pcDNA3.4", "insert": "AB-007 Light Chain",
     "selection": "Hygromycin", "promoter": "CMV", "created": "2026-04-08", "project": "PRJ-002"},
    {"id": "PL-008", "name": "pcDNA3.4-αCD3-scFv", "backbone": "pcDNA3.4", "insert": "AB-008 scFv",
     "selection": "Geneticin", "promoter": "CMV", "created": "2026-04-05", "project": "PRJ-002"},
]

# ══════════════════════════════════════════════
# 实验数据 — ELISA 结合活性
# ══════════════════════════════════════════════

ELISA_DATA = [
    {"antibody_id": "AB-001", "name": "αPDL1-H01", "target": "PD-L1", "antigen_conc_ug_ml": 1.0,
     "od450": 1.85, "ec50_nm": 15.2, "max_binding_pct": 82, "verdict": "活性"},
    {"antibody_id": "AB-002", "name": "αPDL1-H02", "target": "PD-L1", "antigen_conc_ug_ml": 1.0,
     "od450": 2.12, "ec50_nm": 9.8, "max_binding_pct": 91, "verdict": "活性"},
    {"antibody_id": "AB-003", "name": "αPDL1-A01", "target": "PD-L1", "antigen_conc_ug_ml": 1.0,
     "od450": 2.45, "ec50_nm": 4.1, "max_binding_pct": 95, "verdict": "活性"},
    {"antibody_id": "AB-004", "name": "αPDL1-A02", "target": "PD-L1", "antigen_conc_ug_ml": 1.0,
     "od450": 2.68, "ec50_nm": 1.2, "max_binding_pct": 98, "verdict": "活性"},
    {"antibody_id": "AB-005", "name": "αPDL1-A03", "target": "PD-L1", "antigen_conc_ug_ml": 1.0,
     "od450": 2.75, "ec50_nm": 0.5, "max_binding_pct": 99, "verdict": "活性"},
    {"antibody_id": "AB-006", "name": "αHER2-H01", "target": "HER2", "antigen_conc_ug_ml": 1.0,
     "od450": 1.42, "ec50_nm": 32.5, "max_binding_pct": 68, "verdict": "弱活性"},
    {"antibody_id": "AB-007", "name": "αHER2-A01", "target": "HER2", "antigen_conc_ug_ml": 1.0,
     "od450": 2.31, "ec50_nm": 6.2, "max_binding_pct": 93, "verdict": "活性"},
    {"antibody_id": "AB-009", "name": "αTNF-N01", "target": "TNFα", "antigen_conc_ug_ml": 1.0,
     "od450": 2.18, "ec50_nm": 8.5, "max_binding_pct": 89, "verdict": "活性"},
]

# ══════════════════════════════════════════════
# 实验数据 — SPR 动力学
# ══════════════════════════════════════════════

SPR_DATA = [
    {"antibody_id": "AB-001", "name": "αPDL1-H01", "ka_per_ms": 2.5e5, "kd_per_s": 3.1e-3, "kd_nm": 12.4, "chi2": 0.45, "verdict": "合格"},
    {"antibody_id": "AB-002", "name": "αPDL1-H02", "ka_per_ms": 3.8e5, "kd_per_s": 3.2e-3, "kd_nm": 8.4, "chi2": 0.32, "verdict": "合格"},
    {"antibody_id": "AB-003", "name": "αPDL1-A01", "ka_per_ms": 5.2e5, "kd_per_s": 1.7e-3, "kd_nm": 3.3, "chi2": 0.28, "verdict": "合格"},
    {"antibody_id": "AB-004", "name": "αPDL1-A02", "ka_per_ms": 8.1e5, "kd_per_s": 6.5e-4, "kd_nm": 0.8, "chi2": 0.18, "verdict": "优秀"},
    {"antibody_id": "AB-005", "name": "αPDL1-A03", "ka_per_ms": 1.2e6, "kd_per_s": 3.6e-4, "kd_nm": 0.3, "chi2": 0.12, "verdict": "优秀"},
    {"antibody_id": "AB-009", "name": "αTNF-N01", "ka_per_ms": 4.5e5, "kd_per_s": 3.1e-3, "kd_nm": 6.9, "chi2": 0.38, "verdict": "合格"},
    {"antibody_id": "AB-010", "name": "αTNF-N02", "ka_per_ms": 6.8e5, "kd_per_s": 8.2e-4, "kd_nm": 1.2, "chi2": 0.22, "verdict": "优秀"},
    {"antibody_id": "AB-011", "name": "αIL17-H01", "ka_per_ms": 9.5e5, "kd_per_s": 4.8e-4, "kd_nm": 0.5, "chi2": 0.15, "verdict": "优秀"},
]

# ══════════════════════════════════════════════
# 实验数据 — 细胞表达
# ══════════════════════════════════════════════

EXPRESSION_DATA = [
    {"cell_line_id": "CL-001", "name": "CHO-PDL1-P01", "day": 14, "titer_mg_l": 850, "viability_pct": 96.5, "verdict": "达标"},
    {"cell_line_id": "CL-002", "name": "CHO-PDL1-P02", "day": 14, "titer_mg_l": 620, "viability_pct": 95.2, "verdict": "达标"},
    {"cell_line_id": "CL-003", "name": "CHO-IL17-P01", "day": 14, "titer_mg_l": 1200, "viability_pct": 97.8, "verdict": "优秀"},
    {"cell_line_id": "CL-004", "name": "HEK-TNF-T01", "day": 7, "titer_mg_l": 180, "viability_pct": 93.1, "verdict": "瞬转正常"},
    {"cell_line_id": "CL-005", "name": "CHO-TNF-P01", "day": 14, "titer_mg_l": 950, "viability_pct": 96.0, "verdict": "达标"},
    {"cell_line_id": "CL-006", "name": "HEK-HER2-T01", "day": 7, "titer_mg_l": 120, "viability_pct": 91.5, "verdict": "偏低"},
]

# ══════════════════════════════════════════════
# 可开发性评估
# ══════════════════════════════════════════════

DEVELOPABILITY_DATA = [
    {"antibody_id": "AB-005", "name": "αPDL1-A03", "tm_celsius": 76.4, "aggregation_pct": 1.2,
     "viscosity_cp": 8.5, "immunogenicity_score": 12, "chemical_stability": "良好",
     "overall": "通过", "recommendation": "推荐进入CLD"},
    {"antibody_id": "AB-004", "name": "αPDL1-A02", "tm_celsius": 75.1, "aggregation_pct": 2.8,
     "viscosity_cp": 11.2, "immunogenicity_score": 18, "chemical_stability": "良好",
     "overall": "条件通过", "recommendation": "建议优化CDR-H2以降低聚集倾向"},
    {"antibody_id": "AB-010", "name": "αTNF-N02", "tm_celsius": 78.5, "aggregation_pct": 0.8,
     "viscosity_cp": 3.2, "immunogenicity_score": 8, "chemical_stability": "优秀",
     "overall": "通过", "recommendation": "VHH天然稳定性优异，推荐进入CLD"},
    {"antibody_id": "AB-012", "name": "αIL17-H01-HC", "tm_celsius": 76.8, "aggregation_pct": 1.5,
     "viscosity_cp": 9.8, "immunogenicity_score": 15, "chemical_stability": "良好",
     "overall": "通过", "recommendation": "已完成人源化，推荐进入CLD"},
    {"antibody_id": "AB-014", "name": "αPDL1-A04", "tm_celsius": 74.9, "aggregation_pct": 4.5,
     "viscosity_cp": 15.8, "immunogenicity_score": 25, "chemical_stability": "一般",
     "overall": "不通过", "recommendation": "聚集倾向和免疫原性偏高，建议回到P2P优化"},
]

# ══════════════════════════════════════════════
# 干湿闭环迭代数据
# ══════════════════════════════════════════════

CLOSED_LOOP_ITERATIONS = [
    {
        "round": 1, "phase": "初筛",
        "ai_action": "xTrimo F2P模型基于PD-L1靶点结构生成100条候选抗体序列",
        "wet_action": "ELISA高通量筛选100条候选",
        "result": "8个Hit（结合活性OD>1.5）",
        "key_metric": "命中率 8%",
        "sequences_in": 100, "sequences_out": 8,
        "best_kd": 12.5,
        "duration_days": 14,
    },
    {
        "round": 2, "phase": "亲和力优化",
        "ai_action": "xTrimo P2P模型对8个Hit进行CDR区域突变优化，每个生成10条变体",
        "wet_action": "SPR测定80条变体的动力学参数（ka/kd/KD）",
        "result": "3个Lead（KD<5nM），最优KD=0.8nM",
        "key_metric": "亲和力提升 15.6× (12.5→0.8 nM)",
        "sequences_in": 80, "sequences_out": 3,
        "best_kd": 0.8,
        "duration_days": 21,
    },
    {
        "round": 3, "phase": "精细优化",
        "ai_action": "xTrimo P2P对3个Lead做精细亲和力成熟，同时优化稳定性（Tm>75°C）",
        "wet_action": "SPR + DSF(Tm) + SEC(聚集)三重验证",
        "result": "1个Lead确认（KD=0.3nM, Tm=76.4°C, 聚集<2%）",
        "key_metric": "亲和力提升 2.7× (0.8→0.3 nM)",
        "sequences_in": 30, "sequences_out": 1,
        "best_kd": 0.3,
        "duration_days": 18,
    },
    {
        "round": 4, "phase": "可开发性",
        "ai_action": "xTrimo C2P基于可开发性约束生成5条工程化变体（降免疫原性+保持亲和力）",
        "wet_action": "全面可开发性评估（Tm/聚集/粘度/免疫原性/化学稳定性）",
        "result": "最终候选AB-005确定（KD=0.3nM, Tm=76.4°C, 免疫原性评分12）",
        "key_metric": "候选分子锁定",
        "sequences_in": 5, "sequences_out": 1,
        "best_kd": 0.3,
        "duration_days": 14,
    },
]

# ══════════════════════════════════════════════
# AI知识助手 — 预设问答
# ══════════════════════════════════════════════

KNOWLEDGE_QA = [
    {
        "question": "IgG4抗体与IgG1的区别和选择策略？",
        "answer": """**IgG亚型选择**是抗体药物设计的关键决策之一：

**IgG1**（最常用）：
- ADCC/CDC效应强，适合需要免疫效应功能的场景（如肿瘤杀伤）
- Fc与FcγR结合力强，半衰期约21天
- 代表药物：Trastuzumab (Herceptin), Rituximab

**IgG4**：
- ADCC/CDC效应极弱，适合"阻断型"抗体（不需要杀伤靶细胞）
- 天然存在Fab-arm exchange现象，需S228P突变稳定铰链区
- 适用场景：免疫检查点抗体（PD-1/PD-L1）、受体拮抗剂
- 代表药物：Nivolumab (Opdivo), Pembrolizumab (Keytruda)

**选择策略**：
- 需要杀伤靶细胞 → IgG1（或ADCC增强型IgG1）
- 需要阻断信号/中和配体 → IgG4(S228P) 或 IgG1-LALA（效应功能沉默）
- ADC偶联 → IgG1（更稳定的铰链区有利于偶联）""",
        "sources": [
            "Vidarsson G, et al. IgG subclasses and allotypes. Front Immunol. 2014;5:520",
            "Wang X, et al. IgG Fc engineering. Protein Cell. 2018;9(1):63-73",
            "Antibody Society: Therapeutic antibody database (2025)",
        ],
    },
    {
        "question": "如何提高抗体的热稳定性（Tm）？",
        "answer": """**热稳定性（Tm）**是可开发性评估的核心指标，治疗性抗体通常要求Tm>65°C。

**常见优化策略**：

1. **Framework回复突变**：将人源化过程中引入的非germline残基回复为germline序列，通常可提升2-5°C
2. **VH/VL界面优化**：增强VH-VL domain间的疏水相互作用和氢键网络
3. **CDR区稳定化**：
   - 去除易脱酰胺位点（Asn-Gly, Asn-Ser）
   - 去除易氧化位点（游离的Met, Trp）
   - 引入分子内二硫键（适用于VHH）
4. **恒定区工程**：CH2 domain的T307Q/N434Y等突变可提升整体稳定性
5. **计算设计**：基于Rosetta或AI模型预测稳定化突变

**AI辅助方法**（对标xTrimo P2P）：
- 输入当前序列 + 优化目标（Tm>75°C）
- 模型预测每个位点的突变对Tm的影响
- 输出推荐突变组合 + 预测Tm值""",
        "sources": [
            "Ewert S, et al. Biophysical properties of human antibody variable domains. J Mol Biol. 2003;325:531-53",
            "Bedouelle H. Principles and equations for measuring and interpreting protein stability. Biochim Biophys Acta. 2016;1864:422-33",
            "Raybould MIJ, et al. Five computational developability guidelines. PNAS. 2019;116:4025-30",
        ],
    },
    {
        "question": "双特异性抗体的主要构型和各自优劣？",
        "answer": """**双特异性抗体（BsAb）**可同时结合两个不同抗原/表位，是当前最热门的抗体工程方向。

**主要构型**：

| 构型 | 分子量 | 半衰期 | Fc效应 | 代表技术 |
|------|--------|--------|--------|----------|
| **Knobs-in-Holes (KiH)** | ~150kDa | 长(~21d) | 有 | Roche |
| **CrossMAb** | ~150kDa | 长 | 有 | Roche（解决轻链错配）|
| **DVD-Ig** | ~200kDa | 长 | 有 | AbbVie |
| **BiTE (scFv-scFv)** | ~55kDa | 短(~2h) | 无 | Amgen |
| **DART** | ~55kDa | 短 | 无 | Macrogenics |
| **Nanobody融合** | ~30-80kDa | 可调 | 可选 | Sanofi/Ablynx |

**选择依据**：
- 需要长半衰期+Fc效应 → KiH/CrossMAb（IgG-like）
- 需要强T细胞招募 → BiTE/DART（小分子，肿瘤穿透好）
- 需要三靶点/多价 → Nanobody融合（模块化设计灵活）
- 量产工艺简单 → KiH（最接近常规IgG生产流程）""",
        "sources": [
            "Labrijn AF, et al. Bispecific antibodies: a mechanistic review. Nat Rev Drug Discov. 2019;18:585-608",
            "Ma J, et al. Bispecific antibodies: from research to clinical application. Front Immunol. 2021;12:626616",
            "Antibody Society: Bispecific antibodies approved and in clinical trials (2025)",
        ],
    },
    {
        "question": "CDR区域的哪些突变最可能影响亲和力？",
        "answer": """**CDR（互补决定区）**是抗体与抗原直接接触的区域，突变对亲和力影响最大。

**各CDR区对亲和力的贡献**（按重要性排序）：
1. **CDR-H3**（最重要）：位于VH domain D-J连接处，长度和序列变异性最大，是结合特异性的主要决定因素
2. **CDR-H2**：常参与抗原接触，对亲和力贡献显著
3. **CDR-L3**：轻链中对结合贡献最大的区域
4. **CDR-H1/L1/L2**：对结合有贡献，但通常不是关键热点

**亲和力成熟策略**：
- **热点随机突变**：对CDR-H3和CDR-H2的接触残基进行饱和突变
- **Error-prone PCR**：全CDR区低频率随机突变
- **CDR Walking**：逐区域系统突变筛选
- **AI定向突变**（对标xTrimo）：模型预测每个位点突变对ΔΔG的影响，精准推荐突变

**需要避免的突变**：
- 引入游离Cys（可形成非预期二硫键）
- N-X-S/T糖基化位点（CDR区糖基化可能干扰结合）
- Asp-Pro（易断裂）、Asn-Gly（易脱酰胺）""",
        "sources": [
            "Marks C, et al. How repertoire data are changing antibody science. J Biol Chem. 2020;295:9823-37",
            "Sela-Culang I, et al. The structural basis of antibody-antigen recognition. Front Immunol. 2013;4:302",
            "Warszawski S, et al. Optimizing antibody affinity and stability by the automated design. PLoS One. 2014;9:e87901",
        ],
    },
    {
        "question": "CHO细胞表达系统的常见问题和优化策略？",
        "answer": """**CHO（Chinese Hamster Ovary）细胞**是治疗性抗体生产的金标准宿主细胞，全球约70%的重组蛋白药物使用CHO表达。

**常见问题及优化**：

**1. 表达量低（<500 mg/L）**
- 优化密码子（CHO偏好密码子）
- 使用强启动子（hEF1α-HTLV, CMV/EF1α双启动子）
- DHFR/GS基因扩增系统加压筛选
- 优化信号肽（如IL-2 signal peptide）

**2. 产物质量不稳定**
- 控制培养温度（33-37°C，降温培养可提高产物质量）
- 优化补料策略（避免乳酸/氨积累）
- 监控糖基化谱（影响Fc效应功能和半衰期）

**3. 细胞活力下降过快**
- 添加抗凋亡基因（Bcl-2, Bcl-xL）
- 优化培养基（无血清、化学成分确定培养基）
- 控制渗透压（300-350 mOsm/kg）

**4. 克隆稳定性差**
- 使用定点整合（如Cre-loxP系统）替代随机整合
- 扩展稳定性测试（>60代传代）

**典型产量基准**：
- 瞬转表达：50-500 mg/L（HEK293优于CHO）
- 稳定株早期：200-800 mg/L
- 优化稳定株：1-5 g/L
- 工艺优化后：5-10 g/L""",
        "sources": [
            "Kim JY, et al. CHO cells in biotechnology for production of recombinant proteins. Appl Microbiol Biotechnol. 2012;93:917-30",
            "Fischer S, et al. The art of CHO cell engineering. Biotechnol Adv. 2015;33:1878-96",
            "Jayapal KP, et al. Recombinant protein therapeutics from CHO cells. Chem Eng Prog. 2007;103:40-47",
        ],
    },
]

# ══════════════════════════════════════════════
# 最近研发动态
# ══════════════════════════════════════════════

RECENT_ACTIVITIES = [
    {"time": "2026-06-16 16:30", "project": "PRJ-001", "event": "AB-005完成可开发性评估，推荐进入细胞株构建",
     "type": "milestone", "icon": "🏆"},
    {"time": "2026-06-15 14:20", "project": "PRJ-002", "event": "HER2×CD3双抗完成第一轮ELISA筛选，命中12条候选",
     "type": "experiment", "icon": "🧪"},
    {"time": "2026-06-14 10:00", "project": "PRJ-003", "event": "TNFα纳米抗体CL-005稳定株滴度达950mg/L",
     "type": "data", "icon": "📊"},
    {"time": "2026-06-13 09:15", "project": "PRJ-001", "event": "xTrimo P2P模型完成第3轮亲和力优化，最优KD=0.3nM",
     "type": "ai", "icon": "🤖"},
    {"time": "2026-06-12 15:45", "project": "PRJ-004", "event": "IL-17A抗体CHO-IL17-P01稳定株传代第20代，活力97.8%",
     "type": "data", "icon": "🔬"},
    {"time": "2026-06-10 11:30", "project": "PRJ-005", "event": "CD20-ADC项目启动靶点验证实验",
     "type": "milestone", "icon": "🎯"},
]

# ══════════════════════════════════════════════
# Benchling ↔ BioMap OS 模块映射
# ══════════════════════════════════════════════

METHODOLOGY_MAPPING = [
    {
        "dimension": "靶点研究",
        "demo": "多源靶点情报聚合 + AI可药性评估",
        "benchling": "Deep Research Agent",
        "biomap": "xTrimo发现助手",
        "value": "AI驱动的靶点优先级排序",
    },
    {
        "dimension": "实体管理",
        "demo": "抗体/细胞株/质粒Registry",
        "benchling": "Registry + Inventory",
        "biomap": "样本全流程管理",
        "value": "统一实体ID + Schema + 全链路溯源",
    },
    {
        "dimension": "序列设计",
        "demo": "AI抗体序列生成（F2P/P2P/C2P）",
        "benchling": "Model Hub + Biologics",
        "biomap": "xTrimo/AIGP平台",
        "value": "AI从功能需求直接生成蛋白质序列",
    },
    {
        "dimension": "实验记录",
        "demo": "ELISA/SPR/表达 Structured Tables",
        "benchling": "Notebook + Structured Tables",
        "biomap": "实验数据记录模块",
        "value": "结构化数据采集，科学家无额外负担",
    },
    {
        "dimension": "智能分析",
        "demo": "SPR动力学分析 + 可开发性评估",
        "benchling": "Insights + Experiment Optimization",
        "biomap": "智能分析模块",
        "value": "AI多维数据分析 + 优化建议",
    },
    {
        "dimension": "迭代闭环",
        "demo": "4轮干湿闭环：AI设计→实验→数据→再设计",
        "benchling": "Automation (Lab-in-the-Loop)",
        "biomap": "干湿闭环架构",
        "value": "AI与实验室的门控闭环，缩短研发周期",
    },
    {
        "dimension": "知识支撑",
        "demo": "抗体工程RAG问答 + 多轮对话",
        "benchling": "AI Agents (Ask/Research)",
        "biomap": "xTrimo知识助手",
        "value": "RAG检索 + 专业大模型生成 + 引用溯源",
    },
]
