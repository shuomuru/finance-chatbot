from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class MessageRole(str, Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"

class DialogueState(str, Enum):
    START = "start"
    INTENT_CONFIRM = "intent_confirm"
    SLOT_FILLING = "slot_filling"
    PROCESSING = "processing"
    RESPONDING = "responding"
    END = "end"
    ERROR = "error"

class Intent(str, Enum):
    GREETING = "greeting"
    STOCK_QUERY = "stock_query"
    FUND_QUERY = "fund_query"
    INSURANCE_QUERY = "insurance_query"
    INVESTMENT_ADVICE = "investment_advice"
    RISK_ASSESSMENT = "risk_assessment"
    ACCOUNT_INFO = "account_info"
    COMPLAINT = "complaint"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

class Slot(BaseModel):
    name: str
    value: Optional[str] = None
    required: bool = False
    filled: bool = False
    description: Optional[str] = None

class ConversationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    state: DialogueState = DialogueState.START
    current_intent: Optional[Intent] = None
    slots: Dict[str, Slot] = {}
    context: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    question: str
    answer: str
    intent: Intent
    state: DialogueState
    success: bool
    error: Optional[str] = None
    context_maintained: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    database_connected: bool
    nlp_model_loaded: bool
    uptime: float

class StatisticsResponse(BaseModel):
    total_sessions: int
    total_messages: int
    average_response_time: float
    top_intents: Dict[str, int]
    daily_active_users: int

class CompareResponse(BaseModel):
    question: str
    base_model: str
    fine_tuned_model: str
    success: bool
    error: Optional[str] = None

class RAGQuery(BaseModel):
    question: str

class RAGResponse(BaseModel):
    question: str
    answer: str
    success: bool
    error: Optional[str] = None
