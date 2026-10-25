# A Mini-Project Report on
# DOMAIN-SPECIFIC CONVERSATIONAL AI AGENT FOR VIDEO GAME NPCS: CHRONICLES OF PRASA

**Submitted by:**
- **Prasad Kankhar** (Roll No: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)
- **Student Partner** (Roll No: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)

**Under the guidance of:**
- **Mrs. Sarika Zile / Ms. Priya Khandelwal / Ms. Pooja Alone**

**Department of Computer Science and Engineering**  
**Maharashtra Institute of Technology, Chhatrapati Sambhajinagar**  
*(An Autonomous Institute, Affiliated to Dr. BAMU)*  
[Academic Year: 2026-27]

---

## CERTIFICATE

This is to certify that the mini-project report entitled **"DOMAIN-SPECIFIC CONVERSATIONAL AI AGENT FOR VIDEO GAME NPCS: CHRONICLES OF PRASA"** is a bonafide work carried out by **Prasad Kankhar** and team in partial fulfillment for the award of degree of **Bachelor of Technology in Computer Science and Engineering** during the academic year 2026-2027.

The project has been evaluated as the 10th Practical Evaluation for the Discipline Specific Skill Course Laboratory – AI Agent Development.

---

## ACKNOWLEDGEMENT

We express our sincere gratitude to our respected Course Coordinators **Mrs. Sarika Zile, Ms. Priya Khandelwal, and Ms. Pooja Alone** for their invaluable guidance, encouragement, and insightful feedback throughout the conception and implementation of this AI Agent Mini-Project.

We also extend our heartfelt thanks to the Head of Department and Maharashtra Institute of Technology for providing state-of-the-art computational infrastructure and laboratories which enabled the successful deployment and testing of this project.

---

## ABSTRACT

Traditional non-player characters (NPCs) in computer video games rely heavily on rigid decision trees, static rule scripts, and predetermined dialogue branches. These conventional architectures result in repetitive interactions, lack of conversational context, and an inability to dynamically synthesize narrative lore. This project presents the design, architectural development, and production deployment of **"Chronicles of Prasa"**, a domain-specific autonomous conversational AI agent embodied as an in-game archivist NPC named *Eldrin*.

The system leverages state-of-the-art Large Language Model (LLM) inference (Groq Cloud / GPT-OSS architectures), prompt engineering persona guardrails, functional tool execution (`read_lore`), and short-term sliding window memory. The agent strictly restricts responses to in-game lore, preventing hallucinations or out-of-domain query leakage. A client-server architecture was engineered offering dual accessibility: a local containerized FastAPI backend with environment key protection, and a serverless deployment hosted on GitHub Pages utilizing client-side Web Audio API 8-bit sound synthesizers and browser Text-to-Speech (TTS). The project fulfills the requirements of Practical 10 by providing an end-to-end, domain-specific, fully documented AI Agent solution.

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction & Problem Statement**
   - 1.1 Background
   - 1.2 Problem Statement
   - 1.3 Project Objectives
2. **Chapter 2: Literature Review & Technology Stack**
   - 2.1 Evolution of Conversational Agents
   - 2.2 Hardware and Software Stack
3. **Chapter 3: System Architecture & Design**
   - 3.1 System Block Diagram
   - 3.2 Dual Environment Architecture
4. **Chapter 4: Implementation Details**
   - 4.1 Knowledge Base Construction (`game_lore.txt`)
   - 4.2 Tool Definition & Execution Pipeline (`api.py`)
   - 4.3 Conversational State Memory
   - 4.4 Gamified Frontend & Audio Synthesis (`index.html`)
   - 4.5 Production Deployment Configuration (`Dockerfile` & GitHub Pages)
5. **Chapter 5: Results, Test Scenarios & Demonstration**
   - 5.1 Test Scenario 1: In-Domain Knowledge Retrieval
   - 5.2 Test Scenario 2: Out-of-Domain Guardrail Enforcement
   - 5.3 Test Scenario 3: Inventory Interaction & Audio Feedback
   - 5.4 Test Scenario 4: Live GitHub Pages Deployment
