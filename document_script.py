import os
import pandas as pd

data_dir = 'wiki_data/'
out_csv_path = 'documents.csv'
urls_path = 'train_urls.txt'
titles_path = '../wikipedia-biography-dataset/wikipedia-biography-dataset/train/train.title'

def parse_document(document_lines):
    start = 0
    while start < len(document_lines) and document_lines[start] != "Contents\n":
        start += 1

    doc = []
    for i in range(start, len(document_lines)):
        if document_lines[i][0] == "^":
            continue

        line_length = len(document_lines[i].split(" "))
        if "References" == document_lines[i][:len("References")] and line_length < 2:
            break

        if line_length > 10:
            doc.append(document_lines[i])

    return ' '.join(doc)

def get_contents_index(article_lines):
    for i in range(len(article_lines)):
        if article_lines[i] == 'Contents\n':
            return i
    
    return -1

def parse_summary(article_lines):
    index = get_contents_index(article_lines)
    
    while(len(article_lines[index].split(" "))) < 8 and index >= 0:
        index -= 1
    
    summary_indices = []
    summary_indices.append(index)
    
    summary = []
    while len(article_lines[index].split(" ")) > 8 and index >= 0:
        summary.insert(0, article_lines[index].strip())
        index -= 1
        
    summary_indices.append(index)
        
    return ' '.join(summary), summary_indices[::-1]

def parse_dataset_for_documents(csv_path, data_dir, urls_path, titles_path, num_docs):
    df = pd.DataFrame(columns=['Document Number', 'Document', 'Summary', 'Title', 'URL'])
    docs = []
    summaries = []
    numbers = []
    used_document_count = 0
    skipped_document_count = 0
    ordered_urls = []
    ordered_titles = []
    
    urls = open(urls_path, 'r').readlines()
    titles = open(titles_path, 'r').readlines()
    filenames = os.listdir(data_dir)
    num_docs = num_docs if num_docs > 0 else len(filenames)
    print(num_docs)
    for i in range(num_docs):
        filename = filenames[i]
        if filename.split(".")[1] != 'txt':
            continue
            
        lines = open(data_dir + filename).readlines()
        document = parse_document(lines)
        summary, summary_indices = parse_summary(lines)
        
        if document != "" and summary != "":
            doc_num = filename.split(".")[0]
            url = urls[int(doc_num)]
            title = titles[int(doc_num)]
            
            docs.append(document)
            summaries.append(summary)
            numbers.append(doc_num)
            ordered_titles.append(title[:len(title) - 1])
            ordered_urls.append(url[:len(url) - 1])
            
            used_document_count += 1
        else:
            skipped_document_count += 1
                    
        if used_document_count % 10000 == 0:
            print(str(used_document_count) + ' used.')
            
    df['Document'] = docs
    df['Summary'] = summaries
    df['Document Number'] = numbers
    df['Title'] = ordered_titles
    df['URL'] = ordered_urls
    
    df.to_csv(csv_path, index=False)
    
    return used_document_count, skipped_document_count

used_count, skipped_count = parse_dataset_for_documents(out_csv_path, data_dir, urls_path, titles_path, -1)
print(used_count, skipped_count)