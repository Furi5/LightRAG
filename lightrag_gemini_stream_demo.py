import os
import inspect
from lightrag import LightRAG
from lightrag.llm import gemini_complete, gemini_embed
from lightrag.utils import EmbeddingFunc
from lightrag.lightrag import always_get_an_event_loop
from lightrag import QueryParam

# WorkingDir
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = '/home/jovyan/my_code/RAG/output_gemini_2'

api_key = "AIzaSyDVhEJMmWWJCGzrDQWoE0ffYROeRQ4jcp0"
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gemini_complete,
    llm_model_name="gemini-2.0-flash",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs= {"api_key": api_key},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: gemini_embed(
            texts=texts,
            model="models/text-embedding-004",
            api_key=api_key,
        ),
    ),
)

for ff in os.listdir("/home/jovyan/my_code/RAG/Data/pubtabor_output/AD_experiment"):
    with open(f"/home/jovyan/my_code/RAG/Data/pubtabor_output/AD_experiment/{ff}", "r", encoding="utf-8") as f:
        rag.insert(f.read())

resp = rag.query(
    "What are the AD?",
    param=QueryParam(mode="hybrid", stream=True),
)


async def print_stream(stream):
    async for chunk in stream:
        if chunk:
            print(chunk, end="", flush=True)


loop = always_get_an_event_loop()
if inspect.isasyncgen(resp):
    loop.run_until_complete(print_stream(resp))
else:
    print(resp)
