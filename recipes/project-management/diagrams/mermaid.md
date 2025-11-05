# Software Development Lifecycle

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#f5f5f5', 'primaryTextColor': '#333', 'primaryBorderColor': '#666', 'lineColor': '#666', 'secondaryColor': '#f0f0f0', 'tertiaryColor': '#fff' }}}%%
flowchart TB
    subgraph Planning["🗓️ Planning"]
        A(["Requirements Gathering"]) --> B(["Task Prioritization"])
        B --> C(["Sprint Planning"])
    end
    
    subgraph Development["💻 Development"]
        D(["Design"]) --> E(["Coding"])
        E --> F(["Code Review"])
        F -->|Needs Fixes| E
        F -->|Approved| G(["Unit Testing"])
    end
    
    subgraph QA["🔍 Quality Assurance"]
        H(["Integration Testing"]) --> I(["System Testing"])
        I --> J(["User Acceptance Testing"])
        J -->|Bugs Found| K(["Bug Fixing"])
        K --> H
    end
    
    subgraph Deployment["🚀 Deployment"]
        L(["Staging"]) --> M(["Production Deployment"])
        M --> N(["Monitoring"])
    end
    
    C --> D
    G --> H
    J -->|Passed| L
    N -->|Feedback| A
    
    classDef planning fill:#a8dadc80,stroke:#457b9d,stroke-width:1px,color:#1d3557,font-family:Arial
    classDef development fill:#8ecae680,stroke:#219ebc,stroke-width:1px,color:#023047,font-family:Arial
    classDef qa fill:#bee3db80,stroke:#89b0ae,stroke-width:1px,color:#3a506b,font-family:Arial
    classDef deployment fill:#e9c46a80,stroke:#f4a261,stroke-width:1px,color:#264653,font-family:Arial
    
    class A,B,C planning
    class D,E,F,G development
    class H,I,J,K qa
    class L,M,N deployment