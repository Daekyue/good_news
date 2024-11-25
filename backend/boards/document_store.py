from langchain.vectorstores import FAISS
from langchain_community.vectorstores import PGVector
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict, Optional
import os
import pickle
from dotenv import load_dotenv

class NewsDocumentStore:
    """
    뉴스 기사를 위한 문서 저장 및 검색 시스템
    FAISS를 백엔드로 사용하여 벡터 검색을 구현합니다.
    """
    
    def __init__(self, index_file: str = "boards/faiss_index.pkl"):
        # Hugging Face 임베딩 모델 초기화
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        # FAISS 벡터 저장소 초기화 또는 로드
        
        # self.index_file = "/home/ssafy/good_news/backend/boards/faiss_index.pkl"
        self.index_file = "boards/faiss_index.pkl"

        if os.path.exists(self.index_file):
            with open(self.index_file, "rb") as f:
                self.vectorstore = pickle.load(f)
            print("FAISS 인덱스를 로드했습니다.")
        else:
            self.vectorstore = FAISS(embedding_function=self.embeddings)
            print("새로운 FAISS 인덱스를 생성했습니다.")
    
    def save_index(self):
        """FAISS 인덱스를 파일에 저장합니다."""
        with open(self.index_file, "wb") as f:
            pickle.dump(self.vectorstore, f)
        print("FAISS 인덱스를 저장했습니다.")
    
    def process_news_article(self, article: Dict) -> Dict:
        """
        뉴스 기사 데이터를 처리하여 문서와 메타데이터로 변환합니다.
        
        Args:
            article: 뉴스 기사 데이터 딕셔너리
            
        Returns:
            처리된 문서와 메타데이터
        """
        # 본문 텍스트 처리
        content = f"{article['title']}\n\n{article['content']}"
        
        # 메타데이터 구성
        metadata = {
            'title': article['title'],
            'content': article['content'],
            'keywords': article['keywords']
        }
        
        return {
            'content': content,
            'metadata': metadata
        }
    
    def add_news_articles(self, articles: List[Dict]) -> None:
        """
        뉴스 기사들을 FAISS 벡터 저장소에 추가합니다.
        
        Args:
            articles: 뉴스 기사 데이터 리스트
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
                print(f"문서 처리 실패: {e}")
                continue
        
        print(f"처리된 기사 개수: {len(documents)}")
        
        # 벡터 저장소에 문서 추가
        self.vectorstore.add_documents(documents)
        self.save_index()
    
    def find_similar_articles(self, reference_article: Dict, k: int = 5) -> List[Dict]:
        """
        특정 기사를 기준으로 유사한 기사를 검색합니다.
        
        Args:
            reference_article: 기준이 되는 뉴스 기사 데이터
            k: 반환할 결과 개수
            
        Returns:
            유사한 뉴스 기사들의 리스트
        """
        # 기준 기사 임베딩 생성
        processed = self.process_news_article(reference_article)
        reference_doc = Document(
            page_content=processed['content'],
            metadata=processed['metadata']
        )
        
        # 유사도 검색 수행
        docs = self.vectorstore.similarity_search_with_score(
            query=reference_doc.page_content, 
            k=k
        )
        
        # 결과 포매팅
        results = []
        for doc, score in docs:
            results.append({
                'title': doc.metadata.get('title', ''),
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity': 1 - score  # 점수를 유사도로 변환
            })
        
        # for r in results:
        #     print(r['title'])
            
        return results


class ChatbotDocumentStore:
    """
    챗봇을 위한 문서 저장 및 검색 시스템
    pgvector를 백엔드로 사용하여 실시간 데이터 추가 및 검색을 구현합니다.
    """
    
    def __init__(self):
        load_dotenv()
        
        # pgvector 초기화
        self.connection_string = PGVector.connection_string_from_db_params(
            driver=os.getenv("DB_DRIVER", "psycopg2"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "backend"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )

        # Initialize embedding model
        self.embeddings = OpenAIEmbeddings()

        # Initialize vector store
        self.vectorstore = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name="chatbot_documents"
        )
    
    def add_chatbot_context(self, articles: List[Dict]) -> None:
        """
        챗봇 문서들을 pgvector 저장소에 추가합니다.
        
        Args:
            articles: 문서 데이터 리스트
        """
        documents = []
        for article in articles:
            try:
                content = f"{article['title']}\n\n{article['content']}"
                documents.append(
                    Document(
                        page_content=content,
                        metadata=article
                    )
                )
            except Exception as e:
                print(f"문서 처리 실패: {e}")
                continue

        print(f"처리된 문서 개수: {len(documents)}")
        
        # 벡터 저장소에 문서 추가
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Perform similarity-based search for chatbot context.
        """
        # Perform similarity search
        docs = self.vectorstore.similarity_search_with_score(
            query, 
            k=k
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
