from typing import Optional

from sqlalchemy import Column, VARCHAR
from sqlmodel import Field, SQLModel

class {{ table_name }}(SQLModel, table=True):
{% for field in fields %}
    {{ field.name }}:Optional[{{ field.type }}] = Field(sa_column=Column("{{ field.name }}", default=None, primary_key=True)
{% endfor %}
