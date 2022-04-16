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
        return model.sortjson()

    def dump_model_list(self, modellist):
        jsonlist = json.loads('{"data":""}')
        jlst = list()
        for model in modellist:
            jlst.append(model.sortjson())
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
        finally:
            session.close()

    def create_customers(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return customer.customer_id
        except Exception as e:
            log.logger.error('Exception at create_customers(): %s ' % e)
            return None
        finally:
            session.close()

    def get_customers_byid(self, id):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(customers).where(col(customers.customer_id) == id)
                result = session.exec(statement).one()
                #log.logger.debug('get_customers_byid() result is : %s' % result)
                return result
        except Exception as e:
            log.logger.error('Exception at get_customers_byid(): %s ' % e)
            return None
        finally:
            session.close()

    def update_customers_byid(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return customer
        except Exception as e:
            log.logger.error('Exception at update_customers_byid(): %s ' % e)
            return None
        finally:
            session.close()

    def delete_customers_byid(self, id):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(customers).where(col(customers.customer_id) == id)
                result = session.exec(statement).one()
                #log.logger.debug('delete_customers_byid() result is : %s' % result)
                session.delete(result)
                session.commit()
                return True
        except Exception as e:
            log.logger.error('Exception at delete_customers_byid(): %s ' % e)
            return False
        finally:
            session.close()

    def query_customers(self):
        pass

if __name__ == '__main__':
    cs = customersService()
    log.logger.error('====================== getall_customers() ======================')
    log.logger.info('getall_customers() is : %s' % cs.getall_customers())
    log.logger.info('getall_customers() JSON is : %s' % cs.dump_model_list(cs.getall_customers()))
    log.logger.error('====================== a new customer ======================')
    customer_json_str = '{"first_name":"Jun","last_name":"Zhang","gender":"Male","household_income":120000,"birthdate":"1979-09-23","phone_number":17895329550,"email":"zhangjun@gmail.com"}'
    customer_json = json.loads(toolkit.jsonstrsort(customer_json_str))
    log.logger.debug('Customer data is : %s' % customer_json)
    custome_zhangjun = cs.new_model(customer_json)
    log.logger.info('Customer is : %s' % custome_zhangjun)
    #log.logger.debug('Customer JSON is : %s' % cs.dump_model(custome_zhangjun))
    log.logger.debug('Customer JSON is : %s' % custome_zhangjun.sortjson())
    log.logger.error('====================== create_customers() ======================')
    newid = cs.create_customers(custome_zhangjun)
    log.logger.info('The New Customer ID is : %s' % newid)
    log.logger.info('The New Customer is : %s' % custome_zhangjun)
    log.logger.error('====================== get_customers_byid() ======================')
    customer_mod = cs.get_customers_byid(newid)
    log.logger.info('The Customer get by id is : %s' % customer_mod)
    #log.logger.error('====================== delete_customers_byid() ======================')
    #cs.delete_customers_byid(newid)
    #log.logger.info('The Customer get by id is : %s' % cs.get_customers_byid(newid))
    log.logger.error('====================== update_customers_byid() ======================')
    customer_mod.first_name = "SanFeng"
    log.logger.info("The before mod customer is :%s" % customer_mod)
    customer_moded = cs.update_customers_byid(customer_mod)
    log.logger.info("The moded customer is :%s" % customer_moded)
