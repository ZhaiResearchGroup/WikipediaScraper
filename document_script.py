import os
import pandas as pd

data_dir = 'wiki_data/'
out_csv_path = 'documents.csv'

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

def parse_dataset_for_documents(csv_path, data_dir):
    df = pd.DataFrame(columns=['Document Number', 'Document'])
    docs = []
    numbers = []
    used_document_count = 0
    skipped_document_count = 0
    
    for filename in os.listdir(data_dir):
        if filename.split(".")[1] != 'txt':
            continue
            
        document = parse_document(open(data_dir + filename).readlines())
        if document != "":
            docs.append(document)
            numbers.append(filename.split(".")[0])
            used_document_count += 1
        else:
            skipped_document_count += 1
                    
        if used_document_count % 10000 == 0:
            print(str(used_document_count) + ' used.')
            
    df['Document'] = docs
    df['Document Number'] = numbers
    
    df.to_csv(csv_path, index=False)
    
    return used_document_count, skipped_document_count

used_doc_count, skip_doc_count = parse_dataset_for_documents(out_csv_path, data_dir)

print(used_doc_count, skip_doc_count)