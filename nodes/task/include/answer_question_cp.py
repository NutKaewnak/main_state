__author__ = 'cindy'


def answers(question):
    print question
    print type(question)
    if "do you have dreams" in question:
        return "01_wannabe.wav"
    elif "do you know any robot" in question:
        return "02_tonhom.wav"
    elif "february has 28 days true or false" in question:
        return "03_CorrectFebruary.wav"
    elif "what is your name" in question:
        return "04_MyNameIsLumyai.wav"
    elif "how many arms do you have" in question:
        return "05_IHave2HandsAndUseWheel.wav"
    elif "how many people live in thailand" in question:
        return "06_people.wav"
    elif "name one of the county use mandarin language" in question:
        return "07_china.wav"
    elif "january has 28 days true or false" in question:
        return "08_Wrong.wav"
    elif "name one of the greatest thai artist" in question:
        return "10_artist.wav"
    elif "name the main river surrounding bangkok" in question:
        return "09_chaopraya.wav"
    elif "there are seven days in a week true or false" in question:
        return "11_Correct.wav"
    elif "what are the colours of thailand flag" in question:
        return "12_flag.wav"
    elif "what city is the capital of thailand" in question:
        return "13_bangkok.wav"
    elif "what did alan turing create" in question:
        return "14_computer.wav"
    elif "what is the heaviest element" in question:
        return "15_urenium.wav"
    elif "what is the name of the round robot in the new star wars movie" in question:
        return "16_bb8.wav"
    elif "what is today event" in question:
        return "17_openhouse.wav"
    # elif "robot sings a song" in question:
    #     return "18_LumyaiSong.wav"
    elif "what is the zoo name in this city" in question:
        return "19_dusitzoo.wav"
    elif "which company makes asimo" in question:
        return "20_honda.wav"
    elif "who developed you" in question:
        return "21_engineer.wav"
    elif "who is the dean of faculty of engineering" in question:
        return "22_dean.wav"
    elif "who was the first man to walk on the moon" in question:
        return "23_neil.wav"
