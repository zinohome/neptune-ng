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

class car_vins(SQLModel, table=True):
    model_id:Optional[INTEGER] = Field(sa_column=Column("model_id", default=None, primary_key=True))
    option_set_id:Optional[INTEGER] = Field(sa_column=Column("option_set_id", default=None, primary_key=True))
    manufactured_date:Optional[DATE] = Field(sa_column=Column("manufactured_date", default=None, primary_key=True))
    manufactured_plant_id:Optional[INTEGER] = Field(sa_column=Column("manufactured_plant_id", default=None, primary_key=True))
    vin:Optional[INTEGER] = Field(sa_column=Column("vin", default=None, primary_key=True))
