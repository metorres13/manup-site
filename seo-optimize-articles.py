#!/usr/bin/env python3
"""
manup-site (dayue.tech) 文章页 SEO 意图优化 + 收录加速
========================================================
执行:
  python3 seo-optimize-articles.py            # 优化文章 + 重生成 sitemap
  python3 seo-optimize-articles.py --check    # 只检查不改动

做的事:
  1. 按缺资金人群搜索意图漏斗重写 keywords（资金类页面）
  2. 替换泛站 description 为个性化（仅模板描述）
  3. 补/改 og:title og:description
  4. 补 baidu-site-verification meta
  5. JSON-LD: 更新 Article headline/description/dateModified，注入 FAQPage（按分类模板）、BreadcrumbList
  6. 重生成 sitemap.xml（补 lastmod / changefreq）
不动: 正文 H2/段落、title、canonical、og:image、push.js、统计、悬浮按钮。
"""

import os, re, json, glob, sys
from html import escape

BASE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(BASE, "articles")
SITE = "https://dayue.tech"
TODAY = "2026-06-23"  # 统一更新日，利于重抓
WX = "weiona13"
BAIDU_VERIFY = "codeva-eYDCptenb5"

# ============================================================
# 分类映射 (复用 batch-optimize.py 思路)
# ============================================================
CATEGORY = {
    "yangzhou-chedidai": "车抵贷", "carloan": "车抵贷",
    "yangzhou-anjieche": "车抵贷", "yangzhou-dangtian-fangkuan": "车抵贷",
    "yangzhou-siren-jieqian": "车抵贷",
    "debt-collection": "负债自救", "yangzhou-cuishou": "负债自救",
    "debt-creditcard": "负债自救", "debt-deferral": "负债自救",
    "debt-negotiation": "负债自救", "yangzhou-wangdai-xieshang": "负债自救",
    "yangzhou-credit-card-xieshang": "负债自救", "yangzhou-debt-restructure": "负债自救",
    "yidaiyangdai-": "债务置换", "lixi-duibi": "利息对比", "loanfix": "债务置换",
    "debt-strategy": "负债自救", "debt-car-after-overdue": "负债自救",
    "debt-microloan-phone": "负债自救", "debt-penalty": "负债自救",
    "debt-guarantor": "负债自救", "debt-lawsuit": "负债自救",
    "debt-illegal-loan": "防骗避坑", "debt-fees-scam": "防骗避坑",
    "yangzhou-zhongjie-kaopu": "防骗避坑",
    "credit": "征信", "yangzhou-bushang-zhengxin": "征信",
    "debt-blacklist": "征信", "bank-reject": "征信", "debt-credit-report": "征信",
    "debt": "负债自救",
    "bizloan": "资金周转", "biz-bank": "资金周转", "bank-products": "资金周转",
    "yangzhou-ccb": "银行贷款", "yangzhou-abc": "银行贷款", "yangzhou-icbc": "银行贷款",
    "yangzhou-psbc": "银行贷款", "yangzhou-rcb": "银行贷款", "yangzhou-jsb": "银行贷款",
    "yangzhou-njcb": "银行贷款", "yangzhou-suzhou-bank": "银行贷款",
    "yangzhou-gjj": "银行贷款",
}

def get_category(name):
    for prefix, cat in sorted(CATEGORY.items(), key=lambda x: -len(x[0])):
        if name.startswith(prefix):
            return cat
    return "个人成长"