6. **Chapter 6: Conclusion & Future Scope**
   - 6.1 Conclusion
   - 6.2 Future Enhancements
7. **References**

---

## CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT

### 1.1 Background
In modern computer science and interactive entertainment systems, conversational agents play a critical role in user engagement. With the rapid evolution of Large Language Models (LLMs), artificial intelligence agents have shifted from simple pattern-matching bots to autonomous cognitive entities capable of reasoning, recalling contextual history, and invoking programmatic external tools.

However, deploying generic LLMs inside specialized domains—such as healthcare, enterprise customer support, or gaming environments—presents critical challenges: prompt drift, hallucination of facts, loss of persona consistency, and out-of-domain query leakage. A truly domain-specific agent must possess strict boundary constraints, dedicated knowledge retrieval mechanisms, and a cohesive user interface tailored to the end user.

### 1.2 Problem Statement
Traditional video game NPCs rely on static, hardcoded dialogue options that break immersion when a player seeks dynamic information about the game world. Conversely, if a standard, unconstrained LLM is embedded into a game, it may break character by answering real-world homework, solving math equations, or discussing modern political topics, entirely destroying the game's narrative immersion.

The goal of this Mini-Project is to design, develop, test, and deploy a **Domain-Specific Conversational AI Agent** that:
1. Acts as an authentic in-game NPC ("Eldrin the Archivist") within the fantasy world of *Chronicles of Prasa*.
2. Enforces strict domain guardrails, politely refusing out-of-domain real-world questions while maintaining persona.
3. Dynamically retrieves factual lore from an external knowledge base (`game_lore.txt`) using tool-calling capabilities.
4. Maintains multi-turn conversational memory so user follow-ups are coherent.
5. Provides an immersive, retro-gamified Web UI with audio synthesis, voice output, and dual deployment (Localhost & GitHub Pages).

### 1.3 Project Objectives
- **Persona & Prompt Engineering:** Implement a system prompt that locks the model into an ancient fantasy archivist tone.
- **Tool-Enabled Knowledge Grounding:** Integrate an external tool (`read_lore`) so the agent dynamically cites accurate project attributes (developer name, engine stack, story).
- **Memory Retention:** Support continuous multi-turn dialogue history.
- **Deployment Versatility:** Ensure cross-environment execution across local containerized FastAPI and serverless GitHub Pages.

---

## CHAPTER 2: LITERATURE REVIEW & TECHNOLOGY STACK

### 2.1 Evolution of Conversational Agents
The architectural progression of AI conversational systems can be categorized into three paradigms:
1. **Rule-Based Systems:** Relying on regular expressions and keyword lookup tables (as developed in Practical 3). While deterministic, they cannot generalize beyond predefined strings.
2. **Zero-Shot Prompt-Driven Agents:** Employing base LLMs with structured prompts (Practical 4). These handle freeform input but lack live context or external information.
3. **Tool-Augmented Autonomous Agents:** Incorporating function calling (Practical 6) and conversational state memory (Practical 5). The agent can assess user queries, decide whether external files or functions must be executed, and synthesize grounded answers.

### 2.2 Hardware and Software Stack

| Component | Technology / Library | Purpose in Project |
|---|---|---|
| **Programming Language** | Python 3.12 / JavaScript (ES6+) | Core backend logic, tooling, and client-side application logic. |
| **LLM Inference Engine** | Groq Cloud LPU / OpenAI SDK (`openai/gpt-oss-20b`) | Ultra-low latency model inference with function-calling capabilities. |
| **Backend Framework** | FastAPI 0.100+ & Uvicorn 0.23+ | Asynchronous REST API endpoints for `/chat` and `/clear`. |
| **Frontend Architecture** | HTML5, CSS3 Variables, Vanilla JS | Light/Dark theme rendering, RPG HUD, inventory, and chat bubbles. |
| **Audio Synthesizer** | Web Audio API | Purely programmatic 8-bit send and receive sound effects. |
| **Voice Engine** | Web Speech API (`SpeechSynthesis`) | Real-time speech synthesis for NPC verbal dialogue. |
| **Containerization** | Docker (`python:3.9-slim`) | Production containerization exposing standard port 7860. |
| **Cloud Deployment** | GitHub Pages / Git | Live public hosting of the web application. |

