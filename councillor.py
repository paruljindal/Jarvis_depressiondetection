import textblob


def main():

    print "Welcome! I am your anonymous confidant. I will help you understand yourself. Take a few minutes to answer my questions."
    print "It would be easier to understand if you used proper language and grammar.\n"
    age = int(input("What is your age?"))

    print"Answer all questions with a 'Yes.' or 'No.' and ONLY THEN expand on why you fell that way.\n"
    print "1."
    #tiredness
    q1 = raw_input("Would you say that your last two weeks were more tiring than usual? Elaborate on your answer in about 40 words.\n")
    print "\n2."
    #nervousness
    q2 = raw_input("Would you say that during your last two weeks were more nervous than usual? Elaborate on your answer in about 40 words.\n")
    print "\n3."

    #restlessness
    q3 = raw_input("Would you say that during your last two weeks were more restless than usual? Elaborate on your answer in about 40 words.\n")
    print "\n4."
    #workHarderEasyTask
    q4 = raw_input("Would you say that during your last two weeks you had to try harder to accomplish tasks that you usually did not find that challenging? Elaborate on your answer in about 40 words.\n")
    print "\n5."
    #sadness
    q5 = raw_input("During your last two weeks, would you say that for most of the time you were so sad that you could not be cheered up? Elaborate on your answer in about 40 words.\n")
    print "\n6."
    #hopelessness
    q6 = raw_input("During your last two weeks, did you feel that everything was hopeless and that there was no reason to work for anything? Elaborate on your answer in about 40 words.\n")
    print "\n7."
    #worthlessness
    q7 = raw_input("Would you say that you feel that your worth as a person had diminished, that you feel you are have become less valueable to others and yourself? Elaborate on your answer in about 40 words.\n")



    def score(string):
        sc = 0
        string.replace(".", " ")
        ans = string.split(" ")[0]
        if ans.lower() == 'yes':
            sc += 2.5 + (((textblob.TextBlob(string).sentiment.polarity)/2 + 0.5)*2.5)

        elif ans.lower() == 'no':
            sc += (((textblob.TextBlob(string).sentiment.polarity)/2 + 0.5)*2.5)

        return sc

    totScore = score(q1) + score(q2) + score(q3) + score(q4) + score(q5) + score(q6) + score(q7)

    print "\nYour Score: ", totScore


    if totScore < 14:
       return "you are likely to be well"

    elif (totScore >= 14) and (totScore < 17):
        return "you are likely to have a mild depression"

    elif (totScore >= 17) and (totScore < 21):
        return "you are likely to have moderate depression"

    else:
        return "you are likely to have a severe depression"
        


