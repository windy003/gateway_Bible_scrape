import requests
from bs4 import BeautifulSoup
import time
import os

def scrape_matthew_chapter(chapter_num):
    """Scrape a specific chapter of Matthew from BibleGateway"""
    url = f"https://www.biblegateway.com/passage/?search=马太福音+{chapter_num}&version=CSBS"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
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
    chapter_title = soup.find('h3', class_='passage-display')
    title_text = chapter_title.text.strip() if chapter_title else f"马太福音 第{chapter_num}章"
    
    # Extract verses
    verses = passage_content.find_all(['p', 'h3', 'h4'])
    
    chapter_text = [title_text]
    
    for verse in verses:
        # Skip footnotes and other irrelevant elements
        if 'footnotes' in verse.get('class', []) or 'crossrefs' in verse.get('class', []):
            continue
            
        # Check if it's a section heading
        if verse.name in ['h3', 'h4']:
            chapter_text.append(f"\n### {verse.text.strip()}\n")
        else:
            # Clean up the text
            text = verse.text.strip()
            if text and not text.startswith('Footnotes') and not text.startswith('Cross references'):
                chapter_text.append(text)
    
    return "\n".join(chapter_text)

def save_chapter(chapter_num, content):
    """Save the chapter content to a file"""
    if not os.path.exists("马太福音"):
        os.makedirs("马太福音")
        
    with open(f"马太福音/第{chapter_num}章.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved chapter {chapter_num}")

def save_full_book(all_chapters):
    """Save all chapters to a single file"""
    with open("马太福音_完整版.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_chapters))
    print("Saved complete book")

def main():
    all_chapters = []
    
    for chapter_num in range(1, 29):  # Matthew has 28 chapters
        print(f"Scraping chapter {chapter_num}...")
        chapter_content = scrape_matthew_chapter(chapter_num)
        
        if chapter_content:
            all_chapters.append(chapter_content)
            save_chapter(chapter_num, chapter_content)
            
            # Be nice to the server with a delay between requests
            time.sleep(2)
        else:
            print(f"Failed to scrape chapter {chapter_num}")
    
    # Save the complete book
    if all_chapters:
        save_full_book(all_chapters)
        print(f"Successfully scraped {len(all_chapters)} chapters of Matthew")
    else:
        print("Failed to scrape any chapters")

if __name__ == "__main__":
    main()
