#!/usr/bin/env python3
"""
manup-site (dayue.tech) SEO 批处理优化脚本
=========================================
执行:
  python3 batch-optimize.py

改动:
1. 注入 canonical / JSON-LD / og:image / Baidu 自动推送
2. 补充 related 内链区
3. 更新 sitemap.xml
"""

import os, re, json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# --- 配置 ---
SITE_URL = "https://dayue.tech"
WEIXIN_ID = "weiona13"
OG_IMAGE = "/og-image.jpg"  # 请创建 1200×630 的 og:image 放到 manup-site 根目录
BAIDU_TONGJI_ID = ""  # 百度统计 ID，有就填，留空则只加注释占位

# --- 分类映射 (前缀 → 中文分类名) ---
CATEGORY = {
    "debt-": "负债自救", "debt": "负债自救",
    "bank-": "银行贷款", "biz": "资金周转",
    "loan": "贷款方案", "carloan": "车抵贷",
    "yangzhou-chedidai": "车抵贷",
    "credit": "征信", "lixi": "利息对比",
    "yidaiyangdai-": "债务置换",
    "relationship-": "情感关系", "relationship": "情感关系",
    "breakup-": "分手失恋", "breakup": "分手失恋",
    "shit-": "情感关系", "signals": "情感关系",
    "date": "约会技巧", "chat": "聊天技巧",
    "shejiao": "社交圈", "social-": "社交圈", "social": "社交圈",
    "body-": "个人成长", "body": "个人成长",
    "mind-": "个人成长", "mind": "个人成长", "mindset": "个人成长",
    "action-": "个人成长", "action": "个人成长",
    "frame": "个人成长", "nanren-": "个人成长",
    "style": "个人成长",
    "approach": "社交圈",
    "bizloan": "资金周转",
    "finance": "资金周转",
    "loanfix": "债务置换",
}

def get_category(name):
    for prefix, cat in sorted(CATEGORY.items(), key=lambda x: -len(x[0])):
        if name.startswith(prefix):
            return cat
    return "其他"

def is_debt_related(name):
    """判断是否债务类文章（用于定向导流）"""
    return name.startswith("debt-") or name in ("debt", "credit", "loanfix", "lixi-duibi", "yidaiyangdai-shangan", "carloan")

# =============================================
# 1. 采集所有页面
# =============================================
def collect_pages():
    pages = []
    # 首页
    pages.append({"file": "index.html", "url": SITE_URL + "/", "title": "首页"})
    # 文章页
    arts_dir = os.path.join(BASE, "articles")
    for fname in sorted(os.listdir(arts_dir)):
        if fname.endswith(".html"):
            name = fname.replace(".html", "")
            pages.append({
                "file": f"articles/{fname}",
                "url": f"{SITE_URL}/articles/{fname}",
                "name": name,
                "category": get_category(name),
                "is_debt": is_debt_related(name),
            })
    return pages

PAGES = collect_pages()

# 按分类分组（用于 related 推荐）
CAT_GROUPS = {}
for p in PAGES:
    if "category" in p:
        cat = p["category"]
        CAT_GROUPS.setdefault(cat, []).append(p)

