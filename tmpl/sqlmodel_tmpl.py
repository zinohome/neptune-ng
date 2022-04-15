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
{% for field in fields %}
    {{ field.name }}:Optional[{{ field.type }}] = Field(sa_column=Column("{{ field.name }}", default=None, primary_key=True)
{% endfor %}
