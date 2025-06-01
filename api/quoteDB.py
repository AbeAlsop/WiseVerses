import os
import time
import numpy
import csv

from pinecone import Pinecone
from pinecone import ServerlessSpec
from tqdm.auto import tqdm
from openAI import embed
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = "us-east-1"
INDEX_NAME = "wise-quotes-2"

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_spec = ServerlessSpec(cloud="aws", region=AWS_REGION)

class QuoteDB:
    def __init__(self):
        self.index = pinecone_client.Index(INDEX_NAME)

    def load_quotes(self):
        with open('C:/dev/wiseverses/quotes.csv', 'r') as file:
            quote_file = csv.reader(file)
            header = next(quote_file)
            quotes = []
            for row in quote_file:
                quote = {}
                for i in range(0, len(header)):
                    quote[header[i]] = row[i]
                quotes.append(quote)
            print(f"Loaded {len(quotes)} rows")
            return quotes

    def save_quotes_csv(self, data):
        numpy.savetxt("C:/dev/wiseverses/quotes.csv", [[d['author'],d.get('source',''),d['text']] for d in data], delimiter="|", fmt="%s")

    def create_index(self, quotes):
        embed_dim = 1536

        if INDEX_NAME not in pinecone_client.list_indexes().names():
            pinecone_client.create_index(
                INDEX_NAME,
                dimension=embed_dim,
                metric='dotproduct',
                spec=pinecone_spec
            )

        index = pinecone_client.Index(INDEX_NAME)
        time.sleep(1)
        #print("Index stats:", index.describe_index_stats())

        batch_size = 32
        for i in tqdm(range(0, len(quotes), batch_size)):
            end = min(len(quotes), i + batch_size)
            quote_batch = quotes[i:end]
            ids = [str(n) for n in range(i,end)]
            embed_result = embed(
                [f"About {q['Virtue']}: {q['Quote']}" for q in quote_batch]
            )
            embeds = [record.embedding for record in embed_result]
            vectors = list(zip(ids, embeds, quote_batch))
            index.upsert(vectors)

        print(f"Created index of {len(quotes)} quotes")
        return index

    def rebuild_db(self):
        quote_data = self.load_quotes()
        # self.save_quotes_csv(quote_data)
        self.create_index(quote_data)

    #TODO: Avoid repeats within the same conversation
    def lookup_quote(self, prompt):
        embedding = embed([prompt])[0].embedding
        result = self.index.query(vector=[embedding], top_k=1, include_metadata=True)
        return result
