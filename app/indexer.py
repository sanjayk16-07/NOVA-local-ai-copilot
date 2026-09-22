import os
from typing import List, Dict

from dotenv import load_dotenv
from moss import MossClient, DocumentInfo

from app.files import read_project_files

load_dotenv()


def get_moss_client() -> MossClient:
    project_id = os.getenv("MOSS_PROJECT_ID")
    project_key = os.getenv("MOSS_PROJECT_KEY")

    if not project_id or not project_key:
        raise RuntimeError(
            "MOSS_PROJECT_ID and MOSS_PROJECT_KEY must be configured"
        )

    return MossClient(project_id, project_key)


def build_local_documents(
    project_path: str = "data/sample-project",
) -> List[Dict[str, str]]:
    """
    Read safe project files and prepare them
    for local semantic indexing.
    """

    documents = read_project_files(project_path)

    return [
        {
            "path": document["path"],
            "content": document["content"],
        }
        for document in documents
    ]


def create_moss_index(
    project_path: str = "data/sample-project",
    index_name: str = "nova-local-index",
):
    """
    Create a Moss semantic index from the
    locally filtered project documents.
    """

    client = get_moss_client()

    documents = build_local_documents(project_path)

    moss_documents = [
        DocumentInfo(
            id=document["path"],
            text=document["content"],
            metadata={
                "path": document["path"],
            },
        )
        for document in documents
    ]

    return client.create_index(
        name=index_name,
        docs=moss_documents,
        wait=True,
    )