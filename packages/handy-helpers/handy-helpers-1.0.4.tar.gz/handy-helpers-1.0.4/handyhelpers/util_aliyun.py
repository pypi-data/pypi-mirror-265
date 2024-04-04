import os
import logging
import json
import base64
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeVSwitchesRequest import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DeleteInstancesRequest import DeleteInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from aliyunsdkecs.request.v20140526.DescribeInstanceAttributeRequest import DescribeInstanceAttributeRequest

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s [%(levelname)s]: %(message)s",
                    datefmt='%m-%d %H:%M')

logger = logging.getLogger()

class Bootstrap:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def load_config_from_json(self):
        with open(self.json_file_path, 'r') as file:
            self.config = json.load(file)

    def set_environment_variables(self):
        for key, value in self.config.items():
            os.environ[key] = value

    def run(self):
        self.load_config_from_json()
        self.set_environment_variables()

class VMProperty:
    def __init__(self, instance_id=None, hostname=None, public_ip=None, zone=None):
        self.instance_id = instance_id
        self.hostname = hostname
        self.public_ip = public_ip
        self.zone = zone

    def set_instance_id(self, instance_id):
        self.instance_id = instance_id

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_public_ip(self, public_ip):
        self.public_ip = public_ip

class CommandInvocationResult:
    def __init__(self, invocation_status, invoke_record_status, output):
        self.invocation_status = invocation_status
        self.invoke_record_status = invoke_record_status
        self.output = output

def do_action_return_json(client, request):
    response = client.do_action_with_exception(request)
    json_reponse = json.loads(str(response, encoding='utf-8'))
    return json_reponse

class AliyunECSSettings:
    def __init__(self, image_id=None, instance_type=None, system_disk_size=None, system_disk_category=None, system_disk_performance_level=None,
                 security_group_id=None, vswitch_id=None, host_name=None, password=None, biz_tags=None, spot_strategy=None):
        self.image_id = image_id
        self.instance_type = instance_type
        self.system_disk_size = system_disk_size
        self.system_disk_category = system_disk_category
        self.system_disk_performance_level = system_disk_performance_level
        self.security_group_id = security_group_id
        self.vswitch_id = vswitch_id
        self.host_name = host_name
        self.password = password
        self.biz_tags = biz_tags
        self.spot_strategy = spot_strategy

    def set_image_id(self, image_id):
        self.image_id = image_id

    def set_instance_type(self, instance_type):
        self.instance_type = instance_type

    def set_system_disk_size(self, system_disk_size):
        self.system_disk_size = system_disk_size

    def set_system_disk_category(self, system_disk_category):
        self.system_disk_category = system_disk_category

    def set_system_disk_performance_level(self, system_disk_performance_level):
        self.system_disk_performance_level = system_disk_performance_level

    def set_security_group_id(self, security_group_id):
        self.security_group_id = security_group_id

    def set_vswitch_id(self, vswitch_id):
        self.vswitch_id = vswitch_id

    def set_host_name(self, host_name):
        self.host_name = host_name

    def set_password(self, password):
        self.password = password

    def set_biz_tags(self, biz_tags):
        self.biz_tags = biz_tags

    def set_spot_strategy(self, spot_strategy):
        self.spot_strategy = spot_strategy

