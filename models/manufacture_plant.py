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

class manufacture_plant(SQLModel, table=True):
    plant_name:Optional[VARCHAR(50)] = Field(sa_column=Column("plant_name", default=None, primary_key=True))
    plant_type:Optional[TEXT(7)] = Field(sa_column=Column("plant_type", default=None, primary_key=True))
    plant_location:Optional[VARCHAR(100)] = Field(sa_column=Column("plant_location", default=None, primary_key=True))
    company_owned:Optional[INTEGER] = Field(sa_column=Column("company_owned", default=None, primary_key=True))
    manufacture_plant_id:Optional[INTEGER] = Field(sa_column=Column("manufacture_plant_id", default=None, primary_key=True))
