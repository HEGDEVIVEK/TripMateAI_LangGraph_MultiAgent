# TripMate AI ✈️

### A multi-agent travel planner built with React, FastAPI, LangChain, and LangGraph

TripMate AI brings flight information, hotel research, weather, and sightseeing suggestions into one conversational travel planning application. Specialist agents work in parallel, and an itinerary agent combines their findings into a day-wise travel plan.

The project explores how to connect a usable frontend with a stateful agent workflow, external tools, persistent conversations, and execution tracing.

> **Project status:** The core workflow is built. MCP integration is in progress, with two integrations remaining. Guardrails, human-in-the-loop approval, and long-term memory are planned.
>
> **Setup note:** The architecture and features below describe the project as shared by its author. Repository paths, environment-variable names, startup commands, and API examples marked as examples must be aligned with the actual source before publishing this README as a verified installation guide.

## Contents

- [Why I built this](#why-i-built-this)
- [Features and progress](#features-and-progress)
- [Architecture](#architecture)
- [Agents and tools](#agents-and-tools)
- [How a request works](#how-a-request-works)
- [Technology stack](#technology-stack)
- [State and conversation memory](#state-and-conversation-memory)
- [MCP integration](#mcp-integration)
- [Getting started](#getting-started)
- [API example](#api-example)
- [Example conversations](#example-conversations)
- [Tracing and debugging](#tracing-and-debugging)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Acknowledgments](#acknowledgments)

## Why I built this

During my UI Developer internship at Commvault, I worked on reusable React components. That experience got me thinking about automating repetitive UI development tasks and exploring how AI agents could take on specific responsibilities.

TripMate AI is a hands-on project for learning those ideas. It connects familiar frontend development with new challenges: orchestrating agents, managing shared state, integrating tools, and maintaining context across a conversation.

The longer-term goal is to apply these lessons to developer workflows, including UI automation.

## Features and progress

| Capability | Status | Description |
| --- | --- | --- |
| React chat interface | Implemented | Send travel requests and revisit conversations. |
| FastAPI backend | Implemented | Connect the frontend to the agent workflow. |
| Parallel specialist workflow | Implemented | Run independent research tasks before itinerary generation. |
| Itinerary generation | Implemented | Combine specialist results into a day-wise travel plan. |
| MongoDB Atlas checkpoints | Implemented | Persist graph state for individual conversation threads. |
| LangSmith tracing | Implemented | Inspect execution, model interactions, and tool calls. |
| MCP tool integration | Implemented | MCP for agents work  |
| Guardrails | Planned | Validate requests and check generated outputs. |
| Human-in-the-loop approval | Planned | Let users review, approve, or request changes at a defined workflow pause. |
| Long-term memory | Planned | Remember preferences across separate conversations. |
| Supervisor-based routing | Planned | Select relevant agents based on the request. |

## Architecture

The graph uses a parallel split followed by a join. The specialist agents do not run as a sequential chain. The itinerary agent runs after the required specialist results are available.

All nodes work with graph state. The diagram's join represents synchronization before itinerary generation; it does not imply that shared state exists only after specialist execution.

<img width="1383" height="1052" alt="TripMate AI" src="https://github.com/user-attachments/assets/cb57fc61-da2c-4c31-99b8-453b5a0f0ec3" />


## Agents and tools

| Agent | Responsibility | Tool connection / target |
| --- | --- | --- |
| Flight Agent | Retrieve flight details, airlines, routes, and scheduled times. | AviationStack; MCP integration target. |
| Hotel Agent | Research hotels, amenities, reviews, and reported prices. | Tavily; MCP integration target. |
| Weather Agent | Retrieve weather information relevant to the trip. | Weather service; MCP integration target. |
| Sightseeing Agent | Research attractions and places to visit. | Tavily; MCP integration target. |
| Itinerary Agent | Combine specialist results into a day-wise travel plan. | Configured language model and shared state. |

The exact model provider depends on the backend configuration. The project does not require that an agent use OpenAI simply because it is an LLM-based agent.

Flight information is not the same as ticket pricing. The current flight tool should not be described as a cheapest-fare search unless a pricing source is added.

## How a request works

1. The user sends a travel request from the React interface.
2. The frontend sends the request and a conversation `thread_id` to FastAPI.
3. The backend invokes the graph with that thread configuration. Existing checkpointed state can be restored for the same thread.
4. Specialist agents perform their research in parallel and return updates to their state fields.
5. The graph joins the results before running the itinerary agent.
6. The itinerary agent uses the available results to produce a travel plan.
7. FastAPI returns the result to the frontend for display.

Checkpoint persistence operates across graph execution steps, rather than being a single final action after itinerary generation. LangSmith tracing is a separate observability function.

## Technology stack

| Area | Technology | Purpose |
| --- | --- | --- |
| Frontend | React | Chat interface and conversation navigation. |
| Backend | Python, FastAPI | API requests and workflow invocation. |
| Orchestration | LangGraph | Parallel execution, shared state, and checkpoints. |
| Agent tooling | LangChain | Model and tool integration. |
| Tool protocol | MCP | Standardized access to external tools; integration in progress. |
| Persistence | MongoDB Atlas | Durable graph checkpoints. |
| Observability | LangSmith | Execution tracing and debugging. |
| Flight information | AviationStack | Flight details and schedules. |
| Web research | Tavily | Hotel and sightseeing research. |
| Python environment | uv | Dependency and environment management. |

Earlier development used PostgreSQL checkpoints. This README describes the current MongoDB Atlas checkpoint setup.

## State and conversation memory

The state holds the request, conversation messages, specialist results, and generated itinerary. Representative fields from the project architecture are:

| Field | Contents |
| --- | --- |
| `user_query` | Current travel request. |
| `messages` | Conversation messages used by the graph. |
| `flight_result` | Flight agent output. |
| `hotel_result` | Hotel agent output. |
| `weather_info` | Weather agent output. |
| `sightseeing_result` | Sightseeing agent output. |
| `itinerary_result` | Generated itinerary. |

Match these names to the actual state schema if the code uses different keys.

### Thread-based conversations

A `thread_id` identifies one conversation. A new chat uses a new ID; continuing an existing chat reuses its ID.

For example, a user can request a two-day trip and later ask to extend it to three days within the same conversation. Checkpoints make the prior state available again. The nodes must also read and pass the relevant history to the model for that context to influence the answer.

A thread ID is not an authentication mechanism. User ownership and access checks are separate concerns for a multi-user deployment.

### Short-term versus long-term memory

MongoDB checkpoints provide **thread-scoped memory**, often called short-term memory in LangGraph. The data can survive an application restart; “short-term” describes its conversational scope, not how briefly it is stored.

**Long-term memory is planned.** It would allow preferences such as vegetarian food, a preferred budget range, or a travel style to be recalled across different threads.

## MCP integration

MCP stands for **Model Context Protocol**. The intended integration pattern is:

**Agent → MCP client → MCP server → External service**

MCP exposes tools through a common interface. The server is responsible for implementing its tool behavior and connecting to the underlying service. API changes, authentication, errors, and provider limits still need to be handled.

Two MCP integrations are pending. Until those are completed, a diagram label such as “AviationStack MCP” or “Weather MCP” represents the target architecture, rather than confirmation that every connection already runs through MCP.

For each completed integration, document the actual transport, server URL or local launch command, authentication requirements, and tools exposed. Those details depend on the implementation and are not assumed here.

## Getting started

### Prerequisites

- Git.
- Python compatible with the project's `pyproject.toml` / `.python-version`.
- [uv](https://docs.astral.sh/uv/getting-started/installation/).
- Node.js and the package manager used by the frontend.
- MongoDB Atlas access and a database user with the required permissions.
- Credentials for the configured LLM and external services.
- LangSmith credentials if tracing is enabled.

### 1. Clone the repository

Replace the GitHub URL below with the actual repository URL:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git tripmate-ai
cd tripmate-ai
```

### 2. Install backend dependencies

From the directory containing the backend's `pyproject.toml`:

```bash
uv sync
```

Use the repository's dependency manifest and lockfile rather than installing arbitrary latest versions of each package.

### 3. Configure backend environment variables

Create a local `.env` in the location loaded by the backend. Copy `.env.example` if the repository provides one.

The following is a **configuration template**, not a verified list of the variable names read by this repository. Match the names to the backend's configuration code.

```dotenv
# Example names: match these to your MongoDB connection code.
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@YOUR_CLUSTER/
MONGODB_DATABASE=tripmate_ai

# Configure only the model provider actually used by the application.
# Add its API key under the exact name read by your model initialization code.

# Required where your direct tools or MCP servers expect these credentials.
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key

# LangSmith tracing configuration.
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=tripmate-ai

# Add the weather provider and MCP settings required by your implementation.
```

Keep service credentials in backend or server configuration. Do not put secret keys or database credentials in React source code or frontend environment variables. Exclude `.env` from version control.

### 4. Start any required MCP servers

Start the local MCP servers used by the implementation, or configure the required remote endpoints. Use their documented authentication and transport settings. A remote service may require credentials even though no local server process is needed.

### 5. Run FastAPI

**Example only:** if the current directory contains `main.py` and that file defines `app = FastAPI()`:

```bash
uv run uvicorn main:app --reload
```

If the app lives elsewhere, replace `main:app` with its actual module path and application object. Development reload is not a production deployment configuration.

With the default Uvicorn port, the API is available at `http://127.0.0.1:8000`. FastAPI's interactive documentation is normally at `http://127.0.0.1:8000/docs` unless disabled or customized.

### 6. Run the frontend

Open another terminal in the directory containing the frontend's `package.json`.

For an npm-based project:

```bash
npm install
npm run
```

`npm run` lists the available scripts. If the project defines a `dev` script, start it with:

```bash
npm run dev
```

Use the actual script and package manager from the repository. Configure the frontend's API base URL and backend CORS settings to match the local addresses. Open the frontend URL printed in the terminal.

### 7. Check the application

- Send a travel request and confirm that a response appears in the chat.
- Inspect the backend logs or LangSmith trace for the parallel specialist branches and itinerary step.
- Send a follow-up within the same chat and confirm the thread ID is reused.
- Reload the application and reopen the saved conversation.
- Start a new chat and confirm it receives a different thread ID.

These are suggested manual checks, not claims that an automated test suite is included.

## API example

The previously shared backend exposes `POST /chat`. This example reflects the request and itinerary response shown during development; consult the running API's `/docs` for the current contract.

### Request

```http
POST /chat
Content-Type: application/json
```

```json
{
  "user_query": "Plan a two-day trip to Bengaluru with hotel suggestions and historical places to visit.",
  "thread_id": "trip-demo-001"
}
```

### Illustrative response

```json
{
  "thread_id": "trip-demo-001",
  "itinerary_result": "Day 1: ...\nDay 2: ..."
}
```

The itinerary above is a placeholder. If the current endpoint returns serialized `messages` instead, document that response shape here. A chat-history route is not specified because its actual path has not been confirmed.

## Example conversations

**Initial request**

> Plan a three-day trip to Bengaluru. Suggest hotels, historical attractions, and weather-related considerations.

**Follow-up in the same thread**

> Make it four days and keep the schedule relaxed.

**Sightseeing request**

> Focus on historical monuments and include opening hours where available.

**Flight-information request**

> Find flight information from BLR to COK and include the airlines and scheduled times.

These are example prompts, not guaranteed outputs. Results depend on the tools, available data, model behavior, and implemented context handling.

## Tracing and debugging

LangSmith helps inspect which agents ran, which tools were called, the inputs and outputs, and failures during execution. It is separate from MongoDB checkpoint persistence.

| Problem | What to check |
| --- | --- |
| Backend does not start | Working directory, application import path, and installed dependencies. |
| Model or tool authentication fails | Correct credential name, loaded `.env`, account access, and provider quota. |
| MongoDB connection fails | Connection URI, database-user permissions, and Atlas network access settings. |
| MCP tool is unavailable | Server process or remote endpoint, transport, authentication, and exposed tools. |
| Frontend cannot call the API | Backend address, frontend configuration, browser network errors, and CORS. |
| A follow-up loses context | Reused `thread_id`, saved checkpoint state, and history supplied to the model. |
| No LangSmith traces appear | Tracing configuration and instrumentation of the executed code path. |

## Limitations

- This is an evolving learning project, not a booking service.
- Two MCP integrations remain incomplete.
- Web search results do not guarantee live hotel inventory, current prices, or ticket availability.
- Flight schedule information does not establish the cheapest fare.
- Weather coverage depends on the selected provider and forecast horizon.
- Persisting messages does not remove model context-window limits; history management may be needed as conversations grow.
- Generated plans should be checked against official travel and attraction sources before making arrangements.
- Authentication, user ownership checks, deployment hardening, and automated evaluation are not claimed as implemented in this README.

## Roadmap

- [ ] Complete the remaining two MCP integrations.
- [ ] Add input and output guardrails.
- [ ] Add human-in-the-loop review and approval.
- [ ] Add long-term memory for preferences across conversations.
- [ ] Explore supervisor-based selection of specialist agents.
- [ ] Improve handling of missing data, tool failures, and rate limits.
- [ ] Add history management for long conversations.
- [ ] Evaluate itinerary quality using repeatable travel scenarios.

## Documentation references

- [LangGraph persistence and memory](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangSmith SDK and tracing configuration](https://github.com/langchain-ai/langsmith-sdk)
- [uv project workflow](https://docs.astral.sh/uv/guides/projects/)
- [Running FastAPI with an ASGI server](https://fastapi.tiangolo.com/deployment/manually/)

## License

A license has not been specified in this README. Add a `LICENSE` file and update this section when a license is selected.
