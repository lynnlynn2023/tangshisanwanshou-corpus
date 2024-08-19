import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd
import opencc

# Initialize the converter
converter = opencc.OpenCC('t2s')  # Traditional to Simplified Chinese

# Load the CSV file into a dictionary
characters_df = pd.read_csv('characters.csv')
character_map = dict(zip(characters_df['num'], characters_df['character']))


def extract_image_data(book, img_href):
    img_item = book.get_item_with_href(img_href)
    if img_item:
        return img_item.content
    return None


def convert_images_to_text(book, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    poem_text_tags = soup.find_all(['p', 'div'], class_=lambda x: x and 'reference' in x.split())

    for tag in poem_text_tags:
        images = tag.find_all('img')

        for img in images:
            src_text = img.get('src')
            if src_text:
                num_str = os.path.splitext(os.path.basename(src_text))[0]
                try:
                    num = int(num_str.lstrip('0'))
                    character = character_map.get(num, '[UNKNOWN]')
                    img.replace_with(character)
                except ValueError:
                    img.replace_with("[INVALID IMAGE NUMBER]")
            else:
                img.replace_with("[NO IMAGE DATA]")

    return soup


def read_epub(file_path):
    book = epub.read_epub(file_path)
    poems = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')

        title_tag = soup.find('p', class_='catalog')
        author_tag = soup.find('p', class_='right-content')
        poem_text_tags = soup.find_all(['p', 'div'], class_=lambda x: x and (
                    'reference' in x.split() or 'center-reference' in x.split()))
        author_intro_tag = soup.find('p', text='作者')
        poem_analysis_tag = soup.find('p', text='鉴赏')

        if title_tag:
            title = title_tag.get_text().strip().replace(' ', '').replace('\u3000', '')
        else:
            title = ''

        if author_tag:
            author = author_tag.get_text().strip().replace(' ', '').replace('\u3000', '').replace('*', '')
        else:
            author = ''

        content_texts = []
        for tag in poem_text_tags:
            tag_html = str(tag)
            converted_soup = convert_images_to_text(book, tag_html)
            content_texts.append(converted_soup.get_text().strip())

        poem_text = '\n'.join(content_texts)
        author_intro = ''
        poem_analysis = ''

        if author_intro_tag:
            for sibling in author_intro_tag.find_next_siblings('p', {'class': 'content'}):
                if sibling.get_text().strip() == '鉴赏':
                    break
                author_intro += sibling.get_text().strip() + '\n'

        if poem_analysis_tag:
            for sibling in poem_analysis_tag.find_next_siblings('p', {'class': 'content'}):
                poem_analysis += sibling.get_text().strip() + '\n'

        poem_dict = {
            'Title': title,
            'Author': author,
            'Poem': poem_text,
            'AuthorIntro': author_intro.strip(),
            'PoemAnalysis': poem_analysis.strip()
        }
        poems.append(poem_dict)

    return poems


def create_poems_dataframe(poems):
    df = pd.DataFrame(poems)
    return df


# Example usage
epub_file_path = '唐诗鉴赏辞典.epub'
poems_info = read_epub(epub_file_path)
poems_df = create_poems_dataframe(poems_info)

# Save the DataFrame to a CSV file
poems_df.to_csv('唐诗鉴赏辞典.csv', index=False, encoding='utf-8-sig')
