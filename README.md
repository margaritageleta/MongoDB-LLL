# LLM-embedding-based search within log files

## Brief Overview
- Software systems generate massive observability data (logs, traces, events, metrics).
- Existing solutions often involve restrictive querying languages (e.g., Datadog, Prometheus, Splunk).
- Introduction of 3L as a prototype semantic search and analytics engine.

## Implementation Details
### Backend
- MongoDB for vector database and vector search.
- Together.AI for embeddings (m2-bert-80M-32k-retrieval).
### Frontend
- ReactJS.
### Data
- [LogHub](https://github.com/logpai/loghub).

## Usage
### Virtual environment setup

**1. Create a virtual environment on your local repository**

Create venv:

```
$ python3 -m venv env
```

**2. Activate it to install packages and to execute scripts (ALWAYS!) & install the requirements**

```
$ source ./env/bin/activate
$ (env) pip install -r requirements.txt
```

**3. Use this command to start the webserver**
```
uvicorn runner:app --reload
```

**4. Commands for the frontend setup**
```
cd frontend/logfinder
npm install
npm run build
npm run start
```
