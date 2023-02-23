# Extractive Sentence Ranking

import re
import string
from collections import Counter

def format_sentences(sentences):
    formatted_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            formatted_sentence = "- " + sentence[0].upper() + sentence[1:] + "."
            formatted_sentences.append(formatted_sentence)
    return formatted_sentences

# Switch to lowercase, skipping acronyms and other words that are already uppercase.
def selective_lowercase(sentence):
    words = sentence.split()
    result = []
    for word in words:
        if sum(1 for c in word if c.isupper()) >= len(word) / 2:
            result.append(word)
        else:
            result.append(word.lower())
    return " ".join(result)

def is_title(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Count the number of capitalized words
    num_capitalized_words = sum(1 for word in words if word[0].isupper())

    # A sentence is considered a title if at least half of its words are capitalized
    return num_capitalized_words >= len(words) / 2

def strip_titles(sentences):
    # Remove sentences that are considered titles
    body_text = [sentence for sentence in sentences if not is_title(sentence)]
    return body_text

def strip_non_text(sentences):
    """Remove sentences with more non-alphanumeric characters than alphanumeric"""
    text = set(string.ascii_letters)
    stripped_sentences = []
    for sentence in sentences:
        num_text = sum(1 for char in sentence if char in text)
        num_non_text = len(sentence) - num_text
        if num_non_text <= num_text:
            stripped_sentences.append(sentence)
    return stripped_sentences

def replace_newlines(text):
    # Replace newlines before capital letters
    text = re.sub(r"\n\s*([A-Z])", r". \1", text)
    return text

def from_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def extract_sentences(text):
            
    # Fix formatting issues
    text = replace_newlines(text)
    
    # Remove non-alphanumeric characters from the text
    # text = re.sub(r'[^a-z0-9\s]', '', text

    # Split the text into sentences, leave out titles and non-text sentences
    sentences = strip_non_text(strip_titles(re.split(r'[\.\n\-\*>]\s+', text)))
    
    # Convert to lowercase prior to processing
    sentences = list(map(lambda s: selective_lowercase(s), sentences))
    return sentences


def rank_sentences(sentences, query):
    """
    Ranks a list of lists of sentences by those that have the highest frequency of a query word or words.

    Parameters:
    sentences (list of lists of str): The list of sentences to rank.
    file_path (str): path to text
    query (str or list of str): The query word or words.

    Returns:
    list of list of str: The ranked list of sentences.
    """

    # Convert the query to a list of words if it's not already
    if isinstance(query, str):
        query = [query]

    sent_freqs = []
    for sent in sentences:
        freq = sum(1 for word in sent.split() if selective_lowercase(word) in query)
        sent_freqs.append(freq)
    ranked_sentences = [sentences[i] for i in sorted(range(len(sent_freqs)), key=sent_freqs.__getitem__, reverse=True)]
 
    return ranked_sentences
    
# query = input("Query: ")
# file_path = "lecture.txt"
# sentences = extract_sentences(from_file(file_path))
# result = format_sentences(rank_sentences(sentences, query)[:10])
# for sent in result:
#     print(sent.strip())
