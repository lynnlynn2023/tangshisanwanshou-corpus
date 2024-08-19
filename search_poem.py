import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler

# Load the CSV file into a DataFrame
df = pd.read_csv('唐诗鉴赏辞典_with_popularity.csv')


def normalize_spaces(text):
    # Replace any type of space (including full-width spaces) with a regular ASCII space
    return re.sub(r'\s+', ' ', text)


def calculate_relevance_score(poem_analysis, words, weights):
    relevance_score = 0
    for i, word in enumerate(words):
        if word in poem_analysis:
            relevance_score += weights[i]
    return relevance_score


def search_poems(keywords):
    # Normalize spaces in the input keywords
    normalized_keywords = normalize_spaces(keywords)
    # Split the normalized keywords
    words = normalized_keywords.split()

    # Assign exponentially decreasing weights to the keywords
    raw_weights = [1.0 / (2 ** i) for i in range(1, len(words) + 1)]
    total_weight = sum(raw_weights)
    normalized_weights = [w / total_weight for w in raw_weights]

    # Calculate the relevance score for each poem
    df['RelevanceScore'] = df['PoemAnalysis'].apply(
        lambda x: calculate_relevance_score(str(x), words, normalized_weights))

    # Normalize PoemGoogleCounts to a score between 0 and 1
    scaler = MinMaxScaler()
    df['NormalizedGoogleCounts'] = scaler.fit_transform(df[['PoemGoogleCounts']])

    # Combine relevance score and normalized PoemGoogleCounts
    df['FinalScore'] = df['RelevanceScore'] + df['NormalizedGoogleCounts']

    # Sort by FinalScore in descending order
    ranked_results = df.sort_values(by='FinalScore', ascending=False)

    # Create masks for all and any keyword matches
    mask_all = df['PoemAnalysis'].apply(lambda x: all(word in str(x) for word in words))
    mask_any = df['PoemAnalysis'].apply(lambda x: any(word in str(x) for word in words))

    # Rank poems in mask_all first
    ranked_all = ranked_results[mask_all]

    # Remove poems in ranked_all from mask_any
    remaining_any = ranked_results[mask_any & ~mask_all]

    # Concatenate the results, with ranked_all first
    final_results = pd.concat([ranked_all, remaining_any])

    return final_results


# Example usage
keywords = "寒食 贫"
results = search_poems(keywords)

# Print the poem and its google counts
for index, row in results.iterrows():
    print(row['Poem'], row['PoemGoogleCounts'])
