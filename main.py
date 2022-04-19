#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune-NG

'''config'''
import json
import os
import importlib
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.openapi.docs import get_swagger_ui_html
import simplejson as json
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from auth import users
from config import config
from core import dbmeta, security, apimodel, dbengine

from util import toolkit, log
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

cfg = config.app_config

'''logging'''
log = log.Logger(level=cfg['Application_Config'].app_log_level)

'''app_dir'''
app_dir = os.path.dirname(os.path.abspath(__file__))

'''API prefix'''
prefix = cfg['Application_Config'].app_prefix
if prefix.startswith('/'):
    pass
else:
    prefix = '/' + prefix
log.logger.info(cfg['Application_Config'].app_name + ' Start Up ....')
log.logger.info("API prefix is: [ %s ]" % prefix)

'''API define'''
app = FastAPI(
    title=cfg['Application_Config'].app_name,
    description=cfg['Application_Config'].app_description,
    version=cfg['Application_Config'].app_version,
    openapi_url=prefix+"/openapi.json",
    docs_url=None,
    redoc_url=None
)

favicon_path = 'static/favicon.ico'
app.mount("/static", StaticFiles(directory="admin/apps/static"), name="static")

@app.on_event("startup")
async def startup_event():
    log.logger.info(cfg['Application_Config'].app_name + ' Starting ....')
    if cfg['Application_Config'].app_clear_metadat_on_startup:
        clear_meta_cache()
    if cfg['Application_Config'].app_load_metadat_on_load:
        meta = dbmeta.DBMeta()
        #meta.gen_models()
        #meta.gen_services()

@app.on_event("shutdown")
def shutdown_event():
    log.logger.info(cfg['Application_Config'].app_name + ' Shutting Down ....')
    if cfg['Application_Config'].app_clear_metadat_on_shutdown:
        clear_meta_cache()

'''Admin_app'''
#TODO

'''CORS'''
origins = []
# Set all CORS enabled origins
if cfg['Application_Config'].app_cors_origins:
    origins_raw = cfg['Application_Config'].app_cors_origins.split(",")
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

'''app route'''

@app.get("/",
         tags=["Default"],
         summary="Get information for this application.",
         description="Return application information",
         include_in_schema=False)
async def app_root():
    log.logger.debug('Access \'/\' : run in app_root()')
    return {
        "Application_Name": cfg['Application_Config'].app_name,
        "Version": cfg['Application_Config'].app_version,
        "Author": "ibmzhangjun@139.com",
        "Description": cfg['Application_Config'].app_description
    }

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(app_dir, 'admin/apps/static/favicon.ico'))

@app.get('/admin/favicon.ico', include_in_schema=False)
async def adminfavicon():
    return FileResponse(os.path.join(app_dir, 'admin/apps/static/favicon.ico'))

@app.get("/apidocs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_favicon_url="/static/favicon.ico",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/apiredoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico",
        with_google_fonts=False,
    )

@app.post(prefix + "/token",
          response_model=security.Token,
          tags=["Security"],
          summary="Login to get access token.",
          description="",
          )
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    log.logger.debug('Access \'/token\' : run in login_for_access_token(), '
                     'input data username: [%s] and password: [%s]' % (form_data.username, form_data.password))
    user = security.authenticate_user(users.Users().users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=cfg['Security_Config'].access_token_expire_minutes)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    rcontent = {"access_token": access_token, "token_type": "bearer"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=rcontent)

@app.get(prefix + "/users",
         response_model=security.User,
         tags=["Security"],
         summary="Retrieve user information.",
         description="",
         )
async def read_users_me(current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/users/\' : run in read_users_me()')
    return current_user

@app.get(prefix+"/_schema/dbdiagram",
         tags=["Schema"],
         summary="Retrieve Database Diagram Resources.",
         description="By default, all tables are returned .",include_in_schema=False)
async def get_dbdiagram():
    log.logger.debug('Access \'/_schema/dbdiagram\' : run in get_dbdiagram()')
    return dbmeta.DBMeta().response_dbdiagram("dbdiagram-canvas.json")

@app.get(prefix+"/_schema/dbdll",
         tags=["Schema"],
         summary="Retrieve Database Diagram Resources.",
         description="By default, all tables are returned .",include_in_schema=False)
async def get_dbdiagram():
    log.logger.debug('Access \'/_schema/dbdll\' : run in get_dbdiagram()')
    return dbmeta.DBMeta().response_dbdiagram("dbddl.sql")

@app.get(prefix+"/_schema/database",
         tags=["Schema"],
         summary="Retrieve DbSchema Resources.",
         description="By default, all tables are returned .",
         )
