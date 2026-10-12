import uuid
import re
from typing import Dict, List, Optional
from app.models import (
    BroadcastManifest, DialogueLine, DialogueSpeaker, EmotionValence,
    BranchOption, KnowledgeEntity, PerspectiveScore, PersonaStyle,
    GenerateRequest, InterruptRequest
)
from app.data.sample_broadcasts import SAMPLE_BROADCASTS

# Active in-memory storage for generated and sample broadcasts
BROADCAST_STORE: Dict[str, BroadcastManifest] = dict(SAMPLE_BROADCASTS)

class MultiAgentBroadcastEngine:
    """
    Multi-Agent AI Studio Engine orchestrating:
    - Director Agent (narrative pacing and structure)
    - Dr. Maya Vance Agent (Chief Analyst & Systems Thinker)
    - Leo Cruz Agent (Cultural Strategist & Creative Provocateur)
    - Knowledge Graph & Perspective Radar Synthesizer
    """

    @classmethod
    def get_broadcast(cls, broadcast_id: str) -> Optional[BroadcastManifest]:
        return BROADCAST_STORE.get(broadcast_id)

    @classmethod
    def list_broadcasts(cls) -> List[Dict[str, str]]:
        return [
            {
                "id": b.id,
                "title": b.title,
                "subtitle": b.subtitle,
                "topic": b.source_topic,
                "duration": b.duration_est,
                "persona": b.persona_style.value
            }
            for b in BROADCAST_STORE.values()
        ]

    @classmethod
    def generate_custom_broadcast(cls, req: GenerateRequest) -> BroadcastManifest:
        clean_topic = req.topic.strip()
        bid = f"custom-{uuid.uuid4().hex[:8]}"

        # Extract keywords and concepts
        words = [w for w in re.findall(r'\b[A-Za-z0-9_-]{3,}\b', clean_topic) if w.lower() not in {"the", "and", "for", "with", "about"}]
        core_subject = " ".join(words[:4]) if words else clean_topic

        # Adapt dialogue generation based on selected persona style
        style = req.persona
        lines = []

        if style == PersonaStyle.EXECUTIVE:
            rate_maya, rate_leo = 1.15, 1.18
            cue1, cue2, cue3 = "cyber_grid", "neural_glow", "quantum_lattice"
            lines = [
                DialogueLine(
                    id=f"{bid}-1",
                    speaker=DialogueSpeaker.NARRATOR,
                    speaker_name="OmniStory Brief",
                    text=f"Executive 2-Minute Briefing: Strategic impacts of {clean_topic}.",
                    emotion=EmotionValence.URGENT,
                    pitch=1.0,
                    rate=1.1,
                    visual_cue=cue1,
                    chapter="Executive Brief",
                    highlight_terms=[clean_topic, "Strategic Impact"],
                    timestamp_est=0
                ),
                DialogueLine(
                    id=f"{bid}-2",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Bottom line first: {clean_topic} is accelerating past traditional quarterly forecasts. We are tracking a 3x enterprise adoption inflection within the next 18 months.",
                    emotion=EmotionValence.ANALYTICAL,
                    pitch=1.02,
                    rate=rate_maya,
                    visual_cue=cue2,
                    chapter="Market Inflection",
                    highlight_terms=["3x Enterprise Adoption", "Quarterly Forecasts"],
                    timestamp_est=6
                ),
                DialogueLine(
                    id=f"{bid}-3",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"The primary risk factor isn't capital expenditure—it's regulatory friction and legacy organizational inertia. Leaders who delay implementation risk complete margin compression.",
                    emotion=EmotionValence.INSIGHTFUL,
                    pitch=0.98,
                    rate=rate_leo,
                    visual_cue=cue3,
                    chapter="Risk Matrix",
                    highlight_terms=["Regulatory Friction", "Margin Compression"],
                    timestamp_est=16
                ),
                DialogueLine(
                    id=f"{bid}-4",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Actionable takeaway: prioritize autonomous pilot pipelines immediately. What was considered experimental 12 months ago is now table stakes.",
                    emotion=EmotionValence.ANALYTICAL,
                    pitch=1.03,
                    rate=rate_maya,
                    visual_cue=cue1,
                    chapter="Strategic Directive",
                    highlight_terms=["Autonomous Pilot", "Table Stakes"],
                    timestamp_est=26
                ),
                DialogueLine(
                    id=f"{bid}-5",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text="Choose your strategic deep-dive branch below to inspect unit economics, security posture, or competitive benchmarks.",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.0,
                    rate=1.1,
                    visual_cue="studio_pulse",
                    chapter="Audience Choice",
                    highlight_terms=["Strategic Deep-Dive"],
                    timestamp_est=35
                )
            ]
        elif style == PersonaStyle.ELI5:
            rate_maya, rate_leo = 0.98, 1.02
            lines = [
                DialogueLine(
                    id=f"{bid}-1",
                    speaker=DialogueSpeaker.NARRATOR,
                    speaker_name="OmniStory Kids & Curious",
                    text=f"Welcome! Today we are exploring {clean_topic}—explained simply so anyone can understand!",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.05,
                    rate=1.0,
                    visual_cue="biolum_synth",
                    chapter="Welcome & Curiosity",
                    highlight_terms=[clean_topic, "Simple Explanation"],
                    timestamp_est=0
                ),
                DialogueLine(
                    id=f"{bid}-2",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"Imagine your brain had a personal robotic apprentice who could read every book in the world in two seconds. That is essentially what {clean_topic} is trying to build for us!",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.0,
                    rate=rate_leo,
                    visual_cue="nebula_space",
                    chapter="The Big Picture",
                    highlight_terms=["Robotic Apprentice", "Every Book in 2 Seconds"],
                    timestamp_est=7
                ),
                DialogueLine(
                    id=f"{bid}-3",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Exactly, Leo! And just like learning how to ride a bicycle with training wheels, scientists are teaching {clean_topic} to practice safely step by step without falling over.",
                    emotion=EmotionValence.INSIGHTFUL,
                    pitch=1.04,
                    rate=rate_maya,
                    visual_cue="quantum_lattice",
                    chapter="How It Learns",
                    highlight_terms=["Bicycle Training Wheels", "Practice Safely"],
                    timestamp_est=18
                ),
                DialogueLine(
                    id=f"{bid}-4",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"So does this mean robots will do all our homework soon, Maya?",
                    emotion=EmotionValence.CURIOUS,
                    pitch=1.02,
                    rate=1.05,
                    visual_cue="studio_pulse",
                    chapter="Curious Question",
                    highlight_terms=["Homework Robots"],
                    timestamp_est=29
                ),
                DialogueLine(
                    id=f"{bid}-5",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text="Not quite, Leo! It means they become our supercharged paintbrushes. We still have to decide what amazing painting we want to create!",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.05,
                    rate=1.0,
                    visual_cue="biolum_synth",
                    chapter="Supercharged Creativity",
                    highlight_terms=["Supercharged Paintbrushes", "Human Vision"],
                    timestamp_est=37
                ),
                DialogueLine(
                    id=f"{bid}-6",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text="Audience, what adventure should we choose next? Tap a path below!",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.0,
                    rate=1.02,
                    visual_cue="studio_pulse",
                    chapter="Audience Fork",
                    highlight_terms=["Choose Your Path"],
                    timestamp_est=47
                )
            ]
        elif style == PersonaStyle.PROVOCATIVE_DEBATE:
            rate_maya, rate_leo = 1.05, 1.08
            lines = [
                DialogueLine(
                    id=f"{bid}-1",
                    speaker=DialogueSpeaker.NARRATOR,
                    speaker_name="OmniStory The Arena",
                    text=f"Two minds, zero consensus. Welcome to The Arena: The Battle for {clean_topic}.",
                    emotion=EmotionValence.DRAMATIC,
                    pitch=0.98,
                    rate=1.0,
                    visual_cue="cyber_grid",
                    chapter="The Face-Off",
                    highlight_terms=["The Arena", clean_topic],
                    timestamp_est=0
                ),
                DialogueLine(
                    id=f"{bid}-2",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"Let's strip away the corporate PR. The grand promises made around {clean_topic} are overhyped, under-audited, and masking serious structural fragility.",
                    emotion=EmotionValence.SKEPTICAL,
                    pitch=0.96,
                    rate=rate_leo,
                    visual_cue="studio_pulse",
                    chapter="The Critique",
                    highlight_terms=["Corporate PR", "Structural Fragility"],
                    timestamp_est=6
                ),
                DialogueLine(
                    id=f"{bid}-3",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Leo, that's cynical dismissiveness masquerading as prudence! Look at the empirical benchmarks. {clean_topic} has solved foundational bottlenecks in months that took legacy institutions four decades.",
                    emotion=EmotionValence.ANALYTICAL,
                    pitch=1.04,
                    rate=rate_maya,
                    visual_cue="neural_glow",
                    chapter="Empirical Evidence",
                    highlight_terms=["Empirical Benchmarks", "Foundational Bottlenecks"],
                    timestamp_est=17
                ),
                DialogueLine(
                    id=f"{bid}-4",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"Benchmarks on synthetic toy datasets are meaningless if real-world deployments fail the moment edge-case anomalies occur! Who bears the liability when {clean_topic} miscalculates?",
                    emotion=EmotionValence.URGENT,
                    pitch=0.97,
                    rate=rate_leo,
                    visual_cue="quantum_lattice",
                    chapter="Real-World Edge Cases",
                    highlight_terms=["Synthetic Toy Datasets", "Real-World Liability"],
                    timestamp_est=29
                ),
                DialogueLine(
                    id=f"{bid}-5",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Every leap forward carries edge-case risk. The answer isn't paralysis; it's active synthetic governance and dynamic guardrails. You can't regulate an empty room, Leo.",
                    emotion=EmotionValence.INSIGHTFUL,
                    pitch=1.02,
                    rate=rate_maya,
                    visual_cue="biolum_synth",
                    chapter="Dynamic Guardrails",
                    highlight_terms=["Active Governance", "Dynamic Guardrails"],
                    timestamp_est=41
                ),
                DialogueLine(
                    id=f"{bid}-6",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text="Audience, it's your turn to judge. Who has the stronger argument, or do you want to steer the cross-examination?",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.0,
                    rate=1.05,
                    visual_cue="studio_pulse",
                    chapter="Audience Verdict",
                    highlight_terms=["Audience Cross-Examination"],
                    timestamp_est=53
                )
            ]
        else:  # DEEP_DIVE & CINEMATIC
            rate_maya, rate_leo = 1.03, 1.05
            lines = [
                DialogueLine(
                    id=f"{bid}-1",
                    speaker=DialogueSpeaker.NARRATOR,
                    speaker_name="OmniStory Live",
                    text=f"Broadcasting live across the neural frequency. Tonight: An investigative journey into {clean_topic}.",
                    emotion=EmotionValence.DRAMATIC,
                    pitch=1.0,
                    rate=1.0,
                    visual_cue="quantum_lattice",
                    chapter="Deep Dive Initiation",
                    highlight_terms=[clean_topic],
                    timestamp_est=0
                ),
                DialogueLine(
                    id=f"{bid}-2",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"Leo, when you analyze the vector architectures and systemic breakthroughs powering {clean_topic}, it becomes clear we are experiencing a generational phase change.",
                    emotion=EmotionValence.ANALYTICAL,
                    pitch=1.03,
                    rate=rate_maya,
                    visual_cue="neural_glow",
                    chapter="Architectural Phase Change",
                    highlight_terms=["Vector Architectures", "Systemic Breakthroughs"],
                    timestamp_est=7
                ),
                DialogueLine(
                    id=f"{bid}-3",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"What captivates me is the experiential dimension. For the first time, users aren't just consumers of {clean_topic}—they are co-directors shaping its trajectory in real time.",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=0.98,
                    rate=rate_leo,
                    visual_cue="cyber_grid",
                    chapter="Experiential Shift",
                    highlight_terms=["Experiential Dimension", "Co-Directors"],
                    timestamp_est=18
                ),
                DialogueLine(
                    id=f"{bid}-4",
                    speaker=DialogueSpeaker.MAYA,
                    speaker_name="Dr. Maya Vance",
                    text=f"And the downstream second-order effects are immense. From algorithmic trust metrics to dynamic multimodal synthesis, {clean_topic} is collapsing the gap between concept and manifestation.",
                    emotion=EmotionValence.INSIGHTFUL,
                    pitch=1.04,
                    rate=rate_maya,
                    visual_cue="nebula_space",
                    chapter="Second-Order Impacts",
                    highlight_terms=["Algorithmic Trust", "Multimodal Synthesis"],
                    timestamp_est=30
                ),
                DialogueLine(
                    id=f"{bid}-5",
                    speaker=DialogueSpeaker.LEO,
                    speaker_name="Leo Cruz",
                    text=f"Let's put this straight to our live audience. You have direct control over our broadcast studio. Which dimension shall we unlock next?",
                    emotion=EmotionValence.ENTHUSIASTIC,
                    pitch=1.0,
                    rate=1.05,
                    visual_cue="studio_pulse",
                    chapter="Interactive Switchboard",
                    highlight_terms=["Direct Control", "Interactive Switchboard"],
                    timestamp_est=42
                )
            ]

        # Synthesize branches
        branches = [
            BranchOption(
                id=f"branch-tech-{bid}",
                title=f"{core_subject}: Deep Technical Architecture",
                description=f"Explore the underlying algorithmic engine, parameter scaling, and compute requirements.",
                teaser_line="Maya breaks down the latency optimization and system topology.",
                branch_point_line_id=lines[-1].id
            ),
            BranchOption(
                id=f"branch-socio-{bid}",
                title=f"{core_subject}: Cultural & Economic Disruption",
                description=f"Examine market dislocations, creator rights, and human capital transformation.",
                teaser_line="Leo unpacks how business models and cultural consumption will invert.",
                branch_point_line_id=lines[-1].id
            ),
            BranchOption(
                id="branch-future-forecast",
                title="The 2030 Horizon: What Comes Next?",
                description="A speculative forecast mapping the 5-year trajectory and disruptive catalysts.",
                teaser_line="Maya and Leo debate the highest-probability scenarios for 2030.",
                branch_point_line_id=lines[-1].id
            )
        ]

        # Synthesize Knowledge Graph
        kg = [
            KnowledgeEntity(
                id=f"kg-core-{bid}",
                label=core_subject,
                category="technology",
                description=f"Core subject entity representing foundational advances in {clean_topic}.",
                connections=[f"kg-scale-{bid}", f"kg-ethics-{bid}"]
            ),
            KnowledgeEntity(
                id=f"kg-scale-{bid}",
                label="Autonomous Scalability",
                category="concept",
                description="The capacity of systems to expand throughput without proportional human intervention.",
                connections=[f"kg-core-{bid}", f"kg-market-{bid}"]
            ),
            KnowledgeEntity(
                id=f"kg-ethics-{bid}",
                label="Synthesized Governance",
                category="metric",
                description="Dynamic policy frameworks regulating automated generation and synthetic media.",
                connections=[f"kg-core-{bid}"]
            ),
            KnowledgeEntity(
                id=f"kg-market-{bid}",
                label="Generative Economics",
                category="impact",
                description="Economic restructuring driven by near-zero marginal production costs for personalized media.",
                connections=[f"kg-scale-{bid}"]
            )
        ]

        # Synthesize Perspectives
        perspectives = [
            PerspectiveScore(dimension="Innovation Velocity", score=91, summary=f"Breakneck iteration cadence in {clean_topic} research."),
            PerspectiveScore(dimension="Societal Friction", score=58, summary="Ongoing cultural adjustment and legacy policy friction."),
            PerspectiveScore(dimension="Market Readiness", score=84, summary="High enterprise and consumer interest with rapid productization."),
            PerspectiveScore(dimension="Personalization Power", score=96, summary="Unprecedented capacity to adapt content to individual cognitive styles.")
        ]

        # Social assets
        social_assets = {
            "viral_headline": f"Why {clean_topic} Will Redefine Digital Experiences in 2026",
            "thread_post": f"1/4 Everything you thought you knew about {clean_topic} just changed. Dr. Maya Vance and Leo Cruz unpack the architectural breakthroughs and cultural shifts live on OmniStory Studio. 🧵👇",
            "linkedin_take": f"Leaders in media and technology need to pay attention to {clean_topic}. The transition from passive broadcasting to interactive, personalized synthesis is happening now. Are you ready?",
            "short_script_hook": f"[VISUAL: Hologram flickering on] 'What happens when {clean_topic} becomes as ubiquitous as the smartphone?'"
        }

        manifest = BroadcastManifest(
            id=bid,
            title=f"{clean_topic}: The Next Horizon",
            subtitle=f"An Autonomous Deep Dive into the Foundations and Futures of {clean_topic}",
            source_topic=clean_topic,
            persona_style=style,
            duration_est="3m 30s",
            summary=f"A dynamic, multi-agent broadcast analyzing the technical mechanics, cultural ripple effects, and strategic imperatives of {clean_topic}.",
            key_takeaways=[
                f"Breakthrough acceleration in {clean_topic} is reshaping digital ecosystems.",
                "Audience personalization has surpassed generic broadcast distribution.",
                "Multi-agent AI studios allow instant interactive co-creation.",
                "Interactive governance models are essential as synthetic media scales."
            ],
            lines=lines,
            branches=branches,
            knowledge_graph=kg,
            perspectives=perspectives,
            social_assets=social_assets
        )

        BROADCAST_STORE[bid] = manifest
        return manifest

    @classmethod
    def handle_interrupt(cls, req: InterruptRequest) -> Dict:
        """
        Handles real-time audience interruption/question:
        Co-hosts acknowledge the question in character, discuss the nuance, and bridge back smoothly.
        """
        broadcast = BROADCAST_STORE.get(req.broadcast_id)
        topic = broadcast.source_topic if broadcast else "this topic"
        q = req.user_question.strip()

        # Generate contextual host responses
        inter_id = f"inter-{uuid.uuid4().hex[:6]}"

        maya_response = (
            f"Fascinating question from our live audience: '{q}'! "
            f"From an analytical lens, this pinpoints the exact tension in {topic}. "
            f"If we examine the empirical evidence, the solution isn't black or white—it hinges on architectural transparency."
        )

        leo_response = (
            f"I love this question! That's exactly what critics often miss. "
            f"In real-world applications, user experience and trust will make or break how this is received. "
            f"Maya, that leads straight back into the point we were just diving into!"
        )

        interruption_lines = [
            DialogueLine(
                id=f"{inter_id}-audience",
                speaker=DialogueSpeaker.AUDIENCE,
                speaker_name="Live Audience Question",
                text=f"Audience Question: \"{q}\"",
                emotion=EmotionValence.CURIOUS,
                pitch=1.0,
                rate=1.0,
                visual_cue="studio_pulse",
                chapter="Live Audience Q&A",
                highlight_terms=[q],
                timestamp_est=0
            ),
            DialogueLine(
                id=f"{inter_id}-maya",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text=maya_response,
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.04,
                rate=1.04,
                visual_cue="neural_glow",
                chapter="Live Audience Q&A",
                highlight_terms=["Analytical lens", "Architectural transparency"],
                timestamp_est=5
            ),
            DialogueLine(
                id=f"{inter_id}-leo",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text=leo_response,
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=0.98,
                rate=1.06,
                visual_cue="cyber_grid",
                chapter="Live Audience Q&A",
                highlight_terms=["User experience", "Trust"],
                timestamp_est=15
            )
        ]

        return {
            "status": "success",
            "broadcast_id": req.broadcast_id,
            "question": q,
            "dialogue_injection": [line.dict() for line in interruption_lines]
        }

    @classmethod
    def expand_branch(cls, broadcast_id: str, branch_id: str) -> List[DialogueLine]:
        """
        Dynamically synthesizes new dialogue when the user selects a story branch.
        """
        broadcast = BROADCAST_STORE.get(broadcast_id)
        topic = broadcast.source_topic if broadcast else "our topic"

        branch_title = branch_id.replace("branch-", "").replace("-", " ").title()

        b_lines = [
            DialogueLine(
                id=f"ext-{uuid.uuid4().hex[:6]}-1",
                speaker=DialogueSpeaker.NARRATOR,
                speaker_name="OmniStory Switchboard",
                text=f"Branch selected by audience: {branch_title}. Redirecting narrative stream.",
                emotion=EmotionValence.DRAMATIC,
                pitch=1.0,
                rate=1.0,
                visual_cue="quantum_lattice",
                chapter=f"Branch: {branch_title}",
                highlight_terms=[branch_title],
                timestamp_est=0
            ),
            DialogueLine(
                id=f"ext-{uuid.uuid4().hex[:6]}-2",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text=f"Taking this angle on {topic} unlocks critical new data. Look closely at how the underlying mechanisms operate in this specific domain.",
                emotion=EmotionValence.ANALYTICAL,
                pitch=1.03,
                rate=1.04,
                visual_cue="neural_glow",
                chapter=f"Branch: {branch_title}",
                highlight_terms=["Mechanisms", "Underlying data"],
                timestamp_est=6
            ),
            DialogueLine(
                id=f"ext-{uuid.uuid4().hex[:6]}-3",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text=f"And what makes {branch_title} so compelling is that human intuition alone wouldn't have anticipated this convergence six months ago. It changes the entire playing field!",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=0.98,
                rate=1.06,
                visual_cue="studio_pulse",
                chapter=f"Branch: {branch_title}",
                highlight_terms=[branch_title, "Convergence"],
                timestamp_est=17
            ),
            DialogueLine(
                id=f"ext-{uuid.uuid4().hex[:6]}-4",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text=f"Which brings us back to our foundational premise: media is no longer static consumption. It is a living, responsive ecosystem shaped by curious minds like yours.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.04,
                rate=1.02,
                visual_cue="biolum_synth",
                chapter=f"Branch: {branch_title}",
                highlight_terms=["Living ecosystem", "Responsive media"],
                timestamp_est=28
            )
        ]

        if broadcast:
            broadcast.lines.extend(b_lines)

        return b_lines
