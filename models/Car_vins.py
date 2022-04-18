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

class Car_vins(SQLModel, table=True):
    model_id: int = Field(sa_column=Column("model_id", default=None, primary_key=False))
    option_set_id: int = Field(sa_column=Column("option_set_id", default=None, primary_key=False))
    manufactured_date: date = Field(sa_column=Column("manufactured_date", default=None, primary_key=False))
    manufactured_plant_id: int = Field(sa_column=Column("manufactured_plant_id", default=None, primary_key=False))
    vin: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)