async def get_schema(current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/_schema/database\' : run in get_schema()')
    return dbmeta.DBMeta().response_schema()

@app.get(prefix+"/_schema/_table/{table_name}",
         tags=["Schema"],
         summary="Retrieve table definition for the given table.",
         description="This describes the table, its fields and indexes.",
         )
async def get_table_schema(table_name: str, current_user: security.User = Depends(security.get_current_active_user)):
    log.logger.debug('Access \'/_schema/{table_name}\' : run in get_table_schema(), '
                     'input data table_name: [%s]' % table_name)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    return dbmeta.DBMeta().response_table_schema(table_name)

@app.post(prefix+"/_table/_query/{table_name}",
          tags=["Data - Table Level"],
          summary="Retrieve one or more records. ",
          description="",)
async def query_data(table_name: str, tablequerybody: apimodel.TableQueryBody,
                     current_user: security.User = Depends(security.get_current_active_user)):
    """
            Parameters
            - **table_name** (path): **Required** - Name of the table to perform operations on.
            - **request body: **Required**
            ```
                {
                 "queryfields": "string",  -- Optional - Comma-delimited list of properties to be returned for each resource, "*" returns all properties. ex: 'Customers.first_name,Customers.last_name'
                 "distinct": 'False',  -- Optional , default['False'] - Return distinct result.
                 "where": "string",  -- Optional - SQL-like filter to limit the records to retrieve. ex: '((Customers.first_name != \'Tony\') | (Customers.household_income > 80001)) & (Customers.last_name != \'Stark\')'
                 "order_by": "string",  -- Optional - SQL-like order containing field and direction for filter results. ex: 'Customers.phone_number.asc(), Customers.household_income.desc()'
                 "group_by": "string",  -- Optional - Comma-delimited list of the fields used for grouping of filter results. ex: 'Customers.last_name'
                 "limit": 0,  -- Optional - Set to limit the filter results.
                 "offset": 0,  -- Optional - Set to offset the filter results to a particular record count.
                 "count_only": 'False',  -- Optional , default['False'] - Return only the total number of filter results.
                 "include_count": 'True'  -- Optional , default['True'] - Include the total number of filter results in returned result.
                 }
            ```
        """
    log.logger.debug(
        'Access \'/_table/_query{table_name}/\' : run in query_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tablequerybody.json())
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.'+table_name.strip().lower()+'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize()+'Service')()
    return getattr(dataservice, 'query_'+table_name.strip().capitalize())(tablequerybody.json())

@app.post(prefix+"/_table/{table_name}",
          tags=["Data - Table Level"],
         summary="Create one or more records.",
         description="",
         )
async def post_data(table_name: str, tablepost: apimodel.TableBody,
                    current_user_role: bool = Depends(security.get_write_permission)):
    """
        Parameters
        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **request body: Required**
        ```
            {
             "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
             }
        ```
    """
    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in post_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body data: [%s]' % tablepost.json())
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    return getattr(dataservice, 'batch_create_' + table_name.strip().capitalize() + '_byjson')(tablepost.json())

@app.put(prefix+"/_table/{table_name}",
         tags=["Data - Table Level"],
         summary="Update (replace) one or more records.",
         description="",
         deprecated=False
         )
async def put_data(table_name: str, tableput: apimodel.TableBody,
                   current_user_role: bool = Depends(security.get_write_permission)):
    """
            Parameters
            - **table_name** (path): **Required** - Name of the table to perform operations on.
            - **request body: Required**
            ```
                {
                 "data": [{"name":"jack","phone":"55789"}]  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '[{"name":"jack","phone":"55789"}]'
                 }
            ```
    """
    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in put_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tableput.json())
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    return getattr(dataservice, 'batch_update_' + table_name.strip().capitalize() + '_byjson')(tableput.json())

@app.delete(prefix+"/_table/{table_name}",
            tags=["Data - Table Level"],
            summary="Delete one or more records.",
            description="",
            )
async def delete_data(table_name: str,
                      filterstr: str = Header(None),
                      current_user_role: bool = Depends(security.get_write_permission)):
    """
        Parameters
        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **filterstr** (header): Optional - SQL-like filter string to limit the records to retrieve. ex: '(Customers.customer_id == 123) | (Customers.customer_id==234)'
    """
    log.logger.debug(
        'Access \'/_table/{table_name}\' : run in delete_data(), input data table_name: [%s]' % table_name)
    log.logger.debug('filter: [%s]' % filterstr)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    return getattr(dataservice, 'delete_' + table_name.strip().capitalize() + '_byid')(filterstr)

