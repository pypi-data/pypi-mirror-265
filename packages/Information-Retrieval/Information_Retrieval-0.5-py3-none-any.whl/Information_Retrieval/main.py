def hello():
    print("Hello World!!!")





# Stop Word
import nltk
import re
from nltk.corpus import stopwords

nltk.download('stopwords')
 
def Stop_Word_Removal_Code(filename):
    with open(filename, 'r') as file:
        data = file.read()
 
    clean_data = re.sub(r'[^\w\s]', '', data).lower()
 
    clean_data_list = clean_data.split()
 
    clean_data_list = [word for word in clean_data_list if word not in stopwords.words('english')]

    return clean_data_list





# Incident Matrix
from collections import OrderedDict

import sys
sys.path.insert(1, 'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1')

def Incident_Matrix_Creation_Code(documents):
    def Add_Words(dict_incident_matrix, *lists):
        for lst in lists:
            for word in lst:
                if word not in dict_incident_matrix:
                    presense = [0] * len(lists)
                else:
                    dict_incident_matrix[word]
    
                presense[lists.index(lst)] = 1
                dict_incident_matrix[word] = presense
    
        return dict_incident_matrix

    documents_n = []
    for file in documents:
        documents_n.append(Stop_Word_Removal_Code(file))

    dict_incident_matrix = Add_Words({}, *documents_n)

    sorted_dict_incident_matrix = OrderedDict(sorted(dict_incident_matrix.items()))

    header = "Word".ljust(20)
    for i in range(1, len(documents_n) + 1):
        header += f"{'Document ' + str(i): <20}"

    print(header, end="\n\n")

    for word, presence in sorted_dict_incident_matrix.items():
        output = word.ljust(20)
        for i in range(len(documents_n)):
            output += f"{presence[i]: <20}"
        print(output)

    return sorted_dict_incident_matrix


# Add document paths
# print(Incident_Matrix_Creation_Code([
#     'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_1.txt',
#     'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_2.txt',
#     'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_3.txt',
#     'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_4.txt'
#     ]))






# Query Resolver
documents = [
    'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_1.txt',
    'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_2.txt',
    'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_3.txt',
    'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_4.txt'
    ]

sorted_dict_incident_matrix = Incident_Matrix_Creation_Code(documents) 

print('\n\n\n')

def flip_bits(string):
    output = ''
    for char in string:
        if char == '0':
            output += '1'
        elif char == '1':
            output += '0'
    return output

def bitwise_and(bin1, bin2):
    int_bin1 = int(bin1, 2)
    int_bin2 = int(bin2, 2)

    result = int_bin1 & int_bin2

    return bin(result)[2:].zfill(len(documents))

def bitwise_or(bin1, bin2):
    int_bin1 = int(bin1, 2)
    int_bin2 = int(bin2, 2)

    result = int_bin1 | int_bin2

    return bin(result)[2:].zfill(len(documents))


query = str(input("Enter query : "))
query_list = query.split(' ')

for i in range(0, len(query_list)):
    if query_list[i] != "AND" and query_list[i] != "OR" and query_list[i] != "NOT":
        query_list[i] = ''.join(map(str, sorted_dict_incident_matrix[query_list[i]]))

for i in range(0, len(query_list)):
    if query_list[i] == "NOT":
        query_list[i + 1] = flip_bits(query_list[i + 1])

query_list = [x for x in query_list if x != "NOT"]

result = ''

for i in range (1, len(query_list), 2):
    if query_list[i] == "AND":
        result = bitwise_and(query_list[i-1], query_list[i+1])
    elif query_list[i] == "OR":
        result = bitwise_or(query_list[i-1], query_list[i+1])

result_list = [*result]

for i in range(len(result_list)):
    if result_list[i] == '1':
        print(f'File is present in File {i + 1}')