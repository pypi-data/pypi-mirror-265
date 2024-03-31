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





# K-gram
def K_Gram_Code():
    n = int(input("Enter the value for n in n-gram : "))

    filename = "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_1.txt"

    with open(filename, 'r') as file:
        data = file.read().replace(" ", "$")

    data = f"${data}$"

    output = ""

    for i in range(0, len(data) - n + 1):
        output += data[i:i+n] + "\t"

    print(output)





# Edit Distance
def Edit_Distance_Code():
    def compute_edit_distance(s1, s2):
        len_s1 = len(s1)
        len_s2 = len(s2)

        matrix = [[0 for _ in range(len_s1 + 1)] for _ in range(len_s2 + 1)]

        for i in range(len_s1 + 1):
            matrix[0][i] = i

        for i in range(len_s2 + 1):
            matrix[i][0] = i

        for i in range(1, len_s2 + 1):
            for j in range(1, len_s1 + 1):
                if s1[j - 1] == s2[i - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = min(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]) + 1

        return matrix[len_s2][len_s1]

    s1 = "ALICE"
    s2 = "PARIS"

    print(f"\n\nThe edit distance between {s1} and {s2} is {compute_edit_distance(s1.upper(), s2.upper())}")





# Cosine Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    nv1 = np.linalg.norm(v1)
    nv2 = np.linalg.norm(v2)

    if nv1 == 0 or nv2 == 0:
        return 0
    else:
        return dot_product / (nv1 * nv2)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return ' '.join(words)

def compute_similarity(data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data)

    tf_array = tfidf_matrix.toarray()
    tf_terms = vectorizer.get_feature_names_out()

    df = pd.DataFrame(tf_array, columns=tf_terms)

    arr = np.zeros((len(tf_array), len(tf_array)))

    for i in range(len(arr)):
        for j in range(len(arr)):
            arr[i][j] = cosine_similarity(tf_array[i], tf_array[j])

    df_arr = pd.DataFrame(arr)
    print(df_arr, end="\n\n")

    for i in range(len(df_arr)):
        for j in range(i + 1, len(df_arr)):
            if df_arr.iloc[i, j] > 0.7:
                print(f"Documents {i+1} and {j+1} have cosine similarity: {df_arr.iloc[i, j]}")

file_paths = [
    "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_1.txt",
    "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_2.txt",
    "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_3.txt",
    "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_4.txt",
    "P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_1/Paragraph_5.txt"
]
data = [preprocess_text(open(i, 'r').read()) for i in file_paths]

compute_similarity(data)





# Soundex
def Soundex_Code():
    input_text = input("Enter a word: ").upper()
    print(f"Input text is {input_text}")

    soundex_word = input_text[0]

    rules = {
        "0": "AEIOUHW",
        "1": "BFPV",
        "2": "CGJKQSXZ",
        "3": "DT",
        "4": "L",
        "5": "MN",
        "6": "R"
    }

    for char in input_text[1:]:
        for key, value in rules.items():
            if char.upper() in value:
                soundex_word += key
                break

    print("Soundex key:", soundex_word)

    new_soundex_word = soundex_word[0]
    for i in range(1, len(soundex_word)):
        if soundex_word[i] != soundex_word[i - 1]:
            new_soundex_word += soundex_word[i]

    print("Soundex key without consecutive duplicates:", new_soundex_word)

    new_soundex_word = new_soundex_word.replace("0", "")

    print("Soundex key without consecutive duplicates and without '0':", new_soundex_word[:4])





# Page Rank
import numpy as np 

def Page_Rank_Code():
    mat = np.array([
        [1/3, 1/2, 0],
        [1/3, 0, 1/2],
        [1/3, 1/2, 1/2]
    ])

    ini_mat = np.full((len(mat), 1), 1/len(mat))

    B = 0.8

    A = (B * mat) + ((1 - B) * ini_mat)
    print(A)

    temp = np.zeros_like(ini_mat)
    iteration = 1

    while True:
        ini_mat = np.dot(A, ini_mat)
        
        print(f"Iteration {iteration}")
        if np.allclose(ini_mat, temp, atol=1e-4):
            print("Converged!")
            print(ini_mat)
            break
        temp = ini_mat
        iteration += 1
        print(ini_mat)





# Porter Stemmer
from nltk.stem import PorterStemmer

def Porter_Stemmer_Code():
    porter = PorterStemmer()

    words = ["running", "flies", "agreed", "plastered", "motoring", "conflated", "hunger", "fluttering"]

    for word in words:
        stemmed_word = porter.stem(word)
        print(f"{word} -> {stemmed_word}")





# Collaborative Filtering
import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def Collaborative_Filtering():
    matrix_file = 'P2_INFORMATION_RETRIEVAL/PRACTICAL/Practical_10/data.csv' 
    with open(matrix_file, 'r') as file:
        reader = csv.reader(file)
        matrix = [list(map(int, row)) for row in reader]

    for i in range(len(matrix[0]) + 1):
        if i == 0:
            print("-", end="\t")
        else:
            print(i, end="\t")
    print()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j == 0:
                print(chr(i + 65), end="\t")
            if matrix[i][j] == 0:
                print("-", end="\t")
            else:
                print(matrix[i][j], end="\t")
        print("\n")

    cosine_similarity_score = [0, ]

    for i in range(len(matrix) - 1):
        vector1 = np.array(matrix[0]).reshape(1, -1)
        vector2 = np.array(matrix[i + 1]).reshape(1, -1)
        similarity_score = cosine_similarity(vector1, vector2)
        cosine_similarity_score.append(round(similarity_score.item(), 2))

    print(cosine_similarity_score)

    css = cosine_similarity_score.copy()
    max_1 = css.index(max(css))
    css.pop(max_1)
    max_2 = css.index(max(css))

    n = 9

    predicted_rating = ((matrix[max_1][n] * cosine_similarity_score[max_1]) +
                        (matrix[max_2][n] * cosine_similarity_score[max_2])) / (
                            cosine_similarity_score[max_1] + cosine_similarity_score[max_2])

    print(f"The predicted rating is {round(predicted_rating, 3)}")