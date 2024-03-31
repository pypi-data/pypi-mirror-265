import nltk
import re
from nltk.corpus import stopwords

def Stop_Word_Removal_Code(filename):
    with open(filename, 'r') as file:
        data = file.read()
 
    clean_data = re.sub(r'[^\w\s]', '', data).lower()
 
    clean_data_list = clean_data.split()
 
    clean_data_list = [word for word in clean_data_list if word not in stopwords.words('english')]

    return clean_data_list