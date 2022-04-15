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

class {{ name | lower }}(SQLModel, table=True):
{% for column in columns %}
    {{ column.name }}:Optional[{{ column.type }}] = Field(sa_column=Column("{{ column.name }}", default=None, primary_key=True))
{% endfor %}
