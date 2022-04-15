#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, VARCHAR, INTEGER, DATETIME
from sqlmodel import Field, SQLModel

class Customers(SQLModel, table=True):
    customer_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=Column("first_name", VARCHAR))
    last_name: str = Field(sa_column=Column("last_name", VARCHAR))
    gender: str = Field(sa_column=Column("gender", VARCHAR))
    household_income: int = Field(sa_column=Column("household_income", INTEGER))
    birthdate: str = Field(sa_column=Column("birthdate", VARCHAR))
    phone_number: int = Field(sa_column=Column("phone_number", INTEGER))
    email: str = Field(sa_column=Column("email", VARCHAR))