class AliyunECSManager:
    def __init__(self, region_id="ap-southeast-1"):
        self.client = self._get_client(region_id)
    
    def _delete_instance(self, instance_id):
        client = self._get_client()
        delete_instance_request = DeleteInstancesRequest()
        delete_instance_request.set_accept_format('json')
        delete_instance_request.set_InstanceIds([instance_id])
        delete_instance_request.set_Force(True)

        client.do_action_with_exception(delete_instance_request)

    def _get_client(self, region_id="ap-southeast-1"):
        credentials = self._get_default_credential()
        return AcsClient(region_id=region_id, credential=credentials)

    def _get_default_credential(self):
        return AccessKeyCredential(os.environ.get("ACCESS_KEY"), os.environ.get("ACCESS_SECRET"))

    def _run_instance(self, settings):
        client = self._get_client()
        run_instances_request = RunInstancesRequest()
        run_instances_request.set_accept_format('json')
        run_instances_request.set_ImageId(settings.image_id)
        run_instances_request.set_InstanceType(settings.instance_type)
        run_instances_request.set_SystemDiskCategory(settings.system_disk_category)
        run_instances_request.set_SystemDiskPerformanceLevel(settings.system_disk_performance_level)
        run_instances_request.set_SystemDiskSize(settings.system_disk_size)
        run_instances_request.set_SecurityGroupId(settings.security_group_id)
        run_instances_request.set_VSwitchId(settings.vswitch_id)
        run_instances_request.set_InstanceName(settings.host_name)
        run_instances_request.set_InternetMaxBandwidthOut(100)
        run_instances_request.set_HostName(settings.host_name)
        run_instances_request.set_Password(settings.password)
        run_instances_request.set_SpotStrategy(settings.spot_strategy)
        run_instances_request.set_Tags(settings.biz_tags)

        run_instances_response = client.do_action_with_exception(run_instances_request)
        run_instances_response_json = json.loads(str(run_instances_response, encoding='utf-8'))
        instance_id = run_instances_response_json['InstanceIdSets']['InstanceIdSet'][0]

        time.sleep(10) # wait for public ip addr assignment

        return self.describeInstanceAttribute(instance_id=instance_id)

    def _run_command(self, instance_id, cmd_content, timeout):
        try:
            client = self._get_client()
            request = RunCommandRequest()
            request.set_accept_format('json')
            request.set_Type("RunShellScript")
            request.set_CommandContent(cmd_content)
            request.set_InstanceIds([instance_id])
            request.set_Username("root")
            request.set_Timeout(timeout)

            response = client.do_action_with_exception(request)
            invoke_id = json.loads(response).get("InvokeId")
            return invoke_id

        except Exception as e:
            logger.error("run command failed")

    def _get_default_vswitch_id(self):
        client = self._get_client()
        request = DescribeVSwitchesRequest()
        request.set_accept_format('json')
        json_response = do_action_return_json(client, request)
    
        if len(json_response['VSwitches']['VSwitch']):
            return json_response['VSwitches']['VSwitch'][0]['VSwitchId']
        
        return 'na'
    
    def _get_default_security_group_id(self):
        client = self._get_client()
        request = DescribeSecurityGroupsRequest()
        request.set_accept_format('json')
        json_response = do_action_return_json(client, request)
    
        if len(json_response['SecurityGroups']['SecurityGroup']):
            return json_response['SecurityGroups']['SecurityGroup'][0]['SecurityGroupId']
        
        return None

    def execute_command(self, instance_id, cmd_content, timeout=600):
        return self._run_command(instance_id, cmd_content, timeout)
    
    def wait_invocation_result(self, invoke_id):
        client = self._get_client()
        request = DescribeInvocationResultsRequest()
        request.set_accept_format('json')
        request.set_InvokeId(invoke_id)
        invoke_record_status = ''
        invocation_status = ''
        invocation_output = ''

        while invoke_record_status != "Finished":
            time.sleep(3)
            json_response = do_action_return_json(client, request)
            invocation_result = json_response['Invocation']['InvocationResults']['InvocationResult'][0]
            base64_output = invocation_result['Output']
            invocation_status = invocation_result['InvocationStatus']
            invoke_record_status = invocation_result['InvokeRecordStatus']
            decoded_bytes = base64.b64decode(base64_output)
            invocation_output = decoded_bytes.decode('utf-8')

        return CommandInvocationResult(invocation_status=invocation_status, 
                                       invoke_record_status=invoke_record_status, 
                                       output=invocation_output)

    def clean(self, biz_tags):
        vm_properties = self.get_instances(biz_tags)

        if vm_properties == None:
          return
        
        for prop in vm_properties:
            self._delete_instance(prop.instance_id)

    def get_instances(self, biz_tags):
        client = self._get_client()
        describe_instance_request = DescribeInstancesRequest()
        describe_instance_request.set_accept_format('json')
        describe_instance_request.set_Tags(biz_tags)

        describe_instance_response = client.do_action_with_exception(describe_instance_request)
        json_response = json.loads(str(describe_instance_response, encoding='utf-8'))

        instances = json_response['Instances']['Instance']

        if len(instances) < 1:
            return None
        
        return list(map(lambda x: VMProperty(instance_id=x['InstanceId'], 
                                             public_ip=x['PublicIpAddress']['IpAddress'][0]), instances))
    
    def describeInstanceAttribute(self, instance_id):
        client = self._get_client()
        request = DescribeInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instance_id)
        data = do_action_return_json(client, request)
        public_ip_address = data.get("PublicIpAddress", {}).get("IpAddress", [])[0]
        host_name = data.get("HostName", "")

        return VMProperty(instance_id=instance_id, hostname=host_name, public_ip=public_ip_address)

    def create_instance(self, settings):
        return self._run_instance(settings)
  
    def create_default_settings(self):
        default_vswitch_id = self._get_default_vswitch_id()
        default_security_group_id = self._get_default_security_group_id()
    
        settings = AliyunECSSettings()
        settings.set_security_group_id(default_security_group_id)
        settings.set_vswitch_id(default_vswitch_id)
        settings.set_host_name('sg-001')
        settings.set_image_id("aliyun_3_x64_20G_qboot_alibase_20230727.vhd")
        settings.set_password(os.environ.get("VM_PASS"))
        settings.set_instance_type("ecs.g6.large")
        settings.set_system_disk_size(80)
        settings.set_system_disk_category("cloud_essd")
        settings.set_system_disk_performance_level("PL0")
        settings.set_spot_strategy("NoSpot")
        
        return settings