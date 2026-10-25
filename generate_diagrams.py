import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("diagrams", exist_ok=True)

# ----------------- DIAGRAM 1: SYSTEM ARCHITECTURE -----------------
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    # Title
    ax.text(5, 8.2, "SYSTEM ARCHITECTURE: CHRONICLES OF PRASA AI AGENT", 
            fontsize=13, fontweight='bold', ha='center', fontfamily='serif')

    # Color palette
    c_ui = "#e0f2fe"       # Light blue
    c_router = "#fef3c7"   # Amber
    c_backend = "#dcfce7"  # Green
    c_agent = "#f3e8ff"    # Purple
    c_tool = "#ffedd5"     # Orange
    c_border = "#1e293b"

    def draw_box(x, y, w, h, text, bg, title=""):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg, edgecolor=c_border, linewidth=1.5)
        ax.add_patch(rect)
        if title:
            ax.text(x + w/2, y + h - 0.25, title, fontsize=9.5, fontweight='bold', ha='center', va='top', fontfamily='serif')
            ax.text(x + w/2, y + h/2 - 0.1, text, fontsize=8.5, ha='center', va='center', fontfamily='serif')
        else:
            ax.text(x + w/2, y + h/2, text, fontsize=9, fontweight='bold', ha='center', va='center', fontfamily='serif')

    # 1. UI Layer
    draw_box(0.5, 6.2, 9.0, 1.4, 
             "• Interactive RPG Dialogue HUD   • Hero Stats & Inventory Sheet\n• Web Audio API (8-Bit Synthesizer)   • Web Speech API (Voice TTS)", 
             c_ui, title="1. CLIENT PRESENTATION LAYER (Browser Interface)")

    # 2. Dual Routing Strategy
    draw_box(1.0, 4.4, 3.6, 1.2, "FastAPI Backend (:8000)\nDirect Access to .env Key", c_router, title="Localhost Execution")
    draw_box(5.4, 4.4, 3.6, 1.2, "Client-side Groq Fetch\nBrowser localStorage Key", c_router, title="GitHub Pages Execution")

    # Arrows from UI to Routing
    ax.annotate("", xy=(2.8, 5.6), xytext=(2.8, 6.2), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))
    ax.annotate("", xy=(7.2, 5.6), xytext=(7.2, 6.2), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))

    # 3. Agent Cognitive Core
    draw_box(2.0, 2.5, 6.0, 1.4,
             "• Multi-Turn Conversational Memory Buffer\n• Strict Persona Guardrails (Eldrin Medieval Persona)\n• LLM Model: openai/gpt-oss-20b (via Groq Cloud LPU)", 
             c_agent, title="2. COGNITIVE AGENT CONTROLLER")

    # Arrows to Agent
    ax.annotate("", xy=(3.8, 3.9), xytext=(2.8, 4.4), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))
    ax.annotate("", xy=(6.2, 3.9), xytext=(7.2, 4.4), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))

    # 4. Tool & Knowledge Layer
    draw_box(0.8, 0.6, 3.8, 1.3, "Tool Execution: read_lore()\nDynamic Function Calling Hook", c_tool, title="3A. Functional Tool Calling")
    draw_box(5.4, 0.6, 3.8, 1.3, "Knowledge Base: game_lore.txt\nWorld Backstory, Developer, Tech Stack", c_backend, title="3B. Grounded Knowledge Base")

    # Decision Arrows
    ax.annotate("If Lore Query", xy=(2.7, 1.9), xytext=(3.5, 2.5), arrowprops=dict(facecolor="#b91c1c", arrowstyle="->", lw=1.5), fontsize=8, fontfamily='serif', fontweight='bold', color="#b91c1c")
    ax.annotate("", xy=(5.4, 1.25), xytext=(4.6, 1.25), arrowprops=dict(facecolor=c_border, arrowstyle="<->", lw=1.5))
    ax.annotate("Grounded Synthesis", xy=(6.8, 2.5), xytext=(6.8, 1.9), arrowprops=dict(facecolor="#15803d", arrowstyle="->", lw=1.5), fontsize=8, fontfamily='serif', fontweight='bold', color="#15803d")

    plt.tight_layout()
    plt.savefig("diagrams/system_architecture.png", dpi=300)
    plt.close()
    print("Created diagrams/system_architecture.png")


