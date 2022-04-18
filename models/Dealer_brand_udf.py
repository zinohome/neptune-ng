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

class Dealer_brand(SQLModel, table=True):
    dealer_id: int = Field(default=None, primary_key=True)
    brand_id: int = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)