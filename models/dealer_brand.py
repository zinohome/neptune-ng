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

class dealer_brand(SQLModel, table=True):
    dealer_id:Optional[INTEGER] = Field(sa_column=Column("dealer_id", default=None, primary_key=True))
    brand_id:Optional[INTEGER] = Field(sa_column=Column("brand_id", default=None, primary_key=True))
