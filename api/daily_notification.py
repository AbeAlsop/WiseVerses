import datetime

from daily_readings import get_readings
from daily_weather import get_weather
from daily_news import get_news
from daily_feast import get_celebrations
from openAI import get_response

day = datetime.date.today()
#day = datetime.date(2026, 3, 3)
date_context = day.strftime("%A, %B %d")

location = "Boise Idaho"

name = "Abraham Alsop"

weather = get_weather(location, day)

news = get_news(location)
news_headlines = f"Latest news headlines: {". ".join([article['title'] for article in news])}"

personal = 'Catholic man, 49 years old, Married with four adult children and one teenage daughter, software engineering manager at Clearwater Analytics, taking graduate class Anthropology for Technologists at Catholic International University'
personal_context = f"Reader's name: {name}. Personal attributes: {personal}. Located in {location}"

context = [weather, personal_context, news_headlines]
print(context)

readings = get_readings(day)
celebrations = get_celebrations(day)
url = readings['url']
reading_context = ". ".join([f"The {key} is: {value}" for key, value in readings['readings'].items()]) + ". Today's feast days: " + "; ".join(celebrations)

system_message = """
    You are a marketer who knows how to catch people's attention, and your job is to make today's Mass readings relevant to a very targeted audience.
    Your assistant gave you the context information about the reader you're trying to attract and what's going on in his or her world.
    When prompted with today's readings and feast days, pick one aspect of one reading or feast that is most relevant to the reader, then mention it by name
    and show how it relates to one aspect of the reader, or the day of the week, the weather or time of year, or one news headline that was provided.
    Finish the sentence in a way that piques the target reader's interest in that reading or feast without giving away the content.
    For example, if the first reading is about rain and it's a rainy day, you can say "The first reading is appropriate for today's weather."
    If the Gospel is about peace and there is war starting in the Middle East, then say "Today's Gospel message is greatly needed in our world."
    If it is St. Joseph's feast day and the reader is a manual laborer, then say "Today's Saint is a good example for you in your work." 
    The entire content of your response must be small enough to fit into a mobile notification, so limit yourself to one sentence.
"""

notification = get_response(system_message, context, reading_context)
print(notification)
