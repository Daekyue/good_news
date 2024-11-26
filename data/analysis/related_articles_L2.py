from langchain.vectorstores import FAISS
import faiss
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.docstore.in_memory import InMemoryDocstore
from typing import List, Dict
import os
import json
from datetime import datetime
import pickle

class NewsDocumentStore:
    """
    뉴스 기사를 위한 문서 저장 및 검색 시스템
    FAISS를 백엔드로 사용하여 벡터 검색을 구현합니다.
    """
    
    def __init__(self, index_file: str = "faiss_index.pkl"):
        # Hugging Face 임베딩 모델 초기화
        model_name = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-mpnet-base-v2")
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        
        # FAISS 벡터 저장소 초기화 또는 로드
        self.index_file = index_file
        if os.path.exists(index_file):
            with open(index_file, "rb") as f:
                self.vectorstore = pickle.load(f)
            print("FAISS 인덱스를 로드했습니다.")
        else:
            # FAISS 기본 인덱스 생성
            dimension = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatL2(dimension)  # L2 거리 기반 FAISS 인덱스
            self.vectorstore = FAISS(
                index=index,
                docstore=InMemoryDocstore({}),
                index_to_docstore_id={},
                embedding_function=self.embeddings
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
            'category': article['category'],
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
                'title': doc.metadata['title'],
                'content': doc.page_content,
                'metadata': doc.metadata,
                'similarity': 1 - score  # 점수를 유사도로 변환
            })
            
        return results

# 사용 예시
if __name__ == "__main__":
    # 뉴스 문서 저장소 초기화
    news_store = NewsDocumentStore(index_file="faiss_index.pkl")
    
    file_path = "indiewire_data.json"
    index_file = "faiss_index.pkl"


    # JSON 파일 읽기
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # JSON 배열이 Python 리스트로 변환됨
    
    # 문서 추가
    if not os.path.exists(index_file):
        news_store.add_news_articles(data)
    
    # 특정 기사 선택
    reference_article = data[15]  # 첫 번째 기사를 기준으로 예제 실행
    
    # 유사한 기사 검색
    similar_articles = news_store.find_similar_articles(reference_article, k=6)
    similar_articles = similar_articles[1:]
    # 결과 출력
    for i, result in enumerate(similar_articles, 1):

        print(f"\n=== 유사한 기사 {i} ===")
        print(f"제목: {result['title']}")
        print(f"유사도: {result['similarity']:.4f}")
        print(f"내용 미리보기: {result['content'][:100]}...")
        print(result['metadata']['keywords'])