---

## CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN

### 3.1 Architectural Block Diagram

```text
+-------------------------------------------------------------------------+
|                         CLIENT FRONTEND (Browser)                       |
|   [Hero Sheet & Inventory]  [Interactive Chat UI]  [Quick Prompts Bar]  |
|          | Web Audio API (8-Bit SFX) | Web Speech API (TTS)             |
+------------------------------------+------------------------------------+
                                     |
                                     v
                 Dual-Mode Network Routing Strategy
              /                                     \
             v (If Localhost)                        v (If GitHub Pages)
+----------------------------+             +------------------------------+
|   LOCAL FASTAPI SERVER     |             |  SERVERLESS CLIENT RUNTIME   |
|   - api.py (:8000 / :7860) |             |  - Client-side fetch()       |
|   - Reads .env Secret Key  |             |  - localStorage API Key      |
+--------------+-------------+             +--------------+---------------+
               |                                          |
               +--------------------+---------------------+
                                    |
                                    v
                     +------------------------------+
                     | GROQ LLM INFERENCE ENGINE    |
                     | Model: openai/gpt-oss-20b    |
                     +--------------+---------------+
                                    |
                     Tool Decision: Function Calling?
                                  /   \
                         [YES]   /     \   [NO]
                                v       v
               +------------------+   +--------------------+
               | read_lore() Tool |   | Generate Direct    |
               | (game_lore.txt)  |   | In-Character Reply |
               +--------+---------+   +---------+----------+
                        |                       |
                        +-----------+-----------+
                                    |
                                    v
                     [Structured Response Bubble & Voice]
```

### 3.2 Dual Environment Architecture
- **Localhost Mode (FastAPI + Uvicorn):** The web interface automatically detects the origin (`127.0.0.1` or `localhost`) and routes queries to the Python backend. The backend securely loads `GROQ_API_KEY` from the server's `.env` file, bypassing client-side key prompts entirely.
- **Cloud Serverless Mode (GitHub Pages):** When deployed to static hosting (`github.io`), the app seamlessly adapts. Users can input their Groq key into a local browser modal stored exclusively in `localStorage`, maintaining complete zero-leakage security without exposing credentials to GitHub repositories.

---

## CHAPTER 4: IMPLEMENTATION DETAILS

### 4.1 Knowledge Base Construction
The ground truth knowledge base is authored in `game_lore.txt`:
```text
Game Name: Chronicles of Prasa | Developer: Prasa
Engine/Tools Used: Python, HTML/CSS/JS, FastAPI, and Groq AI Core
Backstory: In the year 3042 of the Second Age, the digital kingdom of Aethelgard
was on the brink of collapse from the Great Server Crash. A legendary developer
named Prasa arose from the Outlands, wielding Python and JavaScript to forge a
new realm. Eldrin stands as the wise archivist of Aethelgard.
```

### 4.2 Tool Definition and Execution Pipeline
In `api.py`, the tool is registered using JSON Schema specifications:
```python
TOOLS_SCHEMA = [{
    "type": "function",
    "function": {
        "name": "read_lore",
        "description": "Read sacred texts containing backstory, developer info, and tools.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    }
}]
```
When the user inquires about developer identity or game history, the LLM halts generation and emits a `tool_call`. The backend executes `read_lore()`, appends the file content to the message history with role `"tool"`, and submits a second completion pass to return the finalized grounded response.

