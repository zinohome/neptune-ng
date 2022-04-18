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

class Dealers(SQLModel, table=True):
    dealer_name: str = Field(sa_column=Column("dealer_name", default=None, primary_key=False))
    dealer_address: Optional[str] = Field(sa_column=Column("dealer_address", default=None, primary_key=False))
    dealer_id: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)