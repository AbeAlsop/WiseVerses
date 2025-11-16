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
COMBINED_INDEX_NAME = "wise-quotes-3"
POP_INDEX_NAME = "wise-quotes-pop-3"
FAITH_INDEX_NAME = "wise-quotes-faith-3"
FAITH_GENRES = ["Saint","Bible","Christian","Song"]
MIN_ID_TO_LOAD = 2165

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_spec = ServerlessSpec(cloud="aws", region=AWS_REGION)

class QuoteDB:
    def __init__(self):
        self.pop_index = self.get_or_create_index(POP_INDEX_NAME)
        self.faith_index = self.get_or_create_index(FAITH_INDEX_NAME)
        self.combined_index = self.get_or_create_index(COMBINED_INDEX_NAME)

    def load_quotes(self):
        with open(os.getenv("CSV_FILE_PATH"), 'r', encoding='utf-8') as file:
            quote_file = csv.reader(file)
            header = next(quote_file)
            quotes = []
            for row in quote_file:
                quote = {}
                for i in range(0, len(header)):
                    quote[header[i]] = row[i]
                if int(quote["ID"]) >= MIN_ID_TO_LOAD:
                    quotes.append(quote)
            print(f"Loaded {len(quotes)} rows")
            return quotes

    def save_quotes_csv(self, data):
        numpy.savetxt(os.getenv("CSV_FILE_PATH"), [[d['author'],d.get('source',''),d['text']] for d in data], delimiter="|", fmt="%s")

    def get_or_create_index(self, name):
        embed_dim = 1536
        if name not in pinecone_client.list_indexes().names():
            pinecone_client.create_index(
                name,
                dimension=embed_dim,
                metric='dotproduct',
                spec=pinecone_spec
            )
            time.sleep(1) # ensure index is created
        #print("Index stats:", index.describe_index_stats())
        return pinecone_client.Index(name)

    def add_quotes_to_indexes(self, quotes, indexes):
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
            for index in indexes:
                index.upsert(vectors)

    def load_db(self):
        quote_data = self.load_quotes()
        # self.save_quotes_csv(quote_data)
        self.add_quotes_to_indexes(
            [quote for quote in quote_data if quote["Genre"] not in FAITH_GENRES],
            [self.combined_index,self.pop_index]
        )
        self.add_quotes_to_indexes(
            [quote for quote in quote_data if quote["Genre"] in FAITH_GENRES],
            [self.combined_index,self.faith_index]
        )

    def find_match(self, prompt, index, avoid_ids=[]):
        embedding = embed([prompt])[0].embedding
        result = index.query(vector=[embedding], top_k=1, include_metadata=True, filter={"ID": {"$nin": avoid_ids}})
        return result['matches'][0]

    def lookup_quote_data(self, prompt, style="", avoid_ids=[]):
        selected_index = self.pop_index if style=="pop" else self.faith_index if style=="faith" else self.combined_index
        first_match = self.find_match(prompt, selected_index, avoid_ids)
        return first_match['metadata']

    def lookup_pop_quote(self, prompt):
        return self.find_match(prompt, self.pop_index)

    def lookup_faith_quote(self, prompt):
        return self.find_match(prompt, self.faith_index)

    def lookup_quote_in_genre(self, prompt, genre):
        embedding = embed([prompt])[0].embedding
        result = self.combined_index.query(vector=[embedding], top_k=1, include_metadata=True, filter={"Genre": {"$eq": genre}})
        return result['matches'][0]
