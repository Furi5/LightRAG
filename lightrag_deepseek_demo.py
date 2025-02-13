import asyncio
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc

WORKING_DIR = "/home/jovyan/my_code/RAG/output_deepseek_r1_7b-kg"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="deepseek-r1:7b",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}}, # Added host back
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embedding(
            texts,
            embed_model="nomic-embed-text",
            host="http://localhost:11434"  # added host parameter for embedding
        )
    ),
)


custom_kg = {
    "entities": [],
    'chunks': []
}

# i = 0
# for ff in os.listdir("/home/jovyan/my_code/RAG/Data_v2/AD_pubtabor"):
#     pmid = ff.split(".")[0]
#     if i > 10:
#         break
#     with open(f"/home/jovyan/my_code/RAG/Data_v2/AD_pubtabor/{ff}", "r", encoding="utf-8") as f:
#         i +=1
#         custom_kg['entities'].append({
#                     "entity_name": f"pmid:{pmid}",
#                     "entity_type": "publication",
#                     "description": f"pmid:{pmid}",
#                     "source_id": pmid
#                 })
        
#         text_line = f.readlines()
#         contents_line = text_line[:2]
#         entities_line = text_line[2:-1]
        
#         # process chunk
#         chunk_content = ""
#         chunk_content += f"Publication:pmid{pmid}"
#         chunk_content += f"Title:{contents_line[0].split('|')[-1]}"
#         chunk_content += f"Abstract:{contents_line[1].split('|')[-1]}"
#         custom_kg['chunks'].append({
#             "content": chunk_content,
#             "source_id": pmid
#         })
        
#         # if text_line[1].endswith("|"):
#         #     pass
#         # else:
#         #     i +=1
#         #     rag.insert(chunk_content)
        
#         # process entities
#         for entity_line in entities_line:
#             entity_line = entity_line.strip().split("\t")
#             if len(entity_line) == 6:
#                 custom_kg['entities'].append({
#                     "entity_name": entity_line[3],
#                     "entity_type": entity_line[4],
#                     "description": entity_line[5],
#                     "source_id": pmid
#                 })

# rag.insert_custom_kg(custom_kg)


i = 0
for ff in os.listdir("/home/jovyan/my_code/RAG/Data_v2/AD_pubtabor"):
    pmid = ff.split(".")[0]
    if i > 10:
        break
    with open(f"/home/jovyan/my_code/RAG/Data_v2/AD_pubtabor/{ff}", "r", encoding="utf-8") as f:
        text_line = f.readlines()
        contents_line = text_line[:2]
        entities_line = text_line[2:-1]
        chunk_content = ""
        chunk_content += f"Publication:pmid{pmid}\n"
        chunk_content += f"Title:{contents_line[0].split('|')[-1]}\n"
        chunk_content += f"Abstract:{contents_line[1].split('|')[-1]}"
        rag.insert(chunk_content)
        i+= 1



# Perform naive search
# print('====================naive search====================')
# print(
#     rag.query("What are the Alzheimer's disease biomarker?", param=QueryParam(mode="naive"))
# )

# # Perform local search
# print('====================local search====================')
# print(
#     rag.query("What are the Alzheimer's disease biomarker?", param=QueryParam(mode="local"))
# )

# # Perform global search
# print('====================global search====================')
# print(
#     rag.query("What are the Alzheimer's disease chemical?", param=QueryParam(mode="global"))
# )

# # Perform hybrid search
# print('====================hybrid search====================')
# print(
#     rag.query("What are the Alzheimer's disease biomarker?", param=QueryParam(mode="hybrid"))
# )

# print('====================stream search====================')
# # stream response
# resp = rag.query(
#     "What are the Alzheimer's disease biomarker?",
#     param=QueryParam(mode="hybrid", stream=True),
# )


# async def print_stream(stream):
#     async for chunk in stream:
#         print(chunk, end="", flush=True)


# if inspect.isasyncgen(resp):
#     asyncio.run(print_stream(resp))
# else:
#     print(resp)
