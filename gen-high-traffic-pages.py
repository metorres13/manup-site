#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成6篇高搜索量落地页"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://dayue.tech"

LQ = '\u300c'  # 「
RQ = '\u300d'  # 」
DASH = '\u2014\u2014'  # ——

pages = []

# 1
pages.append({
    "slug": "yangzhou-dangtian-fangkuan",
    "title": "扬州当天放款的贷款有哪些？急用钱今天就要拿到钱怎么办",
    "desc": "扬州急用钱当天放款最快多久到账？车抵贷当场评估当天放款，不押车、不查征信查询次数和机构数。3-50万当天拿钱。",
    "h1": "扬州当天放款的贷款" + DASH + "急用钱今天就要",
    "intro": "急用钱的时候，一天都等不了。房租要交了、货款要付了、家人住院了" + DASH + "这种时候你需要的不是" + LQ + "审核3-5个工作日" + RQ + "，而是今天就能拿到钱的渠道。",
    "sections": [
        ("当天放款的几种渠道", "银行贷款最快也要1-3个工作日，而且征信查询多、机构数多直接拒。网贷看似快但额度低、利率高，每点一次就多一条查询记录。车抵贷是少数真正能做到当天放款的渠道" + DASH + "上午评估、下午放款，不押车、不查查询次数和贷款账户数。"),
        ("为什么车抵贷能当天放款", "车抵贷看的是车不是征信。你有车、车有价值、车在你名下" + DASH + "剩下的就是评估残值、签合同、放款。整个流程3-4个小时。而银行贷款要查征信、查查询次数、查机构数、查负债率" + DASH + "查完基本就拒了。"),
    ],
    "tip": "急用钱的时候最容易被骗" + DASH + "越急越要冷静。正规车抵贷当天放款，不押车、不收前期费用。",
    "pivot": "如果你在扬州急用钱，名下有车的话" + DASH + "车抵贷是目前最快、最正规的当天放款渠道。不押车、当天拿钱、不看征信查询多和机构数多。",
})

# 2
pages.append({
    "slug": "yangzhou-anjieche",
    "title": "扬州按揭车不押车借钱哪里正规？按揭没还完也能贷",
    "desc": "扬州按揭车不押车借钱，车贷没还完也能做二次抵押。不押车、不装GPS、当天放款。按揭车也能再贷一笔出来。",
    "h1": "扬州按揭车不押车借钱" + DASH + "车贷没还完也能贷",
    "intro": "很多人以为车贷没还完就不能再借钱了" + DASH + "其实按揭车也可以做二次抵押。扬州按揭车不押车借钱：车你继续开、贷款不还完也没关系、当天拿钱。",
    "sections": [
        ("按揭车怎么操作", "按揭车做二次抵押不需要先还清车贷。评估车辆当前残值（扣除剩余车贷后就是可贷额度），签合同、放款。流程和全款车一样，只是额度会扣除未还部分。比如车值20万、还剩5万车贷没还" + DASH + "大约可贷10-12万。"),
        ("不押车是什么意思", "不押车就是不扣你的车、不装GPS、不收备用钥匙。你正常开车上下班，钱照样拿到手。这对于只有一辆车的家庭来说很重要" + DASH + "车被押走了工作和生活都受影响。"),
    ],
    "tip": "按揭车不押车借钱在扬州正规渠道就能办，不用找中介代办，直接来咨询。",
    "pivot": "按揭车不押车借钱" + DASH + "车你继续开、钱你当天拿。征信查询多、机构数多也不影响，看的是车不是征信。",
})

# 3
pages.append({
    "slug": "yangzhou-siren-jieqian",
    "title": "扬州私人借钱联系方式" + DASH + "急用钱找本地正规渠道更靠谱",
    "desc": "扬州私人借钱急用钱哪里找？本地私人放款鱼龙混杂，不如正规车抵贷：不押车、当天放款、不收前期费用。",
    "h1": "扬州私人借钱" + DASH + "急用钱找对渠道",
    "intro": "搜" + LQ + "扬州私人借钱" + RQ + "的人，十有八九是被银行和网贷拒过了。走投无路了才找私人。但是" + DASH + "私人借钱水太深。利息说不清、合同做手脚、还不上翻倍涨。",
    "sections": [
        ("私人借钱的风险", "私人放款的问题：第一，利息没有标准，借1万到手8000的都有。第二，催收没有底线" + DASH + "半夜上门、骚扰家人、扣车扣人。第三，还不上就利滚利，一个月翻一倍不是开玩笑。很多扬州人一开始只是差几万块，找到私人借钱后欠了十几万。"),
        ("什么情况下可以找私人", "什么情况下都别找私人。你说你已经征信花了、网贷全拒了" + DASH + "但只要你名下有车，车抵贷不需要看征信。正规渠道、签合同、走对公账户。利息透明、不押车、当天放款。"),
    ],
    "tip": "搜" + LQ + "私人借钱" + RQ + "的人，其实不是要找私人，是要找一个不查征信的正规渠道" + DASH + "车抵贷就是这个渠道。",
    "pivot": "你在扬州如果有车" + DASH + "不用找私人借钱。车抵贷不看征信查询多、不查机构数多、不看你欠了多少网贷。当天评估当天放款。",
})

