# AI Agent Development Setup

This workspace is configured for Python-based AI agent development.

## Environment

Create and activate a local virtual environment:

```powershell
C:/Users/prasa/AppData/Local/Programs/Python/Python312/python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Verify the Setup

```powershell
python verify_setup.py
```

## Rule-Based Agent

Run the rule-based ATM menu system:

```powershell
python rule_based_agent.py
```

## Prompt-Driven Agent

Run the task-oriented Code Explainer agent:

```powershell
python prompt_driven_agent.py
```
Paste a code snippet, type `DONE` on a new line, and get a structured explanation.

## Memory Agent (Sliding Window)

Run the agent that demonstrates conversational short-term memory:

```powershell
python memory_agent.py --window 2
```
It will remember your context up to the defined window limit.

## Tool-Enabled Agent

Run the agent equipped with external tools (Calculator and File Reader):

```powershell
python tool_agent.py
```
Ask it math questions or ask it to read files like `requirements.txt`.

## Web Interface (Streamlit)

Launch the beautiful web-based Chat UI:

```powershell
streamlit run app.py
```
This will automatically open your web browser to `http://localhost:8501`.

## Chat With an LLM

Create a local `.env` file with your Groq API key:

```powershell
GROQ_API_KEY=your_groq_api_key_here
```

Run the chat script:

```powershell
python llm_prompt_analyzer.py
```

You can also choose a model:

```powershell
python llm_prompt_analyzer.py --model llama-3.1-70b-versatile
```

Inside the chat, type messages normally and use `/exit` to quit.

## Included Libraries

- Streamlit for lightweight UI and demos
- LangChain and LangGraph for agent workflows
- OpenAI and Anthropic SDKs for model/API access
- python-dotenv for local configuration
- Groq's OpenAI-compatible API via the OpenAI client
