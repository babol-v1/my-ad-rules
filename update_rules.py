import urllib.request

def fetch_and_clean(url):
    print(f"正在下载: {url}")
    try:
        # 设置请求头防止被部分 CDN 或 GitHub 拦截
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            
        valid_rules = set()
        for line in content.splitlines():
            line = line.strip()
            # 过滤空行，以及以 !、# 或 [ 开头的 AdGuard/Easylist 注释或元数据
            if not line or line.startswith('!') or line.startswith('#') or line.startswith('['):
                continue
            # 直接将整行（包含原生修饰符）作为一个整体加入集合去重
            valid_rules.add(line)
        return valid_rules
    except Exception as e:
        print(f"下载或解析失败 {url}: {e}")
        return set()

def main():
    # 📋 在这里管理你的所有规则源，直接往列表里添加即可
    rule_urls = [
        "https://cdn.jsdelivr.net/gh/blackmatrix7/ios_rule_script@master/rule/AdGuard/Advertising/Advertising.txt",
        "https://anti-ad.net/easylist.txt",
        "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt", # 👈 替换成你要加的第 3 个规则源 URL
    ]
    
    # 创建一个空集合，用来合并所有去重后的规则
    all_combined_rules = set()
    
    # 🔄 循环读取每一个规则源
    for url in rule_urls:
        rules = fetch_and_clean(url)
        all_combined_rules = all_combined_rules.union(rules)
    
    # 字母顺序排序，方便后续追踪规则变化
    sorted_rules = sorted(list(all_combined_rules))
    
    # 输出的目标文件名
    output_file = "purged_ad_rules.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入兼容 AdGuard 订阅格式的通用文件头
        f.write("! Title: My Combined AdBlock Rules\n")
        f.write("! Description: Auto merged and de-duplicated from multiple sources\n")
        f.write(f"! Total Count: {len(sorted_rules)}\n\n")
        
        for rule in sorted_rules:
            f.write(rule + "\n")
            
    print(f"处理完成：共合并去重得到 {len(sorted_rules)} 条原生文本规则，已保存至 {output_file}")

if __name__ == "__main__":
    main()
