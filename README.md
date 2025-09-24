
# 🏦 AI Agent Challenge – Bank Statement Parser

description: |
  This project implements an AI coding agent that automatically generates 
  PDF parsers for bank statements (e.g., ICICI, SBI). 
  The agent writes parser code, generates tests, and validates correctness 
  using CSV ground truth.

features:
  - Agent-based code generation for bank parsers
  - CLI command to generate and test parsers
  - Parser contract with `parse(pdf_path: str) -> pd.DataFrame`
  - Automated pytest validation
  - Extensible for any bank with sample PDF + CSV

project-structure: |
  ai-agent-challenge/
  ├── agent.py                   # Main AI agent loop
  
  ├── run_icici.py               # Quick ICICI run
  
  ├── custom_parsers/            # Generated parsers
      │   └── icici_parser.py
  
  ├── data/
      │   └── icici/
      │       ├── icici_sample.pdf
      │       └── result.csv
      
  ├── tests/
      │   └── test_icici_parser.py
      
  ├── requirements.txt           # Python dependencies
  
  └── README.md

installation: |
  ```bash
  git clone https://github.com/<your-username>/ai-agent-challenge.git
  cd ai-agent-challenge
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  pip install -r requirements.txt
