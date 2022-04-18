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

class Car_options(SQLModel, table=True):
    model_id: Optional[int] = Field(sa_column=Column("model_id", default=None, primary_key=False))
    engine_id: int = Field(sa_column=Column("engine_id", default=None, primary_key=False))
    transmission_id: int = Field(sa_column=Column("transmission_id", default=None, primary_key=False))
    chassis_id: int = Field(sa_column=Column("chassis_id", default=None, primary_key=False))
    premium_sound_id: Optional[int] = Field(sa_column=Column("premium_sound_id", default=None, primary_key=False))
    color: str = Field(sa_column=Column("color", default=None, primary_key=False))
    option_set_price: int = Field(sa_column=Column("option_set_price", default=None, primary_key=False))
    option_set_id: Optional[int] = Field(default=None, primary_key=True)

    def sortjson(self):
        return self.json(sort_keys=True)