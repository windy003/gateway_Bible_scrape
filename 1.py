import requests
from bs4 import BeautifulSoup
import time
import os

def scrape_bible_chapter_titles(chapter_number):
    """爬取指定章节的标题和所有子标题"""
    url = f"https://www.biblegateway.com/passage/?search=%E5%88%9B%E4%B8%96%E8%AE%B0%20{chapter_number}&version=CCB"
    
    # 添加请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取章节标题
        chapter_title = soup.select_one('.dropdown-display-text')
        if chapter_title:
            chapter_title = chapter_title.text.strip()
        else:
            chapter_title = f"创世记 {chapter_number}"
        
        # 获取所有章节子标题
        subtitles = soup.select('h3 span.text, h4 span.text')
        subtitle_texts = [subtitle.text.strip() for subtitle in subtitles if subtitle.text.strip()]
        
        if not subtitle_texts:
            subtitle_texts = ["无子标题"]
        
        return {
            'chapter_title': chapter_title,
            'subtitles': subtitle_texts,
            'url': url
        }
    
    except requests.exceptions.RequestException as e:
        print(f"爬取章节 {chapter_number} 时出错: {e}")
        return None

def main():
    # 创建保存结果的文件
    output_file = "bible_titles.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("圣经创世记标题和子标题\n\n")
        
        # 只爬取创世记的50章
        for chapter in range(1, 51):
            print(f"正在爬取创世记第 {chapter} 章的标题...")
            
            chapter_data = scrape_bible_chapter_titles(chapter)
            
            if chapter_data:
                # 将章节标题和所有子标题写入文件
                f.write(f"章节: {chapter_data['chapter_title']}\n")
                f.write("子标题列表:\n")
                
                for i, subtitle in enumerate(chapter_data['subtitles'], 1):
                    f.write(f"  {i}. {subtitle}\n")
                
                f.write(f"URL: {chapter_data['url']}\n")
                f.write("-" * 50 + "\n\n")
                
                print(f"已保存创世记第 {chapter} 章的标题信息，共 {len(chapter_data['subtitles'])} 个子标题")
            else:
                print(f"无法爬取创世记第 {chapter} 章的标题信息")
            
            # 添加延迟，避免请求过于频繁
            time.sleep(1)

if __name__ == "__main__":
    main()
    print("爬取完成！")
