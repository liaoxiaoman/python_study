# -*- coding:utf-8 -*-
import xmlrpclib
# 登录
common = xmlrpclib.ServerProxy('{}xmlrpc/2/common'.format('http://101.201.75.114:7015/'))
uid = common.authenticate('attendance', 'admin', 'admin', {})
# 调用方法接口
models = xmlrpclib.ServerProxy('{}xmlrpc/2/object'.format('http://101.201.75.114:7015/'))
# 查询
result_list = models.execute_kw('attendance', uid, 'admin', 'hr.employee', 'search', [[['id', '>', 0], ['id', '<', 1000]]])
result_details = models.execute_kw('attendance', uid, 'admin', 'hr.employee', 'search_read', [[['id', '>', 0], ['id', '<', 1000]]])
# 修改
models.execute_kw('attendance', uid, 'admin', 'hr.employee', 'write', [[1], {'notes': '写操作'}])
# 增加
new_id = models.execute_kw('attendance', uid, 'admin', 'hr.employee', 'create', [{'name': "New HR"}])
# 删除
models.execute_kw('attendance', uid, 'admin', 'hr.employee', 'unlink', [[new_id]])
# 自定义方法
# models.execute_kw('attendance', uid, 'admin', 'hr.employee', '方法名', '参数')