# ============================================================
# 意图漏斗: 文件名前缀 → (FAQ分类, keywords, 场景短语)
# FAQ分类: carloan / debt / credit / bank / None(情感成长类不加FAQ)
# ============================================================
INTENT_MAP = {
    # —— 车抵贷 / 资产变现 / 急迫型 ——
    "carloan": ("carloan",
        "扬州车抵贷,不押车贷款,当天放款,车抵押能贷多少,全款车抵押,按揭车再贷,车抵贷利息,扬州资金周转",
        "不押车当天放款，额度3-50万，征信花也能办"),
    "yangzhou-chedidai": ("carloan",
        "扬州车抵贷哪家正规,扬州不押车贷款,车抵贷利息多少,车抵贷当天放款,扬州车抵押,车抵贷避坑,扬州资金周转,正规车抵贷",
        "扬州车抵贷正规公司，不押车当天放款，避坑指南"),
    "yangzhou-anjieche": ("carloan",
        "扬州按揭车抵押,按揭车不押车借钱,车贷没还完能贷吗,二次抵押车,扬州按揭车再贷,不押车当天拿钱,扬州车抵贷,资金周转",
        "按揭车不押车也能借钱，二次抵押当天拿钱"),
    "yangzhou-dangtian-fangkuan": ("carloan",
        "扬州当天放款,扬州急用钱今天到账,10分钟下款,24小时借钱,扬州当天放款贷款,急用钱扬州,快速借款,扬州车抵贷当天",
        "扬州当天放款，急用钱今天到账，车抵贷上午办下午到"),
    "yangzhou-siren-jieqian": ("carloan",
        "扬州私人借钱,扬州本地借款,私人放款联系方式,扬州应急借款,扬州资金周转,私人借钱正规渠道,扬州借钱,本地放款",
        "扬州本地借款渠道，应急周转，正规不坑"),
    # —— 债务困境 / 协商 / 上岸 ——
    "debt-collection": ("debt",
        "催收爆通讯录,催收上门,违法催收,催收报警,12378投诉催收,扬州催收,制止催收,网贷催收怎么办",
        "催收爆通讯录、威胁上门？合法应对+12378投诉"),
    "yangzhou-cuishou": ("debt",
        "扬州催收,扬州催收爆通讯录,扬州违法催收,扬州催收投诉,扬州网贷催收,催收上门怎么办,12378投诉,反催收",
        "扬州催收爆通讯录怎么办，报警+12378投诉制止"),
    "debt-creditcard": ("debt",
        "信用卡逾期,信用卡催收,信用卡还不上,信用卡停息挂账,信用卡分期,扬州信用卡逾期,信用卡协商,债务优化",
        "信用卡逾期还不上，停息挂账+个性化分期协商"),
    "debt-deferral": ("debt",
        "网贷延期还款,网贷协商延期,延期还款话术,网贷逾期协商,自己协商延期,扬州网贷协商,债务延期,停息挂账",
        "网贷逾期协商延期，自己就能谈，不用找第三方"),
    "debt-negotiation": ("debt",
        "债务协商,网贷协商还款,债务谈判,协商减免,债务重组协商,扬州债务协商,还款协商,债务优化",
        "债务协商还款，减免+分期，自己跟平台谈"),
    "yangzhou-wangdai-xieshang": ("debt",
        "扬州网贷协商,扬州网贷延期,网贷逾期协商话术,自己协商延期,扬州网贷还款协商,停息挂账,债务协商,上岸",
        "扬州网贷逾期协商延期，话术全攻略，自己就能谈"),
    "yangzhou-credit-card-xieshang": ("debt",
        "信用卡停息挂账,信用卡个性化分期,60期分期,信用卡逾期协商,银行管理办法70条,扬州信用卡协商,停息挂账怎么谈,债务优化",
        "信用卡停息挂账怎么谈，个性化分期最高60期"),
    "yangzhou-debt-restructure": ("debt",
        "扬州债务重组,债务优化,高息转低息,债务整合,负债高怎么办,扬州债务重组方案,债务置换,上岸",
        "扬州债务重组，高息转低息，3步优化上岸"),
    "yidaiyangdai-shangan": ("debt",
        "以贷养贷,上岸方法,债务上岸,网贷上岸实录,以贷养贷怎么办,扬州上岸,债务规划,停掉网贷",
        "以贷养贷越陷越深，一个能照做的上岸实录"),
    "lixi-duibi": ("debt",
        "网贷利息,车抵贷利息,利息对比,网贷和车抵贷差多少,借款利息计算,扬州低息贷款,高息置换低息,资金周转",
        "网贷和车抵贷利息差多少，一张表算清楚"),
    "loanfix": ("debt",
        "网贷还不起,低息置换高息,债务置换,网贷上岸,低息贷款置换,扬州债务置换,高息转低息,资金周转",
        "网贷还不起，用低息置换高息，一年省几千"),
    "debt-strategy": ("debt",
        "债务规划,上岸策略,负债怎么办,债务整理,还款计划,扬州债务规划,上岸方法,债务优化",
        "负债怎么规划才能上岸，一份可执行的还款策略"),
    "debt-car-after-overdue": ("debt",
        "车贷逾期,车抵贷逾期,逾期车被拖,车贷还不上,扬州车贷逾期,逾期后怎么办,车抵贷逾期处理,负债自救",
        "车贷/车抵贷逾期了怎么办，车被拖前怎么处理"),
    "debt-microloan-phone": ("debt",
        "网贷电话催收,微粒贷逾期,借呗逾期,网贷催收电话,扬州网贷逾期,网贷应对,催收电话,负债自救",
        "微粒贷借呗逾期催收电话，怎么应对不爆通讯录"),
    "debt-penalty": ("debt",
        "网贷逾期后果,逾期罚息,逾期上征信吗,逾期会坐牢吗,扬州逾期后果,网贷逾期影响,债务逾期,扬州",
        "网贷逾期有什么后果，罚息上征信会不会坐牢"),
    "debt-guarantor": ("debt",
        "担保人责任,担保人被催收,担保人征信,替人担保后果,扬州担保,担保人怎么办,担保贷款,负债自救",
        "替人担保被催收，担保人责任和自救方法"),
    "debt-lawsuit": ("debt",
        "网贷起诉,被起诉怎么办,12368短信,法院传票,扬州网贷起诉,借款纠纷,应诉,负债自救",
        "网贷说要起诉你，12368短信真假，被起诉怎么办"),
    "debt-illegal-loan": ("debt",
        "套路贷,高利贷,违法贷款,714高炮,扬州套路贷,非法放贷,贷款骗局,防骗避坑",
        "套路贷高利贷怎么识别，遇到了怎么办"),
    "debt-fees-scam": ("debt",
        "贷款前期费用,贷款诈骗,中介收前期,扬州贷款骗局,贷款被骗,防骗,正规贷款,扬州",
        "贷款收前期费用是骗子吗，怎么分辨防坑"),
    "yangzhou-zhongjie-kaopu": ("debt",
        "扬州贷款中介,扬州贷款中介靠谱吗,正规贷款中介,贷款中介收费,扬州中介骗子,分辨正规中介,贷款防骗,扬州",
        "扬州贷款中介靠谱吗，3招分辨正规和骗子"),
    "debt": ("debt",
        "网贷逾期,催收应对,暴力催收,催收话术,负债逾期,网贷催收,催收电话,反催收扬州",
        "逾期后这8句话别跟催收说，附合法应对方法"),
    # —— 征信受阻型 ——
    "credit": ("credit",
        "征信花了怎么办,征信花了能贷款吗,征信查询多了,征信修复,扬州征信不好贷款,征信报告,网贷上征信,征信恢复",
        "征信花了怎么办，几步自救还能贷"),
    "yangzhou-bushang-zhengxin": ("credit",
        "扬州不上征信贷款,征信花了还能借吗,不看征信贷款,车抵贷不看征信,扬州征信不好,大数据花能借吗,征信黑名单,扬州资金周转",
        "扬州不上征信的贷款，征信花了有车就能做"),
    "debt-blacklist": ("credit",
        "征信黑名单能贷款吗,失信被执行人能借钱吗,黑名单怎么借钱,征信黑了怎么办,扬州黑户贷款,征信不良借款,黑名单车抵贷,扬州资金周转",
        "征信黑名单还能贷款吗，黑户借钱渠道"),
    "bank-reject": ("credit",
        "贷款被拒怎么办,银行贷款批不下来,征信被拒,贷款老被拒原因,扬州贷款被拒,查询多被拒,负债高被拒,车抵贷不看查询",
        "贷款老被拒怎么办，查清原因找替代方案"),
    "debt-credit-report": ("credit",
        "征信报告解读,征信不良记录,征信逾期记录,征信查询记录,扬州征信修复,征信花了多久恢复,征信异议申诉,扬州资金周转",
        "征信报告怎么看，不良记录多久能恢复"),
    # —— 银行 / 企业周转 / 替代渠道 ——
    "bizloan": ("bank",
        "个体户贷款,营业执照贷款,小微企业贷款,经营贷,扬州个体户周转,企业资金周转,营业执照能贷多少,扬州经营贷",
        "个体户缺周转，营业执照就能贷，10-100万"),
    "biz-bank": ("bank",
        "企业贷款,经营贷,税贷,商户贷,流水贷,扬州企业贷款,小微企业周转,营业执照贷款",
        "小微企业周转，税贷商户贷流水贷全对比"),
    "bank-products": ("bank",
        "银行贷款产品,扬州银行贷款,贷款产品对比,低息银行贷款,扬州资金周转,银行经营贷,信用贷,抵押贷",
        "扬州银行贷款产品对比，低息怎么选"),
    "yangzhou-ccb": ("bank",
        "扬州建设银行贷款,建行快贷,建行经营贷,建行房贷,扬州建行贷款条件,建行贷款利率,扬州银行贷款,资金周转",
        "扬州建设银行贷款条件，快贷2.88%起"),
    "yangzhou-abc": ("bank",
        "扬州农业银行贷款,农行经营贷,抵押e贷,助业快e贷,扬州农行贷款,农行贷款条件,扬州银行贷款,经营贷",
        "扬州农业银行经营贷，抵押e贷3.5%起"),
    "yangzhou-icbc": ("bank",
        "扬州工商银行贷款,工行融e借,工行信用贷,扬州工行贷款,工行贷款利率,扬州银行贷款,信用贷,资金周转",
        "扬州工商银行信用贷，融e借2.73%起"),
    "yangzhou-psbc": ("bank",
        "扬州邮储银行贷款,邮享贷,邮储贷款,扬州邮储贷款条件,邮政银行贷款,扬州银行贷款,经营贷,资金周转",
        "扬州邮储银行贷款，邮享贷2.88%起"),
    "yangzhou-rcb": ("bank",
        "扬州农商银行贷款,农商行金易通,小微惠贷,扬州农商行,农商行经营贷,扬州银行贷款,资金周转,经营贷",
        "扬州农商银行贷款，小微惠贷3.85%"),
    "yangzhou-jsb": ("bank",
        "扬州江苏银行贷款,江苏银行经营随e贷,苏科贷,扬州江苏银行,江苏银行贷款条件,扬州银行贷款,经营贷,资金周转",
        "扬州江苏银行贷款，苏科贷最高3000万"),
    "yangzhou-njcb": ("bank",
        "扬州南京银行贷款,南京银行你好e贷,苏贸贷,扬州南京银行,南京银行贷款条件,扬州银行贷款,信用贷,资金周转",
        "扬州南京银行贷款，你好e贷2.98%起"),
    "yangzhou-suzhou-bank": ("bank",
        "扬州苏州银行贷款,苏州银行人才贷,才智贷,扬州苏州银行,苏州银行贷款条件,扬州银行贷款,经营贷,资金周转",
        "扬州苏州银行贷款，人才贷才智贷"),
    "yangzhou-gjj": ("bank",
        "扬州公积金贷款,公积金能贷多少,公积金贷款额度,公积金贷款条件,扬州公积金,月缴800能贷多少,公积金提取,扬州资金周转",
        "扬州公积金能贷多少，月缴800/1000/2000算清楚"),
}

