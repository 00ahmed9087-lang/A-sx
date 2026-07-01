from urllib.parse import urlparse, parse_qs

def filter_unique_urls():
    print("\n" + "="*40)
    print("   ParamFilter-Py | Mobile Friendly")
    print("="*40 + "\n")

    print("[*] الصق الروابط هنا (اضغط Enter مرتين متتاليتين لبدء الفحص):")
    print("-" * 50)
    
    lines = []
    empty_lines_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_lines_count += 1
                if empty_lines_count >= 1: 
                    break
            else:
                empty_lines_count = 0
                lines.append(line)
        except EOFError:
            break

    seen_patterns = set()
    unique_urls = []

    for line in lines:
        url = line.strip()
        
        if not url or '?' not in url: 
            continue
        
        parsed = urlparse(url)
        path = parsed.path
        
        params = tuple(sorted(parse_qs(parsed.query).keys()))
        
        pattern = (parsed.netloc, path, params)
        
        if pattern not in seen_patterns and params:
            seen_patterns.add(pattern)
            unique_urls.append(url)

    print("\n" + "="*40)
    print("   الروابط المشبوهة والفريدة المكتشفة:")
    print("="*40 + "\n")

    if unique_urls:
        for url in unique_urls:
            print(url)
    else:
        print("[!] لم يتم العثور على روابط تحتوي على معلمات حقن.")

    print("\n" + "-" * 40)
    print(f"[+] إجمالي الروابط الفريدة: {len(unique_urls)}")
    print("-" * 40)

if __name__ == "__main__":
    filter_unique_urls()