# =============================================
# 2. head 注入
# =============================================
def inject_head(content, page):
    """注入 canonical, JSON-LD, og:image, Baidu 代码"""
    modifications = []

    title = ""
    m = re.search(r"<title>([^<]+)</title>", content)
    if m:
        title = m.group(1)

    desc = ""
    m = re.search(r'<meta name="description" content="([^"]*)"', content)
    if m:
        desc = m.group(1)

    # 2a. canonical - 在 </title> 后插入
    if 'rel="canonical"' not in content:
        canonical = f'  <link rel="canonical" href="{page["url"]}">'
        content = content.replace("</title>", f"</title>\n{canonical}")
        modifications.append("canonical")

    # 2b. og:image - 在 <meta name="robots"> 后插入，或用 </head> 兜底
    if 'property="og:image"' not in content and 'name="og:image"' not in content:
        og_img = f'  <meta property="og:image" content="{SITE_URL}{OG_IMAGE}">\n'
        # 优先在现有 SEO 区块内插入
        if "<!-- END SEO -->" in content:
            content = content.replace("<!-- END SEO -->", og_img + "<!-- END SEO -->")
            modifications.append("og:image")
        elif '<meta name="robots"' in content:
            content = content.replace('<meta name="robots"', og_img + '<meta name="robots"')
            modifications.append("og:image")
        elif "</head>" in content:
            content = content.replace("</head>", og_img + "</head>")
            modifications.append("og:image")

    # 2c. JSON-LD - 在 og:image 后插入，或用 </head> 兜底
    if 'application/ld+json' not in content:
        is_index = page["file"] == "index.html"
        article_name = page.get("name", "")

        # Organization
        org = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "UP 男性成长",
            "url": SITE_URL,
            "description": "扬州本地资金周转、情感关系、个人成长服务平台。免费车抵贷咨询。",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+86-WeChat-" + WEIXIN_ID,
                "contactType": "customer service"
            }
        }

        ld = []
        # Website
        ld.append({
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "UP 男性成长",
            "url": SITE_URL,
            "description": desc or "扬州本地资金周转、情感关系、个人成长服务平台"
        })
        # Organization
        ld.append(org)

        # Article (如果是文章页)
        if not is_index and article_name and "category" in page:
            article_schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": desc[:200] if desc else "",
                "url": page["url"],
                "mainEntityOfPage": page["url"],
                "datePublished": "2025-06-01",  # 可改为更精确日期
                "dateModified": datetime.now().strftime("%Y-%m-%d"),
                "articleSection": page["category"],
                "publisher": {"@type": "Organization", "name": "UP 男性成长"}
            }
            ld.append(article_schema)

        ld_html = "  <script type=\"application/ld+json\">\n" + \
            json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False, indent=2) + "\n  </script>"

        # 插入 JSON-LD: 在 <!-- END SEO --> 后，或在 </head> 前
        insert_after = "<!-- END SEO -->" if "<!-- END SEO -->" in content else "</head>"
        if insert_after == "</head>":
            content = content.replace("</head>", f"<!-- JSON-LD -->\n{ld_html}\n</head>")
        else:
            content = content.replace("<!-- END SEO -->", f"<!-- JSON-LD -->\n{ld_html}\n<!-- END SEO -->")
        modifications.append("JSON-LD")

    # 2d. Baidu 自动推送
    if 'zz.bdstatic.com/linksubmit/push.js' not in content:
        baidu_push = """  <!-- Baidu 自动推送 -->
  <script>
  (function(){
    var bp = document.createElement('script');
    var curProtocol = window.location.protocol.split(':')[0];
    if (curProtocol === 'https') bp.src = 'https://zz.bdstatic.com/linksubmit/push.js';
    else bp.src = 'http://push.zhanzhang.baidu.com/push.js';
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(bp, s);
  })();
  </script>"""
        content = content.replace("</head>", baidu_push + "\n</head>")
        modifications.append("Baidu push")

    # 2e. Baidu 统计占位
    if BAIDU_TONGJI_ID and f'hm.baidu.com/hm.js?{BAIDU_TONGJI_ID}' not in content:
        baidu_tj = f"""  <!-- Baidu 统计 -->
  <script>
  var _hmt = _hmt || [];
  (function() {{
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?{BAIDU_TONGJI_ID}";
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s);
  }})();
  </script>"""
        content = content.replace("</head>", baidu_tj + "\n</head>")
        modifications.append("Baidu tongji")
    elif not BAIDU_TONGJI_ID and "<!-- BAIDU TONGJI ID -->" not in content:
        # 加一个注释占位
        placeholder = "  <!-- BAIDU TONGJI ID: 填入百度统计 ID 后可开启 -->\n"
        content = content.replace("</head>", placeholder + "</head>")

    return content, modifications


