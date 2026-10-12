from app.models import BroadcastManifest, DialogueLine, DialogueSpeaker, EmotionValence, BranchOption, KnowledgeEntity, PerspectiveScore, PersonaStyle

SAMPLE_BROADCASTS = {
    "health-equity": BroadcastManifest(
        id="health-equity",
        title="Democratizing Public Health: AI Translation of Medical Science for All",
        subtitle="Bridging the Cognitive & Health Divide: Transforming Clinical Research into Accessible, Misinformation-Resistant Community Media",
        source_topic="Public Health Equity, Accessible Medical Communication & Misinformation Defense",
        persona_style=PersonaStyle.ELI5,
        duration_est="4m 20s",
        summary="A deeply impactful broadcast solving the social divide in healthcare literacy. Dr. Maya Vance and Leo Cruz translate complex clinical trials, vaccine efficacy studies, and preventative metabolic science into clear, empathetic, and culturally accessible knowledge for underserved communities.",
        key_takeaways=[
            "Over 65% of adults struggle to understand complex medical research papers and clinical guidelines.",
            "Multimodal AI translation closes the health literacy gap by turning jargon into intuitive visual and audio analogies.",
            "Real-time Socratic Q&A directly debunks dangerous social media health misinformation with verified peer-reviewed evidence.",
            "Accessible digital media empowers marginalized patients to advocate for their own care."
        ],
        lines=[
            DialogueLine(
                id="he-1",
                speaker=DialogueSpeaker.NARRATOR,
                speaker_name="OmniStory Social Impact Dispatch",
                text="Knowledge is health. Welcome to OmniStory Equity: Translating life-saving medical science for every community, regardless of background or education.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.0,
                rate=1.0,
                visual_cue="biolum_synth",
                chapter="The Health Literacy Divide",
                highlight_terms=["Health Equity", "Medical Science", "Accessible Knowledge"],
                timestamp_est=0
            ),
            DialogueLine(
                id="he-2",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Leo, consider this heartbreaking public health statistic: the average peer-reviewed medical paper is written at a postgraduate reading level, yet 54% of global adults read at or below a sixth-grade level. When life-saving cardiovascular and immunization research is locked in dense academic prose, the result is avoidable suffering and the rapid spread of viral misinformation.",
                emotion=EmotionValence.ANALYTICAL,
                pitch=1.02,
                rate=1.03,
                visual_cue="neural_glow",
                chapter="The Literacy Crisis",
                highlight_terms=["Postgraduate reading level", "Sixth-grade level", "Avoidable suffering"],
                timestamp_est=8
            ),
            DialogueLine(
                id="he-3",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="And Maya, predatory health influencers exploit that exact gap every single day! When a community center or a worried mother searches online for symptoms, algorithms feed them sensationalized conspiracy cures because the legitimate scientific consensus is buried behind jargon and paywalls. We have to make real science as engaging, visual, and empathetic as the rumors.",
                emotion=EmotionValence.DRAMATIC,
                pitch=0.98,
                rate=1.06,
                visual_cue="studio_pulse",
                chapter="The Misinformation Trap",
                highlight_terms=["Predatory health influencers", "Conspiracy cures", "Empathetic communication"],
                timestamp_est=21
            ),
            DialogueLine(
                id="he-4",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="That is the core mission of multimodal AI translation. Instead of forcing a patient to decipher terms like 'monoclonal antibody binding kinetics,' our system converts it into an intuitive visual story: imagine custom-crafted security keys that gently disable the lock on a virus without harming the surrounding healthy neighborhood of cells.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.04,
                rate=1.02,
                visual_cue="quantum_lattice",
                chapter="Intuitive Analogies",
                highlight_terms=["Multimodal AI translation", "Security keys analogy", "Cellular defense"],
                timestamp_est=34
            ),
            DialogueLine(
                id="he-5",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="And because it's interactive, a patient who is skeptical or anxious doesn't just get talked at—they can interrupt our broadcast, ask their personal fear or doubt in their own words, and get an honest, compassionate, peer-reviewed explanation without being judged or dismissed.",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=1.0,
                rate=1.05,
                visual_cue="cyber_grid",
                chapter="Compassionate Interactivity",
                highlight_terms=["Interactive patient agency", "Compassionate response", "Peer-reviewed truth"],
                timestamp_est=47
            ),
            DialogueLine(
                id="he-6",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Audience, this is your living classroom. Which health equity frontier should we tackle next? Tap a path below or type your personal question directly to us.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.03,
                rate=1.02,
                visual_cue="biolum_synth",
                chapter="Community Action Point",
                highlight_terms=["Community Action Point", "Health Equity"],
                timestamp_est=59
            )
        ],
        branches=[
            BranchOption(
                id="branch-vaccine-literacy",
                title="Vaccine & Immunization Transparency",
                description="How mRNA and adjuvants actually work inside the body, explained with zero jargon and full clinical rigor.",
                teaser_line="Maya explains how cellular memory cells protect against mutations.",
                branch_point_line_id="he-6"
            ),
            BranchOption(
                id="branch-chronic-nutrition",
                title="Chronic Disease Prevention in Underserved Areas",
                description="Translating metabolic science into affordable, culturally relevant nutritional strategies for food deserts.",
                teaser_line="Leo dives into low-cost grocery hacks backed by metabolic endocrinology.",
                branch_point_line_id="he-6"
            ),
            BranchOption(
                id="branch-clinical-trials",
                title="Inclusive Clinical Trial Access",
                description="Overcoming historic distrust and expanding diverse demographic participation in cutting-edge therapies.",
                teaser_line="Maya and Leo analyze patient rights, informed consent, and community-led research boards.",
                branch_point_line_id="he-6"
            )
        ],
        knowledge_graph=[
            KnowledgeEntity(
                id="kg-health-literacy",
                label="Health Literacy Divide",
                category="concept",
                description="The disparity in ability to obtain, process, and understand basic health information needed to make informed decisions.",
                connections=["kg-misinfo-defense", "kg-multimodal-translation"]
            ),
            KnowledgeEntity(
                id="kg-multimodal-translation",
                label="Multimodal AI Translation",
                category="technology",
                description="AI pipelines that deconstruct dense clinical nomenclature into accessible diagrams, audio narratives, and analogies.",
                connections=["kg-health-literacy", "kg-patient-agency"]
            ),
            KnowledgeEntity(
                id="kg-misinfo-defense",
                label="Misinformation Defense Matrix",
                category="metric",
                description="Real-time automated fact-checking comparing viral social media health claims against PubMed, CDC, and WHO databases.",
                connections=["kg-health-literacy", "kg-multimodal-translation"]
            ),
            KnowledgeEntity(
                id="kg-patient-agency",
                label="Empowered Patient Agency",
                category="impact",
                description="Equipping individuals with the self-confidence and vocabulary to ask critical questions during physician consults.",
                connections=["kg-multimodal-translation"]
            )
        ],
        perspectives=[
            PerspectiveScore(dimension="Social Inclusion Impact", score=98, summary="Directly democratizes life-saving clinical knowledge across varied literacy levels and age groups."),
            PerspectiveScore(dimension="Misinformation Resistance", score=92, summary="Empowers citizens to spot predatory algorithmic pseudoscience and false claims."),
            PerspectiveScore(dimension="Clinical Alignment (PubMed)", score=95, summary="Anchored strictly in peer-reviewed clinical research and consensus medical guidelines."),
            PerspectiveScore(dimension="Global Scalability (GCP)", score=94, summary="Scalable via Google Cloud Run and Vertex AI to translate across hundreds of regional dialects.")
        ],
        social_assets={
            "viral_headline": "Why 50% of the World Can't Understand Their Doctor (And How AI Changes That)",
            "thread_post": "1/6 When medical breakthroughs are locked in academic jargon, misinformation wins and communities suffer. In our latest OmniStory Social Impact session, Dr. Maya Vance and Leo Cruz demonstrate how multimodal AI turns complex clinical trials into life-saving, accessible knowledge for everyone. 🩺❤️👇",
            "linkedin_take": "Health literacy is a fundamental civil right. By deploying multimodal AI engines on Google Cloud to translate complex research into accessible, interactive audio-visual dialogues, we can eliminate the dangerous barrier between peer-reviewed science and the patients who need it most.",
            "short_script_hook": "[VISUAL: A doctor's clipboard filled with illegible medical symbols transforming into a glowing, friendly 3D animation] 'What if you never had to nod along pretending you understood your lab results ever again?'"
        }
    ),

    "climate-resilience": BroadcastManifest(
        id="climate-resilience",
        title="Actionable Climate Resilience: From IPCC Data to Community Action",
        subtitle="Empowering Vulnerable Communities to Understand Local Climate Risks & Drive Grassroots Solutions",
        source_topic="Climate Literacy, Environmental Justice & Community Resilience",
        persona_style=PersonaStyle.DEEP_DIVE,
        duration_est="4m 40s",
        summary="A transformative broadcast translating complex planetary climate models and international policy into tangible, neighborhood-scale resilience strategies for frontline communities.",
        key_takeaways=[
            "Dense 3,000-page IPCC climate reports often create anxiety and fatalism rather than civic agency.",
            "Interactive AI media personalizes global planetary telemetry into actionable neighborhood interventions.",
            "Grassroots climate adaptation requires inclusive, multi-format media accessible on low-bandwidth mobile devices.",
            "Community energy transitions create local green union jobs and energy independence."
        ],
        lines=[
            DialogueLine(
                id="cr-1",
                speaker=DialogueSpeaker.NARRATOR,
                speaker_name="OmniStory Social Impact Dispatch",
                text="The climate crisis is a communication crisis. Welcome to Actionable Climate Resilience: turning global telemetry into neighborhood power.",
                emotion=EmotionValence.DRAMATIC,
                pitch=1.0,
                rate=1.0,
                visual_cue="biolum_synth",
                chapter="From Doom to Action",
                highlight_terms=["Climate Communication", "Neighborhood Power"],
                timestamp_est=0
            ),
            DialogueLine(
                id="cr-2",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Leo, when the IPCC releases a 3,000-page assessment report filled with complex climate sensitivity calculations and SSP emission pathways, the general public doesn't feel empowered—they feel overwhelmed and paralyzed. We have failed the communication test of our century.",
                emotion=EmotionValence.ANALYTICAL,
                pitch=1.02,
                rate=1.03,
                visual_cue="quantum_lattice",
                chapter="The Paralysis Gap",
                highlight_terms=["3,000-page report", "SSP emission pathways", "Overwhelmed public"],
                timestamp_est=8
            ),
            DialogueLine(
                id="cr-3",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="Exactly, Maya! A smallholder farmer in South Asia or a resident in an urban heat island in Chicago doesn't need abstract global temperature anomalies for 2100. They need to know: what is happening to our water aquifer next month? How do we build microgrid solar resilience before the next storm?",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=0.98,
                rate=1.06,
                visual_cue="studio_pulse",
                chapter="Hyper-Local Relevance",
                highlight_terms=["Urban heat island", "Microgrid solar resilience", "Water aquifer"],
                timestamp_est=20
            ),
            DialogueLine(
                id="cr-4",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="That is why adaptive media is essential for environmental justice. By querying satellite telemetry and local weather APIs through Google Cloud, our system synthesizes custom localized broadcasts in seconds, showing community members exactly where urban green canopies or rain harvesting will reduce local temperatures by up to four degrees Celsius.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.04,
                rate=1.02,
                visual_cue="cyber_grid",
                chapter="Satellite Telemetry to Grassroots",
                highlight_terms=["Environmental justice", "Satellite telemetry", "Urban green canopies"],
                timestamp_est=33
            ),
            DialogueLine(
                id="cr-5",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="And it replaces fatalistic doom-scrolling with actionable community solidarity. When people understand the physics and the economic benefits, climate action transforms into community wealth and health.",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=1.0,
                rate=1.05,
                visual_cue="neural_glow",
                chapter="Community Wealth",
                highlight_terms=["Community solidarity", "Actionable wealth"],
                timestamp_est=46
            ),
            DialogueLine(
                id="cr-6",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Let's build this together. Audience, choose your local resilience action track below.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.02,
                rate=1.02,
                visual_cue="biolum_synth",
                chapter="Action Switchboard",
                highlight_terms=["Resilience action track"],
                timestamp_est=57
            )
        ],
        branches=[
            BranchOption(
                id="branch-urban-cooling",
                title="Urban Heat Island Mitigation",
                description="Community-led cool roofs, urban tree canopies, and permeable asphalt that drop street-level temperatures.",
                teaser_line="Maya breaks down the physics of albedo and shade thermodynamics.",
                branch_point_line_id="cr-6"
            ),
            BranchOption(
                id="branch-community-microgrids",
                title="Decentralized Clean Solar Microgrids",
                description="How neighborhoods can generate, store, and share renewable power during grid outages.",
                teaser_line="Leo analyzes battery storage economics and municipal cooperative financing.",
                branch_point_line_id="cr-6"
            ),
            BranchOption(
                id="branch-water-harvesting",
                title="Groundwater & Flood Resilience",
                description="Bio-swales, sponge city design, and rainwater catchment systems for climate extremes.",
                teaser_line="Maya and Leo explain low-cost ecological civil engineering.",
                branch_point_line_id="cr-6"
            )
        ],
        knowledge_graph=[
            KnowledgeEntity(
                id="kg-urban-heat",
                label="Urban Heat Island Effect",
                category="concept",
                description="Dense built environments absorbing and retaining solar heat, disproportionately impacting lower-income neighborhoods.",
                connections=["kg-sponge-city", "kg-microgrid"]
            ),
            KnowledgeEntity(
                id="kg-microgrid",
                label="Community Microgrids",
                category="technology",
                description="Localized distributed energy grids capable of operating autonomously during extreme weather events.",
                connections=["kg-urban-heat", "kg-eco-equity"]
            ),
            KnowledgeEntity(
                id="kg-sponge-city",
                label="Sponge City Engineering",
                category="technology",
                description="Urban water management mimicking nature to absorb, clean, and reuse storm rainfall.",
                connections=["kg-urban-heat"]
            ),
            KnowledgeEntity(
                id="kg-eco-equity",
                label="Environmental Justice",
                category="impact",
                description="Fair distribution of environmental benefits and protections against ecological hazards for all populations.",
                connections=["kg-microgrid", "kg-urban-heat"]
            )
        ],
        perspectives=[
            PerspectiveScore(dimension="Civic Empowerment", score=97, summary="Transforms climate anxiety into proactive community organizing and local infrastructure projects."),
            PerspectiveScore(dimension="Scientific Accuracy (IPCC)", score=96, summary="Faithfully reflects consensus thermodynamic, meteorological, and hydrological data."),
            PerspectiveScore(dimension="Economic Feasibility", score=88, summary="Prioritizes high-ROI green infrastructure with rapid payback cycles for municipalities."),
            PerspectiveScore(dimension="Low-Bandwidth Mobile Access", score=95, summary="Engineered for instant streaming on low-cost mobile devices across the Global South.")
        ],
        social_assets={
            "viral_headline": "Stop Doomscrolling: How Communities Are Cooling Their Streets by 4°C",
            "thread_post": "1/5 The IPCC report is 3,000 pages of dense climate data. But here is what it means for your actual neighborhood street, and how ordinary communities are building solar microgrids and cool canopies right now. 🌳⚡👇",
            "linkedin_take": "Climate communication is broken. If we want global climate resilience, we must replace abstract graphs with localized, participatory digital media. Here is how OmniStory on Google Cloud is democratizing planetary telemetry for grassroots environmental justice.",
            "short_script_hook": "[VISUAL: Thermal infrared satellite camera zooming into an asphalt neighborhood, cooling down from red to calm green] 'What if your neighborhood could cut its summer heatwave temperature by 4 degrees without waiting for politicians?'"
        }
    ),

    "hollywood-3": BroadcastManifest(
        id="hollywood-3",
        title="Hollywood 3.0: Autonomous Studios & The Death of Linear Cinema",
        subtitle="How Generative Media, Neural Rendering, and Interactive Story Engines Are Rewriting Entertainment",
        source_topic="Generative Media, Virtual Actors & The Future of Film",
        persona_style=PersonaStyle.DEEP_DIVE,
        duration_est="4m 45s",
        summary="An exhilarating investigation into the paradigm shift from pre-rendered 2-hour films to living, adaptive narrative engines where viewers interact with virtual actors and reshape story arcs in real time.",
        key_takeaways=[
            "Linear pre-rendered video is transitioning toward real-time procedural narrative engines.",
            "Synthetic digital humans with persistent memory are challenging traditional acting and royalty models.",
            "Audience engagement is shifting from passive observation to participatory co-creation.",
            "Content distribution economics will migrate from subscription streaming to interactive compute-per-story."
        ],
        lines=[
            DialogueLine(
                id="h3-1",
                speaker=DialogueSpeaker.NARRATOR,
                speaker_name="OmniStory Broadcast",
                text="Welcome to OmniStory Live. Today's dispatch: Hollywood 3.0 and the collapse of the 120-minute static film reel.",
                emotion=EmotionValence.DRAMATIC,
                pitch=1.0,
                rate=1.0,
                visual_cue="cyber_grid",
                chapter="Opening Dispatch",
                highlight_terms=["Hollywood 3.0", "Static Film Reel"],
                timestamp_est=0
            ),
            DialogueLine(
                id="h3-2",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Leo, look at the production metrics from the last quarter. 64% of digital visual effects pipelines now incorporate neural diffusion or Gaussian splatting. We aren't just speeding up VFX—we're seeing the end of the traditional camera.",
                emotion=EmotionValence.ANALYTICAL,
                pitch=1.02,
                rate=1.05,
                visual_cue="neural_glow",
                chapter="VFX Paradigm Shift",
                highlight_terms=["Gaussian splatting", "Neural diffusion", "VFX pipelines"],
                timestamp_est=7
            ),
            DialogueLine(
                id="h3-3",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="Maya, that sounds incredible from a tech standpoint, but ask any screenwriter or director. They don't just care about rendering speeds; they care about visceral emotional truth. Can an AI-directed scene actually make a theater weep or hold its breath?",
                emotion=EmotionValence.SKEPTICAL,
                pitch=0.96,
                rate=1.08,
                visual_cue="studio_pulse",
                chapter="The Emotional Core",
                highlight_terms=["Emotional truth", "AI-directed scene", "Visceral storytelling"],
                timestamp_est=17
            ),
            DialogueLine(
                id="h3-4",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="That's the conventional skepticism, Leo, but here's the surprise: the emotional resonance is actually amplified when the narrative adapts to the viewer. When a film's protagonist looks straight at you, recognizes your reaction, and subtly shifts their dialogue, the uncanny valley inverts into profound intimacy.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.05,
                rate=1.02,
                visual_cue="quantum_lattice",
                chapter="Adaptive Resonance",
                highlight_terms=["Emotional resonance", "Adaptive narrative", "Interactive protagonist"],
                timestamp_est=29
            ),
            DialogueLine(
                id="h3-5",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="Wait—so you're telling me we're moving away from 'everyone watches the exact same movie on Friday night' to personalized narrative multiverses? What happens to the shared cultural watercooler moment?",
                emotion=EmotionValence.CURIOUS,
                pitch=0.98,
                rate=1.1,
                visual_cue="nebula_space",
                chapter="Cultural Watercooler",
                highlight_terms=["Narrative multiverses", "Cultural watercooler"],
                timestamp_est=42
            ),
            DialogueLine(
                id="h3-6",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="The watercooler doesn't die; it transforms. Instead of discussing 'did you see what happened to the character in scene four,' friends compare how their differing choices tested the character's moral boundaries. The conversation becomes about philosophy, not spoilers.",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=1.04,
                rate=1.04,
                visual_cue="biolum_synth",
                chapter="The New Conversation",
                highlight_terms=["Moral boundaries", "Philosophy over spoilers", "Participatory media"],
                timestamp_est=53
            ),
            DialogueLine(
                id="h3-7",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="Let's talk about the economic battlefield. Legacy studios are sitting on century-old IP vaults. If independent creators can spin up Pixar-grade animated features on a consumer GPU in two weeks, what protects a billion-dollar franchise?",
                emotion=EmotionValence.ANALYTICAL,
                pitch=0.95,
                rate=1.06,
                visual_cue="cyber_grid",
                chapter="Studio Economics",
                highlight_terms=["Century-old IP", "Pixar-grade animation", "GPU democratization"],
                timestamp_est=66
            ),
            DialogueLine(
                id="h3-8",
                speaker=DialogueSpeaker.MAYA,
                speaker_name="Dr. Maya Vance",
                text="Franchises will survive only if they open up their canon. The future belongs to 'permissionless world-building'—studios licensing their worlds to fans who build official canonical spin-offs with revenue splits mediated by smart contracts.",
                emotion=EmotionValence.INSIGHTFUL,
                pitch=1.03,
                rate=1.03,
                visual_cue="quantum_lattice",
                chapter="Permissionless Canon",
                highlight_terms=["Permissionless world-building", "Canonical spin-offs", "Revenue splits"],
                timestamp_est=78
            ),
            DialogueLine(
                id="h3-9",
                speaker=DialogueSpeaker.LEO,
                speaker_name="Leo Cruz",
                text="And right now, audience, we stand at a critical fork in this story. You have the director's switchboard. Which direction should we explore next?",
                emotion=EmotionValence.ENTHUSIASTIC,
                pitch=1.0,
                rate=1.05,
                visual_cue="studio_pulse",
                chapter="Audience Choice Point",
                highlight_terms=["Director switchboard", "Branching path"],
                timestamp_est=90
            )
        ],
        branches=[
            BranchOption(
                id="branch-ip-wars",
                title="The Guild & IP Wars",
                description="Investigate the legal, labor, and copyright showdown between Hollywood unions and generative platforms.",
                teaser_line="Maya breaks down the landmark digital likeness agreements and royalty contracts.",
                branch_point_line_id="h3-9"
            ),
            BranchOption(
                id="branch-interactive-cinema",
                title="Real-Time Holographic Engines",
                description="Explore the technical breakthrough of rendering interactive 3D cinema in Unreal Engine 5.5 and WebGPU.",
                teaser_line="Leo examines how viewers step inside movie sets with VR and neural radiance fields.",
                branch_point_line_id="h3-9"
            ),
            BranchOption(
                id="branch-indie-renaissance",
                title="The 1-Person Blockbuster",
                description="How solo directors are winning festivals with end-to-end AI pipelines on modest budgets.",
                teaser_line="Maya and Leo analyze the first Oscar-nominated film produced by a 3-person team.",
                branch_point_line_id="h3-9"
            )
        ],
        knowledge_graph=[
            KnowledgeEntity(
                id="k-gaussian",
                label="3D Gaussian Splatting",
                category="technology",
                description="Radiance field technique enabling real-time 60fps rendering of photorealistic 3D volumetric environments.",
                connections=["k-neural-cinema", "k-virtual-actors"]
            ),
            KnowledgeEntity(
                id="k-neural-cinema",
                label="Neural Story Engines",
                category="technology",
                description="Language model agents integrated with physics and rendering engines to dynamically steer character decisions.",
                connections=["k-gaussian", "k-ip-licensing", "k-interactive-branching"]
            ),
            KnowledgeEntity(
                id="k-virtual-actors",
                label="Synthetic Digital Humans",
                category="concept",
                description="Photorealistic virtual performers capable of speech, emotional nuance, and persistent multi-film character continuity.",
                connections=["k-gaussian", "k-ip-licensing"]
            ),
            KnowledgeEntity(
                id="k-interactive-branching",
                label="Procedural Story Trees",
                category="concept",
                description="Dynamic narrative architectures that fork based on audience sentiment, gaze tracking, or explicit choices.",
                connections=["k-neural-cinema"]
            ),
            KnowledgeEntity(
                id="k-ip-licensing",
                label="Open Canon Licensing",
                category="metric",
                description="Decentralized IP revenue models allowing fans and community creators to monetize canonical franchise lore.",
                connections=["k-virtual-actors", "k-neural-cinema"]
            )
        ],
        perspectives=[
            PerspectiveScore(dimension="Creative Democratization", score=94, summary="Enables indie storytellers to achieve Hollywood-scale visual fidelity on micro-budgets."),
            PerspectiveScore(dimension="Labor & Actor Sovereignty", score=48, summary="Intense ongoing negotiations regarding digital likeness consent, residuals, and deepfake vulnerabilities."),
            PerspectiveScore(dimension="Audience Immersion Index", score=89, summary="Personalized story steering dramatically increases user engagement and repeat exploration."),
            PerspectiveScore(dimension="Technical Viability (2026)", score=82, summary="WebGPU and edge neural models allow near real-time synthesis directly in browser runtimes.")
        ],
        social_assets={
            "viral_headline": "Why Hollywood's Next Blockbuster Might Not Be a Movie at All",
            "thread_post": "1/5 The 120-minute static film reel is dying. In our latest OmniStory dispatch, Dr. Maya Vance and Leo Cruz unpack Hollywood 3.0—where movies become living, interactive story engines powered by neural radiance fields. Here's what changes forever: 🧵👇",
            "linkedin_take": "The entertainment industry is facing its biggest transition since the invention of sound. As generative rendering and AI co-stars mature, content is moving from passive consumption to active co-creation. Are media brands ready for permissionless canon?",
            "short_script_hook": "[VISUAL: Studio control room glitching into a 3D hologram] 'What if you didn't just watch the climax of your favorite thriller... what if the villain looked at your webcam and changed his plan?'"
        }
    )
}
