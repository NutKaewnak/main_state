from time import gmtime, strftime, localtime


def tell_team_name():
    return "The name of my team is Skuba."


def tell_my_name():
    return "My name is Lumyai. I am a member of skuba team. I come from Thailand."


def tell_the_time():
    return strftime("%H %M.", localtime())


def tell_you_are_from():
    return "I am come from Thailand."


def tell_the_weather_today():
    return "The weather today is clear with periodic clouds. The highest temperature is 13 degree Celsius. The lowest temperature is 4 degree Celsius"


def tell_the_date_today():
    return strftime("%A of %B, %Y.", localtime())


def tell_day_today():
    return strftime("Today is %A.", localtime())

def tell_day_tomorrow():
    return strftime("Today is %A.", localtime(60*60*24))


def tell_where_are_we():
    return "We are at Aichi Institute of Technology."


def tell_affiliation():
    return "I come from Kasetsart University."


def tell_the_day_of_the_month():
    return strftime("%d of %B.", localtime())

def tell_the_day_of_the_week():
    return strftime("Today is %A.", localtime())

if __name__ == "__main__":
    print tell_my_name()
    print tell_team_name()
    print tell_the_time()
    print tell_the_date_today()
    print tell_day_today()
    print tell_the_weather_today()
    print tell_where_are_we()
    print tell_affiliation()
    print tell_day_tomorrow()
    print tell_the_day_of_the_month()
    print tell_the_day_of_the_week()