# ============================================================
# FAQ 分类模板 (命中缺资金人群高频疑问)
# ============================================================
FAQ_TEMPLATES = {
    "carloan": [
        ("扬州车抵贷征信花了能办吗？", "能。车抵贷看车不看征信，征信花、有逾期、查询多都能办，有车就能聊。"),
        ("车抵贷多久能放款？", "最快当天。上午评估验车，下午装GPS放款，不押车，车继续开。"),
        ("车抵贷要押车吗？", "不押车。装GPS即可，车你照常开，还清当天拆GPS不收费。"),
        ("扬州车抵贷额度和利息多少？", "额度3-50万，月息八厘到一分五，按车评估价定，无前期费用。"),
    ],
    "debt": [
        ("网贷还不起了怎么办？", "别失联，主动协商延期或分期，优先保住征信，可用低息置换高息。停息挂账、个性化分期自己就能谈。"),
        ("催收爆通讯录怎么制止？", "违法催收可报警+向12378投诉，保留录音证据，不要失联也不要乱承诺。"),
        ("欠网贷会不会坐牢？", "普通网贷逾期是民事纠纷不会坐牢，但套路贷、信用卡恶意透支另说。被起诉要积极应诉。"),
        ("负债太多怎么上岸？", "先停掉以贷养贷，列清债务，高息转低息，做债务重组/置换，制定可执行的还款计划。"),
    ],
    "credit": [
        ("征信花了还能贷款吗？", "能。车抵贷不看征信查询次数，有车就能做；银行信用贷对查询次数有要求。"),
        ("征信查询多了多久能恢复？", "硬查询记录保留2年，一般3-6个月不新增查询影响会减弱，养征信期间别再乱申请。"),
        ("有当前逾期还能借吗？", "当前逾期银行基本批不下来，可走车抵贷等不看征信的渠道，先把逾期处理掉。"),
    ],
    "bank": [
        ("扬州银行贷款征信要求高吗？", "银行贷款普遍看征信，查询多、机构数多、有逾期可能批不下来，名下有车可走车抵贷替代。"),
        ("营业执照能贷多少？", "个体户/小微企业凭营业执照可办经营贷、税贷、商户贷，额度10-100万，看流水和纳税。"),
        ("银行贷款多久放款？", "信用贷一般1-3个工作日，抵押贷需评估抵押登记约3-7天，急用钱可走车抵贷当天放款。"),
    ],
}

