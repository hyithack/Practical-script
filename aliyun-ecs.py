import json
from aliyunsdkcms.request.v20190101.DescribeMetricListRequest import DescribeMetricListRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


class AliAcsClient:
    def __init__(self, access_key_id, access_key_secret, region_id):
        self.credentials = AccessKeyCredential(access_key_id=access_key_id, access_key_secret=access_key_secret)
        self.client = AcsClient(region_id=region_id, credential=self.credentials)

    def get_instances(self, number=1):  # 修改页码默认第一页
        req = DescribeInstancesRequest()
        req.set_accept_format("json")
        req.set_PageNumber(number)
        req.set_MaxResults(100)
        resp = self.client.do_action_with_exception(req)
        resp_dict = json.loads(resp)
        instances = resp_dict.get("Instances").get("Instance")
        return [i.get("InstanceId") for i in instances]

    def get_cpu_metrics(self, instance_id, start_time, end_time, page):
        req = DescribeMetricListRequest()
        if start_time:
            req.set_StartTime(start_time)
        if end_time:
            req.set_EndTime(end_time)
        req.set_Namespace("acs_ecs_dashboard")
        req.set_MetricName("CPUUtilization")
        req.set_Dimensions([{"instanceId": instance_id}])
        req.set_accept_format("json")
        req.add_query_param('Page', page)
        resp = self.client.do_action_with_exception(req)
        result = json.loads(resp)
        data_points = result.get("Datapoints")
        data_points = json.loads(data_points)
        cpu = []
        for i in data_points:
            # cpu.append(i.get('instanceId'))
            cpu.append(i.get('Maximum'))
            Cpu = max(cpu)
        print("实例id: {} cpu使用率: {}%".format(instance_id, Cpu))
        # print(str(resp, encoding="utf-8"))

    def get_load_metrics(self, instance_id, start_time, end_time, page):
        req = DescribeMetricListRequest()
        if start_time:
            req.set_StartTime(start_time)
        if end_time:
            req.set_EndTime(end_time)
        req.set_Namespace("acs_ecs_dashboard")
        req.set_MetricName("load_15m")
        req.add_query_param('Page', page)
        req.set_Dimensions([{"instanceId": instance_id}])
        req.set_accept_format("json")
        resp = self.client.do_action_with_exception(req)
        result = json.loads(resp)
        data_points = result.get("Datapoints")
        data_points = json.loads(data_points)
        load = []
        for i in data_points:
            load.append(i.get('Maximum'))
            Load=max(load)
        print("实例id: {} 15分钟负载: {}".format(instance_id,Load))
        # print(str(resp, encoding="utf-8"))

    def get_mem_metrics(self, instance_id, start_time, end_time, page):
        req = DescribeMetricListRequest()
        if start_time:
            req.set_StartTime(start_time)
        if end_time:
            req.set_EndTime(end_time)
        req.set_Namespace("acs_ecs_dashboard")
        req.set_MetricName("memory_usedutilization")
        req.add_query_param('Page', page)
        req.set_Dimensions([{"instanceId": instance_id}])
        req.set_accept_format("json")
        resp = self.client.do_action_with_exception(req)
        result = json.loads(resp)
        data_points = result.get("Datapoints")
        data_points = json.loads(data_points)
        mem = []
        for i in data_points:
            mem.append(i.get('Maximum'))
            Mem=max(mem)
        print("实例id: {} 内存使用率: {}%".format(instance_id,Mem))
        # print(str(resp, encoding="utf-8"))


if __name__ == '__main__':
    region_ids = ["cn-shenzhen"]  # 按需添加地域
    for region in region_ids:
        client = AliAcsClient(
            access_key_id="LTAI**************9W",  # 添加id
            access_key_secret="SKq******************Rdwo",  # 添加secert
            region_id=region
        )
        instance_ids = client.get_instances()
        for instance in instance_ids:
            client.get_cpu_metrics(instance_id=instance, start_time=None, end_time=None, page="10")  # 修改启动时间，结束时间
            client.get_load_metrics(instance_id=instance, start_time=None, end_time=None, page="10")  # 修改启动时间，结束时间
            client.get_mem_metrics(instance_id=instance, start_time=None, end_time=None, page="10")  # 修改启动时间，结束时间
