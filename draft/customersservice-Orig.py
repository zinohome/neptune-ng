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
import distutils

import simplejson as json
from sqlalchemy import func

from sqlmodel import Session, select

from core import dbengine
from config import config
from models.customers import Customers
from util import log, toolkit

from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

'''config'''
cfg = config.app_config

'''logging'''
log = log.Logger(level=cfg['Application_Config'].app_log_level)

class CustomersService(object):
    def __init__(self):
        self._modelName = 'Customers'

    def new_model(self, modeljson):
        newmodel = Customers()
        for field in newmodel.__fields__.values():
            if field.name in modeljson:
                newmodel.__setattr__(field.name, modeljson[field.name])
        return newmodel

    def dump_model(self, model):
        return model.sortJson()

    def dump_model_list(self, modellist):
        jsonlist = json.loads('{"data":""}')
        jlst = list()
        for model in modellist:
            jlst.append(model.sortJson())
        jsonlist['data'] = jlst
        return jsonlist


    def getall_Customers(self):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                results = session.query(Customers).limit(cfg['Query_Config'].query_limit_upset)
                return results.all()
        except Exception as e:
            log.logger.error('Exception at getall_Customers(): %s ' % e)
            return None
        finally:
            session.close()

    def get_Customers_count(self):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                results = session.execute('select count(*) from Customers')
                return results.one()[0]
        except Exception as e:
            log.logger.error('Exception at get_Customers_count(): %s ' % e)
            return None
        finally:
            session.close()

    def create_Customers(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                pks = Customers.getPrimaryKeys(Customers)
                returnjson = {}
                for pk in pks:
                    returnjson[pk] = customer.__getattribute__(pk)
                return returnjson
        except Exception as e:
            log.logger.error('Exception at create_Customers(): %s ' % e)
            return None
        finally:
            session.close()

    def batch_create_Customers_byjson(self, jsonstr):
        batchjson = json.loads(jsonstr)
        batchdata = batchjson['data'] if 'data' in batchjson else None
        returnjson = {"ids":[],"data":[]}
        try:
            for bdata in batchdata:
                newentity = self.new_model(bdata)
                newid = self.create_Customers(newentity)
                returnjson['ids'].append(newid)
                returnjson['data'].append(newentity)
            return returnjson
        except Exception as e:
            log.logger.error('Exception at batch_create_Customers(): %s ' % e)
            return None

    def get_Customers_byid(self, idstr):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(Customers).where(eval(idstr))
                result = session.exec(statement).one()
                #log.logger.debug('get_Customers_byid() result is : %s' % result)
                return result
        except Exception as e:
            log.logger.error('Exception at get_Customers_byid(): %s ' % e)
            return None
        finally:
            session.close()

    def update_Customers(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return customer
        except Exception as e:
            log.logger.error('Exception at update_Customers(): %s ' % e)
            return None
        finally:
            session.close()

    def update_Customers_byjson(self, updatejson):
        log.logger.debug('The update JSON is: %s' % updatejson)
        pks = Customers.getPrimaryKeys(Customers)
        statement = select(Customers)
        for pk in pks:
            statement = statement.where(eval("Customers."+ pk + "==" +str(updatejson[pk])))
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                modcustomer = session.exec(statement).one()
                for field in modcustomer.__fields__.values():
                    if field.name in updatejson:
                        modcustomer.__setattr__(field.name, updatejson[field.name])
                session.add(modcustomer)
                session.commit()
                session.refresh(modcustomer)
                return modcustomer
        except Exception as e:
            log.logger.error('Exception at update_Customers_byjson(): %s ' % e)
            return None
        finally:
            session.close()

    def batch_update_Customers_byjson(self, jsonstr):
        batchjson = json.loads(jsonstr)
        batchdata = batchjson['data'] if 'data' in batchjson else None
        returnjson = {"data": []}
        try:
            for bdata in batchdata:
                updentity = self.update_Customers_byjson(bdata)
                returnjson['data'].append(updentity.sortJson())
            return returnjson
        except Exception as e:
            log.logger.error('Exception at batch_update_Customers_byjson(): %s ' % e)
            return None

    def delete_Customers_byid(self, idstr):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select(Customers).where(eval(idstr))
                result = session.exec(statement).one()
                log.logger.debug('delete_Customers_byid() result is : %s' % result)
                session.delete(result)
                session.commit()
                return True
        except Exception as e:
            log.logger.error('Exception at delete_Customers_byid(): %s ' % e)
            return False
        finally:
            session.close()

    def query_Customers(self,querystr):
        if toolkit.validQueryJson(querystr):
            queryjson = json.loads(querystr)
            log.logger.debug('The query JSON is: %s' % queryjson)
            #add querycolumns
            fullqueryfields = "Customers." + ",Customers.".join(tuple(Customers.__fields__.keys()))
            queryfields = fullqueryfields
            querystr = queryjson['queryfields'] if 'queryfields' in queryjson else None
            if querystr is not None:
                queryfields = querystr.replace(' ','')
                if "*" in queryfields:
                    queryfields=fullqueryfields
            if len(queryfields.split(',')) == 1:
                statement = select(eval(queryfields))
            else:
                statement = select(from_obj=Customers, columns=eval(queryfields))
            #add distinct
            bdistinct = queryjson['distinct'] if 'distinct' in queryjson else None
            if bdistinct is not None and distutils.util.strtobool(str(bdistinct)):
                statement = statement.distinct()
            # add where
            wherefields = queryjson['where'] if 'where' in queryjson else None
            if wherefields is not None:
                statement = statement.where(eval(wherefields))
            #add order_by
            orderfields = queryjson['order_by'] if 'order_by' in queryjson else None
            if orderfields is not None:
                orderfieldslist = tuple(filter(None,orderfields.replace(' ','').split(',')))
                for order in orderfieldslist:
                    statement = statement.order_by(eval(order))
            #add group_by
            #add limit & offset
            dlimit = queryjson['limit'] if 'limit' in queryjson else None
            if dlimit is not None:
                statement = statement.limit(dlimit)
            doffset = queryjson['offset'] if 'offset' in queryjson else None
            if doffset is not None:
                statement = statement.offset(doffset)
            log.logger.debug("The query Statement is: %s" % statement)
            include_count = False
            count_only = False
            record_count = 0
            # add include_count
            binclude_count = queryjson['include_count'] if 'include_count' in queryjson else None
            if binclude_count is not None and distutils.util.strtobool(str(binclude_count)):
                include_count = True
            # add count_only
            bcount_only = queryjson['count_only'] if 'count_only' in queryjson else None
            if bcount_only is not None and distutils.util.strtobool(str(bcount_only)):
                count_only = True
            try:
                engine = dbengine.DBEngine().connect()
                with Session(engine) as session:
                    #get record count
                    if include_count | count_only:
                        pks = Customers.getPrimaryKeys(Customers)
                        qfields = "Customers." + ",Customers.".join(tuple(pks))
                        if len(qfields.split(',')) == 1:
                            cstate = select([func.count(eval(qfields))])
                        else:
                            cstate = select([func.count(eval(qfields.split(',')[0]))])
                        # add distinct
                        if "distinct" in queryjson:
                            if bdistinct is not None and distutils.util.strtobool(str(bdistinct)):
                                cstate = cstate.distinct()
                        # add where
                        if wherefields is not None:
                            cstate = cstate.where(eval(wherefields))
                        log.logger.debug("The record count query Statement is: %s" % cstate)
                        record_count = session.exec(cstate).one()
                        #log.logger.debug("RecordCount is: %s" % record_count)
                    returnjson = {}
                    if count_only:
                        returnjson["record_count"] = record_count
                    else:
                        result = session.exec(statement)
                        data = []
                        rawdata = []
                        fields = ''
                        for row in result:
                            rawdata.append(row._data)
                            fields = row._fields
                            data.append(row._asdict())
                        # log.logger.debug('query_Customers() result is : %s' % result)
                        if include_count:
                            #returnjson = {"data": self.dump_model_list(result)}
                            returnjson["record_count"] = record_count
                            returnjson['fields'] = fields
                            returnjson['data'] = data
                            returnjson['rawdata'] = rawdata
                        else:
                            returnjson['fields'] = fields
                            returnjson['data'] = data
                            returnjson['rawdata'] = rawdata
                    # log.logger.debug('query_Customers() returndict is : %s' % returndict)
                    return returnjson
            except Exception as e:
                log.logger.error('Exception at query_Customers(): %s ' % e)
                return None
            finally:
                session.close()
        else:
            return None

if __name__ == '__main__':
    cs = CustomersService()
    log.logger.error('====================== getall_Customers() ======================')
    log.logger.info('getall_Customers() is : %s' % cs.getall_Customers())
    log.logger.info('getall_Customers() JSON is : %s' % cs.dump_model_list(cs.getall_Customers()))
    log.logger.error('====================== get_Customers_count() ======================')
    count = cs.get_Customers_count()
    log.logger.info('get_Customers_count() is : %s' % count)
    log.logger.error('====================== a new customer ======================')
    customer_json_str = '{"first_name":"Jun","last_name":"Zhang","gender":"Male","household_income":120000,"birthdate":"1979-09-23","phone_number":17895329550,"email":"zhangjun@gmail.com"}'
    customer_json = json.loads(toolkit.jsonstrsort(customer_json_str))
    log.logger.debug('Customer data is : %s' % customer_json)
    custome_zhangjun = cs.new_model(customer_json)
    log.logger.info('Customer is : %s' % custome_zhangjun)
    #log.logger.debug('Customer JSON is : %s' % cs.dump_model(custome_zhangjun))
    log.logger.debug('Customer JSON is : %s' % custome_zhangjun.sortJson())
    log.logger.error('====================== create_Customers() ======================')
    newid = cs.create_Customers(custome_zhangjun)
    log.logger.info('The New Customer ID is : %s' % newid)
    log.logger.info('The New Customer is : %s' % custome_zhangjun)
    log.logger.info('The New Customer JSON is : %s' % custome_zhangjun.sortJson())
    log.logger.error('====================== get_Customers_byid() ======================')
    customer_mod = cs.get_Customers_byid("Customers.customer_id=="+str(newid['customer_id']))
    log.logger.info('The Customer get by id is : %s' % customer_mod)
    log.logger.info('The Customer get by id JSON is : %s' % customer_mod.sortJson())
    log.logger.error('====================== update_Customers() ======================')
    customer_mod.first_name = "SanFeng"
    log.logger.info("The before mod customer is :%s" % customer_mod)
    customer_moded = cs.update_Customers(customer_mod)
    log.logger.info("The moded customer is :%s" % customer_moded)
    log.logger.error('====================== update_Customers_byjson() ======================')
    updatejsonstr = '{"birthdate": "1979-11-26", "customer_id": 630, "email": "zhangjunqd@gmail.com", "first_name": "Jun", "gender": "Male", "household_income": 120000, "last_name": "Zhang", "phone_number": 17895329550}'
    log.logger.info("The before mod customer is :%s" % updatejsonstr)
    customer_moded = cs.update_Customers_byjson(json.loads(updatejsonstr))
    log.logger.info("The moded customer is :%s" % customer_moded)
    log.logger.error('====================== query_Customers() ======================')
    querystr = '{' \
                   '"queryfields":"Customers.first_name,Customers.last_name,Customers.customer_id",' \
                   '"distinct":"False",' \
                   '"where":"((Customers.first_name != \'Jun\') | (Customers.household_income > 80001)) & (Customers.last_name != \'Zhang\')",' \
                   '"order_by":"Customers.phone_number.asc(), Customers.household_income.asc()",' \
                   '"group_by":"Customers.last_name",' \
                   '"limit":2,' \
                   '"offset":2,' \
                   '"include_count":"True",' \
                   '"count_only":"False"' \
                   '}'
    customer_result = cs.query_Customers(querystr)
    log.logger.info("The customer query result is :%s" % customer_result)
    log.logger.error('====================== delete_Customers_byid() ======================')
    log.logger.info('The delete Customer ID is : %s' % newid)
    cs.delete_Customers_byid("Customers.customer_id == "+str(newid['customer_id']))
    log.logger.info('The Customer get by id is : %s' % cs.get_Customers_byid(newid))
