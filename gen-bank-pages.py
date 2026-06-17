#!/usr/bin/env python3
"""一键生成 8 篇 扬州+银行 关键词落地页"""

import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://dayue.tech"

# 每个银行的数据
BANKS = [
    {
        "slug": "yangzhou-ccb",
        "title": "扬州建设银行贷款条件 — 快贷、经营贷、房贷最新政策",
        "desc": "扬州建设银行贷款条件有哪些？建行快贷利率低至2.88%，经营贷最高1000万。查询多、机构数多也能沟通。",
        "h1": "扬州建设银行贷款条件",
        "products": [
            ("建行快贷", "纯信用，最高50万，年化2.88%起，随借随还"),
            ("建行经营贷", "最高1000万，需营业执照满1年，支持房产抵押"),
            ("建行房贷", "首套利率低至3.0%，支持公积金组合贷"),
        ],
        "feature": "2026年扬州担保与建行联合推出「建银信保贷」，免抵押最高1000万",
    },
    {
        "slug": "yangzhou-abc",
        "title": "扬州农业银行经营贷 — 条件、利率、额度全解析",
        "desc": "扬州农业银行经营贷，抵押e贷年化3.5%起，助业快e贷2.85%起。个体户、小微企业主均可申请。",
        "h1": "扬州农业银行经营贷",
        "products": [
            ("抵押e贷", "最高1000万，年化3.5%起，期限最长10年"),
            ("助业快e贷", "最高300万，年化2.85%起，纯信用，凭流水申请"),
            ("商户e贷", "最高50万，凭收款码流水申请"),
        ],
        "feature": "农行经营贷支持无还本续贷，优质客户利率可至3.0%",
    },
    {
        "slug": "yangzhou-icbc",
        "title": "扬州工商银行信用贷 — 融e借利率、额度、申请条件",
        "desc": "扬州工商银行信用贷融e借，年化2.73%起，最高100万，最长7年。公积金/社保/代发工资客户优先。",
        "h1": "扬州工商银行信用贷",
        "products": [
            ("融e借", "最高100万，年化2.73%起，线上最高50万"),
            ("工行经营贷", "需营业执照，支持房产抵押，额度灵活"),
        ],
        "feature": "工行代发工资客户、房贷客户优先审批，线上秒批秒贷",
    },
    {
        "slug": "yangzhou-psbc",
        "title": "扬州邮储银行贷款利率 — 邮享贷、经营贷、贴息政策",
        "desc": "扬州邮储银行贷款利率，邮享贷2.88%起，小微易贷3.5%以下。2026年8月前享个人消费贷贴息。",
        "h1": "扬州邮储银行贷款利率",
        "products": [
            ("邮享贷", "年化2.88%起，3年期，先息后本"),
            ("小微易贷", "综合成本3.5%以下，随借随还"),
            ("房产抵押经营贷", "年化3.2%-4.0%，最高房产评估价8成"),
        ],
        "feature": "2025.9-2026.8期间，个人消费贷可享年化1%财政贴息，最高3000元",
    },
    {
        "slug": "yangzhou-rcb",
        "title": "扬州农商银行贷款 — 金易通、惠民e贷、经营贷产品介绍",
        "desc": "扬州农商银行贷款产品全解：金易通信贷年5.8%，小微惠贷低至3.85%。本地银行审批灵活。",
        "h1": "扬州农商银行贷款",
        "products": [
            ("金易通", "年利率5.8%，最高30万，纯线上公积金贷"),
            ("惠民e贷", "纯信用，手机银行自助放款"),
            ("小微惠贷", "年化3.85%起，单户1000万以内"),
        ],
        "feature": "扬州农商行是本地法人银行，审批灵活，沟通空间大",
    },
    {
        "slug": "yangzhou-jsb",
        "title": "扬州江苏银行贷款 — 经营随e贷、苏科贷、利率条件",
        "desc": "扬州江苏银行贷款产品：经营随e贷最高1000万，苏科贷最高3000万有贴息。科技企业、个体户均可。",
        "h1": "扬州江苏银行贷款",
        "products": [
            ("经营随e贷", "最高1000万，年化4%-5%"),
            ("苏科贷", "最高3000万，享财政贴息"),
            ("惠捷贷", "最高300万，面向农业经营主体"),
        ],
        "feature": "江苏银行扬州分行普惠小微贷款利率再降56BP",
    },
    {
        "slug": "yangzhou-njcb",
        "title": "扬州南京银行贷款 — 你好e贷利率、经营贷、条件介绍",
        "desc": "扬州南京银行贷款，你好e贷年化2.98%起，线上最高20万。苏贸贷、苏旅贷等特色产品可享贴息。",
        "h1": "扬州南京银行贷款",
        "products": [
            ("你好e贷", "年化2.98%起，线上最高20万，线下最高30万"),
            ("出口快贷", "面向外贸企业，利率优惠"),
            ("苏贸贷", "最高1000万，政银合作低成本"),
        ],
        "feature": "南京银行扬州分行科创企业首贷可享年化1%贴息",
    },
    {
        "slug": "yangzhou-suzhou-bank",
        "title": "扬州苏州银行贷款 — 人才贷、才智贷、利率条件",
        "desc": "扬州苏州银行贷款，才智贷最高1000万，人才贷最高1500万。各类人才可享利率优惠。",
        "h1": "扬州苏州银行贷款",
        "products": [
            ("才智贷", "最高1000万，经营类，利率优惠"),
            ("人才贷", "最高1500万，纯信用"),
        ],
        "feature": "苏州银行扬州分行推出「绿扬金凤」人才金融卡，一卡通办22项金融服务",
    },
]

