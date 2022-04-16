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
        {% if column.primary_key | int > 0 %}
    {{column.name}}: Optional[{{column.pythonType}}] = Field(default=None, primary_key=True)
        {% else %}
    {{column.name}}: Optional[{{column.pythonType}}] = Field(sa_column=Column("{{ column.name }}", default={{column.default}}, primary_key=False))
        {% endif %}
    {% else %}
        {% if column.primary_key | int > 0 %}
    {{column.name}}: {{column.pythonType}} = Field(default=None, primary_key=True)
        {% else %}
    {{column.name}}: {{column.pythonType}} = Field(sa_column=Column("{{ column.name }}", default={{column.default}}, primary_key=False))
        {% endif %}
    {% endif %}
{% endfor %}

    def sortjson(self):
        return self.json(sort_keys=True)