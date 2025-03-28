# Singing Evaluation Project

This project consists of a frontend built with React/Next.js and a backend built using FastAPI, designed for evaluating singing performances.

## Project Structure

```
project-root
├── singing_eval (Frontend)
└── backend (FastAPI Backend)
```

## Getting Started

Follow these instructions to set up and run the project locally:

### Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd singing_eval
npm install
npm run dev
```

The frontend will run on [http://localhost:3000](http://localhost:3000).

### Backend Setup

Navigate to the backend directory and set up the Python environment:

```bash
cd backend

# Optional but recommended: create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install --no-cache-dir -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run on [http://localhost:8000](http://localhost:8000).

## Usage

- Access the frontend UI through your web browser at `http://localhost:3000`.
- The frontend communicates with the backend API running at `http://localhost:8000`.

## Contributing

Feel free to open an issue or submit a pull request if you find improvements or encounter issues.

## License

This project is licensed under the MIT License. See `LICENSE` file for details.