# ----------------- DIAGRAM 2: WORKFLOW FLOWCHART -----------------
def create_workflow_diagram():
    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(5, 11.6, "CONVERSATIONAL AGENT EXECUTION WORKFLOW", 
            fontsize=13, fontweight='bold', ha='center', fontfamily='serif')

    c_step = "#f1f5f9"
    c_decision = "#fef9c3"
    c_action = "#e0e7ff"
    c_out = "#dcfce7"
    c_border = "#334155"

    def draw_node(x, y, w, h, text, shape="rect", bg=c_step):
        if shape == "round":
            box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=bg, edgecolor=c_border, linewidth=1.5)
        elif shape == "diamond":
            box = patches.Polygon([[x + w/2, y], [x + w, y + h/2], [x + w/2, y + h], [x, y + h/2]],
                                  facecolor=bg, edgecolor=c_border, linewidth=1.5)
        else:
            box = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=c_border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, fontsize=8.5, ha='center', va='center', fontfamily='serif', fontweight='bold')

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))
        if label:
            ax.text((x1+x2)/2 + 0.15, (y1+y2)/2, label, fontsize=8, fontfamily='serif', fontweight='bold')

    # Step 1: Start
    draw_node(3.2, 10.6, 3.6, 0.7, "User Submits Query / Clicks Item", shape="round", bg="#e2e8f0")
    draw_arrow(5.0, 10.6, 5.0, 9.9)

    # Step 2: Trigger SFX & Append
    draw_node(2.2, 9.2, 5.6, 0.7, "Play 8-Bit Chirp & Append to History Buffer", bg=c_action)
    draw_arrow(5.0, 9.2, 5.0, 8.5)

    # Step 3: LLM Inference
    draw_node(2.0, 7.8, 6.0, 0.7, "Evaluate Persona Prompt + Groq LLM Inference", bg=c_step)
    draw_arrow(5.0, 7.8, 5.0, 7.1)

    # Step 4: Decision: Tool Call?
    draw_node(2.5, 5.9, 5.0, 1.2, "Is Tool Required?\n(read_lore function call)", shape="diamond", bg=c_decision)

    # Branch YES: Tool Call
    draw_arrow(2.5, 6.5, 1.2, 6.5)
    ax.text(1.8, 6.65, "YES", fontsize=8, fontfamily='serif', fontweight='bold', color="#b91c1c")
    draw_node(0.2, 5.2, 2.0, 1.0, "Execute read_lore()\nFetch game_lore.txt", bg="#fed7aa")
    ax.annotate("", xy=(3.0, 5.2), xytext=(1.2, 5.2), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))
    draw_node(3.0, 4.7, 4.0, 0.8, "Append Tool Result & Re-Query LLM", bg=c_action)
    draw_arrow(5.0, 4.7, 5.0, 4.0)

    # Branch NO: Direct
    draw_arrow(7.5, 6.5, 8.5, 6.5)
    ax.text(7.8, 6.65, "NO", fontsize=8, fontfamily='serif', fontweight='bold', color="#15803d")
    ax.annotate("", xy=(8.5, 4.0), xytext=(8.5, 6.5), arrowprops=dict(facecolor=c_border, lw=1.5))
    ax.annotate("", xy=(7.0, 3.6), xytext=(8.5, 4.0), arrowprops=dict(facecolor=c_border, arrowstyle="->", lw=1.5))

    # Step 5: Format response
    draw_node(2.0, 3.2, 5.0, 0.8, "Format In-Character Dialogue Response", bg=c_out)
    draw_arrow(5.0, 3.2, 5.0, 2.5)

    # Step 6: Multi-modal delivery
    draw_node(1.5, 1.7, 7.0, 0.8, "Play Fantasy Chime + Stream Typewriter + Web Speech TTS", bg=c_action)
    draw_arrow(5.0, 1.7, 5.0, 1.0)

    # Step 7: Completed
    draw_node(3.2, 0.3, 3.6, 0.7, "Ready for Next User Input", shape="round", bg="#e2e8f0")

    plt.tight_layout()
    plt.savefig("diagrams/agent_workflow_flowchart.png", dpi=300)
    plt.close()
    print("Created diagrams/agent_workflow_flowchart.png")


