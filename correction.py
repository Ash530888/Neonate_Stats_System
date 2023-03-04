import AWSAPI
from spellchecker import SpellChecker

# check if the time format is correct
def if_correct_format(time):
    if len(time) != 4:
        return False

    hour = int(time[0:2])
    minute = int(time[-2:])
    if 0 <= hour <= 24 and 0 <= minute <= 60:
        return True
    else:
        return False

# calculate utility score for the time
def utility_and_correct(time):
    length = len(time)
    temp = ""
    # For those times with ':'
    if time.find(":") != -1:
        hour = time
    for i in time:
        # for all number 1 similar characters
        if i == "/" or i == "l":
            temp = temp + "1"
        # for all number 0 similar characters
        if i == "o" or i == "O":
            temp = temp + "0"
        if 48 <= ord(i) <= 57:
            temp = temp + i
            #print(temp)
    # most common result
    if len(temp) == 4:
        # correct!
        if if_correct_format(temp):
            return 1, temp
        # the situation when ':' is recognized as 8
        elif temp[1] == "8":
            time = "0" + temp[0] + temp[-2:]
            return 0.9, time
        # wrongly recognized situation
        else:
            return 0.2, temp
    elif len(temp) == 3:
        # for the time in format: 6:00
        if 0 <= int(temp[-2:]) <= 60:
            time = "0" + temp
            return 0.95, time
        # for the time in format: 12:0
        elif 0 <= int(temp[:2]) <= 24:
            time = temp + "0"
            return 0.5, time
        else:
            return 0.2, temp
    # if only one or two digits remains, the utility score should be low. Hard to correct in this situation.
    elif len(temp) <= 2:
        return 0.2, temp
    # sometime it may recognize more digits by mistake
    elif len(temp) >= 5:
        # first situation: ‘:’ is wrongly recognized as 8. It happens on these samples once.
        if temp[2] == '8' and 0 <= int(temp[-2:]) <= 60 and 0 <= int(temp[:2]) <= 24:
            time = temp[:2] + temp[-2:]
            return 0.9, time
        # other situation: wrongly recognize.
        # very hard to correct if this happens. Change to another API might be a good method.
        else:
            return 0.2, temp


def change_format(list):
    li = ""
    for i in list:
        li = li + " " + i
    return li


# Mistakes exist on all kinds of APIs. This method is to correct the recognition errors on time,
# at the same time do the comparison of different methods. A utility score is used to measure the
# probability.  P = confidence_get_from_APIs * probability_situation_happens
def time_correct(confidence, time):
    prob, result = utility_and_correct(time)
    P = prob * confidence
    #print(P, result)

    return P, result


