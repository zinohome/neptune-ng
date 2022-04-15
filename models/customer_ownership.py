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

class customer_ownership(SQLModel, table=True):
    purchase_date:Optional[DATE] = Field(sa_column=Column("purchase_date", default=None, primary_key=True))
    purchase_price:Optional[INTEGER] = Field(sa_column=Column("purchase_price", default=None, primary_key=True))
    warantee_expire_date:Optional[DATE] = Field(sa_column=Column("warantee_expire_date", default=None, primary_key=True))
    dealer_id:Optional[INTEGER] = Field(sa_column=Column("dealer_id", default=None, primary_key=True))
    customer_id:Optional[INTEGER] = Field(sa_column=Column("customer_id", default=None, primary_key=True))
    vin:Optional[INTEGER] = Field(sa_column=Column("vin", default=None, primary_key=True))
