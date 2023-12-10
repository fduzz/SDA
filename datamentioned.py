import os
import re

# def a function to extract and clean data sentences
def extract_clean_data_sentences(text):
    sentences = text.split('。')
    data_pattern = re.compile(r'\d+(\.\d+)?(万|亿|％|%)')
    cleaned_data_sentences = []

    for sentence in sentences:
        sub_sentences = sentence.split('，')
        sub_sentences_with_data = []

        for sub_sentence in sub_sentences:
            if data_pattern.search(sub_sentence):
                if not re.search(r'\d+年|\d+号|‘\d+’平台', sub_sentence):
                    sub_sentences_with_data.append(sub_sentence)

        if sub_sentences_with_data:
            cleaned_sentence = '，'.join(sub_sentences_with_data)
            cleaned_data_sentences.append(cleaned_sentence)

    return cleaned_data_sentences

# def a function to process each file and save the result
def process_file(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_data_sentences = extract_clean_data_sentences(text)
    final_text = '；'.join(cleaned_data_sentences)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_text)

# def a function to process all files in a directory
def process_and_save_all_files(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                output_file_name = os.path.splitext(file)[0] + '_数据提取.txt'
                output_file_path = os.path.join(output_folder_path, output_file_name)
                process_file(file_path, output_file_path)

# Process
input_folder_path = 'C:/Chenyuan/2023秋季学期/SDA/期末/Scrape/Result'  
output_folder_path = 'C:/Chenyuan/2023秋季学期/SDA/期末/datamentioned'  

process_and_save_all_files(input_folder_path, output_folder_path)