# =============================================
# 3. related 内链区（文章页专用）
# =============================================
def inject_related(content, page):
    """为文章页注入/补充 related 区"""
    if "category" not in page:
        return content, []  # 不是文章页

    # 跳过分类枢纽页（没有 <article> 包装且有文章列表的页面）
    if '<article>' not in content and '<div class="articles">' in content:
        return content, []

    name = page["name"]
    modifications = []

    # 取同类文章（最多 4 篇，排除自身）
    cat = page["category"]
    same_cat = [p for p in CAT_GROUPS.get(cat, []) if p["name"] != name]
    # 如果同类不够，补一些债务类（导流到车抵贷）
    if len(same_cat) < 4:
        debt_pages = [p for p in PAGES if "category" in p and p["name"] not in (name, ) and p["name"] not in [s["name"] for s in same_cat] and p["is_debt"]]
        same_cat.extend(debt_pages)

    # 确保至少 4 条 — 从同类补起，不够时用债务/车抵贷填充，再不够用全部文章
    related = same_cat[:4]
    used_names = {p["name"] for p in related}

    # 如果不够 4 条，优先补充债务/车抵贷/征信类（高转化价值）
    if len(related) < 4:
        fill = [p for p in PAGES if "category" in p and p["name"] not in used_names and p["name"] != name
                and ("chedidai" in p["name"] or p["name"] in ("carloan", "credit", "loanfix", "debt-strategy", "debt"))]
        for p in fill:
            if len(related) >= 4:
                break
            if p["name"] not in used_names:
                related.append(p)
                used_names.add(p["name"])

    # 如果还是不够（理论不太会发生），从所有文章中补
    if len(related) < 4:
        for p in PAGES:
            if len(related) >= 4:
                break
            if "category" in p and p["name"] not in used_names and p["name"] != name:
                related.append(p)
                used_names.add(p["name"])

    # 车抵贷/债务类排在前面（除非自身就是车抵贷页）
    if cat != "车抵贷":
        chedidai = [p for p in related if "chedidai" in p["name"] or p["name"] in ("carloan", "credit", "loanfix")]
        others = [p for p in related if p not in chedidai]
        related = (chedidai + others)[:4]

    related_html = '\n<div class="related">\n<p style="font-size:14px;color:#86868b;">相关推荐：</p>\n'
    for p in related:
        # 提取该页面的标题用于显示
        title = get_page_title(p["file"])
        related_html += f'<a href="/articles/{p["name"]}.html">→ {title}</a>\n'
    related_html += '</div>\n'

    # 如果已有 related 区，替换它
    if 'class="related"' in content:
        old_related = re.search(r'<div class="related">.*?</div>\n', content, re.DOTALL)
        if old_related:
            content = content[:old_related.start()] + related_html + content[old_related.end():]
            modifications.append("related (replaced)")
    else:
        # 没有 related — 在有 <article> 的文章页末尾插入，否则在 <footer> 前插入
        if "</article>" in content:
            content = content.replace("</article>", related_html + "</article>")
            modifications.append("related (added)")
        elif "<footer>" in content:
            content = content.replace("<footer>", related_html + "\n<footer>")
            modifications.append("related (added)")
        elif "</body>" in content:
            content = content.replace("</body>", related_html + "\n</body>")
            modifications.append("related (added)")

    return content, modifications


def get_page_title(filepath):
    """读取页面的 title"""
    fpath = os.path.join(BASE, filepath)
    try:
        with open(fpath, encoding="utf-8") as f:
            m = re.search(r"<title>([^<]+)</title>", f.read())
            if m:
                # 只取横线之前的部分
                t = m.group(1).rsplit(" — ", 1)[0].strip()
                return t if len(t) < 40 else t[:38] + "…"
    except:
        pass
    return "阅读更多"


# =============================================
# 4. 更新 sitemap.xml
# =============================================
def update_sitemap():
    priorities = {
        "index.html": 1.0,
    }
    # 分类优先级映射：债务/贷款类 > 情感 > 其他
    cat_priority = {
        "车抵贷": 0.9, "债务置换": 0.85, "负债自救": 0.85,
        "银行贷款": 0.85, "资金周转": 0.85, "贷款方案": 0.8,
        "征信": 0.8, "利息对比": 0.8,
        "情感关系": 0.7, "分手失恋": 0.7, "约会技巧": 0.6,
        "聊天技巧": 0.6, "社交圈": 0.6,
        "个人成长": 0.6, "其他": 0.5,
    }

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += f'  <url><loc>{SITE_URL}/</loc><priority>1.0</priority></url>\n'

    for p in PAGES:
        if p["file"] == "index.html":
            continue
        pr = cat_priority.get(p.get("category", "其他"), 0.6)
        xml += f'  <url><loc>{p["url"]}</loc><priority>{pr}</priority></url>\n'

    xml += '</urlset>\n'
    return xml


# =============================================
# 主流程
# =============================================
import json

def main():
    report = []

    for page in PAGES:
        filepath = page["file"]
        fpath = os.path.join(BASE, filepath)
        if not os.path.exists(fpath):
            report.append(f"⚠️  不存在: {filepath}")
            continue

        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        changes = []

        # 2. head 注入
        content, mods = inject_head(content, page)
        if mods:
            changes.extend(mods)

        # 3. related 区（仅文章页）
        if "category" in page:
            content, mods = inject_related(content, page)
            if mods:
                changes.extend(mods)

        # 写回
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

        if changes:
            report.append(f"✅ {filepath}: {' + '.join(changes)}")
        else:
            report.append(f"   {filepath}: 无改动")

    # 4. sitemap
    sitemap_xml = update_sitemap()
    sm_path = os.path.join(BASE, "sitemap.xml")
    with open(sm_path, "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    report.append(f"📄 sitemap.xml 已更新 ({len(PAGES)} 条)")

    print("\n".join(report))
    print(f"\n=== 完毕 === 处理了 {len(PAGES)} 个页面")


if __name__ == "__main__":
    main()
