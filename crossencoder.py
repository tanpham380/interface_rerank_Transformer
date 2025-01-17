from rerankers import Reranker
from pydantic import BaseModel
from typing import Any, Optional, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class CrossEncoderInput(BaseModel):
    query: str
    property: Optional[str] = None
    documents: Optional[List[str]] = None

class DocumentScore(BaseModel):
    document: str
    score: float
    rank: int

class CrossEncoderResponse(BaseModel):
    query: str
    scores: Optional[List[DocumentScore]] = None
    property: Optional[str] = None
    score: Optional[float] = None

class CrossEncoderRanker:
    lock: Lock
    executor: ThreadPoolExecutor
    model: Any

    def __init__(self, model_path: str):
        self.lock = Lock()
        self.executor = ThreadPoolExecutor()
        self.model = Reranker(model_path ,trust_remote_code=True )

    def _batch_rerank(self, item: CrossEncoderInput) -> CrossEncoderResponse:
        results = self.model.rank(query=item.query, docs=item.documents)
        documentScores = [DocumentScore(document=result.document.text, score=result.score, rank=result.rank) for result in results]
        return CrossEncoderResponse(query=item.query, scores=documentScores)

    def _perform_rerank(self, item: CrossEncoderInput) -> CrossEncoderResponse:
        if item.documents is not None:
            return self._batch_rerank(item)

        result = self.model.rank(query=item.query, docs=[item.property])
        
        score = result.score 
        return CrossEncoderResponse(query=item.query, property=item.property, score=score)

    def _rerank(self, item: CrossEncoderInput) -> CrossEncoderResponse:
        with self.lock:
            return self._perform_rerank(item)

    async def do(self, item: CrossEncoderInput):
        return await asyncio.wrap_future(self.executor.submit(self._rerank, item))