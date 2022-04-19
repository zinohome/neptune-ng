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

from config import config


class TableQueryBody(BaseModel):
    queryfields: Optional[str] = None # eg. "Customers.first_name,Customers.last_name,Customers.customer_id"
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

class TableQueryByIdBody(BaseModel):
    fieldlist: str = '*'
    idfield: str = None
    id: str = None


class TablePostBody(BaseModel):
    fieldvalue: str = None
    idfield: str = None


class TablePutByIdBody(BaseModel):
    fieldvalue: str = None
    idfield: str = None


class TablePutBody(BaseModel):
    filter: str = None
    filterparam: str = None
    fieldvalue: str = None


class UserFuncPostBody(BaseModel):
    sqlparam: str = None
