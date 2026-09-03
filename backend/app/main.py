from fastapi import FastAPI,HTTPException,Request,WebSocket
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from schemas.user_models import user_model
import json
import random
import time
app=FastAPI()


app.mount("/static",StaticFiles(directory="static"),name="static")
templates= Jinja2Templates(directory="templates")

# @app.get('/login',response_class=HTMLResponse)
# async def login(request:Request):
#     return templates.TemplateResponse("login.html",{"request":request})

# @app.post('/login')
# def signup(user:user):
#     print(user.username)
connections=[]


@app.get('/',response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse('home.html',{"request":request , "username":"Nithin"})



# class connection_manager():
     
#      def sent_all():
          
scoreboard=[]

def public_connection():
    return[{
        'username':con['username'],
        'status' : con['status'],
        'player' : con['player']
    }
    for con in connections
    ]
async def handle_status(payload,websocket):
    for con in connections:
            if(con["websocket"]==websocket):
                con["status"]=payload["status"]
    online=public_connection()
    for con in connections:
        await con['websocket'].send_text(json.dumps({"event": "status","data":online}))


async def handle_join(payload,websocket):
    if(connections==[]):
        connections.append({"username":payload["username"] , "websocket":websocket , "status": "not ready","player":"host"})
    else:
        connections.append({"username":payload["username"] , "websocket":websocket , "status": "not ready","player":"member"})
    online=public_connection()
    for con in connections:
        await con['websocket'].send_text(json.dumps({"event": "status","data":online}))

async def handle_disconnect(websocket):
    global connections
    flag=0
    for con in connections:
        if(con['websocket']==websocket):
            if(con['player']=='host'):
                flag=1
        else:
            if(flag==1):
                con['player']='host'
                flag=0



    connections=[
        con for con in connections 
        if con['websocket']!=websocket
    ]

    online=public_connection()
    for con in connections:
        await con['websocket'].send_text(json.dumps({"event": "status","data":online}))

game_const=False
count=6
async def handle_start():
    global game_const
    game_const=False
    n=random.randint(0,len(connections)-1)
    for i,con in enumerate(connections):
        if(i==n):
            con['role']='dumb'
        else:
            con['role']='member'
        await con['websocket'].send_text(json.dumps({'event':'start','role':con['role']}))

    for i in range(300):
        if game_const==False:
            time.sleep(1)
        else:
            break
    else:
        for con in connections:
            await con['websocket'].send_text(json.dumps({'event':'timeup'}))
        count=count-1
        await handle_start()


    

rword=""

async def handle_game(websocket,message):
    global game_const,rword
    if(rword.lower()==message.lower()):
        winner=""
        game_const=True
        for con in connections:
            if(con['websocket']==websocket):
                winner=con['username']
                scoreboard['username']=scoreboard['username']+10
        for con in connections:
            await con['websocket'].send_text(json.dumps({'event':'roundover','winner':winner}))
        if(count==0):
            for con in connections:
                await con['websocket'].send_text(json.dumps({'event':'gameover','scoreboard':scoreboard}))
        
        count=count-1
        await handle_start()
    else:
        await websocket.send_text(json.dumps({'event':'wrong'}))
@app.websocket('/ws')
async def con(websocket:WebSocket):
    await websocket.accept()

    try:

        while True:
             
            data=await websocket.receive_text()
            payload=json.loads(data)

            if(payload['event']=="join"):
                await handle_join(payload,websocket)
        
            if(payload['event']=="status"):
                await handle_status(payload,websocket)
                allready=(
                    len(connections)>=3 and 
                    all(con['status']=='ready' for con in connections) 
                )
                if allready:
                    await handle_start()
            if(payload['event']=="rword"):
                global rword
                rword=payload['word']


            if(payload['event']=="message"):
                await handle_game(websocket,payload['data'])
            
            if payload['event']=='draw':
                for con in connections:
                    await con['websocket'].send_text(json.dumps({'event':'draw','data':payload['data']}))
            
            if payload['event']=='clear':
                for con in connections:
                    await con['websocket'].send_text(json.dumps({'event':'clear'}))

            if payload['event']=='restart':
                await handle_start()

    except:
        await handle_disconnect(websocket)
    




