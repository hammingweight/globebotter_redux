# The Vector Database
This directory contains a ChromaDB database that is populated with document snippets from an Italian travel guide. You
can download the travel guide from [ISI Florence](https://isiflorence.org/wp-content/uploads/2022/02/MINI-TRAVEL-GUIDE.pdf). The
document snippets are created using semantic chunking. Qwen3-4B is used to create the text embeddings of the documents.

If you want to create the database from scratch, download the travel guide and save it in this directory as `italy_guide.pdf`. Then
run

```
rm -rf 2c445656-7422-4d37-924f-03d64eded7d5
rm chroma.sqlite3
PYTHONPATH=../src python create_db.py
```
