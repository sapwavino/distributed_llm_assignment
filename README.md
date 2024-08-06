# Distributed LLM Assignment (LLM Chat API)

This project includes two programs: a Python API and a Node.js API. The Python API uses one of two large language models to answer questions. 
The Node.js API is the public interface that users interact with.

## How They Work Together

1. **Python API**:
   Python 3.12 
   - This is a private API that uses models like Llama2 and Mistral to generate answers & saves conversation history in a MongoDB database.

2. **Node.js API**: 
   Node v20
   - This is the public API that sends user queries to the Python API & retrieves and returns the conversation history from the Python API.

### Communication Flow

- The Node.js API selects a model & receives a query from the user.
- It sends this query to the Python API to generate a response using the selected model.
- The Python API saves the query and response in MongoDB & sends the response back to the user.

## Database

- The MongoDB database stores conversation history.
- Each entry includes:
  - User query
  - Model response
  - Timestamp of the conversation

## Security Considerations

- The Python API is not exposed to the public. Only the Node.js API is public.
- This helps protect the models and database from direct access.
- Input validation is in place to prevent empty queries and other issues.

## A few things to note:

- You need a huggingface token with access to inference to use the models
- The safe tensors that will be downloaded from huggingface are >14GB per model
- The program will run considerably slowly on CPUs ( >~5 mins/request)


## QUICK DOCUMENTATION

### Node.js API Endpoints

1. **Select Model**
   - **Endpoint**: `POST /api/select_model`
   - **Body**: 
     ```json
     {
       "model": "llama2" // or "mistral"
     }
     ```
   - **Description**: Selects the model to use for queries.

2. **Send Query**
   - **Endpoint**: `POST /api/query`
   - **Body**: 
     ```json
     {
       "query": "Your question here"
     }
     ```
   - **Description**: Sends a query to the selected model and gets a response.

3. **Get Conversation History**
   - **Endpoint**: `GET /api/history`
   - **Description**: Retrieves all conversation history, ordered by date (most recent first).

4. **Get Specific Conversation**
   - **Endpoint**: `GET /api/conversation/:id`
   - **Description**: Retrieves details of a specific conversation by ID.

### Docker 

- Docker packages both applications and their dependencies to ensure that the APIs run in the same environment on any machine. This makes it easy to build and run the applications together.

## Running the Project

1. **Build the Docker Containers**:
   ```bash
   docker-compose up --build
