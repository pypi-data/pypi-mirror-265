import time
import random
import string
from fastapi import status,Request,Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.utils import console,TimeOutException,generate_response
import logging

class add_process_time_header(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ''' This will add processing time on every request '''
        start_timestamp = time.time()
        request.state.timestamp = start_timestamp
        response = await call_next(request)
        process_time = time.time() - start_timestamp
        response.headers["X-Process-Time"] = str(process_time)
        print('add_process_time_header middleware')
        print(f'Took {process_time} to process')
        return response

class timeout_middleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ''' Will return exceptions in code as a response'''
        get_local_time = lambda x : str(x.tm_year)+'-'+str(x.tm_mon)+'-'+str(x.tm_mday)+','+str(x.tm_hour)+':'+str(x.tm_min)+':'+str(x.tm_sec)
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        local_time_formatted = get_local_time(time.localtime(start_time))
        logging.info(f"{local_time_formatted} rid={idem} start request path={request.url.path}")
        status_code=0
        response=None
        except_flag=False
        ''' will timeout after certain after amount of time '''
        try:
            response = await call_next(request)
        except TimeOutException:
            response = Response(generate_response('Operation timed out.Please try again',status.HTTP_200_OK))
        except Exception as e:
            response = Response(generate_response('Something went wrong.Please try again',status.HTTP_200_OK))

        finally:
            print('timeout_middleware middleware')
            return response

