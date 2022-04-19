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
from models.{{ name | lower }} import {{ name | capitalize }}
from util import log, toolkit

from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

'''config'''
cfg = config.app_config

'''logging'''
log = log.Logger(level=cfg['Application_Config'].app_log_level)

class {{ name | capitalize }}Service(object):
    def __init__(self):
        self._modelName = '{{ name | capitalize }}'

    def new_model(self, modeljson):
        newmodel = {{ name | capitalize }}()
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


    def getall_{{ name | capitalize }}(self):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                results = session.query({{ name | capitalize }}).limit(cfg['Query_Config'].query_limit_upset)
                return results.all()
        except Exception as e:
            log.logger.error('Exception at getall_{{ name | capitalize }}(): %s ' % e)
            return None
        finally:
            session.close()

    def get_{{ name | capitalize }}_count(self):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                results = session.execute('select count(*) from {{ name }}')
                return results.one()[0]
        except Exception as e:
            log.logger.error('Exception at get_{{ name | capitalize }}_count(): %s ' % e)
            return None
        finally:
            session.close()

    def create_{{ name | capitalize }}(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                pks = {{ name | capitalize }}.getPrimaryKeys({{ name | capitalize }})
                returnjson = {}
                for pk in pks:
                    returnjson[pk] = customer.__getattribute__(pk)
                return returnjson
        except Exception as e:
            log.logger.error('Exception at create_{{ name | capitalize }}(): %s ' % e)
            return None
        finally:
            session.close()

    def batch_create_{{ name | capitalize }}_byjson(self, jsonstr):
        batchjson = json.loads(jsonstr)
        batchdata = batchjson['data'] if 'data' in batchjson else None
        returnjson = {"ids": [], "data": []}
        try:
            for bdata in batchdata:
                newentity = self.new_model(bdata)
                newid = self.create_{{ name | capitalize }}(newentity)
                returnjson['ids'].append(newid)
                returnjson['data'].append(newentity)
            return returnjson
        except Exception as e:
            log.logger.error('Exception at batch_create_{{ name | capitalize }}(): %s ' % e)
            return None

    def get_{{ name | capitalize }}_byid(self, idstr):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select({{ name | capitalize }}).where(eval(idstr))
                result = session.exec(statement).one()
                #log.logger.debug('get_{{ name | capitalize }}_byid() result is : %s' % result)
                return result
        except Exception as e:
            log.logger.error('Exception at get_{{ name | capitalize }}_byid(): %s ' % e)
            return None
        finally:
            session.close()

    def update_{{ name | capitalize }}(self, customer):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                session.add(customer)
                session.commit()
                session.refresh(customer)
                return customer
        except Exception as e:
            log.logger.error('Exception at update_{{ name | capitalize }}(): %s ' % e)
            return None
        finally:
            session.close()

    def update_{{ name | capitalize }}_byjson(self, updatejson):
        log.logger.debug('The update JSON is: %s' % updatejson)
        pks = {{ name | capitalize }}.getPrimaryKeys({{ name | capitalize }})
        statement = select({{ name | capitalize }})
        for pk in pks:
            statement = statement.where(eval("{{ name | capitalize }}."+ pk + "==" +str(updatejson[pk])))
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
            log.logger.error('Exception at update_{{ name | capitalize }}_byjson(): %s ' % e)
            return None
        finally:
            session.close()

    def batch_update_{{ name | capitalize }}_byjson(self, jsonstr):
        batchjson = json.loads(jsonstr)
        batchdata = batchjson['data'] if 'data' in batchjson else None
        returnjson = {"data": []}
        try:
            for bdata in batchdata:
                updentity = self.update_{{ name | capitalize }}_byjson(bdata)
                returnjson['data'].append(updentity)
            return returnjson
        except Exception as e:
            log.logger.error('Exception at batch_update_{{ name | capitalize }}_byjson(): %s ' % e)
            return None

    def delete_{{ name | capitalize }}_byid(self, idstr):
        try:
            engine = dbengine.DBEngine().connect()
            with Session(engine) as session:
                statement = select({{ name | capitalize }}).where(eval(idstr))
                result = session.exec(statement).one()
                log.logger.debug('delete_{{ name | capitalize }}_byid() result is : %s' % result)
                session.delete(result)
                session.commit()
                return True
        except Exception as e:
            log.logger.error('Exception at delete_{{ name | capitalize }}_byid(): %s ' % e)
            return False
        finally:
            session.close()

    def query_{{ name | capitalize }}(self,querystr):
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
                statement = select(from_obj={{ name | capitalize }}, columns=eval(queryfields))
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
                        pks = {{ name | capitalize }}.getPrimaryKeys({{ name | capitalize }})
                        qfields = "{{ name | capitalize }}." + ",{{ name | capitalize }}.".join(tuple(pks))
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
                        # log.logger.debug('query_{{ name | capitalize }}() result is : %s' % result)
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
                    # log.logger.debug('query_{{ name | capitalize }}() returndict is : %s' % returndict)
                    return returnjson
            except Exception as e:
                log.logger.error('Exception at query_{{ name | capitalize }}(): %s ' % e)
                return None
            finally:
                session.close()
        else:
            return None

if __name__ == '__main__':
    pass