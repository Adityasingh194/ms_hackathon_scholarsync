# ScholarSync

ScholarSync is a **multi-agent AI academic assistant** designed to automate student academic workflows.  
It uses **cooperative AI agents orchestrated through LangGraph** to manage assignments, answer questions from academic documents, schedule tasks, and automate communication.

Instead of a single chatbot, ScholarSync operates through **multiple specialized AI agents that collaborate autonomously to complete tasks.**

---

# Architecture Overview

ScholarSync follows a **multi-agent orchestration architecture** where agents cooperate through a central orchestration layer.

```
User
 ↓
Web Interface (Student Portal)
 ↓
LangGraph Agent Orchestrator
 ↓
------------------------------------
| Planner Agent                    |
| Retrieval Agent                  |
| Tool Agent                       |
| Interview Agent                  |
------------------------------------
 ↓
MCP Tool Server
 ↓
External Services
• Google Drive
• Calendar API
• Email Drafting
• Document Retrieval
```

Each agent focuses on a specific responsibility, allowing the system to perform complex workflows autonomously.

---

# Core Agents

## Planner Agent

The **Planner Agent** interprets user requests and decides which agents or tools should be used.

Responsibilities:

- Task planning
- Agent routing
- Multi-step workflow orchestration
- Managing agent cooperation

Example:

```
User: Schedule a reminder for the assignment due tomorrow
```

Planner decides to:

1. Fetch assignment data
2. Send request to Tool Agent
3. Create calendar event

---

## Retrieval Agent

The **Retrieval Agent** handles document intelligence and academic question answering.

Responsibilities:

- Process uploaded PDFs
- Process assignment documents
- Process lecture materials
- Build embeddings
- Perform vector search
- Generate contextual answers

Pipeline:

```
PDF / Document
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Store
 ↓
LLM Retrieval
```

Example query:

```
Explain the time complexity of Strassen’s algorithm from my DSA notes.
```

---

## Tool Agent

The **Tool Agent** interacts with external services through the **MCP server**.

Capabilities:

- Create calendar events
- Draft emails
- Fetch assignments
- Fetch study materials
- Automate academic workflows

Example:

```
User: Schedule my AI assignment submission reminder.
```

Tool agent calls:

```
create_calendar_event()
```

---

# AI Interviewer Agent

ScholarSync also includes an **AI Interviewer system** designed to simulate technical interviews for students.

This module demonstrates how **AI agents can conduct interactive evaluations and provide feedback.**

### Capabilities

- Conduct coding interviews
- Ask behavioral interview questions
- Evaluate answers
- Provide feedback
- Guide students through problem-solving

### Interview Workflow

```
Student Starts Interview
 ↓
Interview Agent selects question
 ↓
Student submits response
 ↓
LLM evaluates response
 ↓
Feedback generated
 ↓
Next question selected
```

### Example Interaction

```
AI Interviewer: Explain the difference between BFS and DFS.

Student: BFS explores level by level using a queue...

AI Interviewer Feedback:
Correct explanation. You may also mention time complexity O(V + E).
```

### Planned Enhancements

- Real-time coding environment
- Automatic code evaluation
- Behavioral interview scoring
- Difficulty-based question selection

---

# MCP Tool Server

The MCP server acts as the **tool execution layer**.

It exposes APIs used by the agents to perform real-world actions.

Tools implemented:

```
create_calendar_event
draft_email
fetch_assignments
fetch_study_material
```

Example tool endpoint:

```
POST /tools/create_calendar_event
```

Input:

```
{
"title": "Submit DSA Assignment",
"start_time": "2026-03-10T19:00:00",
"end_time": "2026-03-10T20:00:00"
}
```

---

# Key Features

## Multi-Agent AI System

ScholarSync uses **cooperating AI agents** instead of a single chatbot.

Each agent specializes in a task and collaborates to complete complex workflows.

---

## Document Question Answering

Students can upload **PDF notes, assignments, and study materials** and ask questions directly.

---

## Assignment Intelligence

Automatically fetch assignments and allow **context-aware question answering**.

---

## Academic Automation

Automates common student tasks:

- scheduling reminders
- drafting emails
- organizing assignments

---

## AI Interview Practice

Students can practice:

- technical interview questions
- behavioral interview questions
- conceptual explanations

The system provides **feedback and guidance to improve responses.**

---

# Tech Stack

## AI / Agent Framework

- LangGraph
- LangChain
- Groq API (LLaMA 3 8B)

## Backend

- Python
- FastAPI
- MCP Tool Server

## AI Processing

- Vector embeddings
- Document chunking
- Retrieval Augmented Generation (RAG)

## Integrations

- Google Drive
- Google Calendar
- Email automation

## Frontend

- HTML
- CSS
- JavaScript

---

# Directory Structure

```
ScholarSync
│
├── agents
│   ├── planner_agent.py
│   ├── retrieval_agent.py
│   ├── tool_agent.py
│   └── interviewer_agent.py
│
├── mcp_server
│   ├── server.py
│   ├── tools
│   │   ├── calendar_tool.py
│   │   ├── email_tool.py
│   │   └── drive_fetch_tool.py
│
├── vector_store
│
├── frontend
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── documents
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```
git clone https://github.com/yourusername/ScholarSync.git
cd ScholarSync
```

---

## Create Virtual Environment

```
python -m venv myenv
```

Activate environment

Windows

```
myenv\Scripts\activate
```

Mac/Linux

```
source myenv/bin/activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```
GROQ_API_KEY=your_groq_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

## Run MCP Tool Server

```
python mcp_server/server.py
```

---

## Run Agent System

```
python main.py
```

---

## Open Web Interface

Open:

```
index.html
```

---

# Current Status

### Fully Functional

- Multi-agent orchestration
- Document Q&A
- Assignment fetching
- Calendar automation
- Email drafting

### Partially Implemented

- AI coding interview environment
- Behavioral interview interaction pipeline

### Known Limitations

- No authentication layer
- MCP server acts as centralized tool execution layer
- AI interviewer evaluation pipeline still under development

---

# Future Improvements

- Full authentication system
- Multi-user student portal
- Advanced AI interview simulation
- Coding challenge auto-grading
- Agent memory system
- Distributed MCP tool architecture

---

# License

MIT License

---

# Author

Aditya Kumar Singh

AI Systems | Multi-Agent Architectures | Full-Stack Development