#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Neptune-NG
import collections
import simplejson as json

from sqlmodel import Session, select, col

from core import dbengine
from config import config
from models.customers import customers
from util import log, toolkit

from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

cfg = config.app_config

'''logging'''
log = log.Logger(level=cfg['Application_Config'].app_log_level)

class customersService(object):
    def __init__(self):
        self._modelName = 'customers'


    def new_model(self, modeljson):
        newmodel = customers()
        for field in newmodel.__fields__.values():
            if field.name in modeljson:
                newmodel.__setattr__(field.name, modeljson[field.name])
        return newmodel


    def dump_model(self, model):
        data = json.loads(model.json(), object_pairs_hook=collections.OrderedDict)
        return json.dumps(data)


    def dump_model_list(self, modellist):
        jsonlist = json.loads('{"data":""}')
        jlst = list()
        for model in modellist:
            jlst.append(self.dump_model(model))
        jsonlist['data'] = jlst
        return jsonlist


    def getall_customers(self):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                results = session.query(customers).limit(cfg['Query_Config'].query_limit_upset)
                return results.all()
        except Exception as e:
            log.logger.error('Exception at getall_Customers(): %s ' % e)
            return None


    def create_customers(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh()
                return customer.customer_id
        except Exception as e:
            log.logger.error('Exception at get_Customers(): %s ' % e)
            return None

    def get_customers(self, id):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(customers).where(col(customers.customer_id) == id)
                result = session.exec(statement).one()
                log.logger.debug('get_Customers() result is : %s' % result)
                return result
        except Exception as e:
            log.logger.error('Exception at get_Customers(): %s ' % e)
            return None

    def update_customers(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(customers).where(col(customers.customer_id) == customer.customer_id)
                result = session.exec(statement).one()
                log.logger.debug('update_Customers() result is : %s' % result)
                #log.logger.debug(result.__fields__)
                fields = result.__fields__.values()
                for field in fields:
                    #log.logger.debug(field)
                    #log.logger.debug(type(field))
                    #log.logger.debug(dir(field))
                    #log.logger.debug(field.name)
                    pass
                result.first_name = customer.first_name
                result.last_name = customer.last_name
                result.gender = customer.gender
                result.household_income = customer.household_income
                result.birthdate = customer.birthdate
                result.phone_number = customer.phone_number
                result.email = customer.email
                # TODO update by get all properties except key
                session.add(result)
                session.commit()
                return 1
        except Exception as e:
            log.logger.error('Exception at get_Customers(): %s ' % e)
            return None

    def delete_customers(self, id):
        pass

    def query_customers(self):
        pass

if __name__ == '__main__':
    cs = customersService()
    log.logger.info('getall_customers() is : %s' % cs.getall_customers())
    log.logger.info('getall_customers() JSON is : %s' % cs.dump_model_list(cs.getall_customers()))
    customer_json_str = '{"first_name":"Jun","last_name":"Zhang","gender":"Male","household_income":120000,"birthdate":"1979-09-23","phone_number":17895329550,"email":"zhangjun@gmail.com"}'
    customer_json = json.loads(customer_json_str)
    log.logger.debug('Customer data is : %s' % customer_json)
    custome_zhangjun = cs.new_model(customer_json)
    log.logger.debug('Customer is : %s' % custome_zhangjun)
    log.logger.debug('Customer JSON is : %s' % cs.dump_model(custome_zhangjun))
    #log.logger.debug('Customer JSON is : %s' % custome_zhangjun.json())


    '''
    cus1 = cs.get_customers(1)
    log.logger.info('cus1 is : %s' % cus1)
    log.logger.info('cus1 type is : %s' % type(cus1))
    cus2 = customers(last_name='Jacobs', household_income=120000, phone_number=9177554315, customer_id=1, birthdate='1990-12-13', first_name='Jeremy', gender='Male', email='Jeremy@Gmail.com')
    log.logger.info('cus2 is : %s' % cus2)
    cs.update_customers(cus2)
    cus3 = cs.get_customers(1)
    log.logger.info('cus3 is : %s' % cus3)
    '''