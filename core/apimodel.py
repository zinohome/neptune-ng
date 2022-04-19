#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune


from pydantic import BaseModel
from pydantic.class_validators import Optional
from pydantic.types import Json, List, Dict

from config import config

class TableQueryBody(BaseModel):
    queryfields: Optional[str] = None  # eg. "Customers.first_name,Customers.last_name,Customers.customer_id"
    distinct: Optional[bool] = None
    where: Optional[str] = None
    order_by: Optional[str] = None
    group_by: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    include_count: Optional[bool] = None
    count_only: Optional[bool] = None
    class Config:
        title = 'Table Query Model'
        anystr_strip_whitespace = True
        optional_by_default = False

class TablePostBody(BaseModel):
    data: List[Dict] = None
    class Config:
        title = 'Table Post Model'
        anystr_strip_whitespace = True
        optional_by_default = False

class TablePutBody(BaseModel):
    data: List[Dict] = None
    class Config:
        title = 'Table Put Model'
        anystr_strip_whitespace = True
        optional_by_default = False

class TableQueryByIdBody(BaseModel):
    fieldlist: str = '*'
    idfield: str = None
    id: str = None

class TablePutByIdBody(BaseModel):
    fieldvalue: str = None
    idfield: str = None

class UserFuncPostBody(BaseModel):
    sqlparam: str = None
