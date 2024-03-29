# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class UpdateTaskStatusReq:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'operation': 'str',
        'param': 'dict(str, str)',
        'switch_hce': 'bool',
        'is_need_consistency_check': 'bool'
    }

    attribute_map = {
        'operation': 'operation',
        'param': 'param',
        'switch_hce': 'switch_hce',
        'is_need_consistency_check': 'is_need_consistency_check'
    }

    def __init__(self, operation=None, param=None, switch_hce=None, is_need_consistency_check=None):
        """UpdateTaskStatusReq

        The model defined in huaweicloud sdk

        :param operation: 操作任务的具体动作 start:开始任务 stop:停止任务 collect_log:收集日志 test:测试 clone_test:克隆测试 restart:重新开始 sync_failed_rollback:同步失败回滚 network_check:网络质量检测 
        :type operation: str
        :param param: 操作参数
        :type param: dict(str, str)
        :param switch_hce: 是否切换hce
        :type switch_hce: bool
        :param is_need_consistency_check: 是否进行一致性校验
        :type is_need_consistency_check: bool
        """
        
        

        self._operation = None
        self._param = None
        self._switch_hce = None
        self._is_need_consistency_check = None
        self.discriminator = None

        self.operation = operation
        if param is not None:
            self.param = param
        if switch_hce is not None:
            self.switch_hce = switch_hce
        if is_need_consistency_check is not None:
            self.is_need_consistency_check = is_need_consistency_check

    @property
    def operation(self):
        """Gets the operation of this UpdateTaskStatusReq.

        操作任务的具体动作 start:开始任务 stop:停止任务 collect_log:收集日志 test:测试 clone_test:克隆测试 restart:重新开始 sync_failed_rollback:同步失败回滚 network_check:网络质量检测 

        :return: The operation of this UpdateTaskStatusReq.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """Sets the operation of this UpdateTaskStatusReq.

        操作任务的具体动作 start:开始任务 stop:停止任务 collect_log:收集日志 test:测试 clone_test:克隆测试 restart:重新开始 sync_failed_rollback:同步失败回滚 network_check:网络质量检测 

        :param operation: The operation of this UpdateTaskStatusReq.
        :type operation: str
        """
        self._operation = operation

    @property
    def param(self):
        """Gets the param of this UpdateTaskStatusReq.

        操作参数

        :return: The param of this UpdateTaskStatusReq.
        :rtype: dict(str, str)
        """
        return self._param

    @param.setter
    def param(self, param):
        """Sets the param of this UpdateTaskStatusReq.

        操作参数

        :param param: The param of this UpdateTaskStatusReq.
        :type param: dict(str, str)
        """
        self._param = param

    @property
    def switch_hce(self):
        """Gets the switch_hce of this UpdateTaskStatusReq.

        是否切换hce

        :return: The switch_hce of this UpdateTaskStatusReq.
        :rtype: bool
        """
        return self._switch_hce

    @switch_hce.setter
    def switch_hce(self, switch_hce):
        """Sets the switch_hce of this UpdateTaskStatusReq.

        是否切换hce

        :param switch_hce: The switch_hce of this UpdateTaskStatusReq.
        :type switch_hce: bool
        """
        self._switch_hce = switch_hce

    @property
    def is_need_consistency_check(self):
        """Gets the is_need_consistency_check of this UpdateTaskStatusReq.

        是否进行一致性校验

        :return: The is_need_consistency_check of this UpdateTaskStatusReq.
        :rtype: bool
        """
        return self._is_need_consistency_check

    @is_need_consistency_check.setter
    def is_need_consistency_check(self, is_need_consistency_check):
        """Sets the is_need_consistency_check of this UpdateTaskStatusReq.

        是否进行一致性校验

        :param is_need_consistency_check: The is_need_consistency_check of this UpdateTaskStatusReq.
        :type is_need_consistency_check: bool
        """
        self._is_need_consistency_check = is_need_consistency_check

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UpdateTaskStatusReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
