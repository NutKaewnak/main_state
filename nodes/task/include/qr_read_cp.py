__author__ = 'cindy'


def answers(question):
    print question
    print type(question)
    if 'Lay\'s original' in question:
        return 'LayRock.wav'
    elif 'yumyum tom yum kung' in question:
        return 'yumyum.wav'
    elif 'lay stack' in question:
        return 'LayStackOriginal.wav'
    elif 'roller coaster' in question:
        return 'RollerCoaster.wav'
    elif 'lay ta wan karm puu' in question:
        return 'Tawan.wav'
    elif 'qlico pocky cookie and cream' in question:
        return 'Guligo.wav'
    elif 'calbee jaxx with ketchup ' in question:
        return 'CalBee.wav'
    elif '7 select corn snack' in question:
        return '7SelectCorn.wav'
    elif 'lactasoy soy milk' in question:
        return 'Lactasoy.wav'
    elif 'knorr cup jok shrimp and crab stick' in question:
        return 'KanorJoke.wav'