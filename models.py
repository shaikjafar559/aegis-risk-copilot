from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class PersonaStyle(str, Enum):
    EXECUTIVE = "executive"
    DEEP_DIVE = "deep_dive"
    CINEMATIC = "cinematic"
    ELI5 = "eli5"
    PROVOCATIVE_DEBATE = "provocative_debate"

class DialogueSpeaker(str, Enum):
    MAYA = "maya"
    LEO = "leo"
    NARRATOR = "narrator"
    AUDIENCE = "audience"

class EmotionValence(str, Enum):
    ANALYTICAL = "analytical"
    CURIOUS = "curious"
    SKEPTICAL = "skeptical"
    ENTHUSIASTIC = "enthusiastic"
    DRAMATIC = "dramatic"
    INSIGHTFUL = "insightful"
    URGENT = "urgent"

class DialogueLine(BaseModel):
    id: str
    speaker: DialogueSpeaker
    speaker_name: str
    text: str
    emotion: EmotionValence
    pitch: float = 1.0
    rate: float = 1.05
    visual_cue: str = "cyber_grid"  # 'cyber_grid', 'quantum_lattice', 'nebula_space', 'biolum_synth'
    chapter: str = "Introduction"
    highlight_terms: List[str] = Field(default_factory=list)
    timestamp_est: int = 0

class BranchOption(BaseModel):
    id: str
    title: str
    description: str
    teaser_line: str
    branch_point_line_id: str

class KnowledgeEntity(BaseModel):
    id: str
    label: str
    category: str  # 'technology', 'concept', 'company', 'person', 'metric', 'impact'
    description: str
    connections: List[str] = Field(default_factory=list)

class PerspectiveScore(BaseModel):
    dimension: str
    score: int  # 0 to 100
    summary: str

class BroadcastManifest(BaseModel):
    id: str
    title: str
    subtitle: str
    source_topic: str
    persona_style: PersonaStyle
    duration_est: str
    summary: str
    key_takeaways: List[str]
    lines: List[DialogueLine]
    branches: List[BranchOption]
    knowledge_graph: List[KnowledgeEntity]
    perspectives: List[PerspectiveScore]
    social_assets: Dict[str, Any] = Field(default_factory=dict)

class GenerateRequest(BaseModel):
    topic: str
    raw_content: Optional[str] = None
    persona: PersonaStyle = PersonaStyle.DEEP_DIVE
    duration: Optional[str] = "standard"  # "short", "standard", "deep"
    creativity_temp: Optional[float] = 0.7

class InterruptRequest(BaseModel):
    broadcast_id: str
    current_line_id: str
    user_question: str
    tone_preference: Optional[str] = "balanced"

class BranchSelectionRequest(BaseModel):
    broadcast_id: str
    branch_id: str
