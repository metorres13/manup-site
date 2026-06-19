#!/usr/bin/env python3
"""dayue.tech 转化优化：悬浮微信按钮 + 面包屑 + 薄内容扩展"""
import os, re
from pathlib import Path

BASE_DIR = Path(__file__).parent
SITE_URL = "https://dayue.tech"
WX = "weiona13"

# 悬浮微信按钮 HTML + CSS + JS
FLOAT_BTN = """
<!-- Float WeChat -->
<style>
.float-wx{position:fixed;bottom:20px;right:20px;z-index:9999;background:#07c160;color:#fff;border-radius:50px;padding:8px 16px;font-size:13px;font-weight:600;box-shadow:0 4px 12px rgba(0,0,0,0.3);display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;transition:transform .2s;border:none;font-family:-apple-system,"Helvetica Neue","PingFang SC",sans-serif;line-height:1.3}
.float-wx:hover{transform:scale(1.05)}
.float-wx .wx-close{position:absolute;top:-6px;right:-6px;background:#666;color:#fff;border-radius:50%;width:18px;height:18px;font-size:10px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
@media(max-width:768px){.float-wx{bottom:16px;right:16px;padding:8px 14px;font-size:12px}}
</style>
<div class="float-wx" id="floatWx" onclick="copyWx()">
  <span>💬 免费咨询</span>
  <span style="font-size:11px;color:#e8f5e9;">15952779025</span>
  <button class="wx-close" onclick="event.stopPropagation();document.getElementById('floatWx').style.display='none'">×</button>
</div>
<script>
function copyWx(){navigator.clipboard.writeText("weiona13").then(()=>{const t=document.getElementById("floatWx");t.innerHTML='<span>✅ 已复制微信号</span><span style="font-size:11px;color:#e8f5e9;">打开微信粘贴添加</span>';setTimeout(()=>{t.innerHTML='<span>💬 免费咨询</span><span style="font-size:11px;color:#e8f5e9;">15952779025</span><button class="wx-close" onclick="event.stopPropagation();document.getElementById(\\'floatWx\\').style.display=\\'none\\'">×</button>'},3000)})}
</script>
"""

def add_float_btn(content):
    if 'float-wx' not in content and 'weiona13' in content:
        content = content.replace("</body>", FLOAT_BTN + "\n</body>")
        return content, True
    return content, False


def add_breadcrumb(content, page_name):
    """文章页加面包屑"""
    if 'breadcrumb' in content or page_name == "index.html":
        return content, False
    
    # 获取文章标题
    m = re.search(r"<h1>(.*?)</h1>", content)
    title = m.group(1) if m else page_name
    
    bc = f"""
<div style="max-width:720px;margin:0 auto;padding:16px 24px 0;font-size:13px;color:#999;">
  <a href="{SITE_URL}/" style="color:#06c;text-decoration:none;">首页</a>
  <span style="margin:0 6px;">›</span>
  <span>{title[:30]}</span>
</div>"""
    content = content.replace(f"<h1>{title}</h1>", bc + f"\n<h1>{title}</h1>")
    return content, True


def expand_thin_articles():
    """扩展内容过薄的文章"""
    thin = []
    for f in sorted((BASE_DIR / "articles").glob("*.html")):
        text = f.read_text(encoding="utf-8")
        body = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'\s+', '', body)
        cn = len(re.findall(r'[\u4e00-\u9fff]', body))
        if cn < 300:
            thin.append((f.name, cn))
    return thin


def main():
    changes = []
    
    # 1. 悬浮按钮 + 面包屑（所有页面）
    for html_file in list(BASE_DIR.rglob("*.html")):
        if "node_modules" in str(html_file):
            continue
        content = html_file.read_text(encoding="utf-8")
        modified = False
        
        # 悬浮微信（跳过首页，首页已有大号CTA）
        if html_file.name != "index.html":
            content, f_ok = add_float_btn(content)
            if f_ok:
                modified = True
                changes.append(f"浮窗:{html_file.name}")
        
        # 面包屑（文章页）
        content, b_ok = add_breadcrumb(content, html_file.name)
        if b_ok:
            modified = True
            changes.append(f"面包屑:{html_file.name}")
        
        if modified:
            html_file.write_text(content, encoding="utf-8")
    
    # 2. 薄内容检查
    thin = expand_thin_articles()
    
    print("✅ 批量优化完成")
    print(f"   悬浮微信按钮: {sum(1 for c in changes if '浮窗' in c)} 页")
    print(f"   面包屑导航:   {sum(1 for c in changes if '面包屑' in c)} 页")
    if thin:
        print(f"   ⚠️ 薄内容文章 ({len(thin)} 篇):")
        for name, cn in thin[:5]:
            print(f"     {name}: {cn}字")
    else:
        print(f"   ✅ 无薄内容文章")

if __name__ == "__main__":
    main()
