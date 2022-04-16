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

class {{ name | lower }}(SQLModel, table=True):
{% for column in columns %}
    {% if column.nullable == 'True' %}
    {{column.name}}: Optional[{{column.pythonType}}] = Field(sa_column=Column("{{ column.name }}", default={{column.default}}, primary_key={{column.primary_key | int > 0}}))
    {% else %}
    {{column.name}}: {{column.pythonType}} = Field(sa_column=Column("{{ column.name }}", default={{column.default}}, primary_key={{column.primary_key | int > 0}}))
    {% endif %}
{% endfor %}
