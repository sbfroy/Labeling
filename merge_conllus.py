import os
import glob

def merge_conllus(folder_path, output_file):
    file_pattern = os.path.join(folder_path, "*.conllu")
    file_list = sorted(glob.glob(file_pattern))
    
    merged_sentences = []
    
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                sentences = content.split("\n\n")
                merged_sentences.extend(sentences)
    
    merged_content = "\n\n".join(merged_sentences) + "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged_content)

if __name__ == '__main__':
    merge_conllus('data/conllus', 'data/all_regplans.conllu')
