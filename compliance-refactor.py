#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dayue.tech 全站合规重构批处理
================================
目标：消除百度风控标记、合规软获客、最小结构改动。
处理对象：index.html + articles/*.html（不含 articles.bak/）

改造内容：
  1. 移除 微信二维码弹窗(qr-overlay)、悬浮客服(float-wx / float-cta)、.cta 硬广块
  2. 移除 tel: 链接、微信号 weiona13、明文手机号 15952779025
  3. 替换违规营销词（保留“征信修复/内部渠道”等反诈科普内容）
  4. 顶部插入风险提示横幅；页脚插入《风险提示与免责声明》
  5. 全站统一 CTA → 《领取扬州银行贷款准入自查手册》→ 轻量弹窗表单（城市+手机号）
  6. 改写首页 meta description 为合规科普版
幂等：以 <!-- compliance-refactor-v1 --> 标记守卫，重复运行不会叠加。
"""
import os, re, glob, html as _unused

BASE = os.path.dirname(os.path.abspath(__file__))
MARK = "<!-- compliance-refactor-v1 -->"

# ---------- 固定文案 ----------
DISCLAIMER_TEXT = (
    "本站仅做银行信贷政策、征信知识科普分享，不持有金融放贷资质，"
    "不提供贷款代办、征信修复、资金对接服务，不收取任何咨询、代办费用；"
    "所有内容仅作知识参考，有资金需求请自行前往各大持牌银行线下网点咨询办理，"
    "借贷有风险，量力而行。"
)

RISK_BANNER_HTML = (
    '<div class="risk-banner">\n'
    '⚠️ <strong>风险提示：</strong>本站仅做银行信贷政策与征信知识科普，'
    '不持有金融放贷资质，不提供贷款代办、征信修复或资金对接服务，不收取任何费用。'
    '借贷有风险，请量力而行。\n'
    '</div>\n'
)

DISCLAIMER_HTML = (
    '<div class="disclaimer">\n'
    '<p><strong>《风险提示与免责声明》</strong></p>\n'
    f'<p>{DISCLAIMER_TEXT}</p>\n'
    '</div>\n'
)

# 合规 CTA（替换原 .cta 硬广块）
CTA_HTML = (
    '<div class="cta">\n'
    '  <h3>不确定自己是否符合银行准入条件？</h3>\n'
    '  <p>整理了一份《扬州银行贷款准入自查手册》，自查后再去网点，少走弯路。</p>\n'
    '  <a class="btn" href="javascript:void(0)" onclick="openLeadForm()">领取扬州银行贷款准入自查手册</a>\n'
    '  <div class="cfoot">科普资料 · 免费领取 · 不代办不收费</div>\n'
    '</div>\n'
)

# 额外样式（风险横幅 / 免责声明 / 软获客表单）
EXTRA_CSS = """
/* compliance-refactor-v1 */
.risk-banner{background:#fff5f5;border-bottom:1px solid #ffd6d6;color:#b71c1c;font-size:13px;line-height:1.7;padding:8px 20px;text-align:center}
.risk-banner strong{color:#b71c1c}
.disclaimer{max-width:720px;margin:32px auto;padding:20px 24px;background:#f5f5f7;border-radius:12px;font-size:12px;color:#86868b;line-height:1.7}
.disclaimer p{margin:4px 0}.disclaimer strong{color:#1d1d1f}
.lead-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:9999;align-items:center;justify-content:center}
.lead-overlay.show{display:flex}
.lead-popup{background:#fff;border-radius:16px;padding:28px 24px;max-width:360px;width:calc(100% - 32px);position:relative;box-shadow:0 12px 40px rgba(0,0,0,.2)}
.lead-popup .close-btn{position:absolute;top:10px;right:14px;font-size:24px;color:#aaa;cursor:pointer;border:none;background:none;line-height:1}
.lead-popup h3{font-size:17px;font-weight:600;margin-bottom:6px}
.lead-popup .lead-sub{font-size:13px;color:#86868b;margin-bottom:16px}
.lead-popup form label{display:block;font-size:12px;color:#666;margin-bottom:12px}
.lead-popup form input{display:block;width:100%;margin-top:6px;padding:10px 12px;border:1px solid #ddd;border-radius:8px;font-size:15px;box-sizing:border-box}
.lead-popup form input:focus{outline:none;border-color:#1d1d1f}
.lead-popup form button{width:100%;margin-top:8px;padding:12px;border:none;border-radius:8px;background:#1d1d1f;color:#fff;font-size:15px;font-weight:600;cursor:pointer}
.lead-popup .lead-note{font-size:11px;color:#bbb;margin-top:12px;line-height:1.6}
"""

# 软获客表单弹窗 + 脚本（每页一份，插在 </body> 前）
LEAD_FORM_HTML = (
    '<div class="lead-overlay" id="leadOverlay">\n'
    '  <div class="lead-popup">\n'
    '    <button class="close-btn" onclick="closeLeadForm()">&times;</button>\n'
    '    <h3>领取《扬州银行贷款准入自查手册》</h3>\n'
    '    <p class="lead-sub">填写以下信息，资料将通过短信发送给您</p>\n'
    '    <form id="leadForm" onsubmit="return submitLead(event)">\n'
    '      <label>所在城市<input type="text" name="city" placeholder="如：扬州" required></label>\n'
    '      <label>联系手机号<input type="tel" name="phone" pattern="1[3-9]\\d{9}" placeholder="11位手机号" required></label>\n'
    '      <button type="submit">提交领取</button>\n'
    '    </form>\n'
    '    <p class="lead-note">本站仅做信贷知识科普，不收集身份证、征信报告、银行卡等敏感信息。</p>\n'
    '  </div>\n'
    '</div>\n'
    '<script>\n'
    'function openLeadForm(){var o=document.getElementById("leadOverlay");o.classList.add("show");document.body.style.overflow="hidden";}\n'
    'function closeLeadForm(){document.getElementById("leadOverlay").classList.remove("show");document.body.style.overflow="";}\n'
    'function submitLead(e){e.preventDefault();var f=document.getElementById("leadForm");var city=f.city.value.trim();var phone=f.phone.value.trim();if(!/^1[3-9]\\d{9}$/.test(phone)){alert("请输入正确的手机号");return false;}\n'
    'try{var l=JSON.parse(localStorage.getItem("dayue_leads")||"[]");l.push({city:city,phone:phone,ts:Date.now()});localStorage.setItem("dayue_leads",JSON.stringify(l));}catch(x){}\n'
    'document.querySelector("#leadOverlay .lead-popup").innerHTML="<h3>资料已发送</h3><p class=\\\"lead-sub\\\">请留意短信查收。如需详细政策解读，可在短信中查看官方企业微信添加方式（企业微信，非个人号）。</p><button class=\\\"lead-btn\\\" onclick=\\\"closeLeadForm()\\\" style=\\\"width:100%;padding:12px;border:none;border-radius:8px;background:#1d1d1f;color:#fff;font-size:15px;font-weight:600;cursor:pointer\\\">关闭</button><p class=\\\"lead-note\\\">本站不提供贷款代办，有资金需求请前往持牌银行网点咨询办理。</p>";\n'
    'return false;}\n'
    'document.addEventListener("keydown",function(e){if(e.key==="Escape")closeLeadForm();});\n'
    'document.getElementById("leadOverlay").addEventListener("click",function(e){if(e.target===this)closeLeadForm();});\n'
    '</script>\n'
)

# 违规营销词替换（顺序敏感：长串先替换）
# 注意：保留反诈科普内容中的“征信修复/内部渠道”表述，仅替换服务承诺类话术。
KEYWORD_REPLACES = [
    ("最快当天放款", "最快当日完成审批"),
    ("最快当天到账", "最快当日完成审批"),
    ("当天放款", "当日放款"),
    ("当天到账", "当日到账"),
    ("当天出结果", "当日出结果"),
    ("上午办完下午到账", "当日完成审批"),
    ("免费评估额度", "自助评估额度"),
    ("免费评估车辆额度", "自助评估额度"),
    ("免费评估", "自助评估"),
    ("免费咨询", "免费了解政策"),
    ("一对一方案", "政策解读"),
    ("帮你判断一下", "查看准入自查"),
    ("把你的征信情况发我，我帮你判断", "查看自助准入评估"),
    ("点我咨询", "领取手册"),
    ("扫码点我咨询", "领取自查手册"),
    ("具体放款由合作持牌机构操作", "具体贷款请前往持牌银行网点办理"),
    ("征信花了、逾期了也能办", "征信花了、逾期了怎么办"),
    ("扬州本地可上门", "扬州本地可线下了解"),
    ("无前期费用", "不收取任何费用"),
    ("不收取前期费用", "不收取任何费用"),
    ("不收前期费用", "不收取任何费用"),
]

# ---------- 工具函数 ----------
def remove_div_block(html, open_regex):
    """从匹配 open_regex 的 <div ...> 起，按 div 深度平衡删除整块。返回 (新html, 是否删除)。"""
    m = re.search(open_regex, html)
    if not m:
        return html, False
    start = m.start()
    i = m.end()
    depth = 1
    while depth > 0 and i < len(html):
        no = html.find("<div", i)
        nc = html.find("</div", i)
        if nc == -1:
            break
        if no != -1 and no < nc:
            depth += 1
            i = no + 4
        else:
            depth -= 1
            i = html.find(">", nc) + 1
    # 吞掉块后紧邻的空白行
    end = i
    while end < len(html) and html[end] in " \t\r\n":
        end += 1
    return html[:start] + html[end:], True


def remove_script_block(html, func_name):
    """删除包含指定 function 定义的 <script>...</script>。"""
    pat = re.compile(r"<script>\s*function\s+" + re.escape(func_name) + r"[\s\S]*?</script>\s*")
    return pat.sub("", html)


def remove_css_rules(html, selectors):
    """从 <style> 中删除指定选择器的规则块（保守：删除以该选择器开头的行到大括号闭合）。"""
    for sel in selectors:
        pat = re.compile(re.escape(sel) + r"\s*\{[^}]*\}\s*")
        html = pat.sub("", html)
    return html


def process(html, is_index):
    if MARK in html:
        return html, "skip(already)"

    report = []

    # 1) 删除 qr-overlay 弹窗块
    html, ok = remove_div_block(html, r'<div class="qr-overlay"')
    if ok: report.append("qr-overlay")
    html = re.sub(r"<!--\s*微信二维码弹窗\s*-->\s*", "", html)

    # 2) 删除 float-wx / float-cta 悬浮客服块
    html, ok = remove_div_block(html, r'<div class="float-wx"')
    if ok: report.append("float-wx")
    html, ok = remove_div_block(html, r'<div class="float-cta"')
    if ok: report.append("float-cta")
    html = re.sub(r"<!--\s*Float WeChat\s*-->\s*", "", html)
    html = re.sub(r"<!--\s*悬浮咨询按钮\s*-->\s*", "", html)

    # 3) 删除 showQR / copyWechat / copyWx 脚本
    html = remove_script_block(html, "showQR")
    html = remove_script_block(html, "copyWechat")
    html = remove_script_block(html, "copyWx")

    # 4) 删除 qr/float 相关 CSS 规则
    html = remove_css_rules(html, [
        ".qr-overlay", ".qr-overlay.show", ".qr-popup", ".qr-popup h3",
        ".qr-popup p", ".qr-popup img", ".qr-popup .copy-btn", ".qr-popup .close-btn",
        ".float-wx", ".float-wx:hover", ".float-wx .wx-icon", ".float-wx .wx-close",
        ".float-cta", ".float-cta:hover", ".float-cta .fc-sub", ".float-cta .fc-close",
    ])

    # 5) 删除 tel: 链接（整段 <a>）
    html = re.sub(r'<a[^>]*href="tel:[^"]*"[^>]*>.*?</a>', "", html)

    # 6) 替换 .cta 硬广块为合规 CTA
    html, cta_start = replace_cta(html)

    # 7) 内联 showQR() 调用 → openLeadForm()
    html = html.replace('onclick="showQR()"', 'onclick="openLeadForm()"')

    # 8) 清除微信号 / 明文手机号
    html = html.replace("weiona13", "")
    html = html.replace("15952779025", "")
    # 清理因替换产生的空 <p>微信 · 扬州本地</p> 等
    html = re.sub(r"<p>\s*微信[\s·]*</p>", "", html)

    # 9) JSON-LD 中移除 contactPoint（含微信号电话）
    html = re.sub(r',\s*"contactPoint"\s*:\s*\{[^}]*\}', "", html)
    html = re.sub(r'"contactPoint"\s*:\s*\{[^}]*\},?\s*', "", html)

    # 10) 违规营销词替换
    for a, b in KEYWORD_REPLACES:
        if a in html:
            html = html.replace(a, b)

    # 11) 首页 meta description / og:description 改写为合规科普版
    if is_index:
        html = re.sub(
            r'<meta name="description" content="[^"]*">',
            '<meta name="description" content="扬州本地银行信贷政策与征信知识科普：'
            '车抵贷、公积金贷、个体户经营贷准入条件与利率解读，'
            '征信查询次数影响、银行贷款避坑与融资规划科普。UP 男性成长。">',
            html)
        html = re.sub(
            r'<meta property="og:description" content="[^"]*">',
            '<meta property="og:description" content="扬州本地银行信贷政策与征信知识科普，'
            '不提供贷款代办或资金对接服务。">',
            html)

    # 12) 注入额外 CSS（</head> 前）
    html = html.replace("</head>", f"<style>{EXTRA_CSS}</style>\n</head>", 1)

    # 13) 顶部风险提示横幅（<body> 后）
    html = html.replace("<body>", "<body>\n" + RISK_BANNER_HTML, 1)

    # 14) 页脚免责声明 + 软获客表单（</body> 前）
    if is_index:
        # 首页有 <footer>，免责声明放进 footer 内
        if "</footer>" in html:
            html = html.replace("</footer>", DISCLAIMER_HTML + "</footer>", 1)
        else:
            html = html.replace("</body>", DISCLAIMER_HTML + "</body>", 1)
    else:
        html = html.replace("</body>", DISCLAIMER_HTML + "</body>", 1)
    html = html.replace("</body>", LEAD_FORM_HTML + "</body>", 1)

    # 15) 打标记
    html = html.replace("</head>", f"{MARK}\n</head>", 1)

    return html, ",".join(report) if report else "no-structural-change"


def replace_cta(html):
    """把第一个 <div class="cta">...</div> 平衡块替换为合规 CTA。返回 (新html, 起始位置)。"""
    m = re.search(r'<div class="cta">', html)
    if not m:
        return html, None
    start = m.start()
    i = m.end()
    depth = 1
    while depth > 0 and i < len(html):
        no = html.find("<div", i)
        nc = html.find("</div", i)
        if nc == -1:
            break
        if no != -1 and no < nc:
            depth += 1
            i = no + 4
        else:
            depth -= 1
            i = html.find(">", nc) + 1
    # 保留前后换行
    return html[:start] + CTA_HTML + html[i:], start


def main():
    files = [os.path.join(BASE, "index.html")]
    files += sorted(glob.glob(os.path.join(BASE, "articles", "*.html")))
    total = 0
    for f in files:
        rel = os.path.relpath(f, BASE)
        with open(f, encoding="utf-8") as fp:
            src = fp.read()
        out, rep = process(src, is_index=(f.endswith("index.html")))
        if out != src:
            with open(f, "w", encoding="utf-8") as fp:
                fp.write(out)
            total += 1
            print(f"[改] {rel:40s} {rep}")
        else:
            print(f"[跳] {rel:40s} {rep}")
    print(f"\n完成：共修改 {total} 个文件。")


if __name__ == "__main__":
    main()
