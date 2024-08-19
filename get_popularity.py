import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

def get_first_line(poem_text):
    if isinstance(poem_text, str):
        match = re.search(r'[^。]*。', poem_text)
        return match.group(0) if match else ''
    return ''

def google_search_results_count(query):
    try:
        # Mimic a request to Google search
        url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the number of search results from Google's result stats
        result_stats = soup.find(id='result-stats')
        if result_stats:
            result_text = result_stats.text
            print(query, result_text)
            result_count = re.search(r'About ([0-9,]+) results', result_text)
            if result_count:
                return int(result_count.group(1).replace(',', ''))
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def update_poem_popularity(csv_file_path):
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')
    df.columns = ['Author', 'Title', 'Poem', 'PoemAnalysis']
    df['FirstLine'] = df['Poem'].apply(get_first_line)
    df['PoemGoogleCounts'] = df['FirstLine'].apply(lambda x: google_search_results_count(x) if x else 0)
    df.drop(columns=['FirstLine'], inplace=True)
    df.to_csv('zhongxiao_with_popularity.csv', index=False, encoding='utf-8-sig')

# Example usage
csv_file_path = 'zhongxiao.csv'
update_poem_popularity(csv_file_path)
