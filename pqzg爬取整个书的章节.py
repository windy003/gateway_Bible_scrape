import requests
from bs4 import BeautifulSoup
import time
import os

def scrape_chapter(chapter_num):
    # 格式化 URL，将 {chapter_num} 替换为实际章节号
    formatted_url = url.format(chapter_num=chapter_num)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(formatted_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve chapter {chapter_num}: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the passage content
    passage_content = soup.find('div', class_='passage-content')
    if not passage_content:
        print(f"Could not find passage content for chapter {chapter_num}")
        return None
    
    # Extract chapter title
    chapter_title = soup.find('div', class_='dropdown-display-text')
    title_text = chapter_title.text.strip() if chapter_title else f"第{chapter_num}章"
    
    # Extract verses
    verses = passage_content.find_all(['p', 'h3', 'h4'])
    
    chapter_text = [title_text]


    chapter_title_text_all.append(title_text)

    for verse in verses:
        # Skip footnotes and other irrelevant elements
        if 'footnotes' in verse.get('class', []) or 'crossrefs' in verse.get('class', []):
            continue
            
        # Check if it's a section heading
        if verse.name in ['h3', 'h4']:
            chapter_text.append(f"\n### {verse.text.strip()}\n")
            chapter_title_text_all.append(f"\n### {verse.text.strip()}\n")

        else:
            # Clean up the text
            text = verse.text.strip()
            if text and not text.startswith('Footnotes') and not text.startswith('Cross references'):
                chapter_text.append(text)
    
    return "\n".join(chapter_text), "\n".join(chapter_title_text_all)

def save_chapter(chapter_num, content):
    """Save the chapter content to a file"""
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        
    with open(f"tmp/{chapter_num}.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved chapter {chapter_num}")


def save_chapter_title_text_all(content):
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with open("tmp/0.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved chapter_title_text_all")

def main():
    
    # 将 chapter_nums 转换为整数
    chapter_nums_int = int(chapter_nums)
    
    for chapter_num in range(1, chapter_nums_int + 1): 
        print(f"Scraping chapter {chapter_num}...")
        chapter_content, chapter_title_text_all = scrape_chapter(chapter_num)
        
        if chapter_content:
            save_chapter(chapter_num, chapter_content)
            
            # Be nice to the server with a delay between requests
            time.sleep(2)
        else:
            print(f"Failed to scrape chapter {chapter_num}")
    
    save_chapter_title_text_all(chapter_title_text_all)

if __name__ == "__main__":
    chapter_title_text_all = []
    chapter_nums = input("请输入要爬取的总章节数：")
    url = input("请输入要爬取的url系列,比如:'https://www.biblegateway.com/passage/?search=马太福音+{chapter_num}&version=CSBS':")
    main()
