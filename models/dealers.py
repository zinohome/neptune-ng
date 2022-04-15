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

class dealers(SQLModel, table=True):
    dealer_name:Optional[VARCHAR(50)] = Field(sa_column=Column("dealer_name", default=None, primary_key=True))
    dealer_address:Optional[VARCHAR(100)] = Field(sa_column=Column("dealer_address", default=None, primary_key=True))
    dealer_id:Optional[INTEGER] = Field(sa_column=Column("dealer_id", default=None, primary_key=True))
