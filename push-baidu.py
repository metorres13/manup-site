#!/usr/bin/env python3
"""
dayue.tech 百度普通收录主动推送
================================
用法:
  1. 在下方填入 BAIDU_SITE 和 BAIDU_TOKEN
     (百度搜索资源平台 → 普通收录 → API提交 获取)
  2. python3 push-baidu.py --dry-run    # 先看将推送的 URL
  3. python3 push-baidu.py              # 真实推送

百度普通收录 API:
  POST http://data.zz.baidu.com/urls?site=<SITE>&token=<TOKEN>
  body: 每行一个 URL (text/plain)
  单次上限 2000 条，本站 71 条一次推送即可。
"""

import os, re, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))

# ============ 百度推送凭据 (从环境变量读取，避免泄露进 git) ============
# 用法: BAIDU_TOKEN=xxxx python3 push-baidu.py
#       BAIDU_TOKEN=xxxx python3 push-baidu.py --dry-run
BAIDU_SITE = os.environ.get("BAIDU_SITE", "dayue.tech")   # 百度普通收录 site= 纯域名
BAIDU_TOKEN = os.environ.get("BAIDU_TOKEN", "")           # 百度普通收录 API token
# =============================================================

SITEMAP = os.path.join(BASE, "sitemap.xml")

def read_urls():
    s = open(SITEMAP, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", s)

def push(urls, dry):
    endpoint = f"http://data.zz.baidu.com/urls?site={BAIDU_SITE}&token={BAIDU_TOKEN}"
    body = "\n".join(urls).encode("utf-8")
    if dry:
        print(f"[DRY-RUN] 将推送 {len(urls)} 条 URL 到百度:")
        for u in urls:
            print("  ", u)
        print(f"\nendpoint: {endpoint}")
        print("填入 BAIDU_SITE / BAIDU_TOKEN 后去掉 --dry-run 真实推送。")
        return
    req = urllib.request.Request(endpoint, data=body, method="POST",
                                 headers={"Content-Type": "text/plain"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = resp.read().decode("utf-8")
            print("百度推送响应:", res)
            # 成功格式: {"remain":4999,"success":71}
            import json
            try:
                d = json.loads(res)
                print(f"\n成功推送: {d.get('success')} 条, 剩余额度: {d.get('remain')}")
                if d.get("remain", 0) > 0:
                    print("✓ 推送成功，额度充足")
                else:
                    print("⚠ 额度已用完，明天再推")
            except Exception:
                pass
    except urllib.error.HTTPError as e:
        print(f"推送失败 HTTP {e.code}: {e.read().decode('utf-8', 'ignore')}")
        print("常见原因: site/token 不匹配，或 site 未在百度资源平台验证")
    except Exception as e:
        print(f"推送出错: {e}")

def main():
    dry = "--dry-run" in sys.argv
    if not BAIDU_SITE or not BAIDU_TOKEN:
        if not dry:
            print("✗ 未设置百度推送凭据，请通过环境变量传入：")
            print("  BAIDU_TOKEN=xxxx python3 push-baidu.py")
            print("  (token 在百度搜索资源平台 → 普通收录 → API提交 获取)")
            print("  仅查看 URL 列表请加 --dry-run")
            sys.exit(1)
    urls = read_urls()
    print(f"从 sitemap.xml 读取 {len(urls)} 条 URL\n")
    push(urls, dry)

if __name__ == "__main__":
    main()
