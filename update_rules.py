import urllib.request

def fetch_and_clean(url):
    print(f"正在下载: {url}")
    try:
        # 设置请求头防止被部分 CDN 拦截
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            
        valid_rules = set()
        for line in content.splitlines():
            line = line.strip()
            # 过滤空行，以及以 !、# 或 [ 开头的 AdGuard/Easylist 注释或元数据
            if not line or line.startswith('!') or line.startswith('#') or line.startswith('['):
                continue
            # 直接将整行（包含 @@||, ^, $ 等原生修饰符）作为一个整体加入集合去重
            valid_rules.add(line)
        return valid_rules
    except Exception as e:
        print(f"下载或解析失败 {url}: {e}")
        return set()

def main():
    # 你指定的两个原生 AdGuard / Easylist 规则源
    url1 = "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/AdGuard/Advertising/Advertising.txt"
    url2 = "https://anti-ad.net/easylist.txt"
    
    # 抓取并清洗
    rules1 = fetch_and_clean(url1)
    rules2 = fetch_and_clean(url2)
    
    # 取并集，利用 set 的特性完美去重
    combined_rules = rules1.union(rules2)
    
    # 字母顺序排序，方便后续追踪规则变化
    sorted_rules = sorted(list(combined_rules))
    
    # 输出的目标文件名
    output_file = "purged_ad_rules.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入兼容 AdGuard 订阅格式的通用文件头
        f.write("! Title: My Combined AdBlock Rules\n")
        f.write("! Description: Auto merged and de-duplicated from blackmatrix7 & anti-AD\n")
        f.write(f"! Total Count: {len(sorted_rules)}\n\n")
        
        for rule in sorted_rules:
            f.write(rule + "\n")
            
    print(f"处理完成：共合并去重得到 {len(sorted_rules)} 条原生文本规则，已保存至 {output_file}")

if __name__ == "__main__":
    main()
