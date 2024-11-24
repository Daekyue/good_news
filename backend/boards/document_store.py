from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

class NewsDocumentStore:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Create database connection string
        self.connection_string = PGVector.connection_string_from_db_params(
            driver=os.getenv("DB_DRIVER", "psycopg2"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "vectordb"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )

        # Initialize embedding model
        self.embeddings = OpenAIEmbeddings()

        # Initialize vector store
        self.vectorstore = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name="news_documents"
        )

    def process_news_article(self, article: Dict) -> Dict:
        """
        Process news article data into document and metadata.
        """
        content = f"{article['title']}\n\n{article.get('subtitle', '')}\n\n{article['content']}"
        metadata = {
            'title': article['title'],
            'category': article.get('category', ''),
            'date': article.get('date', ''),
            'keywords': article.get('keywords', ''),
            'processed_date': datetime.now().isoformat()
        }
        return {
            'content': content,
            'metadata': metadata
        }

    def add_news_articles(self, articles: List[Dict]) -> None:
        """
        Add news articles to the vector store.
        """
        documents = []
        for article in articles:
            try:
                processed = self.process_news_article(article)
                documents.append(
                    Document(
                        page_content=processed['content'],
                        metadata=processed['metadata']
                    )
                )
            except Exception as e:
                print(f"Error processing article: {e}")

        print(f"Number of articles processed: {len(documents)}")

        # Add documents to vector store
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query: str, k: int = 3, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        Perform similarity-based search for news articles.
        """
        # Perform similarity search
        docs = self.vectorstore.similarity_search_with_score(
            query, 
            k=k,
            filter=filter_dict
        )

        # Format results
        results = []
        for doc, score in docs:
            results.append({
                'title': doc.metadata.get('title', ''),
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity': 1 - score  # Convert score to similarity
            })

        return results

    @classmethod
    def from_existing(cls, collection_name: str = "news_documents"):
        """
        Create a NewsDocumentStore instance using an existing collection.
        """
        instance = cls()
        instance.vectorstore = PGVector(
            connection_string=instance.connection_string,
            embedding_function=instance.embeddings,
            collection_name=collection_name
        )
        return instance

    def delete_collection(self):
        """
        Delete the current collection.
        """
        self.vectorstore.delete_collection()
        print(f"Collection '{self.vectorstore.collection_name}' has been deleted successfully.")
