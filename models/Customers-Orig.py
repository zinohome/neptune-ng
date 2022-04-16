#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune-NG

from typing import Optional
from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, SQLModel
from datetime import date, timedelta, time, datetime
import decimal

class customers(SQLModel, table=True):
    first_name: str = Field(sa_column=Column("first_name", default=None, primary_key=False))
    last_name: str = Field(sa_column=Column("last_name", default=None, primary_key=False))
    gender: Optional[str] = Field(sa_column=Column("gender", default=None, primary_key=False))
    household_income: Optional[int] = Field(sa_column=Column("household_income", default=None, primary_key=False))
    birthdate: date = Field(sa_column=Column("birthdate", default=None, primary_key=False))
    phone_number: int = Field(sa_column=Column("phone_number", default=None, primary_key=False))
    email: Optional[str] = Field(sa_column=Column("email", default=None, primary_key=False))
    customer_id: Optional[int] = Field(sa_column=Column("customer_id", default=None, primary_key=True))
