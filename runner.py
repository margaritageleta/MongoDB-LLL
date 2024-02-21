import openai
from openai import OpenAI
import json
import time
import pymongo
from config import get_keys
from pymongo.server_api import ServerApi
from fastapi.middleware.cors import CORSMiddleware


print(pymongo.__version__)

keychain = get_keys('./config.yml')

print('pretty-print keys')
print(json.dumps(keychain,sort_keys=True, indent=4))
print('\n')

print(f"Connection to: {keychain['MONGODB_ATLAS_CLUSTER_URI']+'/?retryWrites=true&w=majority'}")
try:
    client = pymongo.MongoClient(keychain['MONGODB_ATLAS_CLUSTER_URI']+'/?retryWrites=true&w=majority', server_api=ServerApi('1'))
    try:
        client.server_info()
        print("Connection Established!")
    except pymongo.errors.OperationFailure as err:
        print(err)
except Exception as err:
    print(err)

db = client.sample_mflix
collection = db.movies

openai.api_key = keychain['OPENAI_API_KEY']
openai_client = OpenAI(api_key=keychain['TOGETHER_API_KEY'], base_url="https://api.together.xyz/v1")


model = "text-embedding-3-small"
def generate_embedding(text):
    text = text.replace("\n", " ")
    model="togethercomputer/m2-bert-80M-32k-retrieval"
    return openai_client.embeddings.create(input = [text], model=model).data[0].embedding # 768 dim
    # return openai.embeddings.create(input = [text], model=model).data[0].embedding # 1536 dim

DB_NAME = 'logdb'
COLLECTION_NAME = 'OpenSSH2'
INDEX_NAME = 'vector_index'

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

doc_count = collection.count_documents(filter={})
print(doc_count)

## Insert log file into database:
def populate_db(raw_data, collection):
    with open(raw_data, "r") as f: #276
        for i, line in enumerate(f):
            embedding = generate_embedding(line)
            if i == 0: print(len(embedding))
            x = collection.insert_one({'logline': line, 'embedding': embedding})
            print(i, x.inserted_id)

    doc_count = collection.count_documents(filter={})
    print(doc_count)

# Handy function
from fastapi import FastAPI
from bson import json_util
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import time

## TODO: Hookup frontend to use the upload pdf functionality
# def pdf_to_string(pdf_file):
#     elements = partition("example-docs/layout-parser-paper.pdf")
#     return elements

# @app.post("/uploadpdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     if not file.filename.lower().endswith('.pdf'):
#         raise HTTPException(status_code=400, detail="Only PDF files are allowed")

#     try:
#         pdf_text = pdf_to_string(file.file)
#         return {"pdf_text": pdf_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
@app.get("/vector_search")
async def do_vector_search(query: str):
    print(query)
    t1a = time.perf_counter()
    embedding = generate_embedding(query)
    # print("embedding value: ", embedding)
    t1b = time.perf_counter()
    print (f"Getting embeddings from OpenAI took {(t1b-t1a)*1000:,.0f} ms")
    
    t2a = time.perf_counter()
    results = collection.aggregate(
        [
            {
                '$vectorSearch': {
                    'queryVector': embedding,
                    'path': 'embedding', 
                    'numCandidates': 100, 
                    'index': INDEX_NAME, 
                    'limit': 10
                }
            }
        ]
    )
    t2b = time.perf_counter()

    docs = []
    for doc in results:
        docs.append(doc)

    # print(f"Type of results: {type(results)}")
    print(f"Altas query returned {len(docs)} results in {(t2b-t2a)*1000:,.0f} ms")

    for idx, log in enumerate(docs):
        print(f'{log["_id"]}\text: {log["logline"]}')

    return json.loads(json.dumps(docs, default=json_util.default))

# print("Performing LLM search")
# query = "List all the IP addresses which is of format [w.x.y.z] trying to hack in? Give counts "
# # query = "List all the users which starts with the line 'Accepted password'."
# docs = do_vector_search(db, query)  # Await the coroutine
# print("docs found length: ", len(docs['docs']))
