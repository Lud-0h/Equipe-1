import pandas as npd
from sklearn.feature_extraction.text import TfidfVectorizer

mpr = npd.read_csv(
    r"C:\\Users\\alexa\\Downloads\\Datathon-2022-data-master\\data\\dataset\\CanBank\\monetary_policy_report.csv")

def calendar():
    cahhlendar = []
    for i in range(len(mpr.index)):
        cahhlendar.append([mpr['date'][i],mpr['text'][i]])
        print(cahhlendar[i], '\n')


calendar()












