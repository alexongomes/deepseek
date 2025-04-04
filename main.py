from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configuração do Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:7b"  # Altere para "deepseek-r1" se disponível

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": question,
            "stream": False
        }
      
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_API_URL, json=payload)
            print(payload)
            response.raise_for_status()
            answer = response.json().get("response", "Sem resposta.")
        
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "question": question, "answer": answer}
            
        )
    
    except Exception as e:
        print(e)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Erroooo: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)