# KG auto construction

This is a project for KG auto construction. To run this project, you should install neo4j==5.7.0 and python>=3.8.

Cause this project is still under development, so there is no guarantee that it will work properly.

```
pip install -r requirements.txt
```

I would like to summarize the workflow of this project as follows:

1. paper crawling
   1. currently, we only support arxiv crawling.
   2. For arxiv, you can use `src/tools/arxiv/base.py` to crawl papers from arxiv.
   3. The crawled papers will be stored in `data/**.json` which can be used for further processing.
2. paper processing
   1. currently, we only support arxiv processing.
   2. The processing process are divided into two parts: paper preprocess and triple extraction.
   3. For paper preprocess, you can use `process/add_from_arxiv.py` to preprocess papers from arxiv saved in `data/**.json`. The result would be written into neo4j database.
   4. For triple extraction, you can use `mian.py` to extract triples from arxiv saved in the neo4j database.

### 2023-05-29

1. devide author entities from arxiv entities.
2. add clean function into neo4j module.
3. extract conceptions from arxiv.
4. idea: to verify a conception is general or not, different sources should be used. For example, stright output of LLM, common degree...

### 2023-05-25
1. basic arxiv requirement module has been finished.
2. thinking about how to build a minimal dataset for entity alignment.