from quoteDB import QuoteDB
from openAI import get_virtue, apply_quote
import logging

class Chatter:
    context = {}

    def __init__(self):
        self.quote_db = QuoteDB()

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

    # TODO: Detect when the input is too short to be a coherent thought, and respond with something like "Tell me more"
    def respond_with_context(self, user_input, session):
        user_context = self.context[session] if session in self.context else []

        prompt = self.assemble_prompt(user_input, user_context)
        pop_quote_data = self.quote_db.lookup_quote(prompt, session, "pop")
        pop_formatted_quote = self.format_quote(pop_quote_data)

        faith_quote_data = self.quote_db.lookup_quote(prompt, session, "faith")
        faith_formatted_quote = self.format_quote(faith_quote_data)

        explanation = apply_quote(user_input, [pop_formatted_quote, faith_formatted_quote], user_context)
        self.context[session] = [*user_context, [user_input, f"{pop_formatted_quote} {faith_formatted_quote} {explanation}"]]
        return {"Quotes": [pop_quote_data, faith_quote_data], "FormattedQuote": pop_formatted_quote, "FormattedQuote2": faith_formatted_quote, "Explanation": explanation}

    def find_song(self, user_input):
        song_data = self.quote_db.lookup_quote_in_genre(user_input, "Song")
        return song_data