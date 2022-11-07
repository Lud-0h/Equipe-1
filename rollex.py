import pandas as npd

mpr = npd.read_csv(
    r"C:\\Users\\alexa\\Downloads\\Datathon-2022-data-master\\data\\dataset\\CanBank\\monetary_policy_report.csv")

def calendar():
    cahhlendar = []
    for i in range(len(mpr.index)):
        cahhlendar.append([mpr['date'][i],mpr['text'][i]])
        print(cahhlendar[i], '\n')

#test
calendar()












