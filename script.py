import requests
from bs4 import BeautifulSoup
import re
import time

# Files
input_file = 'new_chapters.txt'
output_file = 'c1.txt'

base_url = 'https://novelbin.com/b/shadow-slave/'

with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

with open(output_file, 'w', encoding='utf-8') as out:
    for line in lines:
        # Match lines like: Chapter 1 Nightmare Begins
        match = re.match(r'Chapter\s+(\d+)\s+(.+)', line, re.IGNORECASE)
        if not match:
            print(f"Line skipped (format issue): {line}")
            continue

        chapter_num = match.group(1)
        title = match.group(2)

        # Format title for URL
        title_for_url = title.lower().replace(' ', '-')
        url = f"{base_url}chapter-{chapter_num}-{title_for_url}"

        print(f"Fetching: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get all <p> tags
            paragraphs = soup.find_all('p')
            if not paragraphs:
                print(f"No paragraphs found at: {url}")
                continue

            chapter_text = '\n'.join(p.get_text(strip=True) for p in paragraphs)

            # Write to output
            out.write(f"Chapter {chapter_num}: {title}\n")
            out.write(chapter_text + "\n\n")

            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(5)  # Increase delay on failure (in case of rate limit)