# ----------------- DIAGRAM 3: GUARDRAILS & DOMAIN BOUNDARY -----------------
def create_guardrails_diagram():
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    ax.text(5, 6.6, "DOMAIN-SPECIFIC GUARDRAIL & PERSONA ENFORCEMENT", 
            fontsize=12.5, fontweight='bold', ha='center', fontfamily='serif')

    # Left: In-Domain
    rect_in = patches.FancyBboxPatch((0.5, 1.2), 4.2, 4.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#ecfdf5", edgecolor="#059669", linewidth=2.0)
    ax.add_patch(rect_in)
    ax.text(2.6, 5.6, "IN-DOMAIN QUERIES", fontsize=11, fontweight='bold', ha='center', color="#065f46", fontfamily='serif')
    ax.text(2.6, 4.8, "[+] Game Lore & Realm Backstory\n[+] Developer Credits (Prasa)\n[+] Technical Stack & Tools\n[+] Hero Inventory Artifacts\n[+] Quest Opportunities", 
            fontsize=9.5, ha='center', va='center', fontfamily='serif', color="#064e3b")
    
    rect_in_res = patches.Rectangle((0.8, 1.5), 3.6, 1.2, facecolor="#10b981", edgecolor="#047857", linewidth=1.5)
    ax.add_patch(rect_in_res)
    ax.text(2.6, 2.1, "SYSTEM ACTION:\nCall read_lore() & Answer\nin Full Ancient Persona", 
            fontsize=9, fontweight='bold', ha='center', va='center', color="white", fontfamily='serif')

    # Right: Out-of-Domain
    rect_out = patches.FancyBboxPatch((5.3, 1.2), 4.2, 4.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor="#fef2f2", edgecolor="#dc2626", linewidth=2.0)
    ax.add_patch(rect_out)
    ax.text(7.4, 5.6, "OUT-OF-DOMAIN QUERIES", fontsize=11, fontweight='bold', ha='center', color="#991b1b", fontfamily='serif')
    ax.text(7.4, 4.8, "[-] Real-world Math / Calculus\n[-] Modern Politics & World Events\n[-] Academic School Homework\n[-] General Real-world Geography\n[-] General Code Generation", 
            fontsize=9.5, ha='center', va='center', fontfamily='serif', color="#7f1d1d")
    
    rect_out_res = patches.Rectangle((5.6, 1.5), 3.6, 1.2, facecolor="#ef4444", edgecolor="#b91c1c", linewidth=1.5)
    ax.add_patch(rect_out_res)
    ax.text(7.4, 2.1, "SYSTEM ACTION:\nStrict Persona Refusal\n'I know only of Aethelgard'", 
            fontsize=9, fontweight='bold', ha='center', va='center', color="white", fontfamily='serif')

    # Bottom Footer
    ax.text(5, 0.5, "Guaranteed Persona Immersion: Zero Out-of-Domain Leakage or Prompt Drift", 
            fontsize=10, fontstyle='italic', ha='center', fontfamily='serif', color="#334155")

    plt.tight_layout()
    plt.savefig("diagrams/domain_guardrails_diagram.png", dpi=300)
    plt.close()
    print("Created diagrams/domain_guardrails_diagram.png")

if __name__ == "__main__":
    create_architecture_diagram()
    create_workflow_diagram()
    create_guardrails_diagram()
