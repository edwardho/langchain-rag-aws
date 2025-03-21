from langchain_chroma import Chroma
from rag_app.get_embedding_function import get_embedding_function
import os
import shutil
import sys

CHROMA_PATH = os.environ.get("CHROMA_PATH", "data/chroma")
IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))
CHROMA_DB_INSTANCE = None  # Reference to singleton instance of ChromaDB

def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:

        if IS_USING_IMAGE_RUNTIME:
            copy_chroma_to_tmp()

        # Prepare the DB.
        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=get_runtime_chroma_path(),
            embedding_function=get_embedding_function(),
        )
        print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {CHROMA_PATH}")

    return CHROMA_DB_INSTANCE

def copy_chroma_to_tmp():
    dst_path = get_runtime_chroma_path()

    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    tmp_contents = os.listdir(dst_path)
    if len(tmp_contents) > 0:
        print(f"🔥 ChromaDB already exists in {dst_path}. Skipping copy.")
        return

    print(f"🔥 Copying ChromaDB from {CHROMA_PATH} to {dst_path}.")
    os.makedirs(dst_path, exist_ok=True)
    shutil.copytree(CHROMA_PATH, dst_path, dirs_exist_ok=True)

def get_runtime_chroma_path():
    if IS_USING_IMAGE_RUNTIME:
        return f"/tmp/{CHROMA_PATH}"
    else:
        return CHROMA_PATH