# 4
pages.append({
    "slug": "yangzhou-zhongjie-kaopu",
    "title": "扬州贷款中介靠谱吗？怎么分辨正规贷款业务员和骗子",
    "desc": "扬州贷款中介靠谱吗？正规的中介不收前期费用、不承诺包下款、不让你做假资料。3招分辨骗子和正规业务员。",
    "h1": "扬州贷款中介靠谱吗？正规的怎么找",
    "intro": "扬州贷款中介这个行业，有真正帮你解决问题的，也有专门坑人的。问题不是你应不应该找中介，而是你怎么分辨谁是靠谱的。",
    "sections": [
        ("正规中介长什么样", "1）不收前期费用" + DASH + "正规中介是放款后收服务费，放款前不收一分钱。2）不承诺100%下款" + DASH + "任何说" + LQ + "包过" + RQ + "" + LQ + "包下款" + RQ + "的都是假的。3）不做假资料" + DASH + "让你伪造流水、假工作证明的，出了事你背锅。"),
        ("骗子中介的套路", "先收保证金/包装费/加急费" + DASH + "收了钱就消失。" + LQ + "不看征信不看负债只要身份证" + RQ + "" + DASH + "这种话你也信？" + LQ + "内部有人" + RQ + "" + LQ + "银行有关系" + RQ + "" + DASH + "都是话术。"),
    ],
    "tip": "扬州做贷款中介的有几百家，真正靠谱的不到三分之一。记住：放款前不收钱、不承诺包过、不做假材料" + DASH + "三条符合就是正规的。",
    "pivot": "不管找不找中介，最后能走通的渠道才是真的。查询多、机构数多、征信花了" + DASH + "车抵贷不看这些。正规渠道、签合同走对公、当天放款。",
})

# 5
pages.append({
    "slug": "yangzhou-bushang-zhengxin",
    "title": "扬州不上征信的贷款有哪些？征信花了网贷全拒还有办法吗",
    "desc": "扬州不上征信的贷款哪里找？正规渠道中车抵贷不查征信记录、不看查询次数和机构数。名下有车就能做，不押车当天放款。",
    "h1": "扬州不上征信的贷款" + DASH + "征信花了但有车就行",
    "intro": "搜" + LQ + "不上征信的贷款" + RQ + "的人，征信基本都花透了。查了无数次、拒了无数次、能点的网贷全点了。正规渠道里还有一个最后的选择：车抵贷。",
    "sections": [
        ("为什么说车抵贷是唯一选择", "车抵贷是所有正规贷款里对征信要求最低的。它不看你的征信查询次数、不看你有多少家机构的贷款、不看你的网贷笔数。只查有没有当前逾期。没有当前逾期，名下有车就能做。"),
        ("其他的不上征信都是坑", "所谓的" + LQ + "不上征信的网贷平台" + RQ + "大部分利息高得离谱（年化36%以上）。真正正规且不上征信的渠道，只有抵押类贷款（车抵贷、房抵贷），因为它们看的是抵押物不是信用记录。"),
    ],
    "tip": "征信花了不代表借不到钱了。名下有车，车抵贷就是你的备用金。",
    "pivot": "征信花、查询多、机构数多、网贷全拒" + DASH + "这些都不影响车抵贷。有车就能做，不看征信记录。扬州本地当天拿钱。",
})

