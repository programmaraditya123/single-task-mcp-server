from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/')
def home():
    return {'hello':'this is the homepage'} 



if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080)) 
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

    
