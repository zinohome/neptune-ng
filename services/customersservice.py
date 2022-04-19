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
                return json.dumps(returnjson)
        except Exception as e:
            log.logger.error('Exception at create_Customers(): %s ' % e)
            return None
        finally:
            session.close()

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

    def update_Customers_byjson(self, updatejsonstr):
        updatejson = json.loads(updatejsonstr)
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
            if "queryfields" in queryjson:
                queryfields = queryjson['queryfields'].replace(' ','')
                if "*" in queryfields:
                    queryfields=fullqueryfields
            if len(queryfields.split(',')) == 1:
                statement = select(eval(queryfields))
            else:
                statement = select(from_obj=Customers, columns=eval(queryfields))
            #add distinct
            if "distinct" in queryjson:
                if distutils.util.strtobool(queryjson['distinct'].replace(' ','')):
                    statement = statement.distinct()
            #add where
            wherefields = queryjson['where'] if 'where' in queryjson else None
            if wherefields is not None:
                statement = statement.where(eval(wherefields))
            #add ordercolumns
            if "order_by" in queryjson:
                orderfields = queryjson['order_by']
                orderfieldslist = tuple(filter(None,orderfields.replace(' ','').split(',')))
                for order in orderfieldslist:
                    statement = statement.order_by(eval(order))
            #add group_by
            #add limit & offset
            if "limit" in queryjson:
                statement = statement.limit(queryjson['limit'])
            if "offset" in queryjson:
                statement = statement.offset(queryjson['offset'])
            log.logger.debug("The query Statement is: %s" % statement)
            include_count = False
            count_only = False
            record_count = 0
            # add include_count
            if "include_count" in queryjson:
                if distutils.util.strtobool(queryjson['include_count'].replace(' ', '')):
                    include_count = True
            # add count_only
            if "count_only" in queryjson:
                if distutils.util.strtobool(queryjson['count_only'].replace(' ', '')):
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
                            if distutils.util.strtobool(queryjson['distinct'].replace(' ', '')):
                                cstate = cstate.distinct()
                        # add where
                        if "where" in queryjson:
                            wherefields = queryjson['where']
                            cstate = cstate.where(eval(wherefields))
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
    pass