# 6
pages.append({
    "slug": "yangzhou-cuishou",
    "title": "扬州催收爆通讯录怎么办？网贷催收骚扰家人怎么制止",
    "desc": "扬州网贷催收爆通讯录、骚扰家人怎么办？催收违法！爆通讯录可报警、可投诉12378。主动协商延期还款才是正解。",
    "h1": "扬州催收爆通讯录怎么办？怎么制止",
    "intro": "网贷逾期了，催收开始爆通讯录" + DASH + "打电话给你家人、朋友、同事，甚至发短信威胁。这是违法的。",
    "sections": [
        ("爆通讯录是违法的", "根据《互联网金融逾期债务催收自律公约》，催收人员不得骚扰债务人的家人、朋友、同事，不得向无关第三人透露债务信息。爆通讯录、威胁恐吓" + DASH + "这些行为可以报警处理。保存好通话录音和短信截图，直接打110。"),
        ("怎么制止催收骚扰", "告诉催收" + LQ + "我已录音，你爆通讯录的行为已违法" + RQ + "" + DASH + "再打一次我就报警+投诉12378。和家人朋友说清楚" + DASH + "你的债务和他们无关。收集证据向12378投诉该平台暴力催收。"),
    ],
    "tip": "催收爆通讯录是违法的，你可以报警。但更根本的办法是把债务解决" + DASH + "车抵贷置换高息网贷，一步上岸。",
    "pivot": "爆通讯录只是催收的开始。如果你有车，车抵贷可以帮你把所有高息网贷一次性还清。不押车、当天放款、不看查询次数和机构数" + DASH + "这才是真正解决催收的办法。",
})

def gen_page(data):
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + data['title'] + """ — UP 男性成长</title>
<link rel="canonical" href=""" + '"' + SITE + '/articles/' + data['slug'] + '.html' + """"/>
<meta name="description" content=""" + '"' + data['desc'] + """"/>
<meta name="keywords" content=""" + '"' + data['slug'].replace('-', ',') + ',扬州贷款,扬州车抵贷' + """"/>
<meta property="og:image" content="https://dayue.tech/og-image.jpg"/>
<meta name="robots" content="index, follow">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif;background:#fff;color:#1d1d1f;line-height:1.8;padding:24px;max-width:720px;margin:0 auto}
.back{font-size:14px;color:#86868b;text-decoration:none;display:inline-block;margin-bottom:24px}
h1{font-size:28px;font-weight:700;margin-bottom:12px;line-height:1.3}
h2{font-size:20px;font-weight:600;margin:28px 0 12px;padding-bottom:4px;border-bottom:2px solid #f5f5f7}
p{font-size:15px;margin-bottom:14px;color:#333}
.tip{background:#fffbe6;border-left:4px solid #f59e0b;padding:12px 16px;margin:20px 0;border-radius:4px;font-size:14px}
.cta{text-align:center;margin:40px 0;padding:32px 20px;background:#1d1d1f;border-radius:12px;color:#fff}
.cta h3{font-size:18px;color:#fff;margin-bottom:8px}
.cta p{font-size:14px;color:#aaa;margin-bottom:16px}
.cta .wx{font-size:22px;font-weight:700;color:#f59e0b}
.related{margin-top:48px;padding-top:24px;border-top:1px solid #eee}
.related p{font-size:14px;color:#86868b;margin-bottom:12px}
.related a{display:block;font-size:14px;color:#06c;margin-bottom:8px;text-decoration:none}
</style>
</head>
<body>
<a class="back" href="../index.html">&larr; 返回首页</a>
<h1>""" + data['h1'] + """</h1>
<p>""" + data['intro'] + """</p>
"""
    for title, content in data['sections']:
        html += "<h2>" + title + "</h2>\n<p>" + content + "</p>\n"
    html += """<div class="tip">""" + data['tip'] + """</div>
<p>""" + data['pivot'] + """</p>
<div class="cta">
  <h3>扬州本地 · 免费咨询</h3>
  <p>车抵贷 · 不押车 · 当天放款 · 不看征信查询多</p>
  <div class="wx">weiona13</div>
  <div style="font-size:11px;color:#999;margin-top:8px">具体放款由合作持牌机构操作</div>
</div>
<div class="related">
<p>相关推荐：</p>
<a href="/articles/carloan.html">&rarr; 车抵贷：不押车、当天放款、额度3-50万</a>
<a href="/articles/yangzhou-chedidai.html">&rarr; 扬州车抵贷哪家正规？不押车全攻略</a>
<a href="/articles/credit.html">&rarr; 查询多、机构数多、贷款账户数太多？征信花了怎么办</a>
</div>
</body>
</html>"""
    return html

for p in pages:
    html = gen_page(p)
    fpath = os.path.join(BASE, "articles", p['slug'] + ".html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK articles/" + p['slug'] + ".html")