# Here to choose one result, at the same time, choose if to use the AWS api.
# Rule 1
def choose_a_result(con_G, result_G, con_M, result_M, result_I, file, time, word):
    # first rule: if the prediction results have two or more same results, choose the result as the final.
    result_G_1 = change_format(result_G)
    result_M_1 = change_format(result_M)
    result_I_1 = change_format(result_I)
    """
    list = [result_G_1, result_M_1, result_I_1]
    result = check_same_result(list)
    if len(result) > 0:
        return result[0]
    # No same results
    else:
        # use AWS API for another test
        con_A, result_A = AWSAPI.handwritten_AWS_onecell(file)
        con_A = con_A/100
        result_A_1 = change_format(result_A)
        if time:
            con_G, result_G_1 = time_correct(con_G, result_G_1)
            con_M, result_M_1 = time_correct(con_M, result_M_1)
            con_I, result_I_1 = time_correct(0, result_I_1)
            con_A, result_A_1 = time_correct(con_A, result_A_1)
        if word:
            result_G_1 = check_words(result_G)
            result_M_1 = check_words(result_M)
            result_I_1 = check_words(result_I)
            result_A_1 = check_words(result_A)
        # have a result same with result of AWS
        list = [result_G_1, result_M_1, result_I_1,result_A_1]
        result = check_same_result(list)
        if len(result) > 0:
            return result[0]
        # don't have same result, higher confidence, more accurate result
        else:
            dict_ = {result_G_1:con_G,result_M_1:con_M,result_I_1:0.3,result_A_1:con_A}
            max_key = max(dict_, key=dict_.get)
            return max_key
    """
    if time:
        con_G, result_G_1 = time_correct(con_G, result_G_1)
        con_M, result_M_1 = time_correct(con_M, result_M_1)
        con_I, result_I_1 = time_correct(0, result_I_1)
        list = [result_G_1, result_M_1, result_I_1]
        result = check_same_result(list)
        if len(result) > 0:
            return result[0]
        else:
            con_A, result_A = AWSAPI.handwritten_AWS_onecell(file)
            con_A = con_A / 100
            result_A_1 = change_format(result_A)
            con_A, result_A_1 = time_correct(con_A, result_A_1)
            list = [result_G_1, result_M_1, result_I_1, result_A_1]
            result = check_same_result(list)
            if len(result) > 0:
                return result[0]
            # don't have same result, higher confidence, more accurate result
            else:
                dict_ = {result_G_1: con_G, result_M_1: con_M, result_I_1: 0.3, result_A_1: con_A}
                max_key = max(dict_, key=dict_.get)
                return max_key
    elif word:
        result_G_1 = check_words(result_G)
        result_M_1 = check_words(result_M)
        result_I_1 = check_words(result_I)
        print(result_G_1,result_M_1,result_I_1)
        list = [result_G_1, result_M_1, result_I_1]
        for i in list:
            i=i.strip()
            if in_words(i):
                return i
        else:
            con_A, result_A = AWSAPI.handwritten_AWS_onecell(file)
            con_A = con_A / 100
            result_A_1 = check_words(result_A)
            list = [result_G_1, result_M_1, result_I_1, result_A_1]
            for i in list:
                if in_words(i):
                    return i
            result = check_same_result(list)
            if len(result) > 0:
                return result[0]
            # don't have same result, higher confidence, more accurate result
            else:
                dict_ = {result_G_1: con_G, result_M_1: con_M, result_I_1: 0.3, result_A_1: con_A}
                max_key = max(dict_, key=dict_.get)
                return max_key
    else:
        result_G_1 = change_format(result_G)
        result_M_1 = change_format(result_M)
        result_I_1 = change_format(result_I)
        list = [result_G_1, result_M_1, result_I_1]
        result = check_same_result(list)
        if len(result) > 0:
            return result[0]
        else:
            con_A, result_A = AWSAPI.handwritten_AWS_onecell(file)
            con_A = con_A / 100
            result_A_1 = change_format(result_A)
            list = [result_G_1, result_M_1, result_I_1, result_A_1]
            result = check_same_result(list)
            if len(result) > 0:
                return result[0]
            # don't have same result, higher confidence, more accurate result
            else:
                dict_ = {result_G_1: con_G, result_M_1: con_M, result_I_1: 0.3, result_A_1: con_A}
                max_key = max(dict_, key=dict_.get)
                return max_key

# check if there are same results
def check_same_result(list):
    from collections import Counter
    b = dict(Counter(list))
    result = ([key for key, value in b.items() if value > 1])
    return result

# check if the word is in the high frequency dictionary
def in_words(word):
    spell = SpellChecker(language=None, case_sensitive=True)
    text = " "
    spell.distance = 1
    spell.word_frequency.load_dictionary("./dictionary.json")
    print(spell[word])
    if spell[word] > 0:
        return True
# spell checker
def check_words(words):
    spell = SpellChecker(language=None, case_sensitive=True)
    text = " "
    spell.distance = 1
    spell.word_frequency.load_dictionary("./dictionary.json")

    for word in words:
        new_word = ""
        for chara in word:
            if 'A'<=chara<='Z':
                chara = chara.lower()
                new_word = new_word+chara
            else:
                new_word = new_word+chara
        misspelled = spell.unknown(new_word)
        if len(misspelled) == 0:
            text = text + " " + word
        else:
            # Get the one `most likely` answer
            if text is not None and spell.correction(new_word):
                text = text + " " + spell.correction(new_word)
    return text
#print(check_words(["chople"]))
"""
time_correct(98, "23/5")
time_correct(98, "200")
time_correct(98, "00:30")
time_correct(98, "12805")
time_correct(98, "3230")

print(check_words(["chages", "it"]))
list = ["1", "2"]
check_same_result(["cnm", "nmsl", "cnm1"])

dict_ = {"result_G": 0.4, "result_M": 0.5, "result_I": 0}
if "result_I" in dict_:
    print("yes")
else:
    dict_["result_A"] = 0.5
    print(dict_)
"""

