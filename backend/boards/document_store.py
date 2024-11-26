# backend / boards / document_store.py

from langchain.vectorstores import FAISS
from langchain_community.vectorstores import PGVector
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from typing import List, Dict, Optional
import os
import pickle
from dotenv import load_dotenv
from movies.models import Movie
from django.core.cache import cache
import numpy as np

class NewsDocumentStore:
    """
    뉴스 기사를 위한 문서 저장 및 검색 시스템
    FAISS를 백엔드로 사용하여 벡터 검색을 구현합니다.
    """
    
    def __init__(self, index_file: str = "boards/faiss_index.pkl"):
        # Hugging Face 임베딩 모델 초기화
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-mpnet-base-v2")
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        # FAISS 벡터 저장소 초기화 또는 로드
        self.index_file = "boards/faiss_index.pkl"

        if os.path.exists(self.index_file):
            with open(self.index_file, "rb") as f:
                self.vectorstore = pickle.load(f)
            print("FAISS 인덱스를 로드했습니다.")
        else:
            # FAISS 기본 인덱스 생성 (코사인 유사도 기반)
            dimension = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatIP(dimension)  # Inner Product 기반 FAISS 인덱스
            self.vectorstore = FAISS(
                index=index,
                docstore=InMemoryDocstore({}),
                index_to_docstore_id={},
                embedding_function=self.embeddings.embed_documents
            )
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
            # 'category': article['category'],
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
    
    def find_similar_articles(self, reference_article: Dict, k: int = 6) -> List[Dict]:
        """
        특정 기사를 기준으로 유사한 기사를 검색합니다.
        
        Args:
            reference_article: 기준이 되는 뉴스 기사 데이터
            k: 반환할 결과 개수
            
        Returns:
            유사한 뉴스 기사들의 리스트
        """
        # 기준 기사 임베딩 생성 및 정규화
        processed = self.process_news_article(reference_article)
        reference_embedding = self.embeddings.embed_query(processed['content'])
        reference_embedding = reference_embedding / np.linalg.norm(reference_embedding)
        
        # 유사도 검색 수행
        distances, indices = self.vectorstore.index.search(
            np.array([reference_embedding]), k
        )
        
        # 결과 포매팅
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            doc_id = self.vectorstore.index_to_docstore_id[idx]
            doc = self.vectorstore.docstore.search(doc_id)
            results.append({
                'title': doc.metadata['title'],
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity': distance  # 코사인 유사도
            })
            
        return results


class ChatbotDocumentStore:
    """
    챗봇을 위한 문서 저장 및 검색 시스템
    PGVector를 백엔드로 사용하여 영화 데이터를 사전 학습 데이터로 사용합니다.
    """
    
    def __init__(self):
        load_dotenv()
        
        # PGVector 초기화
        self.connection_string = PGVector.connection_string_from_db_params(
            driver=os.getenv("DB_DRIVER", "psycopg2"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "backend"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )

        # 임베딩 모델 초기화
        self.embeddings = OpenAIEmbeddings()

        # 벡터 저장소 초기화
        self.vectorstore = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name="chatbot_documents"
        )

        # 벡터 스토어에 데이터가 있는지 확인하고, 없으면 영화 데이터를 인제스트
        if self.is_vectorstore_empty():
            self.ingest_movies_data()
            
    def is_vectorstore_empty(self) -> bool:
        """
        벡터 저장소가 비어 있는지 확인합니다.
        """
        try:
            # 임의로 문서를 검색하여 저장소가 비어 있는지 확인
            docs = self.vectorstore.similarity_search("test", k=1)
            return len(docs) == 0
        except Exception:
            return True
        
    def ingest_movies_data(self):
        """
        영화 데이터를 데이터베이스에서 읽어와 문서로 변환하고 벡터 저장소에 추가합니다.
        """
        # 영화 데이터를 가져옵니다
        movies = Movie.objects.all()
        documents = []

        for movie in movies:
            # 영화 정보를 문자열로 만듭니다
            content = f"제목: {movie.title}\n줄거리: {movie.overview}\n"

            # 장르, 감독, 배우 정보를 추가합니다
            genres = ", ".join([genre.name for genre in movie.genres.all()])
            if genres:
                content += f"장르: {genres}\n"
            directors = ", ".join([director.name for director in movie.directors.all()])
            if directors:
                content += f"감독: {directors}\n"
            actors = ", ".join([actor.name for actor in movie.actors.all()])
            if actors:
                content += f"배우: {actors}\n"
            if movie.release_date:
                content += f"개봉일: {movie.release_date}\n"

            # 메타데이터를 구성합니다
            metadata = {
                'title': movie.title,
                'tmdb_id': movie.tmdb_id,
                'release_date': str(movie.release_date),
                'genres': genres,
                'directors': directors,
                'actors': actors
            }

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

        print(f"총 {len(documents)}개의 영화를 벡터 저장소에 추가합니다.")

        # 벡터 저장소에 문서 추가
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query: str, k: int = 3) -> List[Dict]:
        """
        사용자 질문을 기반으로 유사한 영화 정보를 검색합니다.
        """
        # 유사도 검색 수행
        docs = self.vectorstore.similarity_search_with_score(
            query, 
            k=k
        )

        # 결과 포맷팅
        results = []
        for doc, score in docs:
            results.append({
                'title': doc.metadata.get('title', ''),
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity': 1 - score  # 점수를 유사도로 변환
            })

        return results