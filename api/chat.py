from quoteDB import QuoteDB
from openAI import get_virtue, apply_quote

class Chatter:
    def __init__(self):
        self.quote_db = QuoteDB()

    def assemble_prompt(self, user_input):
        virtue = get_virtue(user_input)
        #print(virtue)
        query = user_input
        if user_input[-1] != '.':
            query += '.'
        query += f"Seeking {virtue.replace(',' , ' or ')}."
        return query

    def assemble_response(self, user_input, quote_data):
        author = quote_data['Author']
        genre = quote_data['Genre']
        source = quote_data['Source']
        quote = quote_data['Quote']
        formatted_quote = f"{author} {"sang" if genre == "Song" else "said"} \"{quote}\""
        if source and source[:4] != 'http' and author != 'Abraham Alsop':
            formatted_quote += f" ({source})"
        explanation = apply_quote(user_input, formatted_quote)
        return f"{formatted_quote} {explanation}"

    def respond(self, user_input):
        prompt = self.assemble_prompt(user_input)
        db_response = self.quote_db.lookup_quote(prompt)['matches'][0]
        quote_data = db_response['metadata']
        return self.assemble_response(user_input, quote_data)
