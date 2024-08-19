from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub

# Load EPUB file
book = epub.read_epub('宋词鉴赏大辞典.epub')

# Prepare to store extracted contents
extracted_contents = []

# Iterate over items in the EPUB
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    # Parse HTML content of the item
    soup = BeautifulSoup(item.content, 'html.parser')

    # Find all <span> elements
    span_elements = soup.find_all('span')

    # Process each pair of <span> tags
    for i in range(len(span_elements) - 1):
        start_span = span_elements[i]
        end_span = span_elements[i + 1]

        # Find all elements between start_span and end_span
        contents = []
        current_tag = start_span.find_next_sibling()
        while current_tag and current_tag != end_span:
            contents.append(current_tag)
            current_tag = current_tag.find_next_sibling()

        # Extract text from contents
        extracted_content = '\n'.join(tag.get_text(strip=True) for tag in contents if tag.name == 'p' or tag.name == 'b')
        extracted_contents.append(extracted_content)

    break

# Print or further process `extracted_contents` list as needed
for index, content in enumerate(extracted_contents):
    print(f'Content {index + 1}:')
    print(content)
    print('------------------------\n')