# ============================================================
# HTML 解析/改写工具
# ============================================================
TITLE_SUFFIX_RE = re.compile(r'\s*[—|\-·]\s*UP\s*男性成长\s*$', re.S)

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    if not m:
        return "", ""
    full = m.group(1).strip()
    main = TITLE_SUFFIX_RE.sub('', full).strip()
    return full, main

def get_meta(html, name):
    """取 meta content (name 或 property)"""
    m = re.search(r'<meta\s+(?:name|property)=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']', html, re.S)
    return m.group(1).strip() if m else None

def set_meta(html, name, content):
    """替换已有 meta，无则返回原 html(由调用方决定插入位置)"""
    pat = re.compile(r'(<meta\s+(?:name|property)=["\']' + re.escape(name) + r'["\']\s+content=["\'])[^"\']*(["\'])', re.S)
    if pat.search(html):
        return pat.sub(lambda m: m.group(1) + content + m.group(2), html)
    return None  # 不存在

def is_generic_desc(desc):
    """泛站描述: 同时含三大站词，或 UP男性成长 开头模板"""
    if not desc:
        return True
    if "资金周转" in desc and "情感关系" in desc and "个人成长" in desc:
        return True
    if desc.startswith("UP男性成长"):
        return True
    return False

def build_desc(main_title, scene):
    base = main_title.replace(" — UP 男性成长", "").strip()
    d = f"{base}。{scene}。扬州本地免费咨询，无前期费用。"
    if len(d) > 90:
        d = d[:88] + "。"
    return d

