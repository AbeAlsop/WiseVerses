import datetime

from daily_readings import get_readings
from daily_weather import get_weather
from daily_news import get_news
from openAI import get_response

day = datetime.date.today()
#day = datetime.date(2026, 2, 24)
date_context = day.strftime("%A, %B %d")

location = "Boise Idaho"

name = "Abraham Alsop"

#weather = get_weather(location, day)
weather = "On Tuesday, February 24, 2026 in Boise, Idaho, the weather was rainy with a high of 53 degrees Fahrenheit and a low of 41"

news = get_news(location)
news_headlines = f"Latest news headlines: {". ".join([article['title'] for article in news])}"

personal = 'Catholic man, 49 years old, Married with five adult children, software engineering manager at Clearwater Analytics, taking graduate class Anthropology for Technologists at Catholic International University'
personal_context = f"Reader's name: {name}. Personal attributes: {personal}. Located in {location}"

context = [weather, personal_context, news_headlines]
print(context)

readings = get_readings(day)
url = readings['url']
reading_map = {r['header']: r['readings'][0]['text'] for r in readings['sections']}
reading_context = ". ".join([f"The {key} is: {value}" for key, value in reading_map.items()])

system_message = "You are a marketer who knows how to catch people's attention, and your job is to make today's Mass readings relevant to a very targeted audience. Your assistant gave you the context information about the reader you're trying to attract and what's going on in his or her world. When prompted with today's readings, pick one aspect of the reader, or the day of the week, the season, or the news or weather that is provided, and relate it to one aspect of the daily readings. Use that to respond with one short sentence that piques the target reader's interest by showing how the readings are relevant."

notification = get_response(system_message, context, reading_context)
print(notification)
