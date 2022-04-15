#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune

from typing import Optional
from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, SQLModel

class customers(SQLModel, table=True):
    first_name:Optional[TEXT(50)] = Field(sa_column=Column("first_name", default=None, primary_key=True))
    last_name:Optional[TEXT(50)] = Field(sa_column=Column("last_name", default=None, primary_key=True))
    gender:Optional[TEXT(20)] = Field(sa_column=Column("gender", default=None, primary_key=True))
    household_income:Optional[INTEGER] = Field(sa_column=Column("household_income", default=None, primary_key=True))
    birthdate:Optional[DATE] = Field(sa_column=Column("birthdate", default=None, primary_key=True))
    phone_number:Optional[INTEGER] = Field(sa_column=Column("phone_number", default=None, primary_key=True))
    email:Optional[TEXT(128)] = Field(sa_column=Column("email", default=None, primary_key=True))
    customer_id:Optional[INTEGER] = Field(sa_column=Column("customer_id", default=None, primary_key=True))
