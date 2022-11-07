import numpy as np
import pandas as npd
import matplotlib.pyplot as plt
import numpy

from MasterDictionary import load_masterdictionary

mpr = npd.read_csv(r'monetary_policy_report.csv')
fed = npd.read_csv(r'statement.csv')
fxusdcad = npd.read_csv(r'FXUSDCAD.csv')
dico = load_masterdictionary("Loughran-McDonald_MasterDictionary_1993-2021.csv")


def calendar_mpr(document):  # create array with date and text values
    cahhlendar = []
    for i in range(len(document.index)):
        cahhlendar.append([document['date'][i], document['text'][i]])
        # print(cahhlendar[i], '\n')
    return cahhlendar


def calendar_fed(document):
    cahhlendar = []
    for i in range(len(document.index)):
        cahhlendar.append([document['date'][i], document['contents'][i]])
        # print(cahhlendar[i], '\n')
    return cahhlendar

def calendar_fxusdcad(document):
    cahhlendar = []
    for i in range(len(document.index)):
        cahhlendar.append([document['date'][i], document['FXUSDCAD'][i]])
        # print(cahhlendar[i], '\n')
    return cahhlendar

def clean_text(text):  # Input: string
    # Output: list of uppercase words, no numbers/punctuation, "stop words" and short invalid words still included
    checked_chars = []
    for char in text:
        if char not in checked_chars:
            if char == '-':
                text = text.replace(char, ' ')
            if not (char.isalpha() or char.isspace()) or char == '-':
                text = text.replace(char, '')
            checked_chars.append(char)

    text = text.split()

    for word_index in range(len(text)):
        text[word_index] = text[word_index].upper()

    return text


def infl(spltTxt, i):  # checks if word is in dictionnary, taking into account badly split words
    if spltTxt[i] in dico:
        return spltTxt[i]
    elif i + 1 < len(spltTxt) and spltTxt[i] + spltTxt[i + 1] in dico:
        return spltTxt[i] + spltTxt[i + 1]
    else:
        return None


def score(listemot):
    current_score = 0
    current_modifier = 1

    for word_index in range(len(listemot)):
        current_word = infl(listemot, word_index)
        if current_word:
            positivity = numpy.clip(dico[current_word].positive, 0, 1) - numpy.clip(dico[current_word].negative, 0, 1)
            modifier = numpy.clip(dico[current_word].strong_modal, 0, 1) * 2 + numpy.clip(dico[current_word].weak_modal,
                                                                                          0, 1) * 0.5

            current_score += positivity * current_modifier
            if modifier != 0:
                current_modifier = modifier
            else:
                current_modifier = 1
    return current_score / len(listemot) * 1000


def result_mpr(document):
    list = calendar_mpr(document)
    new_list = []
    for date_index in range(len(list)):
        new_list.append([])
        new_list[date_index].append(list[date_index][0])
        new_list[date_index].append(clean_text(list[date_index][1]))
        new_list[date_index].append(score(new_list[date_index][1]))
    return new_list


def result_fed(document):
    list = calendar_fed(document)
    new_list = []
    for date_index in range(len(list)):
        new_list.append([])
        new_list[date_index].append(list[date_index][0])
        new_list[date_index].append(clean_text(list[date_index][1]))
        new_list[date_index].append(score(new_list[date_index][1]))
    return new_list


def z_score_creator(results):
    scores = []
    for date in results:
        scores.append(date[2])
    mean = numpy.mean(scores)
    std = numpy.std(scores)
    new_results = results
    for date in new_results:
        date.append((date[2] - mean) / std)
    return new_results


results_mpr = result_mpr(mpr)
results_fed = result_fed(fed)
new_resultsfed = z_score_creator(results_fed)
new_resultsmpr = z_score_creator(results_mpr)


#for line in new_resultsfed:
#    print(line[0], " ", round(line[2], 1), " ", round(line[3], 2))

arrayresultsfed = np.array(new_resultsfed, dtype=object)
arrayresultsmpr = np.array(new_resultsmpr, dtype=object)
arrayresultsfxusdcad = np.array(calendar_fxusdcad(fxusdcad), dtype=object)
subarrayfed = np.argsort(arrayresultsfed[:, 0])
print(subarrayfed)
subarraympr = np.argsort(arrayresultsmpr[:, 0])
print(subarraympr)
subarrayfxusdcad = np.argsort(arrayresultsfxusdcad[:, 0])
print(subarrayfxusdcad)
points_to_display = min(len(arrayresultsfed), len(arrayresultsmpr), len(arrayresultsfxusdcad))
fed = arrayresultsfed[:, 3]
mpr = arrayresultsmpr[:, 3]
fxusdcad = np.empty(points_to_display)

for i in range(points_to_display):
    fxusdcad[i] = arrayresultsfxusdcad[int(i/points_to_display*(len(arrayresultsfxusdcad) - 1)), 1]



plt.plot(fed)
plt.plot(mpr)
plt.plot(fxusdcad)
plt.show()
