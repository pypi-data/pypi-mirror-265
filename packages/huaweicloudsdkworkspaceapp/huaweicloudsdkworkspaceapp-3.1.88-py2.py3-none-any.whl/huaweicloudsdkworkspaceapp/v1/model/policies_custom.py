# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class PoliciesCustom:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'custom_configuration1_enable': 'bool',
        'options': 'CustomOptions'
    }

    attribute_map = {
        'custom_configuration1_enable': 'custom_configuration1_enable',
        'options': 'options'
    }

    def __init__(self, custom_configuration1_enable=None, options=None):
        """PoliciesCustom

        The model defined in huaweicloud sdk

        :param custom_configuration1_enable: 自定义策略配置项1： false: 表示关闭 true: 表示开启
        :type custom_configuration1_enable: bool
        :param options: 
        :type options: :class:`huaweicloudsdkworkspaceapp.v1.CustomOptions`
        """
        
        

        self._custom_configuration1_enable = None
        self._options = None
        self.discriminator = None

        if custom_configuration1_enable is not None:
            self.custom_configuration1_enable = custom_configuration1_enable
        if options is not None:
            self.options = options

    @property
    def custom_configuration1_enable(self):
        """Gets the custom_configuration1_enable of this PoliciesCustom.

        自定义策略配置项1： false: 表示关闭 true: 表示开启

        :return: The custom_configuration1_enable of this PoliciesCustom.
        :rtype: bool
        """
        return self._custom_configuration1_enable

    @custom_configuration1_enable.setter
    def custom_configuration1_enable(self, custom_configuration1_enable):
        """Sets the custom_configuration1_enable of this PoliciesCustom.

        自定义策略配置项1： false: 表示关闭 true: 表示开启

        :param custom_configuration1_enable: The custom_configuration1_enable of this PoliciesCustom.
        :type custom_configuration1_enable: bool
        """
        self._custom_configuration1_enable = custom_configuration1_enable

    @property
    def options(self):
        """Gets the options of this PoliciesCustom.

        :return: The options of this PoliciesCustom.
        :rtype: :class:`huaweicloudsdkworkspaceapp.v1.CustomOptions`
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this PoliciesCustom.

        :param options: The options of this PoliciesCustom.
        :type options: :class:`huaweicloudsdkworkspaceapp.v1.CustomOptions`
        """
        self._options = options

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
        if not isinstance(other, PoliciesCustom):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
