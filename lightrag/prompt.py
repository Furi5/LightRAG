GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["disease","gene","organism","omics type","method","region","cell type","group"]

PROMPTS["entity_extraction"] = """-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
"""Example 1:
Entity_types: ["disease","gene","organism","omics type","method","region","cell type","group"]
Text:
PMID: 19295912
Title: Transcriptome analysis of synaptoneurosomes identifies neuroplasticity genes overexpressed in incipient Alzheimer's disease
Abstract: In Alzheimer's disease (AD), early deficits in learning and memory are a consequence of synaptic modification induced by toxic beta-amyloid oligomers (oAbeta). To identify immediate molecular targets downstream of oAbeta binding, we prepared synaptoneurosomes from prefrontal cortex of control and incipient AD (IAD) patients, and isolated mRNAs for comparison of gene expression. This novel approach concentrates synaptic mRNA, thereby increasing the ratio of synaptic to somal mRNA and allowing discrimination of expression changes in synaptically localized genes. In IAD patients, global measures of cognition declined with increasing levels of dimeric Abeta (dAbeta). These patients also showed increased expression of neuroplasticity related genes, many encoding 3'UTR consensus sequences that regulate translation in the synapse. An increase in mRNA encoding the GluR2 subunit of the alpha-amino-3-hydroxy-5-methyl-4-isoxazole propionic acid receptor (AMPAR) was paralleled by elevated expression of the corresponding protein in IAD. These results imply a functional impact on synaptic transmission as GluR2, if inserted, maintains the receptors in a low conductance state. Some overexpressed genes may induce early deficits in cognition and others compensatory mechanisms, providing targets for intervention to moderate the response to dAbeta. 
################
Output:
("entity"{tuple_delimiter}"Alzheimer's disease"{tuple_delimiter}"disease"{tuple_delimiter}"Transcriptome analysis of synaptoneurosomes identifies neuroplasticity genes overexpressed in incipient Alzheimer's disease"){record_delimiter}
("entity"{tuple_delimiter}"GluR2"{tuple_delimiter}"gene"{tuple_delimiter}" These results imply a functional impact on synaptic transmission as GluR2, if inserted, maintains the receptors in a low conductance state."){record_delimiter}
("entity"{tuple_delimiter}"Human"{tuple_delimiter}"organism"{tuple_delimiter}"These patients also showed increased expression of neuroplasticity related genes, many encoding 3'UTR consensus sequences that regulate translation in the synapse."){record_delimiter}
("entity"{tuple_delimiter}"Transcriptome"{tuple_delimiter}"omics type"{tuple_delimiter}"Transcriptome analysis of synaptoneurosomes identifies neuroplasticity genes overexpressed in incipient Alzheimer's disease"){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"method"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"region"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"cell type"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"group"{tuple_delimiter}""){record_delimiter}
("relationship"{tuple_delimiter}"Alzheimer's disease"{tuple_delimiter}"GluR2"{tuple_delimiter}"These results imply a functional impact on synaptic transmission as GluR2, if inserted, maintains the receptors in a low conductance state."{tuple_delimiter}"These results"{tuple_delimiter}){record_delimiter}
("content_keywords"{tuple_delimiter}"Alzheimer's Disease, Transcriptome, gene expression"){completion_delimiter}
#############################""",
"""Example 2:
Entity_types: ["disease", "gene", "organism","omics type","method","region","cell type","group"]
Text:
PMID: 29523845
Title: Whole transcriptome profiling of Late-Onset Alzheimer's Disease patients provides insights into the molecular changes involved in the disease
Abstract:Alzheimer's Disease (AD) is the most common cause of dementia affecting the elderly population worldwide. We have performed a comprehensive transcriptome profiling of Late-Onset AD (LOAD) patients using second generation sequencing technologies, identifying 2,064 genes, 47 lncRNAs and 4 miRNAs whose expression is specifically deregulated in the hippocampal region of LOAD patients. Moreover, analyzing the hippocampal, temporal and frontal regions from the same LOAD patients, we identify specific sets of deregulated miRNAs for each region, and we confirm that the miR-132/212 cluster is deregulated in each of these regions in LOAD patients, consistent with these miRNAs playing a role in AD pathogenesis. Notably, a luciferase assay indicates that miR-184 is able to target the 3'UTR NR4A2 - which is known to be involved in cognitive functions and long-term memory and whose expression levels are inversely correlated with those of miR-184 in the hippocampus. Finally, RNA editing analysis reveals a general RNA editing decrease in LOAD hippocampus, with 14 recoding sites significantly and differentially edited in 11 genes. Our data underline specific transcriptional changes in LOAD brain and provide an important source of information for understanding the molecular changes characterizing LOAD progression. 
################
Output:
("entity"{tuple_delimiter}"Alzheimer's Disease"{tuple_delimiter}"disease"{tuple_delimiter}"Whole transcriptome profiling of Late-Onset Alzheimer's Disease patients provides insights into the molecular changes involved in the disease"){record_delimiter}
("entity"{tuple_delimiter}"NR4A2"{tuple_delimiter}"gene"{tuple_delimiter}"Moreover, analyzing the hippocampal, temporal and frontal regions from the same LOAD patients, we identify specific sets of deregulated miRNAs for each region, and we confirm that the miR-132/212 cluster is deregulated in each of these regions in LOAD patients, consistent with these miRNAs playing a role in AD pathogenesis.Notably, a luciferase assay indicates that miR-184 is able to target the 3'UTR NR4A2 - which is known to be involved in cognitive functions and long-term memory and whose expression levels are inversely correlated with those of miR-184 in the hippocampus."){record_delimiter}
("entity"{tuple_delimiter}"Human"{tuple_delimiter}"organism"{tuple_delimiter}"Whole transcriptome profiling of Late-Onset Alzheimer's Disease patients provides insights into the molecular changes involved in the disease"){record_delimiter}
("entity"{tuple_delimiter}"Transcriptome"{tuple_delimiter}"omics type"{tuple_delimiter}"Whole transcriptome profiling of Late-Onset Alzheimer's Disease patients provides insights into the molecular changes involved in the disease"){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"method"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"hippocampal"{tuple_delimiter}"region"{tuple_delimiter}"Moreover, analyzing the hippocampal, temporal and frontal regions from the same LOAD patients, we identify specific sets of deregulated miRNAs for each region, and we confirm that the miR-132/212 cluster is deregulated in each of these regions in LOAD patients, consistent with these miRNAs playing a role in AD pathogenesis.Notably, a luciferase assay indicates that miR-184 is able to target the 3'UTR NR4A2 - which is known to be involved in cognitive functions and long-term memory and whose expression levels are inversely correlated with those of miR-184 in the hippocampus."){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"cell type"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"group"{tuple_delimiter}""){record_delimiter}
("relationship"{tuple_delimiter}"Alzheimer's disease"{tuple_delimiter}"NR4A2"{tuple_delimiter}"Notably, a luciferase assay indicates that miR-184 is able to target the 3'UTR NR4A2 - which is known to be involved in cognitive functions and long-term memory and whose expression levels are inversely correlated with those of miR-184 in the hippocampus."{tuple_delimiter}"target to"{tuple_delimiter}){record_delimiter}
("content_keywords"{tuple_delimiter}"Alzheimer's Disease, Transcriptome, gene expression"){completion_delimiter}
#############################""",
"""Example 3:
Entity_types: ["disease","gene","organism","omics type","method","region","cell type","group"]
Text:
PMID: 31042697
Title: Single-cell transcriptomic analysis of Alzheimer's disease
Abstract: Alzheimer's disease is a pervasive neurodegenerative disorder, the molecular complexity of which remains poorly understood. Here, we analysed 80,660 single-nucleus transcriptomes from the prefrontal cortex of 48 individuals with varying degrees of Alzheimer's disease pathology. Across six major brain cell types, we identified transcriptionally distinct subpopulations, including those associated with pathology and characterized by regulators of myelination, inflammation, and neuron survival. The strongest disease-associated changes appeared early in pathological progression and were highly cell-type specific, whereas genes upregulated at late stages were common across cell types and primarily involved in the global stress response. Notably, we found that female cells were overrepresented in disease-associated subpopulations, and that transcriptional responses were substantially different between sexes in several cell types, including oligodendrocytes. Overall, myelination-related processes were recurrently perturbed in multiple cell types, suggesting that myelination has a key role in Alzheimer's disease pathophysiology. Our single-cell transcriptomic resource provides a blueprint for interrogating the molecular and cellular basis of Alzheimer's disease. 
################
Output:
("entity"{tuple_delimiter}"Alzheimer's Disease"{tuple_delimiter}"disease"{tuple_delimiter}"Single-cell transcriptomic analysis of Alzheimer's disease"){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"gene"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"organism"{tuple_delimiter}"Whole transcriptome profiling of Late-Onset Alzheimer's Disease patients provides insights into the molecular changes involved in the disease"){record_delimiter}
("entity"{tuple_delimiter}"Transcriptome"{tuple_delimiter}"omics type"{tuple_delimiter}"Single-cell transcriptomic analysis of Alzheimer's disease"){record_delimiter}
("entity"{tuple_delimiter}"Single-cell"{tuple_delimiter}"method"{tuple_delimiter}"Single-cell transcriptomic analysis of Alzheimer's disease"){record_delimiter}
("entity"{tuple_delimiter}"brain"{tuple_delimiter}"region"{tuple_delimiter}"Moreover, analyzing the hippocampal, temporal and frontal regions from the same LOAD patients, we identify specific sets of deregulated miRNAs for each region, and we confirm that the miR-132/212 cluster is deregulated in each of these regions in LOAD patients, consistent with these miRNAs playing a role in AD pathogenesis.Notably, a luciferase assay indicates that miR-184 is able to target the 3'UTR NR4A2 - which is known to be involved in cognitive functions and long-term memory and whose expression levels are inversely correlated with those of miR-184 in the hippocampus."){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"cell type"{tuple_delimiter}""){record_delimiter}
("entity"{tuple_delimiter}"UNKNOWN"{tuple_delimiter}"group"{tuple_delimiter}""){record_delimiter}
("content_keywords"{tuple_delimiter}"Alzheimer's Disease, Transcriptome, gene expression"){completion_delimiter}
#############################""",
]


PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """---Role---

You are a professional assistant responsible for answering questions based on knowledge graph and textual information. Please respond in the same language as the user's question.

---Goal---

Generate a concise response that summarizes relevant points from the provided information. If you don't know the answer, just say so. Do not make anything up or include information where the supporting evidence is not provided.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Data Sources---

1. Knowledge Graph Data:
{kg_context}

2. Vector Data:
{vector_context}

---Response Requirements---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Aim to keep content around 3 paragraphs for conciseness
- Each paragraph should be under a relevant section heading
- Each section should focus on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References", clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (VD)
  Format: [KG/VD] Source content

Add sections and commentary to the response as appropriate for the length and format. If the provided information is insufficient to answer the question, clearly state that you don't know or cannot provide an answer in the same language as the user's question."""
