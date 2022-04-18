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

class Models(SQLModel, table=True):
    model_name: str = Field(sa_column=Column("model_name", default=None, primary_key=False))
    model_base_price: int = Field(sa_column=Column("model_base_price", default=None, primary_key=False))
    brand_id: int = Field(sa_column=Column("brand_id", default=None, primary_key=False))
    model_id: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)