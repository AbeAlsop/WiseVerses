from quoteDB import QuoteDB
from openAI import get_virtue, apply_quote
import logging
import cachetools

class History:
    quote_ids: list = []
    messages: list = []

class Chatter:
    def __init__(self):
        self.quote_db = QuoteDB()
        #Support 100 concurrent sessions up to 1 day
        self.context = cachetools.TTLCache(maxsize=100, ttl=60 * 60 * 24)

    def append_virtue(self, user_input, virtue):
        query = user_input
        if user_input[-1] != '.':
            query += '.'
        query += f" Seeking {virtue.replace(',' , ' or ')}."
        return query

    def assemble_prompt(self, user_input, user_context):
        virtue = get_virtue(user_input, user_context)
        logging.info(f"Associated virtue {virtue} with {user_input}")
        return self.append_virtue(user_input, virtue)

    def format_quote(self, quote_data):
        author = quote_data['Author']
        genre = quote_data['Genre']
        source = quote_data['Source']
        quote = quote_data['Quote']
        formatted_quote = f"{author} {"sang" if genre == "Song" else "said"} \"{quote}\""
        if source and source[:4] != 'http' and source[:6] != 'Lesson':
            formatted_quote += f" ({source})"
        return formatted_quote

    def respond_with_context(self, user_input, session):
        user_context = self.context.setdefault(session,History())

        prompt = self.assemble_prompt(user_input, user_context.messages)
        pop_quote_data = self.quote_db.lookup_quote_data(prompt, "pop", user_context.quote_ids)
        pop_formatted_quote = self.format_quote(pop_quote_data)

        faith_quote_data = self.quote_db.lookup_quote_data(prompt, "faith", user_context.quote_ids)
        faith_formatted_quote = self.format_quote(faith_quote_data)

        explanation = apply_quote(user_input, [pop_formatted_quote, faith_formatted_quote], user_context.messages)

        user_context.quote_ids.append(pop_quote_data["ID"])
        user_context.quote_ids.append(faith_quote_data["ID"])
        user_context.messages.append([user_input, f"{pop_formatted_quote} {faith_formatted_quote} {explanation}"])

        return {"Quotes": [pop_quote_data, faith_quote_data], "FormattedQuote": pop_formatted_quote, "FormattedQuote2": faith_formatted_quote, "Explanation": explanation}

    def find_song(self, user_input):
        song_data = self.quote_db.lookup_quote_in_genre(user_input, "Song")
        return song_data