@app.get(prefix+"/_table/{table_name}/{id}",
         tags=["Data - Row Level"],
         summary="Retrieve one record by identifier.",
         description="",
         )
async def get_data_by_id(table_name: str, id: str,
                         idfield: str = Header(None),
                         current_user: security.User = Depends(security.get_current_active_user)):
    """
        Parameters
        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **id** (path): **Required** - The id value of identifier ex:10 , for mutiple ids, use ex: 10-20-……
        - **idfield** (header): - Comma-delimited list of the fields used as identifiers. ex: 'Customers.id,Customers.id2'
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in get_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('idfield: [%s]' % idfield)
    log.logger.debug('id: [%s]' % id)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    idfldtuple = tuple(filter(None,idfield.replace(' ','').split(',')))
    idtuple = tuple(filter(None,id.replace(' ','').split('-')))
    idqrytuple = tuple(zip(idfldtuple,idtuple))
    idstr = ''
    for idqry in idqrytuple:
        idstr = idstr + "==".join(idqry)+","
    idwherestr = "("+ ") & (".join(tuple(filter(None, idstr.replace(' ', '').split(',')))) + ")"
    log.logger.debug('get_data_by_id() querystr: [%s]' % idwherestr)
    return getattr(dataservice, 'get_' + table_name.strip().capitalize() + '_byid')(idwherestr)

@app.post(prefix+"/_table/_querybyid/{table_name}",
          tags=["Data - Row Level"],
          summary="Retrieve one record by identifier.",
          description="",
          )
async def query_data_by_id(table_name: str, tablequerybyid: apimodel.RecordBody,
                           current_user: security.User = Depends(security.get_current_active_user)):
    """
            Parameters
            - **table_name** (path): **Required** - Name of the table to perform operations on.
            - **request body: Required**
            ```
                {
                 "data": {string}  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '{"Customers.customer_id":10,"Customers.ex_key_id":111}'
                 }
            ```
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/querybyid\' : run in query_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tablequerybyid)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    idstr = ''
    for key,value in tablequerybyid.data.items():
        idstr = idstr + key + "==" + str(value) + ","
    idwherestr = "("+ ") & (".join(tuple(filter(None, idstr.replace(' ', '').split(',')))) + ")"
    log.logger.debug('query_data_by_id() querystr: [%s]' % idwherestr)
    return getattr(dataservice, 'get_' + table_name.strip().capitalize() + '_byid')(idwherestr)

@app.put(prefix+"/_table/{table_name}/{id}",
         tags=["Data - Row Level"],
         summary="Replace the content of one record by identifier.",
         description="",
         )
async def put_data_by_id(table_name: str, id: str,
                         tableputbyid: apimodel.PutRecordBody,
                         current_user_role: bool = Depends(security.get_write_permission)):
    """
            Parameters
            - **table_name** (path): **Required** - Name of the table to perform operations on.
            - **id** (path): **Required** - The id value of identifier ex:10 , for mutiple ids, use ex: 10-20-……
            - **request body: Required**
            ```
                {
                 "data": {"name":"jack","phone":"55789"},  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '{"name":"jack","phone":"55789"}'
                 "ids": {string}  -- **Required** - Json formated fieldname-fieldvalue pair. ex: '"Customers.customer_id,Customers.ex_key_id"'
                 }
            ```
        """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in put_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('body: [%s]' % tableputbyid)
    log.logger.debug('id: [%s]' % id)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    updateentity = tableputbyid.data
    idtuple = tuple(filter(None,id.replace(' ','').split('-')))
    idstrtuple = tuple(filter(None,tableputbyid.ids.replace(' ','').split(',')))
    idkvtuple = tuple(zip(idstrtuple,idtuple))
    ikdv = dict((x, y) for x, y in idkvtuple)
    for key,value in ikdv.items():
        updateentity[key.strip(table_name+'.')] = value
    return getattr(dataservice, 'update_' + table_name.strip().capitalize() + '_byjson')(updateentity)

@app.delete(prefix+"/_table/{table_name}/{id}",
            tags=["Data - Row Level"],
            summary="Delete one record by identifier.",
            description="",
            )
