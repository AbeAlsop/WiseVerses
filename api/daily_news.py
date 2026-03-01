import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
load_dotenv()

#Documentation: https://newsdata.io/documentation#latest-news
#Categories:
# breaking
# business
# crime
# domestic
# education
# entertainment
# environment
# food
# health
# lifestyle
# politics
# science
# sports
# technology
# top
# tourism
# world
# other

def get_news(query):
    api = NewsDataApiClient(apikey=os.getenv("NEWSDATA_API_KEY"))
    response = api.latest_api(country='US',
                              language='en',
                              size=10,
                              #timezone='America/Denver',
                              q=' OR '.join(query.split()),
                              category='crime,domestic,science,technology,world',
                              sort='relevancy',
                              removeduplicate=True)
    return response['results']

if __name__ == "__main__":
    news = get_news('Boise Idaho')
    print([article['title'] for article in news])