from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import post, auth

# for frontend
origins = [
    "http://192.168.0.107:3000",
    "http://localhost:3000",
]

app = FastAPI()
# for fix errors with CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# this event for myself
@app.on_event("startup")
def on_startup():
    pass


# adding various routes in project
app.include_router(auth.router, tags=['Auth'])
app.include_router(post.router, tags=['Posts'], prefix='/api')