async def delete_data_by_id(table_name: str, id: str,
                            idfield: str = Header(None, max_length=200),
                            current_user_role: bool = Depends(security.get_write_permission)):
    """
        Parameters
        - **table_name** (path): **Required** - Name of the table to perform operations on.
        - **id** (path): **Required** - The id value of identifier ex:10 , for mutiple ids, use ex: 10-20-……
        - **idfield** (header): - Comma-delimited list of the fields used as identifiers. ex: 'Customers.id,Customers.id2'
    """
    log.logger.debug(
        'Access \'/_table/{table_name}/{id}\' : run in delete_data_by_id(), input data table_name: [%s]' % table_name)
    log.logger.debug('id: [%s]' % id)
    log.logger.debug('idfield: [%s]' % idfield)
    if not dbmeta.DBMeta().check_table_schema(table_name):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail='Table [ %s ] not found' % table_name
        )
    dataservicemodel = importlib.import_module('services.' + table_name.strip().lower() + 'service')
    dataservice = getattr(dataservicemodel, table_name.strip().capitalize() + 'Service')()
    idfldtuple = tuple(filter(None, idfield.replace(' ', '').split(',')))
    idtuple = tuple(filter(None, id.replace(' ', '').split('-')))
    idqrytuple = tuple(zip(idfldtuple, idtuple))
    idstr = ''
    for idqry in idqrytuple:
        idstr = idstr + "==".join(idqry) + ","
    idwherestr = "("+ ") & (".join(tuple(filter(None, idstr.replace(' ', '').split(',')))) + ")"
    log.logger.debug('delete_data_by_id() querystr: [%s]' % idwherestr)
    return getattr(dataservice, 'delete_' + table_name.strip().capitalize() + '_byid')(idwherestr)

@app.get("/sys/config",
         tags=["System"],
         summary="Show the system configuration.",
         description="",
         )
async def sys_config(SecuretKey: str = Header(..., min_length=5),
                      current_user_role: bool = Depends(security.get_super_permission)):
    """
        Please use 'app_confirm_key' as SecuretKey to confirm the operation
        - **SecuretKey** (header): **Required** - use 'app_confirm_key' default value is 'Confirmed'.
    """
    log.logger.debug(
        'Access \'/sys/config\' : run in main.py, input data: [ %s ]' % SecuretKey)
    if SecuretKey == cfg['Application_Config'].app_confirm_key:
        return {
            "System_Config": cfg
        }
    else:
        return {
            "System_Config": 'Operation Aborted'
        }

@app.get("/sys/reloadmeta",
         tags=["System"],
         summary="Reload the Database Schema .",
         description="",
         )
async def reload_meta(SecuretKey: str = Header(..., min_length=5),
                      current_user_role: bool = Depends(security.get_super_permission)):

    """
        Please use 'app_confirm_key' as SecuretKey to confirm the operation
        - **SecuretKey** (header): **Required** - use 'app_confirm_key' default value is 'Confirmed'.
    """
    log.logger.debug(
        'Access \'/sys/reloadmeta\' : run in reload_meta(), input data: [ %s ]' % SecuretKey)
    if SecuretKey == cfg['Application_Config'].app_confirm_key:
        clear_meta_cache()
        schema_file = dbmeta.DBMeta().schema_file
        if os.path.exists(schema_file):
            os.remove(schema_file)
        dbmeta.DBMeta().load_metadata()
        dbmeta.DBMeta().gen_schema()
        dbmeta.DBMeta().load_schema()
        dbmeta.DBMeta().gen_models()
        dbmeta.DBMeta().gen_services()
        return {
            "Reload_Meta": 'Sucessful'
        }
    else:
        return {
            "Reload_Meta": 'Operation Aborted'
        }

@app.get("/sys/status",
         tags=["System"],
         summary="Show the database connection pool status.",
         description="",
         )
async def sys_status(SecuretKey: str = Header(..., min_length=5),
                      current_user_role: bool = Depends(security.get_super_permission)):
    """
        Please use 'app_confirm_key' as SecuretKey to confirm the operation
        - **SecuretKey** (header): **Required** - use 'app_confirm_key' default value is 'Confirmed'.
    """
    log.logger.debug(
        'Access \'/sys/status\' : run in main.py, input data: [ %s ]' % SecuretKey)
    if SecuretKey == cfg['Application_Config'].app_confirm_key:
        return {
            "Pool_status": dbengine.DBEngine().connect().pool.status()
        }
    else:
        return {
            "Sys_status": 'Operation Aborted'
        }

def clear_meta_cache():
    # cache file define
    metadata_pickle_filename = cfg['Schema_Config'].schema_cache_filename
    cache_path = os.path.join(os.path.expanduser("~"), ".neptune_cache")
    cache_file = os.path.join(cache_path, metadata_pickle_filename)
    if os.path.exists(cache_file):
        os.remove(cache_file)
        log.logger.info('API cache cleared ....')
    else:
        log.logger.info('API cache does not exists ....')