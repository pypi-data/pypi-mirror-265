import os
import click
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter


from chat_cli_anything.util import cache_path, calculate_hash
from typing import Union, List, Tuple, Dict


__SUPPORTED_FILES__ = [
    # documents
    '.txt', '.md', '.pdf', '.docx', '.doc',
    # programming language
    '.py', '.c', '.cpp', '.java', '.js', '.ts',
    '.go', '.rs', '.php', '.html', '.css', '.json',
    '.yaml', '.yml'
]

FileHash = Dict[str, str]


def parse_files(
    input: str,
    do_cache: bool=True,
    recursive: bool=True,
    verbose: bool=True,
) -> Union[Tuple[List[List[Document]], Dict[str, str]], None]:
    """Check file given folder."""
    # md5: file_path
    all_files_processed = {}

    all_pages: List[List[Document]] = []
    if os.path.isdir(input):
        for item in os.listdir(input):
            sub_item = os.path.join(input, item)
            if os.path.isfile(sub_item):
                if os.path.splitext(sub_item)[-1] in __SUPPORTED_FILES__:
                    pages, _files_processed = parse_files(sub_item, do_cache=do_cache)
                    all_pages.extend(pages)
                    all_files_processed.update(_files_processed)
            else:
                if recursive:
                    pages, _files_processed = parse_files(sub_item, do_cache=do_cache, recursive=recursive)
                    all_pages.extend(pages)
                    all_files_processed.update(_files_processed)

    elif os.path.exists(input):
        ext = os.path.splitext(input)[1]
        if ext not in __SUPPORTED_FILES__:
            click.secho(f'File type {ext} not supported', fg='red')
            return
        if verbose:
            click.secho(f'found "{input}"', fg='green')
        if ext == '.pdf':
            loader = PyPDFLoader(input)
        elif ext in ['.docx', '.doc']:
            loader = UnstructuredWordDocumentLoader(input)
        else:
            loader = TextLoader(input)
        pages = loader.load()
        # from_tiktoken_encoder enables use to split on tokens rather than characters
        recursive_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=400, 
            chunk_overlap=100,
        )
        pages = recursive_text_splitter.split_documents(pages)
        all_pages.append(pages)
        all_files_processed[calculate_hash(input)] = os.path.abspath(input)

    else:
        click.secho(f'File {input} not found', fg='red')
    return all_pages, all_files_processed
