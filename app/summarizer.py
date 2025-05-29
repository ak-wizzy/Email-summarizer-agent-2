from transformers import pipeline
from config import MODEL_NAME
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load the summarization pipeline
logging.info(f"Loading summarization model: {MODEL_NAME}")
summarizer = pipeline("summarization", model=MODEL_NAME)

def split_text_into_chunks(text: str, max_words: int = 400):
    """
    Split long texts into manageable chunks for summarization.
    """
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def bullet_format(summary_text: str) -> str:
    """
    Format summary text into bullet points per sentence.
    Avoids awkward line breaks by splitting only on periods.
    """
    sentences = [s.strip() for s in summary_text.split('. ') if s.strip()]
    return "\n".join(f"- {s.rstrip('.') + '.'}" for s in sentences)

def summarize_email(text: str) -> str:
    """
    Summarizes a given block of text using a Hugging Face summarization pipeline.
    Splits long text into chunks and aggregates bullet-pointed summaries.
    """
    try:
        if not text or len(text.strip()) < 30:
            logging.warning("Email body too short to summarize.")
            return "[Email body too short to summarize.]"

        input_length = len(text.split())
        logging.info(f"Summarizing email content ({input_length} words)...")

        chunks = split_text_into_chunks(text)
        bullet_points = []

        for chunk in chunks:
            try:
                summary = summarizer(
                    chunk,
                    max_length=150,
                    min_length=50,
                    do_sample=False
                )
                if isinstance(summary, list) and len(summary) > 0:
                    chunk_summary = summary[0].get('summary_text', '').strip()
                    if chunk_summary:
                        bullet_points.append(bullet_format(chunk_summary))
                    else:
                        logging.warning("Empty summary_text received from model.")
                else:
                    logging.warning("Unexpected summary format received.")
            except Exception as chunk_err:
                logging.error(f"Error summarizing chunk: {str(chunk_err)}")
                bullet_points.append("[Error summarizing this section.]")

        final_summary = "\n".join(bullet_points) if bullet_points else "[No summary could be generated.]"
        logging.info("Summarization complete.")
        return final_summary

    except IndexError:
        logging.error("Summarization error: index out of range in self")
        return "[Summarization error: index out of range in input]"
    except Exception as e:
        logging.error(f"Summarization error: {str(e)}")
        return f"[Summarization error: {str(e)}]"