def build_faq(faq_cat):
    items = []
    for q, a in FAQ_TEMPLATES[faq_cat]:
        items.append({
            "@context": "https://schema.org",
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}

def build_breadcrumb(main_title, category):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": category, "item": SITE + "/#articles"},
            {"@type": "ListItem", "position": 3, "name": main_title, "item": ""},
        ],
    }

def process_jsonld(html, full_title, desc, faq_cat, main_title, category):
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S)
    if not m:
        return html, "no-jsonld"
    try:
        data = json.loads(m.group(2))
    except Exception as e:
        return html, f"jsonld-parse-err:{e}"
    changed = False
    for obj in data:
        if obj.get("@type") == "Article":
            obj["headline"] = full_title
            obj["description"] = desc
            obj["dateModified"] = TODAY
            changed = True
        elif obj.get("@type") in ("WebSite", "Organization"):
            if obj.get("description", "").startswith("UP男性成长") or is_generic_desc(obj.get("description", "")):
                obj["description"] = desc
    types = [o.get("@type") for o in data]
    if faq_cat and "FAQPage" not in types:
        data.append(build_faq(faq_cat)); changed = True
    if "BreadcrumbList" not in types:
        data.append(build_breadcrumb(main_title, category)); changed = True
    if not changed:
        return html, "jsonld-skip"
    new_block = m.group(1) + "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n  " + m.group(3)
    return html[:m.start()] + new_block + html[m.end():], "jsonld-updated"

