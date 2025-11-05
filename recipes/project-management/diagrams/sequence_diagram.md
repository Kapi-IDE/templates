sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Service as Service Layer
    participant Task as Celery Task
    participant Redis
    participant LLM as LLM Provider
    participant DB as Database
    
    Client->>API: Request LLM-based operation
    API->>Service: Process request
    Service->>Task: Submit async task
    Task->>Redis: Queue task
    Task-->>API: Return task ID
    API-->>Client: Return task ID for tracking
    
    alt Streaming response
        Redis->>Task: Process task
        Task->>LLM: Send request
        loop Stream chunks
            LLM->>Task: Stream response chunk
            Task->>Service: Process chunk
            Service->>API: Stream to client
            API->>Client: Stream response chunk
        end
    else Non-streaming response
        Redis->>Task: Process task
        Task->>LLM: Send request
        LLM->>Task: Complete response
        Task->>Service: Process response
        Service->>DB: Save results
        Client->>API: Poll for results
        API->>Service: Check status
        Service->>DB: Get results
        DB->>Service: Return results
        Service->>API: Return results
        API->>Client: Return complete response
    end
    
    Task->>DB: Log token usage
    Task->>DB: Update user stats
    Task->>DB: Save completion