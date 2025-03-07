import sys
import re
import os
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_file_context(file_path):
    if(os.path.exists(file_path) == False):
        raise FileNotFoundError(f"找不到 '{file_path}' 文件！");
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def remove_punctuation(text):
    chinese_punctuation = r'、。！？《》【】“”‘’；：·—，'
    english_punctuation = r'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    combined_pattern = f'[{re.escape(chinese_punctuation + english_punctuation)}]'
    return re.sub(combined_pattern, '', text)

def tokenize_with_spaces(text):
    return ' '.join(jieba.cut(text))

def get_similarity_score(original_content, plagiarized_content):
    processed_original = remove_punctuation(original_content.strip())
    processed_plagiarized = remove_punctuation(plagiarized_content.strip())

    tokenized_original = tokenize_with_spaces(processed_original)
    tokenized_plagiarized = tokenize_with_spaces(processed_plagiarized)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_results = tfidf_vectorizer.fit_transform([tokenized_original, tokenized_plagiarized])

    similarity_score = cosine_similarity(tfidf_results[0:1], tfidf_results[1:2])[0][0]

    return similarity_score

def main():
    if(len(sys.argv) != 4):
        print("正确用法: python main.py [论文原文路径] [抄袭版论文路径] [结果保存路径]")
        sys.exit(1)

    original_file_path = sys.argv[1]
    plagiarized_file_path = sys.argv[2]
    answer_file_path = sys.argv[3]

    original_content = get_file_context(original_file_path)
    plagiarized_content = get_file_context(plagiarized_file_path)

    similarity_score = get_similarity_score(original_content, plagiarized_content)

    with open(answer_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("{:.2f}".format(similarity_score))

    print("{:.2f}".format(similarity_score))

if __name__ == '__main__':
    main()