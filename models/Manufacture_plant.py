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

class Manufacture_plant(SQLModel, table=True):
    plant_name: str = Field(sa_column=Column("plant_name", default=None, primary_key=False))
    plant_type: Optional[str] = Field(sa_column=Column("plant_type", default=None, primary_key=False))
    plant_location: Optional[str] = Field(sa_column=Column("plant_location", default=None, primary_key=False))
    company_owned: Optional[int] = Field(sa_column=Column("company_owned", default=None, primary_key=False))
    manufacture_plant_id: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)