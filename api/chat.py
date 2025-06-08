from quoteDB import QuoteDB
from openAI import get_virtue, apply_quote
import logging

class Chatter:
    context = {}

    def __init__(self):
        self.quote_db = QuoteDB()

    def assemble_prompt(self, user_input, session=None):
        user_context = self.context[session] if session and session in self.context else []
        virtue = get_virtue(user_input, user_context)
        logging.info(f"Associated virtue {virtue} with {user_input}")
        query = user_input
        if user_input[-1] != '.':
            query += '.'
        query += f"Seeking {virtue.replace(',' , ' or ')}."
        return query

    def format_quote(self, quote_data):
        author = quote_data['Author']
        genre = quote_data['Genre']
        source = quote_data['Source']
        quote = quote_data['Quote']
        formatted_quote = f"{author} {"sang" if genre == "Song" else "said"} \"{quote}\""
        if source and source[:4] != 'http' and source[:6] != 'Lesson':
            formatted_quote += f" ({source})"
        return formatted_quote

    def assemble_response(self, user_input, quote_data):
        formatted_quote = self.format_quote(quote_data)
        explanation = apply_quote(user_input, formatted_quote)
        return f"{formatted_quote} {explanation}"

    def respond(self, user_input):
        prompt = self.assemble_prompt(user_input)
        db_response = self.quote_db.lookup_quote(prompt)['matches'][0]
        quote_data = db_response['metadata']
        return self.assemble_response(user_input, quote_data)

    def respond_with_context(self, user_input, session):
        prompt = self.assemble_prompt(user_input, session)
        db_response = self.quote_db.lookup_quote(prompt)['matches'][0]
        quote_data = db_response['metadata']
        formatted_quote = self.format_quote(quote_data)
        user_context = self.context[session] if session in self.context else []
        explanation = apply_quote(user_input, formatted_quote, user_context)
        new_history = [user_input, f"{formatted_quote} {explanation}"]
        self.context[session] = [*user_context, new_history]
        return {**quote_data, "FormattedQuote": formatted_quote, "Explanation": explanation}