def process_file(path, dry=False):
    name = os.path.splitext(os.path.basename(path))[0]
    html = open(path, encoding="utf-8").read()
    full_title, main_title = extract_title(html)
    category = get_category(name)
    intent = None
    for prefix in sorted(INTENT_MAP, key=lambda k: -len(k)):
        if name.startswith(prefix):
            intent = INTENT_MAP[prefix]; break
    faq_cat = intent[0] if intent else None
    actions = []

    # --- keywords ---
    if intent:
        new_kw = intent[1]
        r = set_meta(html, "keywords", new_kw)
        if r is not None:
            html = r; actions.append("kw")
        else:
            # 无 keywords meta，插到 description 后
            ins = f'\n<meta name="keywords" content="{new_kw}">'
            html = re.sub(r'(<meta\s+name="description"[^>]*>)', r'\1' + ins, html, count=1)
            actions.append("kw+")

    # --- description (仅泛站替换) ---
    cur_desc = get_meta(html, "description") or ""
    if intent and is_generic_desc(cur_desc):
        new_desc = build_desc(main_title, intent[2])
        r = set_meta(html, "description", new_desc)
        if r is not None:
            html = r; actions.append("desc")
            cur_desc = new_desc
    # 同步 WebSite description 若是泛站，也在 process_jsonld 内处理

    # --- og:title ---
    og_t = get_meta(html, "og:title")
    if og_t in (None, "UP 男性成长", "UP 男性成长 "):
        target = full_title
        r = set_meta(html, "og:title", target)
        if r is not None:
            html = r; actions.append("ogt")
        else:
            ins = f'\n<meta property="og:title" content="{target}">'
            html = re.sub(r'(<meta\s+property="og:image"[^>]*>)', r'\1' + ins, html, count=1)
            actions.append("ogt+")

    # --- og:description ---
    og_d = get_meta(html, "og:description")
    if (og_d in (None, "") or is_generic_desc(og_d)) and cur_desc:
        r = set_meta(html, "og:description", cur_desc)
        if r is not None:
            html = r; actions.append("ogd")
        else:
            ins = f'\n<meta property="og:description" content="{cur_desc}">'
            html = re.sub(r'(<meta\s+property="og:title"[^>]*>)', r'\1' + ins, html, count=1)
            actions.append("ogd+")

    # --- baidu-site-verification ---
    if "baidu-site-verification" not in html:
        ins = f'\n<meta name="baidu-site-verification" content="{BAIDU_VERIFY}" />'
        html = re.sub(r'(<meta\s+name="robots"[^>]*>)', r'\1' + ins, html, count=1)
        actions.append("baidu-verify")

    # --- JSON-LD ---
    html, jstat = process_jsonld(html, full_title, cur_desc, faq_cat, main_title, category)
    if jstat not in ("jsonld-skip", "no-jsonld"):
        actions.append(jstat)

    if not dry and actions:
        open(path, "w", encoding="utf-8").write(html)
    return name, faq_cat or "-", ",".join(actions) if actions else "skip"

# ============================================================
# sitemap 重生成 (补 lastmod / changefreq)
# ============================================================
def regen_sitemap():
    entries = [("https://dayue.tech/", 1.0, "daily")]
    for f in sorted(glob.glob(os.path.join(ART, "*.html"))):
        name = os.path.splitext(os.path.basename(f))[0]
        cat = get_category(name)
        url = f"{SITE}/articles/{name}.html"
        # priority
        if name in ("carloan", "yangzhou-chedidai") or cat == "车抵贷":
            pri, freq = 0.9, "weekly"
        elif cat in ("负债自救", "征信", "债务置换", "利息对比", "防骗避坑"):
            pri, freq = 0.85, "weekly"
        elif cat in ("银行贷款", "资金周转"):
            pri, freq = 0.8, "monthly"
        elif cat in ("情感关系", "分手失恋", "个人成长"):
            pri, freq = 0.6, "monthly"
        else:
            pri, freq = 0.6, "monthly"
        entries.append((url, pri, freq))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, pri, freq in entries:
        lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    lines.append('</urlset>')
    out = "\n".join(lines) + "\n"
    open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8").write(out)
    return len(entries)

# ============================================================
def main():
    dry = "--check" in sys.argv
    if dry:
        print("=== CHECK 模式 (不写文件) ===")
    files = sorted(glob.glob(os.path.join(ART, "*.html")))
    print(f"共 {len(files)} 篇文章\n")
    cnt = {"faq_added": 0, "touched": 0, "skip": 0}
    for f in files:
        name, faq, acts = process_file(f, dry=dry)
        if faq != "-":
            cnt["faq_added"] += 1
        if acts == "skip":
            cnt["skip"] += 1
        else:
            cnt["touched"] += 1
        print(f"  {name:32s} faq={faq:7s} {acts}")
    if not dry:
        n = regen_sitemap()
        print(f"\nsitemap.xml 重生成: {n} 条 URL (含 lastmod/changefreq)")
    print(f"\n汇总: 改动 {cnt['touched']} 篇, 跳过 {cnt['skip']} 篇, 注入FAQ {cnt['faq_added']} 篇")

if __name__ == "__main__":
    main()
