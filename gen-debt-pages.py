#!/usr/bin/env python3
"""生成4篇公积金+负债协商关键词落地页"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://dayue.tech"

PAGES = [
    {
        "slug": "yangzhou-gjj",
        "title": "扬州公积金贷款能贷多少钱？月缴800/1000/2000额度对照 — UP 男性成长",
        "desc": "扬州公积金月缴800能贷多少？2026年单缴存人最高108万双缴180万。月缴800约可贷30-40万，月缴2000可贷80-108万。",
        "h1": "扬州公积金贷款能贷多少钱？",
        "intro": "2026年扬州公积金政策大幅放宽。单缴存人最高可贷108万，双缴存人最高180万。但很多人最关心的是——我每个月交800块钱，到底能贷多少钱出来？",
        "sections": [
            ("月缴800元能贷多少", 
             "月缴800元（个人+单位合计），缴存基数约8000元，连续缴满2年余额约1.9万。按账户余额20倍计算约38万。综合还贷能力核算后，大约可贷30-40万。注意：2026年新增最低保障额度30万，就算算出来很低也不会低于30万。"),
            ("月缴1000元能贷多少",
             "月缴1000元，缴存基数约1万，连续缴满2年余额约2.4万。按20倍计算约48万，综合估算可贷45-60万。如果是本科及以上学历，额度还可上浮20%。"),
            ("月缴2000元能贷多少",
             "月缴2000元，缴存基数约2万，连续缴满2年余额约4.8万。按20倍计算约96万，接近单缴存人最高限额108万。综合评估后可贷80-108万。"),
        ],
        "tip": "以上为估算值，实际以公积金中心系统核算为准。微信搜索「扬州住房公积金」小程序可试算准确额度。",
        "pivot": "但是注意——公积金贷款对征信要求很高。查询多、机构数多、贷款账户数太多、有逾期记录，都可能被拒。如果你公积金有余额但是征信过不了银行审批，车抵贷是另一条路：不押车、当天放款、看车不看征信记录。",
    },
    {
        "slug": "yangzhou-wangdai-xieshang",
        "title": "网贷逾期了怎么协商延期还款？话术流程全攻略 — UP 男性成长",
        "desc": "网贷逾期还不上了怎么办？主动协商延期还款，3步搞定。话术+证明材料+避坑指南，自己就能谈，不用花钱找第三方。",
        "h1": "网贷逾期了怎么协商延期还款？",
        "intro": "网贷逾期了，催收电话一天打几十个，利息违约金每天在涨，但手上真的没钱还——这种时候唯一正确的做法是：主动找平台协商延期还款。",
        "sections": [
            ("协商前的准备",
             "打电话之前先理清三件事：1）欠了哪些平台、本金多少、逾期多久、利息多少；2）月收入多少、必要生活开支多少、每月能还多少；3）准备好困难证明——失业证明、病历、解除劳动合同通知、银行流水。没有这些材料，平台不会信你。"),
            ("协商话术",
             "打电话给平台官方客服，语气平静地说：'你好，我并非恶意逾期，目前因为XX原因（失业/生病/家里出事）暂时没有还款能力，但我有强烈的还款意愿。我目前每月收入X元，扣除生活费后能拿出X元还款，希望能申请延期X个月或分期X期。'注意：不要说'我没钱'——这句话催收天天听，没用。给一个具体方案。"),
            ("避坑指南",
             "1）不要失联——失联=放弃协商，平台直接走起诉。2）不要以贷养贷——借新还旧只会越陷越深。3）不要找第三方代办——正规协商自己就能做，收费的都是骗子。4）协商成功后一定要拿到书面确认（APP站内信或短信），口头承诺不算数。"),
        ],
        "tip": "如果平台拒绝协商，可向12378（银保监会热线）投诉该平台'在借款人无力偿还的情况下拒绝平等协商'。",
        "pivot": "如果网贷已经全面逾期、查询多、机构数多、根本借不到钱了——车抵贷是目前少数还能走通的渠道。名下有车就能沟通，不押车、当天放款、不看网贷记录。",
    },
    {
        "slug": "yangzhou-credit-card-xieshang",
        "title": "信用卡逾期停息挂账怎么跟银行谈？个性化分期60期攻略 — UP 男性成长",
        "desc": "信用卡逾期还不上了怎么办？依据《商业银行信用卡监督管理办法》第70条，可申请个性化分期，停息挂账最高60期。自己就能谈，不用花钱。",
        "h1": "信用卡逾期停息挂账怎么跟银行谈？",
        "intro": "信用卡逾期了，利息违约金每个月还在涨，银行催收也在打。别慌——法律给你留了一条路。根据《商业银行信用卡业务监督管理办法》第七十条，信用卡欠款超出还款能力、但你有还款意愿的，可以和银行协商个性化分期还款协议，最高分60期（5年），停息挂账。",
        "sections": [
            ("协商流程5步走",
             "第1步：主动打信用卡背面客服电话，说'我遇到经济困难，申请个性化分期还款'。第2步：银行会让专员联系你，提交困难证明材料（失业证、病历、收入证明等）。第3步：正式协商——明确说每月能还多少钱、分多少期。第4步：签协议——必须是电话录音或书面确认。第5步：严格按时还款——再逾期一次协议作废。"),
            ("和银行谈判的技巧",
             "1）态度诚恳：不吵不闹，强调'我真的想还但暂时还不了'。2）用数据说话：列出月收入X元、生活开支X元、每月可还X元。3）主动提第70条——银行知道你有这个权利。4）被拒了不要放弃，换一个时间段再打，换一个专员再谈。5）如果银行一直拒绝，打12378投诉。"),
            ("千万不要做的3件事",
             "1）不要失联——失联等于放弃协商，银行直接起诉。2）不要以贷养贷——信用卡利息已经够高了，再借网贷只会更糟。3）不要找'停息挂账代办'——收取高额费用的全是骗子，正规协商自己就能做。"),
        ],
        "tip": "注意：协商成功不代表征信记录消除，征信上仍会显示逾期记录。但至少能停止利息增长、避免被起诉。",
        "pivot": "如果信用卡和网贷全面逾期、查询多、机构数多、银行贷款全被拒了——但你名下有车的话，车抵贷还能走通。不押车、当天放款、不看查询次数和网贷笔数。",
    },
    {
        "slug": "yangzhou-debt-restructure",
        "title": "扬州债务重组怎么操作？负债高、查询多怎么优化上岸 — UP 男性成长",
        "desc": "扬州负债太高了还不上怎么办？债务重组不是只有企业能做，个人也能优化。高息转低息、延长期限、债务整合——3步上岸方案。",
        "h1": "扬州债务重组怎么操作？负债高怎么上岸？",
        "intro": "负债高、查询多、每个月收入全还利息了、本金一分没少——这是目前很多扬州人的真实状态。债务重组不是只有企业才能做，个人负债也可以优化。",
        "sections": [
            ("什么情况需要做债务重组",
             "1）每个月还款额超过收入50%，靠借新还旧维持。2）同时在3家以上的平台借钱，查询次数超标。3）信用卡循环套现、以贷养贷。4）有稳定收入或资产（车/房/公积金）但被高息压得翻不了身。符合以上任意一条，就应该考虑债务重组。"),
            ("个人债务重组的3步方案",
             "第一步：盘点——理清所有债务的本金、利率、逾期情况，分清优先级（高息网贷>信用卡>银行贷款）。第二步：置换——有房有车的做抵押贷款置换高息网贷，利率从18%-36%降到3%-6%。有公积金的做公积金信用贷置换。有营业执照的做经营贷置换。第三步：协商——逾期部分主动找平台谈停息挂账或延期还款。"),
            ("扬州的特殊资源",
             "扬州市企业重整服务中心（电话0514-82925116）也面向个人提供债务清理咨询。2022年扬州就开始试点'类个人破产'制度，符合条件的诚实债务人可通过法院程序豁免部分债务。具体需要连续在江苏缴纳社保满3年、有法院执行案件、非恶意欠债。"),
        ],
        "tip": "债务重组最忌讳的是：没有方案就开始借钱。先理清楚、再行动。",
        "pivot": "债务重组的第一步是看名下有没有资产可以盘活。如果你在扬州有车，车抵贷是目前最快的资金盘活方式——不押车、当天放款、征信花查询多也能沟通。很多人置换完高息网贷后，月供直接降一半以上。",
    },
]

def gen_page(data):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data['title']}</title>
<link rel="canonical" href="{SITE}/articles/{data['slug']}.html">
<meta name="description" content="{data['desc']}">
<meta name="keywords" content="{data['slug'].replace('-', ',')},扬州贷款,扬州车抵贷">
<meta property="og:image" content="https://dayue.tech/og-image.jpg">
<meta name="robots" content="index, follow">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif;background:#fff;color:#1d1d1f;line-height:1.8;padding:24px;max-width:720px;margin:0 auto}}
.back{{font-size:14px;color:#86868b;text-decoration:none;display:inline-block;margin-bottom:24px}}
h1{{font-size:28px;font-weight:700;margin-bottom:12px;line-height:1.3}}
.date{{font-size:13px;color:#aaa;margin-bottom:24px}}
h2{{font-size:20px;font-weight:600;margin:28px 0 12px;padding-bottom:4px;border-bottom:2px solid #f5f5f7}}
p{{font-size:15px;margin-bottom:14px;color:#333}}
.tip{{background:#fffbe6;border-left:4px solid #f59e0b;padding:12px 16px;margin:20px 0;border-radius:4px;font-size:14px}}
.cta{{text-align:center;margin-top:40px;padding:32px 20px;background:#1d1d1f;border-radius:12px;color:#fff}}
.cta h3{{font-size:18px;color:#fff;margin-bottom:8px}}
.cta p{{font-size:14px;color:#aaa;margin-bottom:16px}}
.cta .wx{{font-size:22px;font-weight:700;color:#f59e0b}}
.cfoot{{text-align:center;margin-top:16px;font-size:12px;color:#666}}
.related{{margin-top:48px;padding-top:24px;border-top:1px solid #eee}}
.related p{{font-size:14px;color:#86868b;margin-bottom:12px}}
.related a{{display:block;font-size:14px;color:#06c;margin-bottom:8px;text-decoration:none}}
.related a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<a class="back" href="../index.html">← 返回首页</a>
<h1>{data['h1']}</h1>
<div class="date">扬州 · 贷款咨询</div>

<p>{data['intro']}</p>
"""

    for title, content in data['sections']:
        html += f"<h2>{title}</h2>\n<p>{content}</p>\n"

    html += f"""<div class="tip">{data['tip']}</div>

<p>{data['pivot']}</p>

<div class="cta">
  <h3>免费咨询 · 不收取前期费用</h3>
  <p>扬州本地 · 车抵贷 · 债务优化 · 当天放款</p>
  <div class="wx">weiona13</div>
  <div style="font-size:11px;color:#999;margin-top:8px">具体放款由合作持牌机构操作</div>
</div>

<div class="related">
<p>相关推荐：</p>
<a href="/articles/carloan.html">→ 车抵贷：不押车、当天放款、额度3-50万</a>
<a href="/articles/credit.html">→ 查询多、机构数多、贷款账户数太多？征信花了怎么办</a>
<a href="/articles/yangzhou-chedidai.html">→ 扬州车抵贷哪家正规？不押车全攻略</a>
</div>

</body>
</html>"""
    return html


def main():
    for p in PAGES:
        html = gen_page(p)
        fpath = os.path.join(BASE, "articles", f"{p['slug']}.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ articles/{p['slug']}.html")

if __name__ == "__main__":
    main()
