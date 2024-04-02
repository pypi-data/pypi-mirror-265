import re
from collections import Counter
import textdistance
import pandas as pd
import os


current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'autocorrect book.txt')

print("Attempting to open file at:", file_path)
# Get the absolute path to the file



words = []

with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read().lower()
    words = re.findall('\w+', data)
    words += words

# Create a set of unique words and a frequency dictionary
V = set(words)
words_freq_dict = Counter(words)
Total = sum(words_freq_dict.values())
probs = {}

for k in words_freq_dict.keys():
    probs[k] = words_freq_dict[k] / Total

def get_suggestions(keyword):
    keyword = keyword.lower()
    if keyword:
        similarities = [1 - textdistance.Jaccard(qval=len(keyword)-1).distance(v, keyword) for v in words_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df.columns = ['Word', 'Prob']
        df['Similarity'] = similarities
        suggestions = df.sort_values(['Similarity', 'Prob'], ascending=False).head(10)['Word'].tolist()
        return suggestions
    else:
        return []

if __name__ == '__main__':
    
        keyword = input("Enter a word: ")
        suggestions = get_suggestions(keyword)
        print("Suggestions:", suggestions)
