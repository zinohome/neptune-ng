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

class car_options(SQLModel, table=True):
    model_id:Optional[INTEGER] = Field(sa_column=Column("model_id", default=None, primary_key=True))
    engine_id:Optional[INTEGER] = Field(sa_column=Column("engine_id", default=None, primary_key=True))
    transmission_id:Optional[INTEGER] = Field(sa_column=Column("transmission_id", default=None, primary_key=True))
    chassis_id:Optional[INTEGER] = Field(sa_column=Column("chassis_id", default=None, primary_key=True))
    premium_sound_id:Optional[INTEGER] = Field(sa_column=Column("premium_sound_id", default=None, primary_key=True))
    color:Optional[VARCHAR(30)] = Field(sa_column=Column("color", default=None, primary_key=True))
    option_set_price:Optional[INTEGER] = Field(sa_column=Column("option_set_price", default=None, primary_key=True))
    option_set_id:Optional[INTEGER] = Field(sa_column=Column("option_set_id", default=None, primary_key=True))
