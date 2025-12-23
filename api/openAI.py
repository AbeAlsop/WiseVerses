import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-small"
LANG_MODEL = "gpt-4.1"

#embed one item or a list of items
def embed(text):
    result = open_ai_client.embeddings.create(input=text, model=EMBED_MODEL)
    return result.data

#TODO: Find closest match from my descriptions of virtues, rather than asking OpenAI
def get_virtue(text, context = []):
    messages = [
        {'role': 'system', 'content': '''
        You are a counselor who helps people be more aware of the spiritual side of life and to be ready for their next calling. 
        Select a virtue from the list below that is most relevant to the user, and respond with nothing but the name of the selected word.
        For example, if someone is going on a vacation, then this is related to "Journey". If the user is calling himself stupid, this is related to "Self-respect". Questions about marriage are related to "Love". 
        Preparation,Body of Christ,Providence,Grace,Faith,Fidelity,Hope,Trust,Longing for God,Devotion,Scripture,Purity,Virtue,Prayer,Acceptance,Contentment,Patience,Flexibility,Agility,Self-control,Detachment,Gratitude,Potential,Vision,Initiative,Planning,Creativity,Resilience,Perseverance,Recovery,Renewal,Resurrection,Inspiration,Ambition,Motivation,Opportunity,Direction,Growth,Learning,Education,Practice,Confidence,Eagerness,Courage,Dedication,Responsibility,Effort,Action,Accountability,Speed,Determination,Persistence,Diligence,Excellence,Accomplishment,Completion,Truth,Honesty,Wisdom,Focus,Awareness,Realism,Intelligence,Pondering,Discernment,Writing,Intuition,Imagination,Dignity,Priorities,Vocation,Leisure,Rest,Nature,Health,Journey,Integrity,Humility,Self-awareness,Self-respect,Uniqueness,Caution,Mindfulness,Perspective,Attitude,Optimism,Joy,Peace,Silence,Surprise,Wonder,Passion,Compassion,Relationship,Friendship,Love,Family,Parenting,Listening,Gentleness,Discretion,Respect,Commitment,Community,Communion of Saints,Justice,Kindness,Leadership,Forgiveness,Equality,Charity,Generosity,Simplicity,Teaching,Surrender,Sacrifice,Martyrdom,Incarnation
        '''}
    ] #turn away from obsession with material things, and work to fulfill their spiritual calling.
    for history in context:
        messages.append({'role': 'user', 'content': history[0]})
        messages.append({'role': 'assistant', 'content': history[1]})
    messages.append({'role': 'user', 'content': text})
    response = open_ai_client.chat.completions.create(
        model=LANG_MODEL,
        messages=messages,
        max_completion_tokens=50
    )
    return response.choices[0].message.content


# Context is a list of pairs
#   The first element of each pair is the user request; the second is the response
def apply_quote(text, verses, context = []):
    messages = [
        {'role': 'system', 'content': '''
            You are a librarian who is connecting people to the works of famous authors and artists.
            The assistant has provided one or two relevant verses. Do not repeat them or provide a new quote.
            Simply give a brief explanation, no more than one sentence, of how the verses or quotes provided by the assistant are applicable to the user's situation.
            Your sentence should be relevant to both the user's prompt and the assistant's verses.
        '''}
    ]
    for history in context:
        messages.append({'role': 'user', 'content': history[0]})
        messages.append({'role': 'assistant', 'content': history[1]})
    messages.append({'role': 'user', 'content': text})
    for verse in verses:
        messages.append({'role': 'assistant', 'content': verse})

    response = open_ai_client.chat.completions.create(
        model=LANG_MODEL,
        messages=messages,
        max_completion_tokens = 500
    )
    return response.choices[0].message.content
