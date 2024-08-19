import pandas as pd
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub

# Load EPUB file
book = epub.read_epub('宋词鉴赏大辞典.epub')

# Prepare to store poem data
poems = []

# Iterate over items in the EPUB
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    # Parse HTML content of the item
    soup = BeautifulSoup(item.content, 'html.parser')

    # Find all <span> elements
    span_elements = soup.find_all('span')
    if len(span_elements) < 1:
        continue

    # -------------------
    # Process type 1: Poets that start from the beginning of HTML, end with a <span>
    # -------------------
    first_span = span_elements[0]
    previous_tags = []
    current_tag = first_span.previous_sibling
    while current_tag:
        previous_tags.append(current_tag)
        current_tag = current_tag.previous_sibling

    previous_tags.reverse()
    previous_content = ''.join(str(tag) for tag in previous_tags)

    # Process the content before the first <span>
    content_soup = BeautifulSoup(previous_content, 'html.parser')

    # Process all poems within this content
    while True:
        # Find <b> tag for author and clean up author name
        author_tag = content_soup.find('b')
        if author_tag:
            raw_author = author_tag.text.strip()  # Get raw author name
            author = raw_author.replace('词作鉴赏', '').strip()  # Clean up author name

            # Process all poems within this content
            while True:
                # Find the <p> tag containing '●' as the start of the title
                title_start_tag = content_soup.find('p', string=lambda text: '●' in text if text else False)
                if not title_start_tag:
                    break  # No more titles found

                # Find the <p> tag exactly matching the author's name as the end of the title
                title_end_tag = title_start_tag.find_next_sibling('p', string=author)
                if not title_end_tag:
                    break  # No end tag found, likely the end of content

                # Extract title lines
                title_lines = []
                current_tag = title_start_tag
                while current_tag and current_tag != title_end_tag:
                    if current_tag.name == 'p':
                        title_lines.append(current_tag)
                    current_tag = current_tag.find_next_sibling()

                # Format title with '·' between lines
                formatted_title = '·'.join(tag.text.strip() for tag in title_lines).replace('●','')

                # Find poem content starting after the title ends
                poem_lines = []
                poem_tag = title_end_tag.find_next_sibling()
                while poem_tag and poem_tag.name == 'p' and not poem_tag.text.strip().startswith(author):
                    poem_lines.append(poem_tag)
                    poem_tag = poem_tag.find_next_sibling()

                # Join poem lines with '\n'
                poem_content = '\n'.join(tag.text.strip() for tag in poem_lines)

                # Find analysis content starting after the poem content
                analysis_lines = []
                analysis_tag = poem_tag
                while analysis_tag and analysis_tag.name == 'p' and '●' not in analysis_tag.text and analysis_tag.name != 'span':
                    analysis_lines.append(analysis_tag)
                    analysis_tag = analysis_tag.find_next_sibling()

                # Join analysis lines with '\n'
                analysis_content = '\n'.join(tag.text.strip() for tag in analysis_lines)

                # Store poem data in a dictionary
                poem_data = {
                    'author': author,
                    'title': formatted_title,
                    'content': poem_content,
                    'analysis': analysis_content
                }
                poems.append(poem_data)

                # Remove the processed poem from the content_soup to avoid duplicate processing
                for tag in title_lines:
                    tag.extract()
                title_end_tag.extract()
                for tag in poem_lines:
                    tag.extract()
                for tag in analysis_lines:
                    tag.extract()

        # Remove the processed content from the soup to avoid reprocessing
        content_soup.clear()

        # Break loop if no more poems found before the first <span>
        break

    # -------------------
    # Process type 2: Poets that are between two sibling <span> tags
    # -------------------
    for i in range(len(span_elements) - 1):
        start_span = span_elements[i]
        end_span = span_elements[i + 1]

        # Extract all tags between start_span and end_span
        contents = []
        current_tag = start_span.find_next_sibling()
        while current_tag and current_tag != end_span:
            contents.append(current_tag)
            current_tag = current_tag.find_next_sibling()

        # Convert contents to a soup for easier processing
        content_soup = BeautifulSoup(''.join(str(tag) for tag in contents), 'html.parser')

        # Process all poems within this content
        while True:
            # Find <b> tag for author and clean up author name
            author_tag = content_soup.find('b')
            if author_tag:
                raw_author = author_tag.text.strip()  # Get raw author name
                author = raw_author.replace('词作鉴赏', '').strip()  # Clean up author name

                # Process all poems within this content
                while True:
                    # Find the <p> tag containing '●' as the start of the title
                    title_start_tag = content_soup.find('p', string=lambda text: '●' in text if text else False)
                    if not title_start_tag:
                        break  # No more titles found

                    # Find the <p> tag exactly matching the author's name as the end of the title
                    title_end_tag = title_start_tag.find_next_sibling('p', string=author)
                    if not title_end_tag:
                        break  # No end tag found, likely the end of content

                    # Extract title lines
                    title_lines = []
                    current_tag = title_start_tag
                    while current_tag and current_tag != title_end_tag:
                        if current_tag.name == 'p':
                            title_lines.append(current_tag)
                        current_tag = current_tag.find_next_sibling()

                    # Format title with '·' between lines
                    formatted_title = '·'.join(tag.text.strip() for tag in title_lines).replace('●','')

                    # Find poem content starting after the title ends
                    poem_lines = []
                    poem_tag = title_end_tag.find_next_sibling()
                    while poem_tag and poem_tag.name == 'p' and not poem_tag.text.strip().startswith(author):
                        poem_lines.append(poem_tag)
                        poem_tag = poem_tag.find_next_sibling()

                    # Join poem lines with '\n'
                    poem_content = '\n'.join(tag.text.strip() for tag in poem_lines)

                    # Find analysis content starting after the poem content
                    analysis_lines = []
                    analysis_tag = poem_tag
                    while analysis_tag and analysis_tag.name == 'p' and '●' not in analysis_tag.text and analysis_tag.name != 'span':
                        analysis_lines.append(analysis_tag)
                        analysis_tag = analysis_tag.find_next_sibling()

                    # Join analysis lines with '\n'
                    analysis_content = '\n'.join(tag.text.strip() for tag in analysis_lines)

                    # Store poem data in a dictionary
                    poem_data = {
                        'author': author,
                        'title': formatted_title,
                        'content': poem_content,
                        'analysis': analysis_content
                    }
                    poems.append(poem_data)

                    # Remove the processed poem from the content_soup to avoid duplicate processing
                    for tag in title_lines:
                        tag.extract()
                    title_end_tag.extract()
                    for tag in poem_lines:
                        tag.extract()
                    for tag in analysis_lines:
                        tag.extract()

            # Remove the processed content from the soup to avoid reprocessing
            content_soup.clear()

            # Break loop if no more poems found between sibling <span> tags
            break

    # -------------------
    # Process type 3: Poets that are after the last <span> in the HTML
    # -------------------
    last_span = span_elements[-1]
    if last_span:

        # get every tag after the last_span
        contents = []
        current_tag = last_span.find_next_sibling()
        while current_tag:
            contents.append(current_tag)
            current_tag = current_tag.find_next_sibling()

        content_soup = BeautifulSoup('.'.join(str(tag) for tag in contents), 'html.parser')

        # Process all poems within this content
        while True:
            # Find <b> tag for author and clean up author name
            author_tag = content_soup.find('b')
            if author_tag:
                raw_author = author_tag.text.strip()  # Get raw author name
                author = raw_author.replace('词作鉴赏', '').strip()  # Clean up author name

                # Process all poems within this content
                while True:
                    # Find the <p> tag containing '●' as the start of the title
                    title_start_tag = content_soup.find('p', string=lambda text: '●' in text if text else False)
                    if not title_start_tag:
                        break  # No more titles found

                    # Find the <p> tag exactly matching the author's name as the end of the title
                    title_end_tag = title_start_tag.find_next_sibling('p', string=author)
                    if not title_end_tag:
                        break  # No end tag found, likely the end of content

                    # Extract title lines
                    title_lines = []
                    current_tag = title_start_tag
                    while current_tag and current_tag != title_end_tag:
                        if current_tag.name == 'p':
                            title_lines.append(current_tag)
                        current_tag = current_tag.find_next_sibling()

                    # Format title with '·' between lines
                    formatted_title = '·'.join(tag.text.strip() for tag in title_lines).replace('●','')

                    # Find poem content starting after the title ends
                    poem_lines = []
                    poem_tag = title_end_tag.find_next_sibling()
                    while poem_tag and poem_tag.name == 'p' and not poem_tag.text.strip().startswith(author):
                        poem_lines.append(poem_tag)
                        poem_tag = poem_tag.find_next_sibling()

                    # Join poem lines with '\n'
                    poem_content = '\n'.join(tag.text.strip() for tag in poem_lines)

                    # Find analysis content starting after the poem content
                    analysis_lines = []
                    analysis_tag = poem_tag
                    while analysis_tag and analysis_tag.name == 'p' and '●' not in analysis_tag.text and analysis_tag.name != 'span':
                        analysis_lines.append(analysis_tag)
                        analysis_tag = analysis_tag.find_next_sibling()

                    # Join analysis lines with '\n'
                    analysis_content = '\n'.join(tag.text.strip() for tag in analysis_lines)

                    # Store poem data in a dictionary
                    poem_data = {
                        'author': author,
                        'title': formatted_title,
                        'content': poem_content,
                        'analysis': analysis_content
                    }
                    poems.append(poem_data)

                    # Remove the processed poem from the content_soup to avoid duplicate processing
                    for tag in title_lines:
                        tag.extract()
                    title_end_tag.extract()
                    for tag in poem_lines:
                        tag.extract()
                    for tag in analysis_lines:
                        tag.extract()

            # Remove the processed content from the soup to avoid reprocessing
            content_soup.clear()

            # Break loop if no more poems found after the last <span>
            break


# 将诗词数据写入CSV文件
df = pd.DataFrame(poems)
df.to_csv('songci.csv', index=False, encoding='utf-8-sig')

print("转换完成，CSV文件已生成。")