# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListManagedAccountsRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'control_id': 'str',
        'limit': 'int',
        'marker': 'str'
    }

    attribute_map = {
        'control_id': 'control_id',
        'limit': 'limit',
        'marker': 'marker'
    }

    def __init__(self, control_id=None, limit=None, marker=None):
        """ListManagedAccountsRequest

        The model defined in huaweicloud sdk

        :param control_id: 启用的控制策略信息。
        :type control_id: str
        :param limit: 分页页面的最大值。
        :type limit: int
        :param marker: 页面标记。
        :type marker: str
        """
        
        

        self._control_id = None
        self._limit = None
        self._marker = None
        self.discriminator = None

        if control_id is not None:
            self.control_id = control_id
        if limit is not None:
            self.limit = limit
        if marker is not None:
            self.marker = marker

    @property
    def control_id(self):
        """Gets the control_id of this ListManagedAccountsRequest.

        启用的控制策略信息。

        :return: The control_id of this ListManagedAccountsRequest.
        :rtype: str
        """
        return self._control_id

    @control_id.setter
    def control_id(self, control_id):
        """Sets the control_id of this ListManagedAccountsRequest.

        启用的控制策略信息。

        :param control_id: The control_id of this ListManagedAccountsRequest.
        :type control_id: str
        """
        self._control_id = control_id

    @property
    def limit(self):
        """Gets the limit of this ListManagedAccountsRequest.

        分页页面的最大值。

        :return: The limit of this ListManagedAccountsRequest.
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this ListManagedAccountsRequest.

        分页页面的最大值。

        :param limit: The limit of this ListManagedAccountsRequest.
        :type limit: int
        """
        self._limit = limit

    @property
    def marker(self):
        """Gets the marker of this ListManagedAccountsRequest.

        页面标记。

        :return: The marker of this ListManagedAccountsRequest.
        :rtype: str
        """
        return self._marker

    @marker.setter
    def marker(self, marker):
        """Sets the marker of this ListManagedAccountsRequest.

        页面标记。

        :param marker: The marker of this ListManagedAccountsRequest.
        :type marker: str
        """
        self._marker = marker

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
        if not isinstance(other, ListManagedAccountsRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
