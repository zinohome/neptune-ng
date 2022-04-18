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
from config import config


class TableQueryBody(BaseModel):
    querystr: str = '{' \
                   '"queryfields":"Customers.first_name,Customers.last_name,Customers.customer_id",' \
                   '"distinct":"True",' \
                   '"where":"((Customers.first_name != \'Jun\') | (Customers.household_income > 80001)) & (Customers.last_name != \'Zhang\')",' \
                   '"order_by":"Customers.phone_number.asc(), Customers.household_income.asc()",' \
                   '"group_by":"Customers.last_name",' \
                   '"limit":2,' \
                   '"offset":2,' \
                   '"include_count":"True",' \
                   '"count_only":"False"' \
                   '}'


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