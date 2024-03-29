# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RocketMQExtendProductInfoEntity:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'type': 'str',
        'product_id': 'str',
        'ecs_flavor_id': 'str',
        'billing_code': 'str',
        'arch_types': 'list[str]',
        'charging_mode': 'list[str]',
        'ios': 'list[RocketMQExtendProductIosEntity]',
        'properties': 'RocketMQExtendProductPropertiesEntity',
        'available_zones': 'list[str]',
        'unavailable_zones': 'list[str]',
        'support_features': 'list[RocketMQProductSupportFeaturesEntity]',
        'qingtian_incompatible': 'bool'
    }

    attribute_map = {
        'type': 'type',
        'product_id': 'product_id',
        'ecs_flavor_id': 'ecs_flavor_id',
        'billing_code': 'billing_code',
        'arch_types': 'arch_types',
        'charging_mode': 'charging_mode',
        'ios': 'ios',
        'properties': 'properties',
        'available_zones': 'available_zones',
        'unavailable_zones': 'unavailable_zones',
        'support_features': 'support_features',
        'qingtian_incompatible': 'qingtian_incompatible'
    }

    def __init__(self, type=None, product_id=None, ecs_flavor_id=None, billing_code=None, arch_types=None, charging_mode=None, ios=None, properties=None, available_zones=None, unavailable_zones=None, support_features=None, qingtian_incompatible=None):
        """RocketMQExtendProductInfoEntity

        The model defined in huaweicloud sdk

        :param type: 实例类型
        :type type: str
        :param product_id: 产品ID
        :type product_id: str
        :param ecs_flavor_id: 该产品使用的ECS规格
        :type ecs_flavor_id: str
        :param billing_code: 账单计费类型。
        :type billing_code: str
        :param arch_types: 支持的CPU架构类型
        :type arch_types: list[str]
        :param charging_mode: 支持的计费模式类型
        :type charging_mode: list[str]
        :param ios: 磁盘IO信息
        :type ios: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductIosEntity`]
        :param properties: 
        :type properties: :class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductPropertiesEntity`
        :param available_zones: 有可用资源的可用区列表
        :type available_zones: list[str]
        :param unavailable_zones: 资源售罄的可用区列表
        :type unavailable_zones: list[str]
        :param support_features: 支持的特性功能
        :type support_features: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQProductSupportFeaturesEntity`]
        :param qingtian_incompatible: 是否为擎天实例。
        :type qingtian_incompatible: bool
        """
        
        

        self._type = None
        self._product_id = None
        self._ecs_flavor_id = None
        self._billing_code = None
        self._arch_types = None
        self._charging_mode = None
        self._ios = None
        self._properties = None
        self._available_zones = None
        self._unavailable_zones = None
        self._support_features = None
        self._qingtian_incompatible = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if product_id is not None:
            self.product_id = product_id
        if ecs_flavor_id is not None:
            self.ecs_flavor_id = ecs_flavor_id
        if billing_code is not None:
            self.billing_code = billing_code
        if arch_types is not None:
            self.arch_types = arch_types
        if charging_mode is not None:
            self.charging_mode = charging_mode
        if ios is not None:
            self.ios = ios
        if properties is not None:
            self.properties = properties
        if available_zones is not None:
            self.available_zones = available_zones
        if unavailable_zones is not None:
            self.unavailable_zones = unavailable_zones
        if support_features is not None:
            self.support_features = support_features
        if qingtian_incompatible is not None:
            self.qingtian_incompatible = qingtian_incompatible

    @property
    def type(self):
        """Gets the type of this RocketMQExtendProductInfoEntity.

        实例类型

        :return: The type of this RocketMQExtendProductInfoEntity.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this RocketMQExtendProductInfoEntity.

        实例类型

        :param type: The type of this RocketMQExtendProductInfoEntity.
        :type type: str
        """
        self._type = type

    @property
    def product_id(self):
        """Gets the product_id of this RocketMQExtendProductInfoEntity.

        产品ID

        :return: The product_id of this RocketMQExtendProductInfoEntity.
        :rtype: str
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        """Sets the product_id of this RocketMQExtendProductInfoEntity.

        产品ID

        :param product_id: The product_id of this RocketMQExtendProductInfoEntity.
        :type product_id: str
        """
        self._product_id = product_id

    @property
    def ecs_flavor_id(self):
        """Gets the ecs_flavor_id of this RocketMQExtendProductInfoEntity.

        该产品使用的ECS规格

        :return: The ecs_flavor_id of this RocketMQExtendProductInfoEntity.
        :rtype: str
        """
        return self._ecs_flavor_id

    @ecs_flavor_id.setter
    def ecs_flavor_id(self, ecs_flavor_id):
        """Sets the ecs_flavor_id of this RocketMQExtendProductInfoEntity.

        该产品使用的ECS规格

        :param ecs_flavor_id: The ecs_flavor_id of this RocketMQExtendProductInfoEntity.
        :type ecs_flavor_id: str
        """
        self._ecs_flavor_id = ecs_flavor_id

    @property
    def billing_code(self):
        """Gets the billing_code of this RocketMQExtendProductInfoEntity.

        账单计费类型。

        :return: The billing_code of this RocketMQExtendProductInfoEntity.
        :rtype: str
        """
        return self._billing_code

    @billing_code.setter
    def billing_code(self, billing_code):
        """Sets the billing_code of this RocketMQExtendProductInfoEntity.

        账单计费类型。

        :param billing_code: The billing_code of this RocketMQExtendProductInfoEntity.
        :type billing_code: str
        """
        self._billing_code = billing_code

    @property
    def arch_types(self):
        """Gets the arch_types of this RocketMQExtendProductInfoEntity.

        支持的CPU架构类型

        :return: The arch_types of this RocketMQExtendProductInfoEntity.
        :rtype: list[str]
        """
        return self._arch_types

    @arch_types.setter
    def arch_types(self, arch_types):
        """Sets the arch_types of this RocketMQExtendProductInfoEntity.

        支持的CPU架构类型

        :param arch_types: The arch_types of this RocketMQExtendProductInfoEntity.
        :type arch_types: list[str]
        """
        self._arch_types = arch_types

    @property
    def charging_mode(self):
        """Gets the charging_mode of this RocketMQExtendProductInfoEntity.

        支持的计费模式类型

        :return: The charging_mode of this RocketMQExtendProductInfoEntity.
        :rtype: list[str]
        """
        return self._charging_mode

    @charging_mode.setter
    def charging_mode(self, charging_mode):
        """Sets the charging_mode of this RocketMQExtendProductInfoEntity.

        支持的计费模式类型

        :param charging_mode: The charging_mode of this RocketMQExtendProductInfoEntity.
        :type charging_mode: list[str]
        """
        self._charging_mode = charging_mode

    @property
    def ios(self):
        """Gets the ios of this RocketMQExtendProductInfoEntity.

        磁盘IO信息

        :return: The ios of this RocketMQExtendProductInfoEntity.
        :rtype: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductIosEntity`]
        """
        return self._ios

    @ios.setter
    def ios(self, ios):
        """Sets the ios of this RocketMQExtendProductInfoEntity.

        磁盘IO信息

        :param ios: The ios of this RocketMQExtendProductInfoEntity.
        :type ios: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductIosEntity`]
        """
        self._ios = ios

    @property
    def properties(self):
        """Gets the properties of this RocketMQExtendProductInfoEntity.

        :return: The properties of this RocketMQExtendProductInfoEntity.
        :rtype: :class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductPropertiesEntity`
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this RocketMQExtendProductInfoEntity.

        :param properties: The properties of this RocketMQExtendProductInfoEntity.
        :type properties: :class:`huaweicloudsdkrocketmq.v2.RocketMQExtendProductPropertiesEntity`
        """
        self._properties = properties

    @property
    def available_zones(self):
        """Gets the available_zones of this RocketMQExtendProductInfoEntity.

        有可用资源的可用区列表

        :return: The available_zones of this RocketMQExtendProductInfoEntity.
        :rtype: list[str]
        """
        return self._available_zones

    @available_zones.setter
    def available_zones(self, available_zones):
        """Sets the available_zones of this RocketMQExtendProductInfoEntity.

        有可用资源的可用区列表

        :param available_zones: The available_zones of this RocketMQExtendProductInfoEntity.
        :type available_zones: list[str]
        """
        self._available_zones = available_zones

    @property
    def unavailable_zones(self):
        """Gets the unavailable_zones of this RocketMQExtendProductInfoEntity.

        资源售罄的可用区列表

        :return: The unavailable_zones of this RocketMQExtendProductInfoEntity.
        :rtype: list[str]
        """
        return self._unavailable_zones

    @unavailable_zones.setter
    def unavailable_zones(self, unavailable_zones):
        """Sets the unavailable_zones of this RocketMQExtendProductInfoEntity.

        资源售罄的可用区列表

        :param unavailable_zones: The unavailable_zones of this RocketMQExtendProductInfoEntity.
        :type unavailable_zones: list[str]
        """
        self._unavailable_zones = unavailable_zones

    @property
    def support_features(self):
        """Gets the support_features of this RocketMQExtendProductInfoEntity.

        支持的特性功能

        :return: The support_features of this RocketMQExtendProductInfoEntity.
        :rtype: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQProductSupportFeaturesEntity`]
        """
        return self._support_features

    @support_features.setter
    def support_features(self, support_features):
        """Sets the support_features of this RocketMQExtendProductInfoEntity.

        支持的特性功能

        :param support_features: The support_features of this RocketMQExtendProductInfoEntity.
        :type support_features: list[:class:`huaweicloudsdkrocketmq.v2.RocketMQProductSupportFeaturesEntity`]
        """
        self._support_features = support_features

    @property
    def qingtian_incompatible(self):
        """Gets the qingtian_incompatible of this RocketMQExtendProductInfoEntity.

        是否为擎天实例。

        :return: The qingtian_incompatible of this RocketMQExtendProductInfoEntity.
        :rtype: bool
        """
        return self._qingtian_incompatible

    @qingtian_incompatible.setter
    def qingtian_incompatible(self, qingtian_incompatible):
        """Sets the qingtian_incompatible of this RocketMQExtendProductInfoEntity.

        是否为擎天实例。

        :param qingtian_incompatible: The qingtian_incompatible of this RocketMQExtendProductInfoEntity.
        :type qingtian_incompatible: bool
        """
        self._qingtian_incompatible = qingtian_incompatible

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
        if not isinstance(other, RocketMQExtendProductInfoEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
