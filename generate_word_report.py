import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def create_report():
    doc = Document()

    # 1. Page Setup & Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        
        # Configure footer with centered page number
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Add page number XML field to footer
        run_f = f_p.add_run()
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        run_f._r.append(fldSimple)
        run_f.font.name = 'Times New Roman'
        run_f.font.size = Pt(11)

    # Helper styling functions
    def set_font(run, size_pt, bold=False, italic=False, color=RGBColor(0,0,0)):
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = color

    def add_p(text="", size_pt=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, line_spacing=1.5, indent=0.0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if indent > 0:
            p.paragraph_format.first_line_indent = Inches(indent)
        if text:
            r = p.add_run(text)
            set_font(r, size_pt, bold, italic)
        return p

    def add_heading(text, level=1):
        if level == 1:
            # 14 TNR BOLD ALL CAPS
            p = add_p(text.upper(), size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=18, space_after=8, line_spacing=1.15)
        elif level == 2:
            p = add_p(text, size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=6, line_spacing=1.15)
        elif level == 3:
            p = add_p(text, size_pt=12, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4, line_spacing=1.15)
        return p

    # ================= PAGE 1: TITLE PAGE =================
    p_inst = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_after=20)
    r = p_inst.add_run("G. S. Mandal's\n")
    set_font(r, 12, bold=True)
    r = p_inst.add_run("Maharashtra Institute of Technology\n")
    set_font(r, 13, bold=True)
    r = p_inst.add_run("(An Autonomous Institute)\n")
    set_font(r, 11, bold=False)
    r = p_inst.add_run("Affiliated to Dr. Babasaheb Ambedkar Marathwada University (Dr. BAMU), Chhatrapati Sambhajinagar\n")
    set_font(r, 10, bold=False)
    r = p_inst.add_run("AICTE Approved, (Accredited with \"Grade A\" by NAAC)\n")
    set_font(r, 10, bold=False)
    r = p_inst.add_run("Department of Computer Science and Engineering\n")
    set_font(r, 12, bold=True)

    add_p("A Mini-Project Report on", size_pt=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=15)

    # Title: All Capital - 16 TNR Bold (Max 2 lines)
    p_title = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=35, line_spacing=1.2)
    r_title = p_title.add_run("DOMAIN-SPECIFIC CONVERSATIONAL AI AGENT FOR VIDEO GAME NPCS: CHRONICLES OF PRASA")
    set_font(r_title, 16, bold=True)

    p_sub = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_after=25)
    r = p_sub.add_run("Submitted by\n")
    set_font(r, 11)
    r = p_sub.add_run("Prasad Kankhar ")
    set_font(r, 12, bold=True)
    r = p_sub.add_run("(Roll No: ____________)\n")
    set_font(r, 11)
    r = p_sub.add_run("Student Partner ")
    set_font(r, 12, bold=True)
    r = p_sub.add_run("(Roll No: ____________)\n")
    set_font(r, 11)

    p_guide = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_after=25)
    r = p_guide.add_run("Under the guidance of\n")
    set_font(r, 11)
    r = p_guide.add_run("Mrs. Sarika Zile / Ms. Priya Khandelwal / Ms. Pooja Alone\n")
    set_font(r, 12, bold=True)

    p_ful = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_after=35)
    r = p_ful.add_run("In partial fulfillment of the award of Bachelor of Technology in Computer Science and Engineering")
    set_font(r, 12, bold=True)

    p_foot = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=20)
    r = p_foot.add_run("Department of Computer Science and Engineering\n")
    set_font(r, 14, bold=False)
    r = p_foot.add_run("Maharashtra Institute of Technology,\nChhatrapati Sambhajinagar\n")
    set_font(r, 14, bold=True)
    r = p_foot.add_run("[2026-27]")
    set_font(r, 12, bold=True)

    doc.add_page_break()

    # ================= PAGE 2: CERTIFICATE & ACKNOWLEDGEMENT =================
    add_heading("CERTIFICATE", level=1)
    p_cert_sub = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)
    r = p_cert_sub.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nMAHARASHTRA INSTITUTE OF TECHNOLOGY, CHHATRAPATI SAMBHAJINAGAR")
    set_font(r, 11, bold=True)

    add_p("This is to certify that the mini-project report entitled \"DOMAIN-SPECIFIC CONVERSATIONAL AI AGENT FOR VIDEO GAME NPCS: CHRONICLES OF PRASA\" is a bonafide work carried out by Prasad Kankhar and team in partial fulfillment for the award of degree of Bachelor of Technology in Computer Science and Engineering during the academic year 2026-2027.", indent=0.4)
    add_p("The project has been successfully evaluated as the 10th Practical Evaluation for the Discipline Specific Skill Course Laboratory – AI Agent Development.", indent=0.4, space_after=50)

    # Signatures
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.autofit = True
    c0 = t_sig.rows[0].cells[0].paragraphs[0]
    c0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = c0.add_run("_______________________\nCourse Teacher / Guide")
    set_font(r0, 11, bold=True)

    c1 = t_sig.rows[0].cells[1].paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = c1.add_run("_______________________\nHead of Department (CSE)")
    set_font(r1, 11, bold=True)

    add_heading("ACKNOWLEDGEMENT", level=1)
    add_p("We express our sincere gratitude to our respected Course Coordinators Mrs. Sarika Zile, Ms. Priya Khandelwal, and Ms. Pooja Alone for their invaluable guidance, encouragement, and insightful feedback throughout the conception and implementation of this AI Agent Mini-Project.", indent=0.4)
    add_p("We also extend our heartfelt thanks to the Head of Department and Maharashtra Institute of Technology for providing state-of-the-art computational infrastructure and laboratories which enabled the successful deployment and testing of this project.", indent=0.4)

    doc.add_page_break()

    # ================= PAGE 3: ABSTRACT & TABLE OF CONTENTS =================
    add_heading("ABSTRACT", level=1)
    add_p("Traditional non-player characters (NPCs) in computer video games rely heavily on rigid decision trees, static rule scripts, and predetermined dialogue branches. These conventional architectures result in repetitive interactions, lack of conversational context, and an inability to dynamically synthesize narrative lore. This project presents the design, architectural development, and production deployment of \"Chronicles of Prasa\", a domain-specific autonomous conversational AI agent embodied as an in-game archivist NPC named Eldrin.", indent=0.4)
    add_p("The system leverages state-of-the-art Large Language Model (LLM) inference (Groq Cloud / GPT-OSS architectures), prompt engineering persona guardrails, functional tool execution (read_lore), and short-term sliding window memory. The agent strictly restricts responses to in-game lore, preventing hallucinations or out-of-domain query leakage. A client-server architecture was engineered offering dual accessibility: a local containerized FastAPI backend with environment key protection, and a serverless deployment hosted on GitHub Pages utilizing client-side Web Audio API 8-bit sound synthesizers and browser Text-to-Speech (TTS). The project fulfills the requirements of Practical 10 by providing an end-to-end, domain-specific, fully documented AI Agent solution.", indent=0.4)

    add_heading("TABLE OF CONTENTS", level=1)
    toc_data = [
        ("Chapter 1: Introduction & Problem Statement", "4"),
        ("Chapter 2: Literature Review & Technology Stack", "5"),
        ("Chapter 3: System Architecture & Design", "6"),
        ("Chapter 4: Implementation Details", "8"),
        ("Chapter 5: Results, Test Scenarios & Demonstration", "10"),
        ("Chapter 6: Conclusion & Future Scope", "12"),
        ("References", "13")
    ]
    t_toc = doc.add_table(rows=len(toc_data), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (ch, pg) in enumerate(toc_data):
        row = t_toc.rows[i]
        c_title = row.cells[0].paragraphs[0]
        c_title.paragraph_format.space_after = Pt(4)
        c_title.paragraph_format.space_before = Pt(2)
        r = c_title.add_run(ch)
        set_font(r, 11, bold=True)

        c_pg = row.cells[1].paragraphs[0]
        c_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        c_pg.paragraph_format.space_after = Pt(4)
        c_pg.paragraph_format.space_before = Pt(2)
        r = c_pg.add_run(pg)
        set_font(r, 11)

    doc.add_page_break()

    # ================= CHAPTER 1: INTRODUCTION =================
    add_heading("CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT", level=1)

    add_heading("1.1 Background", level=2)
    add_p("In modern computer science and interactive entertainment systems, conversational agents play a critical role in user engagement. With the rapid evolution of Large Language Models (LLMs), artificial intelligence agents have shifted from simple pattern-matching bots (such as ELIZA or AIML rule-based bots) to autonomous cognitive entities capable of reasoning, recalling contextual history, and invoking programmatic external tools.", indent=0.4)
    add_p("However, deploying generic LLMs inside specialized domains—such as healthcare, enterprise customer support, or gaming environments—presents critical challenges: prompt drift, hallucination of facts, loss of persona consistency, and out-of-domain query leakage. A truly domain-specific agent must possess strict boundary constraints, dedicated knowledge retrieval mechanisms, and a cohesive user interface tailored to the end user.", indent=0.4)

    add_heading("1.2 Problem Statement", level=2)
    add_p("Traditional video game NPCs rely on static, hardcoded dialogue options that break immersion when a player seeks dynamic information about the game world. Conversely, if a standard, unconstrained LLM is embedded into a game, it may break character by answering real-world homework, solving math equations, or discussing modern political topics, entirely destroying the game's narrative immersion.", indent=0.4)
    add_p("The goal of this Mini-Project is to design, develop, test, and deploy a Domain-Specific Conversational AI Agent that:", indent=0.4)
    
    add_p("1. Acts as an authentic in-game NPC (\"Eldrin the Archivist\") within the fantasy world of Chronicles of Prasa.", indent=0.4)
    add_p("2. Enforces strict domain guardrails, politely refusing out-of-domain real-world questions while maintaining persona.", indent=0.4)
    add_p("3. Dynamically retrieves factual lore from an external knowledge base (game_lore.txt) using tool-calling capabilities.", indent=0.4)
    add_p("4. Maintains multi-turn conversational memory so user follow-ups are coherent.", indent=0.4)
    add_p("5. Provides an immersive, retro-gamified Web UI with audio synthesis, voice output, and dual deployment (Localhost & GitHub Pages).", indent=0.4)

    add_heading("1.3 Project Objectives", level=2)
    add_p("• Persona & Prompt Engineering: Implement a system prompt that locks the model into an ancient fantasy archivist tone.", indent=0.4)
    add_p("• Tool-Enabled Knowledge Grounding: Integrate an external tool (read_lore) so the agent dynamically cites accurate project attributes (developer name, engine stack, story).", indent=0.4)
    add_p("• Memory Retention: Support continuous multi-turn dialogue history.", indent=0.4)
    add_p("• Deployment Versatility: Ensure cross-environment execution across local containerized FastAPI and serverless GitHub Pages.", indent=0.4)

    doc.add_page_break()

    # ================= CHAPTER 2: TECHNOLOGY STACK =================
    add_heading("CHAPTER 2: LITERATURE REVIEW & TECHNOLOGY STACK", level=1)

    add_heading("2.1 Evolution of Conversational Agents", level=2)
    add_p("The architectural progression of AI conversational systems can be categorized into three distinct generations:", indent=0.4)
    add_p("1. Rule-Based Systems: Relying on regular expressions and keyword lookup tables (as developed in Practical 3). While deterministic, they cannot generalize beyond predefined strings.", indent=0.4)
    add_p("2. Zero-Shot Prompt-Driven Agents: Employing base LLMs with structured prompts (Practical 4). These handle freeform input but lack live context or external information.", indent=0.4)
    add_p("3. Tool-Augmented Autonomous Agents: Incorporating function calling (Practical 6) and conversational state memory (Practical 5). The agent can assess user queries, decide whether external files or functions must be executed, and synthesize grounded answers.", indent=0.4)

    add_heading("2.2 Hardware and Software Stack", level=2)
    add_p("The project integrates modern web technologies and high-throughput language inference hardware:", indent=0.4)

    # Tech Table
    t_tech = doc.add_table(rows=1, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t_tech.rows[0].cells
    hdr[0].paragraphs[0].add_run("Component").bold = True
    hdr[1].paragraphs[0].add_run("Technology / Tool").bold = True
    hdr[2].paragraphs[0].add_run("Role in Project").bold = True

    tech_rows = [
        ("Programming Language", "Python 3.12 & JavaScript (ES6+)", "Core agent logic, backend endpoints, and client-side web application."),
        ("LLM Inference Engine", "Groq Cloud LPU / openai/gpt-oss-20b", "High-speed inference offering sub-second latency with tool-calling capabilities."),
        ("Backend Framework", "FastAPI 0.100+ & Uvicorn 0.23+", "Asynchronous REST API endpoints (/chat and /clear) with CORS handling."),
        ("Frontend Architecture", "HTML5, CSS3 Custom Properties, Vanilla JS", "Light/Dark theme rendering, RPG HUD, inventory panel, and dialogue boxes."),
        ("Audio Synthesizer", "Web Audio API", "Real-time programmatic 8-bit sound synthesizers for send/receive audio feedback."),
        ("Voice Speech Engine", "Web Speech API (SpeechSynthesis)", "Real-time voice narration for the NPC dialogue without external audio files."),
        ("Containerization", "Docker (python:3.9-slim)", "Standard production containerization exposing cloud port 7860."),
        ("Cloud Deployment", "GitHub Pages / Git VCS", "Live public hosting of the serverless interactive AI application.")
    ]

    for c, t, r in tech_rows:
        row = t_tech.add_row().cells
        row[0].paragraphs[0].add_run(c)
        row[1].paragraphs[0].add_run(t)
        row[2].paragraphs[0].add_run(r)
        for cell in row:
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(3)
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)

    doc.add_page_break()

    # ================= CHAPTER 3: ARCHITECTURE & DESIGN =================
    add_heading("CHAPTER 3: SYSTEM ARCHITECTURE & DESIGN", level=1)

    add_heading("3.1 System Architecture Diagram", level=2)
    add_p("The end-to-end architecture is organized into four decoupled modular layers: the Presentation Layer, the Dual Routing Layer, the Cognitive Agent Controller, and the Functional Knowledge Layer.", indent=0.4)

    # Insert Real Diagram 1
    if os.path.exists("diagrams/system_architecture.png"):
        doc.add_picture("diagrams/system_architecture.png", width=Inches(6.0))
        p_cap = add_p("Figure 3.1: Detailed System Architecture of the Chronicles of Prasa AI Agent", size_pt=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14)

    add_heading("3.2 Dual Environment Architecture", level=2)
    add_p("A core innovation in this project is the Dual-Execution Strategy:", indent=0.4)
    add_p("• Localhost Execution: When accessed on localhost or 127.0.0.1, the web application detects the local origin and routes all chat traffic to the FastAPI backend. The server accesses GROQ_API_KEY directly from the root .env file, removing the need for user key input.", indent=0.4)
    add_p("• Cloud Serverless Execution: When hosted on GitHub Pages (github.io), the app utilizes client-side fetch calls to Groq API. The user inputs their API key into a secure browser prompt stored solely in localStorage, ensuring zero key leakage to public repositories.", indent=0.4)

    doc.add_page_break()

    # ================= CHAPTER 3 (CONTD): WORKFLOW & GUARDRAILS =================
    add_heading("3.3 Agent Interaction Sequence Workflow", level=2)
    add_p("The conversation lifecycle follows an event-driven sequence: user input submission, 8-bit audio generation, prompt augmentation, LLM inference evaluation, functional tool branching, and multi-modal audio-visual delivery.", indent=0.4)

    # Insert Real Diagram 2
    if os.path.exists("diagrams/agent_workflow_flowchart.png"):
        doc.add_picture("diagrams/agent_workflow_flowchart.png", width=Inches(4.8))
        p_cap = add_p("Figure 3.2: Execution Workflow Flowchart of the AI Agent", size_pt=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14)

    add_heading("3.4 Domain-Specific Guardrail Architecture", level=2)
    add_p("To eliminate prompt drift, the agent incorporates two distinct operational boundaries:", indent=0.4)

    # Insert Real Diagram 3
    if os.path.exists("diagrams/domain_guardrails_diagram.png"):
        doc.add_picture("diagrams/domain_guardrails_diagram.png", width=Inches(5.5))
        p_cap = add_p("Figure 3.3: In-Domain Knowledge Retrieval vs Out-of-Domain Guardrail Refusal", size_pt=10.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=14)

    doc.add_page_break()

    # ================= CHAPTER 4: IMPLEMENTATION =================
    add_heading("CHAPTER 4: IMPLEMENTATION DETAILS", level=1)

    add_heading("4.1 Knowledge Base Construction (game_lore.txt)", level=2)
    add_p("The domain ground truth is defined in game_lore.txt. It acts as the immutable factual document containing project history, developer credits (Prasa), technical engine stack (Python, FastAPI, HTML/JS, Groq Core), and the narrative backstory of Aethelgard.", indent=0.4)

    add_heading("4.2 Backend API & Tool Calling Logic (api.py)", level=2)
    add_p("The FastAPI application implements OpenAI-compatible function calling schemas. When a user asks about the game lore, the model emits a tool call invocation for read_lore. The backend reads the file, appends the tool payload, and requests the final completion pass.", indent=0.4)

    add_heading("4.3 Gamified Frontend Interface (index.html)", level=2)
    add_p("The user interface implements comprehensive gamification features:", indent=0.4)
    add_p("1. Illuminated Light Theme: Active by default with an antique parchment color scheme (#f7f3ea), warm gold borders (#b48a28), and high-contrast dark charcoal ink text (#291e14).", indent=0.4)
    add_p("2. Dark Mode Toggle: A one-click toggle in the header switches dynamically between Light and Dark dungeon themes.", indent=0.4)
    add_p("3. Hero Stats & Inventory Sheet: A collapsible RPG HUD displaying character level (Level 10 Master), HP/Mana gauges, and clickable artifacts (Sacred Lore Scroll, Groq AI Core, Python Blade).", indent=0.4)
    add_p("4. Quick Dialogue Options: Fast-tap dialogue pills for immediate narrative queries.", indent=0.4)
    add_p("5. Web Audio API 8-Bit Synthesizer: Generates ascending chirp waveforms on message dispatch and multi-frequency harmonic arpeggios on assistant receipt.", indent=0.4)
    add_p("6. Web Speech API (Text-to-Speech): Configures pitch and speech rate to give Eldrin an authentic, resonant wizard voice.", indent=0.4)
    add_p("7. Typewriter Text Streaming: Character-by-character typewriter streaming mimicking retro 16-bit RPG text engines.", indent=0.4)

    add_heading("4.4 Containerization and Deployment Configuration", level=2)
    add_p("The project includes a Dockerfile based on python:3.9-slim exposing port 7860, ready for deployment on Hugging Face Spaces or container clusters. Furthermore, the repository is synchronized with GitHub Pages for immediate browser accessibility.", indent=0.4)

    doc.add_page_break()

    # ================= CHAPTER 5: RESULTS & DEMONSTRATION =================
    add_heading("CHAPTER 5: RESULTS, TEST SCENARIOS & DEMONSTRATION", level=1)

    add_p("Extensive functional test cases were executed to validate domain boundaries, tool calls, and user interaction responsiveness.", indent=0.4)

    add_heading("5.1 Test Scenario 1: In-Domain Knowledge Retrieval", level=2)
    add_p("• User Query: \"Who created this world and what tools did they use?\"", indent=0.4)
    add_p("• Execution Path: The agent identifies the query as lore-specific, invokes the read_lore tool, reads game_lore.txt, and formulates the response.", indent=0.4)
    add_p("• Result: Eldrin praises Prasa as the legendary developer and explicitly cites Python, HTML/CSS/JS, FastAPI, and the Groq AI Core as the tools used.", indent=0.4)

    # Box Placeholder for Screenshot 1
    p_s1 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)
    r = p_s1.add_run("[ SCREENSHOT 1: IN-DOMAIN QUERY OUTPUT ]\n(Attach screenshot of browser showing Eldrin praising developer Prasa and citing technical tools)")
    set_font(r, 10, italic=True)

    add_heading("5.2 Test Scenario 2: Out-of-Domain Guardrail Enforcement", level=2)
    add_p("• User Query: \"What is the square root of 6561 in modern calculus?\"", indent=0.4)
    add_p("• Execution Path: The persona guardrail evaluates the query as modern mathematics external to Aethelgard.", indent=0.4)
    add_p("• Result: Eldrin politely refuses to perform the computation, stating that he is only the archivist of Aethelgard and possesses no knowledge of modern arithmetic.", indent=0.4)

    # Box Placeholder for Screenshot 2
    p_s2 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)
    r = p_s2.add_run("[ SCREENSHOT 2: OUT-OF-DOMAIN GUARDRAIL REFUSAL ]\n(Attach screenshot of browser showing Eldrin refusing calculus/math questions to maintain character)")
    set_font(r, 10, italic=True)

    doc.add_page_break()

    # ================= CHAPTER 5 (CONTD): RESULTS =================
    add_heading("5.3 Test Scenario 3: Inventory Interaction & Audio Feedback", level=2)
    add_p("• User Action: Clicking on \"🔮 Groq AI Core\" in the inventory panel.", indent=0.4)
    add_p("• Result: The 8-bit send audio tone triggers immediately. Eldrin verbally narrates the power of the Groq inference engine via Speech Synthesis while typewriter text renders onto the screen.", indent=0.4)

    # Box Placeholder for Screenshot 3
    p_s3 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)
    r = p_s3.add_run("[ SCREENSHOT 3: INVENTORY INTERACTION & LIGHT THEME ]\n(Attach screenshot showing the Hero sheet, inventory items, and illuminated light parchment theme)")
    set_font(r, 10, italic=True)

    add_heading("5.4 Test Scenario 4: Live GitHub Pages Deployment", level=2)
    add_p("• Deployment URL: https://prasadkankhar10.github.io/AIAD/", indent=0.4)
    add_p("• Result: The application runs with zero installation overhead across both desktop and mobile browsers, supporting full voice and sound synthesis.", indent=0.4)

    # Box Placeholder for Screenshot 4
    p_s4 = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=10)
    r = p_s4.add_run("[ SCREENSHOT 4: GITHUB PAGES LIVE DEPLOYMENT ]\n(Attach screenshot of browser displaying the live GitHub Pages URL with running application)")
    set_font(r, 10, italic=True)

    doc.add_page_break()

    # ================= CHAPTER 6: CONCLUSION & FUTURE SCOPE =================
    add_heading("CHAPTER 6: CONCLUSION & FUTURE SCOPE", level=1)

    add_heading("6.1 Conclusion", level=2)
    add_p("The Chronicles of Prasa Game NPC Agent successfully demonstrates a complete, domain-specific AI Agent application fulfilling all requirements of the AI Agent Development syllabus and Mini-Project guidelines. By combining:", indent=0.4)
    add_p("• Strict System Prompt Persona Engineering to eliminate out-of-domain prompt leakage,", indent=0.4)
    add_p("• Dynamic Functional Tool Execution (read_lore) to ground answers in factual project specifications,", indent=0.4)
    add_p("• Conversational History Memory for multi-turn coherence, and", indent=0.4)
    add_p("• Dual-Mode Gamified Web Architecture with audio synthesis and voice narration,", indent=0.4)
    add_p("the project bridges the gap between raw LLMs and immersive, bounded interactive experiences. It delivers deterministic guardrails without sacrificing natural conversational fluency.", indent=0.4)

    add_heading("6.2 Future Scope", level=2)
    add_p("The extensible modular architecture enables numerous future research directions:", indent=0.4)
    add_p("1. Retrieval-Augmented Generation (RAG): Integrating vector embeddings (ChromaDB / FAISS) to index encyclopedic lore across multi-volume game compendiums.", indent=0.4)
    add_p("2. Multi-Agent Ecosystems: Introducing multiple distinct NPCs (merchants, quest givers, companions) that coordinate and trade autonomously using LangGraph.", indent=0.4)
    add_p("3. Player State Cloud Persistence: Linking character progression and inventory state to persistent databases (PostgreSQL or Firebase).", indent=0.4)
    add_p("4. 3D WebGL / Three.js Visual Avatars: Synchronizing real-time phoneme audio with 3D animated character meshes.", indent=0.4)

    doc.add_page_break()

    # ================= REFERENCES =================
    add_heading("REFERENCES", level=1)
    refs = [
        "Vaswani, A., et al. (2017). \"Attention Is All You Need.\" Advances in Neural Information Processing Systems (NeurIPS), 30.",
        "Schick, T., et al. (2023). \"Toolformer: Language Models Can Teach Themselves to Use Tools.\" arXiv preprint arXiv:2302.04761.",
        "OpenAI API Documentation. (2024). \"Function Calling and Structured Outputs.\" Available: https://platform.openai.com/docs/guides/function-calling",
        "Groq Cloud Documentation. (2024). \"Fast LLM Inference on Language Processing Units (LPUs).\" Available: https://console.groq.com/docs",
        "Ramírez, E. (2023). \"FastAPI: High Performance Modern Python Web Framework.\" Available: https://fastapi.tiangolo.com",
        "W3C Web Audio Working Group. (2021). \"Web Audio API Specification.\" Available: https://www.w3.org/TR/webaudio/",
        "W3C Speech API Community Group. (2020). \"Web Speech API Specification.\" Available: https://wicg.github.io/speech-api/",
        "Prasad Kankhar. (2026). \"AIAD - Chronicles of Prasa Repository & Live Deployment.\" GitHub: https://github.com/prasadkankhar10/AIAD"
    ]
    for i, ref in enumerate(refs, 1):
        add_p(f"[{i}] {ref}", size_pt=11, space_after=8, indent=0.0)

    output_path = "Mini_Project_Report_AIAD.docx"
    doc.save(output_path)
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    create_report()
