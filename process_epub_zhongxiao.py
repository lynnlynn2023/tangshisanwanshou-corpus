import zipfile
import pandas as pd
from bs4 import BeautifulSoup


# Function to extract text from a specific class, excluding <sup> tags
def extract_text(elements, class_name):
    texts = []
    for element in elements:
        for sup in element.find_all("sup", class_="suptext"):
            sup.decompose()
        if element.get("class") and class_name in element.get("class"):
            texts.append(element.get_text(strip=True))
    return "\n".join(texts)  # Use '\n' to concatenate lines


# Function to remove all spaces (including Chinese character spaces)
def remove_spaces(text):
    if text:
        return text.replace(" ", "").replace("　", "")
    return text

# Path to the EPUB file
epub_path = '../中学生必背古诗词.epub'

# Open the EPUB file
with zipfile.ZipFile(epub_path, 'r') as epub:
    # List of target files
    target_files = [
        'EPUB/text00006.html', 'EPUB/text00007.html', 'EPUB/text00008.html',
        'EPUB/text00009.html', 'EPUB/text00010.html', 'EPUB/text00011.html'
    ]

    # Data structure to hold the extracted data
    data = []

    # Process each relevant HTML file
    for file in target_files:
        try:
            with epub.open(file) as f:
                soup = BeautifulSoup(f, 'html.parser')

                # Find all poems in the file
                poems = soup.find_all(class_='subtitle03')
                for poem in poems:
                    # Extract Title
                    title = remove_spaces(poem.get_text(strip=True))

                    # Extract Author if available
                    author_tag = poem.find_next_sibling(class_='subtitle001')
                    if author_tag:
                        # Exclude <sup> tags from author
                        for sup in author_tag.find_all("sup", class_="suptext"):
                            sup.decompose()
                        author = remove_spaces(author_tag.get_text(strip=True))
                    else:
                        author = '佚名'

                    # Extract Poem
                    poem_elements = []
                    next_sibling = poem.find_next_sibling()
                    while next_sibling and 'subtitle03' not in next_sibling.get("class", []):
                        poem_elements.append(next_sibling)
                        next_sibling = next_sibling.find_next_sibling()
                    poem_text = remove_spaces(extract_text(poem_elements, 'normaltext'))

                    # Extract PoemAnalysis
                    poem_analysis_elements = [el for el in poem_elements if 'normaltext02' in el.get("class", [])]
                    poem_analysis = remove_spaces(extract_text(poem_analysis_elements, 'normaltext02'))

                    # Append to data list
                    data.append({
                        'Title': title,
                        'Author': author,
                        'Poem': poem_text,
                        'PoemAnalysis': poem_analysis
                    })
        except KeyError:
            print(f"File {file} not found in the EPUB archive.")

# Create a DataFrame and write to CSV
df = pd.DataFrame(data)
output_path = 'zhongxiao.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Data extracted and saved to {output_path}")
