# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json
import pymysql

#连接数据库
conn= pymysql.connect(host='192.xxx.xxx.xx', user='root',password='xxxxxxxx', db ='aliyun',port=3306, charset='utf8')
print('连接数据库成功！')
cursor = conn.cursor()
#判断表是否存在，若存在则删除此表
cursor.execute("DROP TABLE IF EXISTS pkpk")
#创建表
sql = """CREATE TABLE `pkpk` (
  `CreationTime` varchar(255) DEFAULT NULL COMMENT '创建时间',
  `SerialNumber` varchar(255) DEFAULT NULL COMMENT '序列号',
  `Status` varchar(255) DEFAULT NULL COMMENT '运行状态',
  `InstanceId` varchar(255) DEFAULT NULL COMMENT '实例ID',
  `Description` varchar(255) DEFAULT NULL COMMENT '实例描述',
  `InstanceName` varchar(255) DEFAULT NULL COMMENT '实例名称',
  `RegionId` varchar(255) DEFAULT NULL COMMENT '所在区域',
  `ZoneId` varchar(255) DEFAULT NULL COMMENT '网络所在区域',
  `InstanceType` varchar(255) DEFAULT NULL COMMENT '实例类型',
  `OSNameEn` varchar(255) DEFAULT NULL COMMENT '操作系统型号',
  `OSType` varchar(255) DEFAULT NULL COMMENT '操作系统类型',
  `Cpu` varchar(255) DEFAULT NULL COMMENT 'CPU核心数',
  `Memory` varchar(255) DEFAULT NULL COMMENT '内存',
  `ExpiredTime` varchar(255) DEFAULT NULL COMMENT '实例到期时间',
  `PrimaryIpAddress` varchar(255) DEFAULT NULL COMMENT '实例私网ip',
  `ipAddress` varchar(255) DEFAULT NULL COMMENT '实例公网ip')"""
cursor.execute(sql)
conn.commit()


# AccessKey Id,
access_key_id = 'LTA*********************kB'
# AccessKey Secret,
access_key_secret = '4************************z8j'
# 区域id，根据实际情况补充列表
region_id = ['cn-qingdao', 'cn-beijing', 'cn-zhangjiakou', 'cn-huhehaote', 'cn-wulanchabu', 'cn-hangzhou',
             'cn-shanghai',
             'cn-shenzhen', 'cn-heyuan', 'cn-guangzhou', 'cn-chengdu', 'cn-nanjing', 'cn-hongkong', 'ap-southeast-1',
             'ap-southeast-2', 'ap-southeast-3', 'ap-southeast-5', 'ap-southeast-6', 'ap-southeast-7', 'ap-south-1',
             'ap-northeast-1', 'ap-northeast-2', 'us-west-1', 'us-east-1', 'eu-central-1', 'eu-west-1', 'me-east-1']


def get_ecs_data(access_key_id, access_key_secret, region_id):
    cli = client.AcsClient(access_key_id, access_key_secret, region_id)
    res = DescribeInstancesRequest.DescribeInstancesRequest()
    res.set_accept_format('json')
    res.set_PageSize(100)  ##  单页条数
    for i in range(1, 5):  ##  遍历500条数据，根据阿里云ecs实例实际情况调整
        res.set_PageNumber(i)  ## 遍历每页
        result = json.loads(cli.do_action_with_exception(res))
        ecs_info = result.get('Instances').get('Instance')
        # 遍历获取到的结果
        for info in ecs_info:
            CreationTime = info.get('CreationTime')  ## 创建时间
            SerialNumber = info.get('SerialNumber')  ## sn序列号
            Status = info.get('Status')  ## 实例状态
            InstanceId = info.get('InstanceId')  ## 实例id
            if info.get('Description'):
                Description = info.get('Description')
            else:
                Description = '{}'  ## 实例描述
            InstanceName = info.get('InstanceName')  ## 实例名称
            RegionId = info.get('RegionId')  ## 所在区域
            ZoneId = info.get('ZoneId')  ## 网络所在区域
            InstanceType = info.get('InstanceType')  ## 实例类型
            OSNameEn = info.get('OSNameEn')  ## 操作系统型号
            OSType = info.get('OSType')  ## 操作系统类型
            Cpu = str(info.get('Cpu'))  ## cpu核心数
            Memory = str(int(info.get('Memory')) / 1024)  ## 内存，单位G
            ExpiredTime = info.get('ExpiredTime')  ## 实例到期时间
            PrimaryIpAddress_ = info.get('NetworkInterfaces').get('NetworkInterface')
            PrimaryIpAddress = PrimaryIpAddress_[0].get('PrimaryIpAddress')  ## 实例私网ip
            if info.get('PublicIpAddress').get('IpAddress'):
                ipAddress = info.get('PublicIpAddress').get('IpAddress')
                if ipAddress:
                    ipAddress = ipAddress[0]
            else:
                ipAddress = '{}'
            innerIpAddress = info.get('InnerIpAddress').get('IpAddress')
            if innerIpAddress:
                innerIpAddress = innerIpAddress[0]
            else:
                innerIpAddress = '{}'
            print("insert into pkpk (CreationTime,SerialNumber,Status,InstanceId,Description,InstanceName,RegionId,ZoneId,InstanceType,OSNameEn,OSType,Cpu,Memory,ExpiredTime,PrimaryIpAddress,ipAddress) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(CreationTime, SerialNumber, Status, InstanceId, Description, InstanceName, RegionId, ZoneId, InstanceType, OSNameEn, OSType, Cpu, Memory, ExpiredTime, PrimaryIpAddress, ipAddress))
            sql = "insert into pkpk (CreationTime,SerialNumber,Status,InstanceId,Description,InstanceName,RegionId,ZoneId,InstanceType,OSNameEn,OSType,Cpu,Memory,ExpiredTime,PrimaryIpAddress,ipAddress) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(CreationTime, SerialNumber, Status, InstanceId, Description, InstanceName, RegionId, ZoneId, InstanceType, OSNameEn, OSType, Cpu, Memory, ExpiredTime, PrimaryIpAddress, ipAddress)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                cursor.rollback()
                print('写入失败')
for i in region_id:
    get_ecs_data(access_key_id=access_key_id, access_key_secret=access_key_secret, region_id=i)
