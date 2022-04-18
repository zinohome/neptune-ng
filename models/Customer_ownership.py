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

class Customer_ownership(SQLModel, table=True):
    purchase_date: date = Field(sa_column=Column("purchase_date", default=None, primary_key=False))
    purchase_price: int = Field(sa_column=Column("purchase_price", default=None, primary_key=False))
    warantee_expire_date: Optional[date] = Field(sa_column=Column("warantee_expire_date", default=None, primary_key=False))
    dealer_id: int = Field(sa_column=Column("dealer_id", default=None, primary_key=False))
    customer_id: int = Field(default=None, primary_key=True)
    vin: int = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)