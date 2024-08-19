import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def read_epub(file_path):
    book = epub.read_epub(file_path)
    image_references = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')

        # Find all 'p' tags with either 'reference' or 'center-reference' class that contain an 'img' tag
        poem_text_tags = soup.find_all(lambda tag: (tag.name == 'p' and 'reference' in tag.get('class', []) and tag.find('img')) or
                                                   (tag.name == 'p' and 'center-reference' in tag.get('class', []) and tag.find('img')))

        for poem_text_tag in poem_text_tags:
            image_references.append(str(poem_text_tag))

    return image_references

def save_references_to_txt(references, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for ref in references:
            file.write(ref + '\n\n')  # Separate each reference with a blank line

# Example usage
epub_file_path = '唐诗鉴赏辞典.epub'
output_txt_path = 'image_references.html'

image_references = read_epub(epub_file_path)
save_references_to_txt(image_references, output_txt_path)

print(f'Extracted image references have been saved to {output_txt_path}')
