# Common imports across all the programs
import warnings
warnings.filterwarnings("ignore")

# FastAPI imports
from fastapi import FastAPI, Request, Cookie, BackgroundTasks, Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import traceback
from fastapi import Depends
from config.database_config import get_db
from sqlalchemy.orm import Session

# Utils imports
from utils.Logging import debug
from utils.utils import console

# File-related imports
from starlette.responses import FileResponse


# Other imports
import uvicorn
import logging
import hashlib
import os
import sys
import requests
import re
import pandas as pd
import time

# Pydantic imports
from pydantic import BaseModel
from typing import Optional
from distutils.dir_util import copy_tree

# Q&A and conversation-related imports
from conversation.qna import run_query_pipeline
from text_qna.default_page import default_page,menu
from text_qna.qna import recommended_query, facebook_result
from sqladmin import Admin
# Monitoring and admin imports
from monitor.models import (
    TokenUsageAdminModel,
    ChatHistoryAdminModel,
    ModelManagerAdminModel,
    # ConversationConfigurationAdminModel,
)
from monitor.database import engine
from monitor.feedback import insert_chat_to_db ,most_liked_ans
from monitor.router import router as monitor_router
from monitor.utils import MonitorPipeLineObject
from autocomplete.autocomplete import get_closest_matches,cache_conversation
from autocomplete.top_question import get_top_questions_view
from generate_map import generate_map
from fastapi.responses import HTMLResponse
from middleware import add_process_time_header
from themes import get_project_content, get_project_recommended_query, get_project_themes
# from api.router import router as api_router


from finlense_model.utils import *
from api.router import file_router as file_router
from api.router import kpi_router as kpi_router

''' FastAPI object for router class '''

description = r'CGLENSE API provides the complete documentation of all the API for required for the CGLENSE voicebot web application.'
title_name = r'CGLENSE Voicebot API'
app = FastAPI(title=title_name, description=description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(monitor_router)
# New API Router
app.include_router(file_router, tags=["Upload Files"], prefix="/file")
app.include_router(kpi_router, tags=["KPI Configuration"], prefix="/kpi")


@app.post("/chat")
async def chat(request : Request,db: Session = Depends(get_db)):
    chat_history = await request.json()
    enable_cache = True
    try:
        console.print(chat_history["language"])
        language=chat_history["language"]
    except:
        language="English"
    # pipeline = MonitorPipeLineObject()
    try:
        pipeline = MonitorPipeLineObject(user_id='user',history=chat_history['history'],
        query=chat_history['history'][-1]['user'],latest_query=chat_history['history'][-1]['user'],
        language=language)
    except Exception as e:
        print(e)
    console.print('Starting Gpt Pipeline \n Created pipeline object : ',style='green1')
    pipeline = run_query_pipeline(pipeline)

    console.print('Predict user question class',style='green1')
    query_type = "Other"
    # try:
    #     query_type = predict_value(chat_history['history'][-1]['user'])
    #     # print(query_type)
    # except:
    #     query_type = "Other"

    latest_query=chat_history["history"][-1]["user"]
    chat_id = insert_chat_to_db(
        role="user",
        email='user',
        session_id='user',
        text=chat_history["history"][-1]["user"],
        
        response=pipeline.answer[-1],
        like=0,
        chat_id="123",  # from chatID 
        text_type=query_type
    )
    result = pipeline.get_api_response()
    result["exchange_id"] = chat_id
    # suggestion_question
    console.log('Before recommened query section')
    del pipeline


    if enable_cache:
        cache_conversation(latest_query, result,db) 
    return result


@app.post("/suggested_question/")
async def suggested_question(chat_history: dict):
    answer = chat_history["answer"]
    print(" answer :",answer)
    try:
        console.print(chat_history["language"])
        language=chat_history["language"]
    except:
        language="English"
    try:
        pipeline = MonitorPipeLineObject(user_id='user',history=answer,
        query=answer,latest_query=answer,
        language=language)
    except Exception as e:
        print(e)
    chat_id = insert_chat_to_db(
        role="user",
        email='user',
        session_id='user',
        text=answer,
        response=answer,
        like=0,
    )
    pipeline.exchange_id = chat_id
    suggestion_question = recommended_query(pipeline)
    if len(suggestion_question)>3:
        questions = suggestion_question[0:3]
    else:
        questions = suggestion_question
    return questions


@app.get("/generate_map/")
async def api_data(request: Request):
    query_params = dict(request.query_params)
    name = query_params['name']
    if os.path.exists(name):
        response = HTMLResponse(open(name,"r").read())
    else:
        response = HTMLResponse("""<html>File does not exist</html>""")
    return response

"""
sample_queries and ui-content-data API Manage from admin Portal
"""
PROJECT_NAME_ADMIN="CGLense"


@app.get("/sample_queries")
async def faq_question():
    response = {}
    try:
        query_object = get_project_content(PROJECT_NAME_ADMIN)
        faq_query = get_project_recommended_query(query_object.id)
        response['question'] = faq_query if faq_query else []
        response['status'] = "PASS"
        print("sample_queries response :",response)
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except:
        response['question'] = []
        response['status'] = "FAIL"
        print("recommended_queries response :",response)
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/most_liked_answers")
async def most_liked_answers(page:int=1,limit:int=10,sort_by: Optional[str] = None,order_by: Optional[str] = None,db: Session = Depends(get_db)):
    response = {
        "message": "Server Error",
        "results": [],
        "status": status.HTTP_400_BAD_REQUEST
    }
    try:
        offset = (page - 1) * limit
        result = most_liked_ans(db,sort_by,order_by,offset,limit)
        #result = db.query(ChatHistory).all()

        response["message"] = "Result has successful retrieved"
        response["status"] = status.HTTP_200_OK
        response["result"] = result
        return response
    except Exception as e:
        
        print(" Exception",e)
        response["text"] = [str(traceback.format_exc())]
        response["status"] = status.HTTP_400_BAD_REQUEST
        debug.error(f"Most liked answer error: Bad request to fetch data")
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
    
@app.get("/autocomplete")
async def get_closest_matches_api(question: str, closest_matches: int = 5,db: Session = Depends(get_db)):
    """API to get the closest matches to the given text"""
    response = {
        "message": "Server Error",
        "results": [],
        "status": status.HTTP_400_BAD_REQUEST
    }
    try:
        return_list = get_closest_matches(question,db,closest_matches)
        
        
        response["results"] = return_list
        response["message"] = "Query has successfully ran"
        response["status"] = status.HTTP_200_OK
        
        return response
    
    except Exception as e:
        response ["Message"] = "Issue in retrieving data"
        debug.error(f"In Auto complete there is issue in retrieving data")
        response["text"] = [str(traceback.format_exc())]
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)
    