def gen_page(bank):
    slug = bank["slug"]
    title = bank["title"]
    desc = bank["desc"]
    h1 = bank["h1"]
    products = bank["products"]
    feature = bank["feature"]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{SITE}/articles/{slug}.html">
<meta name="description" content="{desc}">
<meta name="keywords" content="{slug.replace('-', ',')},扬州车抵贷,扬州贷款">
<meta property="og:image" content="https://dayue.tech/og-image.jpg">
<meta name="robots" content="index, follow">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif;background:#fff;color:#1d1d1f;line-height:1.8;padding:24px;max-width:720px;margin:0 auto}}
.back{{font-size:14px;color:#86868b;text-decoration:none;display:inline-block;margin-bottom:24px}}
h1{{font-size:28px;font-weight:700;margin-bottom:12px;line-height:1.3}}
.date{{font-size:13px;color:#aaa;margin-bottom:32px}}
h2{{font-size:20px;font-weight:600;margin:28px 0 12px}}
p{{font-size:15px;margin-bottom:14px;color:#333}}
.box{{background:#f5f5f7;border-radius:12px;padding:20px;margin:20px 0}}
.box h4{{font-size:16px;font-weight:600;margin-bottom:8px}}
.box p{{font-size:14px;color:#86868b;margin:0}}
.cta{{text-align:center;margin-top:40px;padding:32px 20px;background:#1d1d1f;border-radius:12px;color:#fff}}
.cta h3{{font-size:18px;color:#fff;margin-bottom:8px}}
.cta p{{font-size:13px;color:#aaa;margin-bottom:16px}}
.cta .wx{{font-size:22px;font-weight:700;color:#f59e0b;margin:12px 0}}
.cfoot{{text-align:center;margin-top:16px;font-size:12px;color:#666}}
</style>
</head>
<body>
<a class="back" href="../index.html">← 返回首页</a>
<h1>{h1}</h1>
<div class="date">扬州 · 贷款咨询</div>

<p>{desc}</p>

<h2>主要产品</h2>
<div class="box">
"""

    for name, detail in products:
        html += f"<h4>✅ {name}</h4><p style='margin-left:0;'>{detail}</p>"

    html += f"""</div>

<p><strong>{feature}</strong>。但注意——银行审批看征信、看查询次数、看负债率。如果你的<strong>查询多、机构数多、贷款账户数太多</strong>，银行贷款很可能批不下来。</p>

<p>这不是你一个人的问题——大多数被银行拒的人不是因为逾期，而是因为查询多、机构数多、贷款账户数太多。银行系统自动标记为"多头借贷"，直接拒。</p>

<p>但是——<strong>车抵贷不看这些</strong>。车抵贷看的是你名下有没有车、车的残值够不够。征信只查有没有当前逾期，不关心你查询多少次、有几家机构的贷款。</p>

<div class="cta">
  <h3>查询多、银行拒了？</h3>
  <p>扬州本地 · 免费评估车辆额度 · 不押车当天放款</p>
  <div class="wx">weiona13</div>
  <div class="cfoot">线上咨询 · 隐私保障 · 不收取前期费用</div>
  <div style="font-size:11px;color:#999;margin-top:8px">具体放款由合作持牌机构操作</div>
</div>

<div class="related">
<p style="font-size:14px;color:#86868b;">相关推荐：</p>
<a href="/articles/carloan.html">→ 车抵贷：不押车、当天放款、额度3-50万</a>
<a href="/articles/credit.html">→ 查询多、机构数多、贷款账户数太多？征信花了怎么办</a>
<a href="/articles/yangzhou-chedidai.html">→ 扬州车抵贷哪家正规？不押车全攻略</a>
<a href="/articles/debt-car-after-overdue.html">→ 逾期了征信花了还能贷款吗？车抵贷是唯一出路</a>
</div>

</body>
</html>"""
    return html


def main():
    for bank in BANKS:
        slug = bank["slug"]
        html = gen_page(bank)
        fpath = os.path.join(BASE, "articles", f"{slug}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ articles/{slug}.html")

if __name__ == "__main__":
    main()
