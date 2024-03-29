# coding: utf-8

import six

from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class NeutronListSubnetsResponse(SdkResponse):

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'subnets': 'list[NeutronSubnet]',
        'subnets_links': 'list[NeutronPageLink]'
    }

    attribute_map = {
        'subnets': 'subnets',
        'subnets_links': 'subnets_links'
    }

    def __init__(self, subnets=None, subnets_links=None):
        """NeutronListSubnetsResponse

        The model defined in huaweicloud sdk

        :param subnets: subnet对象列表
        :type subnets: list[:class:`huaweicloudsdkvpc.v2.NeutronSubnet`]
        :param subnets_links: 分页信息
        :type subnets_links: list[:class:`huaweicloudsdkvpc.v2.NeutronPageLink`]
        """
        
        super(NeutronListSubnetsResponse, self).__init__()

        self._subnets = None
        self._subnets_links = None
        self.discriminator = None

        if subnets is not None:
            self.subnets = subnets
        if subnets_links is not None:
            self.subnets_links = subnets_links

    @property
    def subnets(self):
        """Gets the subnets of this NeutronListSubnetsResponse.

        subnet对象列表

        :return: The subnets of this NeutronListSubnetsResponse.
        :rtype: list[:class:`huaweicloudsdkvpc.v2.NeutronSubnet`]
        """
        return self._subnets

    @subnets.setter
    def subnets(self, subnets):
        """Sets the subnets of this NeutronListSubnetsResponse.

        subnet对象列表

        :param subnets: The subnets of this NeutronListSubnetsResponse.
        :type subnets: list[:class:`huaweicloudsdkvpc.v2.NeutronSubnet`]
        """
        self._subnets = subnets

    @property
    def subnets_links(self):
        """Gets the subnets_links of this NeutronListSubnetsResponse.

        分页信息

        :return: The subnets_links of this NeutronListSubnetsResponse.
        :rtype: list[:class:`huaweicloudsdkvpc.v2.NeutronPageLink`]
        """
        return self._subnets_links

    @subnets_links.setter
    def subnets_links(self, subnets_links):
        """Sets the subnets_links of this NeutronListSubnetsResponse.

        分页信息

        :param subnets_links: The subnets_links of this NeutronListSubnetsResponse.
        :type subnets_links: list[:class:`huaweicloudsdkvpc.v2.NeutronPageLink`]
        """
        self._subnets_links = subnets_links

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
        if not isinstance(other, NeutronListSubnetsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
