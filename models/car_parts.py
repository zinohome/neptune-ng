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

class car_parts(SQLModel, table=True):
    part_name:Optional[VARCHAR(100)] = Field(sa_column=Column("part_name", default=None, primary_key=True))
    manufacture_plant_id:Optional[INTEGER] = Field(sa_column=Column("manufacture_plant_id", default=None, primary_key=True))
    manufacture_start_date:Optional[DATE] = Field(sa_column=Column("manufacture_start_date", default=None, primary_key=True))
    manufacture_end_date:Optional[DATE] = Field(sa_column=Column("manufacture_end_date", default=None, primary_key=True))
    part_recall:Optional[INTEGER] = Field(sa_column=Column("part_recall", default=None, primary_key=True))
    part_id:Optional[INTEGER] = Field(sa_column=Column("part_id", default=None, primary_key=True))
