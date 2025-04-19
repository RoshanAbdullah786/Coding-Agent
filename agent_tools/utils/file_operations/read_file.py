from Agents.agent_tools.utils.text_operations.response_generator import response_text
from Agents.logg.logger import logger

def read_file_content(path):
    from pathlib import Path

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No file found at: {path}")

    if path.suffix.lower() == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif path.suffix.lower() == ".docx":
        from docx import Document
        doc = Document(str(path))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    else:
        # Treat it as a normal text file
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


def read_file(path,agent):
    try:
        content = read_file_content(path)
        logger.info(f"{agent} -- The Read File tool at the path {path} has been successfully executed")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE READ FILE AT THE PATH {path} HAS SUCCESSFULLY EXECUTED.THIS IS THE CONTENT OF THE FILE\n"+content)
    except Exception as e:
        logger.warning(f"{agent} -- The Read File tool at the path {path} has produced the following Error when executed {e}")
        return response_text(f"THIS IS AN AUTOMATED MESSAGE. DO NOT REPLY TO IT CONVERSATIONALLY. THE READ FILE AT THE PATH {path} HAS PRODUCED THE FOLLOWING ERROR ==> {e} WHEN EXECUTED")