### 4.3 Gamified Frontend & Audio Synthesis
The user interface (`index.html`) features:
1. **Illuminated Light Theme (Default):** Ivory parchment background (`#f7f3ea`), warm antique gold borders (`#b48a28`), and deep charcoal ink text (`#291e14`) fulfilling WCAG 2.1 AAA contrast guidelines.
2. **Dark Theme Option:** 1-click toggle to a midnight dungeon palette (`#121212`) with luminescent gold accents.
3. **Hero Sheet & Interactive Inventory:** A dedicated side panel showing adventurer stats (HP/Mana) and clickable items (`📜 Sacred Lore Scroll`, `🔮 Groq AI Core`, `🗡️ Python Blade`) that automatically trigger conversational inquiries.
4. **Quick Dialogue Pills:** One-tap prompt suggestions (`👑 Who made this world?`, `📜 Tell the Backstory`, `🧪 Test Guardrail`).
5. **Web Audio API 8-Bit Synthesizer:** Eliminates external audio dependencies by programmatically generating audio waves.
6. **Web Speech API (Text-to-Speech):** Synthesizes live audio speech for Eldrin's replies.
7. **Typewriter Animation:** Dynamically streams characters to simulate authentic retro console dialogue boxes.

---

## CHAPTER 5: RESULTS, TEST SCENARIOS & SCREENSHOTS

### 5.1 Test Scenario 1: In-Domain Knowledge Retrieval
- **Query:** *"Who created this world and what tools did they use?"*
- **Observed Result:** The agent activates the `read_lore` function. It responds in character, praising **Prasa** as the legendary developer and citing **Python, HTML/CSS/JS, FastAPI, and the Groq AI Core** as the foundational artifacts.

### 5.2 Test Scenario 2: Out-of-Domain Guardrail Enforcement
- **Query:** *"What is the square root of 6561 in modern calculus?"*
- **Observed Result:** The agent stays strictly in persona. It politely refuses the calculation, stating that such modern mathematics are foreign to the medieval realm of Aethelgard.

### 5.3 Test Scenario 3: Inventory Interaction & Audio Feedback
- **Action:** Clicking on the **`🔮 Groq AI Core`** item in the left Hero Inventory panel.
- **Observed Result:** An 8-bit audio chirp triggers immediately. The query is submitted, and Eldrin verbally narrates (via Speech Synthesis) the divine speed of the Groq inference engine while typewriter text streams onto the dialogue box.

### 5.4 Test Scenario 4: Live GitHub Pages Deployment
- **URL:** [https://prasadkankhar10.github.io/AIAD/](https://prasadkankhar10.github.io/AIAD/)
- **Observed Result:** The application loads without requiring server installation, connects securely to Groq inference, and delivers sub-second response times across desktop and mobile devices.

---

## CHAPTER 6: CONCLUSION & FUTURE SCOPE

### 6.1 Conclusion
The **Chronicles of Prasa Game NPC Agent** successfully demonstrates a complete, domain-specific AI Agent application fulfilling all requirements of the AI Agent Development syllabus and Mini-Project guidelines. By combining:
- Strict System Prompt Persona Engineering,
- Dynamic Functional Tool Execution (`read_lore`),
- Conversational History Memory, and
- Dual-Mode Gamified Web Architecture with audio synthesis and voice narration,

the project bridges the gap between raw LLMs and immersive, bounded interactive experiences.

### 6.2 Future Scope
- **Retrieval-Augmented Generation (RAG):** Integrating vector databases (ChromaDB / FAISS) for sprawling lore volumes.
- **Multi-Agent Game Ecosystems:** Deploying multiple NPCs communicating via LangGraph.
- **Player Quest State Persistence:** Cloud databases (PostgreSQL / Firebase) for persistent player stats.
- **3D Canvas Integration:** WebGL / Three.js 3D character avatars with phoneme lip-syncing.

---

## REFERENCES

1. Vaswani, A., et al. (2017). "Attention Is All You Need." *Advances in Neural Information Processing Systems (NeurIPS)*, 30.
2. Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." *arXiv preprint arXiv:2302.04761*.
3. OpenAI API Documentation. (2024). "Function Calling and Structured Outputs."
4. Groq Cloud Documentation. (2024). "Fast LLM Inference on Language Processing Units (LPUs)."
5. Ramírez, E. (2023). "FastAPI: High Performance Modern Python Web Framework."
6. W3C Web Audio Working Group. (2021). "Web Audio API Specification."
7. W3C Speech API Community Group. (2020). "Web Speech API Specification."
8. Prasad Kankhar. (2026). "AIAD - Chronicles of Prasa Repository & Live Deployment." GitHub: `https://github.com/prasadkankhar10/AIAD`
