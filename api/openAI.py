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

#TODO: Detect when the input is too short to be a coherent thought, and respond with something like "Tell me more"
def get_virtue(text):
    response = open_ai_client.chat.completions.create(
        model=LANG_MODEL,
        messages=[
            {'role': 'system', 'content': '''
                You are a counselor who helps people improve.
                Select one of the following virtues or attributes that are most needed or desired by the user, and respond with nothing but the name of the selected virtue.
                Body of Christ,Providence,Grace,Faith,Fidelity,Hope,Trust,Longing for God,Devotion,Scripture,Purity,Virtue,Acceptance,Contentment,Patience,Flexibility,Agility,Self-control,Detachment,Gratitude,Potential,Vision,Initiative,Planning,Preparation,Creativity,Resilience,Perseverance,Recovery,Innovation,Renewal,Inspiration,Ambition,Motivation,Opportunity,Direction,Fortitude,Growth,Learning,Education,Practice,Journey,Confidence,Eagerness,Courage,Dedication,Responsibility,Effort,Action,Accountability,Speed,Determination,Persistence,Diligence,Excellence,Accomplishment,Completion,Truth,Honesty,Wisdom,Focus,Awareness,Realism,Intelligence,Pondering,Vigilance,Discernment,Writing,Intuition,Imagination,Dignity,Mission,Priorities,Vocation,Adventure,Leisure,Rest,Nature,Health,Integrity,Humility,Self-awareness,Self-respect,Uniqueness,Originality,Caution,Mindfulness,Perspective,Attitude,Optimism,Happiness,Joy,Peace,Silence,Surprise,Wonder,Passion,Compassion,Relationship,Friendship,Love,Family,Parenting,Encouragement,Listening,Gentleness,Discretion,Respect,Commitment,Community,Communion of Saints,Justice,Kindness,Leadership,Forgiveness,Equality,Charity,Generosity,Simplicity,Teaching,Surrender,Sacrifice,Martyrdom
            '''},
            {'role': 'user', 'content': text}
        ],
        max_completion_tokens=20
    )
    return response.choices[0].message.content


#TODO: use context of prior conversation as part of input
def apply_quote(text, assistant):
    response = open_ai_client.chat.completions.create(
        model=LANG_MODEL,
        messages=[
            {'role': 'system', 'content': '''
                You are a librarian who is connecting people to the works of famous authors and artists.
                Your assistant has provided the quote that is most relevant to the user.
                Give a brief explanation, no more than one sentence, of how that message applies to the user's situation.
            '''},
            {'role': 'user', 'content': text},
            {'role': 'assistant', 'content': assistant}
        ],
        max_completion_tokens = 250
    )
    return response.choices[0].message.content