@app.get("/top_questions_view")
async def get_top_questions_view_api(categories: str, closest_matches: int = 5,db: Session = Depends(get_db)):
    response = {
        "message": "Server Error",
        "results": [],
        "status": status.HTTP_400_BAD_REQUEST
    }
    try:
        categories = categories.lower()
        return_list = get_top_questions_view(categories,db,closest_matches)
        
        
        response["results"] = return_list
        response["message"] = "Query has successfully ran"
        response["status"] = status.HTTP_200_OK
        
        return response
    
    except Exception as e:
        response ["Message"] = "Issue in retrieving data based on views"
        debug.error(f"In top_questions_view there is issue in retrieving data")
        response["text"] = [str(traceback.format_exc())]
        return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)



        

    
    
@app.get("/ui-content-data")
async def ui_content_data_api():
    query_object = get_project_content(PROJECT_NAME_ADMIN)
    response = {
        "projectTitle": "CGLense",
        "projectLogoPath": "https://covalenseaccessibility.blob.core.windows.net/ai-portal/JcrewLogo.png",
        "projectLogoHeight": "30px",
        "companyInfo": "CGLense AI, your advanced visual companion! Empowering businesses across sectors with cutting-edge image analysis, object recognition, and custom insights. Experience precise AI solutions for diverse industries. Uncover image enhancement tools, metadata extraction, and deep learning capabilities. Seamlessly integrate with workflows for heightened efficiency. From precise visual data interpretation to tailored solutions, CGLense AI bot streamlines operations. Explore the potential of images with unparalleled accuracy. Simplify complexities, elevate decision-making, and harness the true power of visual data. Your key to unlocking innovation, driving progress, and transforming how you perceive and utilize visual information - that`s CGLense AI.",
        "chatbotInfo": "As for the CGLense Navigation Tool with ChatGPT integration, it represents an innovative approach to enhancing the online visual experience for CGLense users. The tool harnesses ChatGPT, an advanced conversational AI model, enabling natural language interactions. It simplifies product searches, offers personalized recommendations, and aids in order tracking, returns, and real-time customer support. This integration aims to streamline visual exploration, elevate user satisfaction, and provide comprehensive assistance, redefining how users engage with visual data through CGLense.",
        "chatbotInsideImage": "https://covalenseaccessibility.blob.core.windows.net/ai-portal/CGLENSE_AI_BOT_INSIDE_LOGO.png",
        "chatbotHeaderLink": "AI Assistant",
        "chatbotHeaderLink": "Get started with CGLense",
        "exampleListQuestion": [
            {
                "text": "What industries benefit most from CGLense's visual data analysis capabilities?",
                "value": "What industries benefit most from CGLense's visual data analysis capabilities?",
            },
            {
                "text": "Can CGLense extract relevant information from text descriptions associated with images?",
                "value": "Can CGLense extract relevant information from text descriptions associated with images?",
            },
            {"text": "hi , can you help me?", "value": "hi , can you help me?"},
        ],
    }
    try:
        response["projectTitle"] = query_object.title
        response["projectLogoPath"] = query_object.image
        response["companyInfo"] = query_object.company_info
        response["chatbotInfo"] = query_object.chatbot_info
        response["chatbotInsideImage"] = query_object.chatbox_inside_image
        response["chatbotInsideText"] = query_object.chatbox_inside_text
        response["chatbotHeaderLink"] = query_object.header_link_name
        response["exampleListQuestion"] = [
            {
                "text": query_object.question1,
                "value": query_object.question1,
            },
            {
                "text": query_object.question2,
                "value": query_object.question2,
            },
            {
                "text": query_object.question3,
                "value": query_object.question3,
            },
        ]
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)


admin = Admin(app=app, engine=engine, base_url="/admin/")
admin.add_view(TokenUsageAdminModel)
admin.add_view(ChatHistoryAdminModel)
admin.add_view(ModelManagerAdminModel)


''' Static files serving section & Manage Themes'''
def setupThemes():
    try:
        query_object = get_project_content(PROJECT_NAME_ADMIN)
        themes = get_project_themes(query_object.id)
        from_directory = f"themes/{themes.themes_types}"
        to_directory = 'static'
        copy_tree(from_directory, to_directory)
    except:
        to_directory = 'static'
        copy_tree("themes/theme1", to_directory)


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        setupThemes()
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:  # earlier it was except (HTTPException, StarletteHTTPException) as ex
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex

app.mount("/", SPAStaticFiles(directory="static", html = True), name="static")
""" Middleware section of the code """
app.add_middleware(add_process_time_header)


if __name__ == "__main__":
    uvicorn.run("app:app", reload =False, host="127.0.0.1",port=8544,workers=4)