import re
from pathlib import Path

import pandas as pd
from chromadb import Collection as ChromaCollection
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_core.documents import Document as LCDocument

from .chroma import (
    CHROMA_DEVICE,
    CHROMA_DIR,
    CHROMA_EMBEDDING_MODEL,
    chroma_collection,
    lc_docs_to_chroma_docs,
)
from .utils import resolve_data_path

CHUNK_SIZE = 100
CHUNK_OVERLAP = 10
SEPARATORS = ["."]
CHROM_COLLECTION_NAME = "pdf_collection"
CHROMA_DELETE_EXISTING = False
PARENTS_DF_NAME = "parents_df"
CHILDREN_COLLECTION_NAME = "children_collection"


def pdf_pages(
    pdf_file: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    separators: list[str] = SEPARATORS,
) -> list[LCDocument]:
    page_loader = UnstructuredPDFLoader(pdf_file, mode="paged")
    if chunk_size:
        page_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            keep_separator=False,
        )
        pages = page_loader.load_and_split(text_splitter=page_splitter)
    else:
        pages = page_loader.load()
    return pages


def pdf_to_collection(
    pdf_file: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    separators: list[str] = SEPARATORS,
    collection_name: str = CHROM_COLLECTION_NAME,
    persistent_dir: str = CHROMA_DIR,
    delete_existing: bool = CHROMA_DELETE_EXISTING,
    embedding_model: str = CHROMA_EMBEDDING_MODEL,
    device: str = CHROMA_DEVICE,
) -> ChromaCollection:
    pages = pdf_pages(
        pdf_file=pdf_file,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    collection = chroma_collection(
        name=collection_name,
        persistent_dir=persistent_dir,
        delete_existing=delete_existing,
        embedding_model=embedding_model,
        device=device,
    )
    ids, docs, metadatas = lc_docs_to_chroma_docs(pages)
    collection.add(ids=ids, documents=docs, metadatas=metadatas)
    return collection


def pdf_pages_to_df(
    pdf_file: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    separators: list[str] = SEPARATORS,
) -> pd.DataFrame:
    pages = pdf_pages(
        pdf_file,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )
    df = pd.DataFrame(
        [
            {
                "page_number": page.metadata.get("page_number", 0),
                "page_content": page.page_content,
                "filename": page.metadata["filename"],
            }
            for page in pages
        ]
    )
    return df


def pdf_to_family_collection(
    data_path: str | list[str] | None = None,
    parent_pages: list[LCDocument] | None = None,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    separators: list[str] = SEPARATORS,
    parents_df_name: str = PARENTS_DF_NAME,
    children_collection_name: str = CHILDREN_COLLECTION_NAME,
    delete_existing: bool = CHROMA_DELETE_EXISTING,
) -> tuple[ChromaCollection, pd.DataFrame]:
    assert (
        data_path or parent_pages
    ), "Either data_path or parent_pages must be provided."
    children_collection = chroma_collection(
        name=children_collection_name, delete_existing=delete_existing
    )
    page_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        keep_separator=False,
    )
    parent_dfs = []
    if data_path:
        data_list = resolve_data_path(data_path)
    else:
        data_list = [parent_pages]
    for data in data_list:
        if isinstance(data, str):
            if Path(data).suffix != ".pdf":
                continue
            parent_pages = pdf_pages(data)
        else:
            parent_pages = data
        parent_df = pd.DataFrame(
            [
                {
                    "page_number": page.metadata.get("page_number", 0),
                    "page_content": re.sub(r"\n+", "\n", page.page_content),
                    "filename": page.metadata["filename"],
                }
                for page in parent_pages
            ]
        )
        parent_dfs.append(parent_df)

        children = page_splitter.split_documents(parent_pages)
        children_ids, children_texts, children_metadatas = lc_docs_to_chroma_docs(
            children
        )
        print(f"\n\nCHILDREN IDS: {children_ids}\n\n")
        children_collection.add(
            ids=children_ids, documents=children_texts, metadatas=children_metadatas
        )
    parents_df = pd.concat(parent_dfs).reset_index(drop=True)
    parents_df_name: Path = Path(parents_df_name).with_suffix(".csv")
    if not delete_existing and parents_df_name.exists():
        existing_parents_df = pd.read_csv(parents_df_name)
        parents_df = pd.concat([existing_parents_df, parents_df]).reset_index(drop=True)
    parents_df.to_csv(parents_df_name, index=False)
    return children_collection, parents_df
