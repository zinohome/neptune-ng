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

class Car_parts(SQLModel, table=True):
    part_name: str = Field(sa_column=Column("part_name", default=None, primary_key=False))
    manufacture_plant_id: int = Field(sa_column=Column("manufacture_plant_id", default=None, primary_key=False))
    manufacture_start_date: date = Field(sa_column=Column("manufacture_start_date", default=None, primary_key=False))
    manufacture_end_date: Optional[date] = Field(sa_column=Column("manufacture_end_date", default=None, primary_key=False))
    part_recall: Optional[int] = Field(sa_column=Column("part_recall", default=0, primary_key=False))
    part_id: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)