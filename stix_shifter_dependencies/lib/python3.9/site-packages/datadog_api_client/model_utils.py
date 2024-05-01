# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.

from contextlib import suppress
from datetime import date, datetime
import enum
import inspect
import io
import os
import pprint
import re
import tempfile
from types import MappingProxyType
from typing import Collection, Mapping, Union
from typing_extensions import Final

from dateutil.parser import parse

from datadog_api_client.exceptions import (
    ApiKeyError,
    ApiAttributeError,
    ApiTypeError,
    ApiValueError,
)

none_type = type(None)
file_type = io.IOBase
empty_dict = MappingProxyType({})  # type: ignore


class UnsetType(enum.Enum):
    unset = 0


unset: Final = UnsetType.unset


class cached_property(object):
    # This caches the result of the function call for fn with no inputs
    # use this as a decorator on function methods that you want converted
    # into cached properties
    result_key = "_results"

    def __init__(self, fn):
        self._fn = fn

    def __get__(self, instance, cls=None):
        if self.result_key in vars(self):
            return vars(self)[self.result_key]
        else:
            result = self._fn(instance)
            setattr(self, self.result_key, result)
            return result


PRIMITIVE_TYPES = (list, float, int, bool, datetime, date, str, file_type)


def allows_single_value_input(cls):
    """
    This function returns True if the input composed schema model or any
    descendant model allows a value only input.
    """
    if issubclass(cls, ModelSimple) or cls in PRIMITIVE_TYPES:
        return True
    elif issubclass(cls, ModelComposed):
        if not cls._composed_schemas["oneOf"]:
            return False
        return any(allows_single_value_input(c) for c in cls._composed_schemas["oneOf"])
    return False


def composed_model_input_classes(cls):
    """
    This function returns a list of the possible models that can be accepted as
    inputs.
    """
    if issubclass(cls, ModelSimple) or cls in PRIMITIVE_TYPES:
        return [cls]
    elif issubclass(cls, ModelNormal):
        return [cls]
    elif issubclass(cls, ModelComposed):
        if not cls._composed_schemas["oneOf"]:
            return []
        input_classes = []
        for c in cls._composed_schemas["oneOf"]:
            input_classes.extend(composed_model_input_classes(c))
        return input_classes
    return []


class OpenApiModel(object):
    """The base class for all OpenAPIModels.

    :var attribute_map: The key is attribute name and the value is json
        key in definition.
    :type attribute_map: dict
    :var validations: The key is the name of the attribute. The value is a dict
        that stores validations for max_length, min_length, max_items,
        min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
        inclusive_minimum, and regex.
    :type validations: dict
    :var additional_properties_type: A tuple of classes accepted
        as additional properties values.
    :type additional_properties_type: tuple
    """

    _composed_schemas = empty_dict

    additional_properties_type = None

    attribute_map: Mapping[str, str] = empty_dict

    _nullable = False

    validations: Mapping[str, Mapping[str, int]] = empty_dict

    openapi_types = empty_dict

    read_only_vars: Collection[str] = frozenset()

    def set_attribute(self, name, value):
        # this is only used to set properties on self

        path_to_item = []
        if self._path_to_item:
            path_to_item.extend(self._path_to_item)
        path_to_item.append(name)

        if name in self.openapi_types:
            required_types_mixed = self.openapi_types[name]
        elif self.additional_properties_type is None:
            raise ApiAttributeError("{0} has no attribute '{1}'".format(type(self).__name__, name), path_to_item)
        elif self.additional_properties_type is not None:
            required_types_mixed = self.additional_properties_type

        if get_simple_class(name) != str:
            error_msg = type_error_message(var_name=name, var_value=name, valid_classes=(str,), key_type=True)
            raise ApiTypeError(error_msg, path_to_item=path_to_item, valid_classes=(str,), key_type=True)

        if self._check_type and value is not None:
            value = validate_and_convert_types(
                value,
                required_types_mixed,
                path_to_item,
                self._spec_property_naming,
                self._check_type,
                configuration=self._configuration,
            )
        if name in self.validations:
            check_validations(self.validations[name], name, value, self._configuration)
        self.__dict__["_data_store"][name] = value
        if isinstance(value, OpenApiModel) and value._unparsed:
            self._unparsed = True

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def __setattr__(self, attr, value):
        """Set the value of an attribute using dot notation: `instance.attr = val`."""
        self[attr] = value

    def __getattr__(self, attr):
        """Get the value of an attribute using dot notation: `instance.attr`."""
        return self.__getitem__(attr)

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            arg = args[0]
            if arg is None and is_type_nullable(cls):
                # The input data is the 'null' value and the type is nullable.
                return None

            if issubclass(cls, ModelComposed) and allows_single_value_input(cls):
                model_kwargs = {}
                oneof_instance = get_oneof_instance(cls, model_kwargs, kwargs, model_arg=arg)
                return oneof_instance

        return super(OpenApiModel, cls).__new__(cls)

    def __init__(self, kwargs):
        """
        :param _check_type: If True, values for parameters in openapi_types
            will be type checked and a TypeError will be raised if the wrong type is input.
            Defaults to True.
        :type _check_type: bool
        :param _path_to_item: This is a list of keys or values to drill down to
            the model in received_data when deserializing a response.
        :type _path_to_item: tuple/list
        :param _spec_property_naming: True if the variable names in the input
            data are serialized names, as specified in the OpenAPI document.  False if the
            variable names in the input data are pythonic names, e.g. snake case (default).
        :type _spec_property_naming: bool
        :param _configuration: The instance to use when deserializing a
            file_type parameter.  If passed, type conversion is attempted If omitted no
            type conversion is done.
        :type _configuration: Configuration
        """
        _check_type = kwargs.pop("_check_type", True)
        _spec_property_naming = kwargs.pop("_spec_property_naming", False)
        _path_to_item = kwargs.pop("_path_to_item", ())
        _configuration = kwargs.pop("_configuration", None)

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._unparsed = False

    def _check_pos_args(self, args):
        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments."
                % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=self._path_to_item,
                valid_classes=(self.__class__,),
            )

    def _check_kw_args(self, kwargs):
        if kwargs:
            raise ApiTypeError(
                "Invalid named arguments=%s passed to %s. Remove those invalid named arguments."
                % (
                    kwargs,
                    self.__class__.__name__,
                ),
                path_to_item=self._path_to_item,
                valid_classes=(self.__class__,),
            )


class ModelSimple(OpenApiModel):
    """
    The parent class of models whose type != object in their
    swagger/openapi.

    :var allowed_values: Set of allowed values.
    :type allowed_values: set
    """

    allowed_values: Collection[Union[str, int]] = frozenset()

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_spec_property_naming",
            "_path_to_item",
            "_configuration",
            "_unparsed",
        ]
    )

    def __init__(self, value, **kwargs):
        super().__init__(kwargs)
        self.value = value
        self._check_kw_args(kwargs)

    def __setitem__(self, name, value):
        """Set the value of an attribute using square-bracket notation: `instance[attr] = val`."""
        if name in self.required_properties:
            self.__dict__[name] = value
            return

        if self.allowed_values and name == "value":
            try:
                check_allowed_values(self.allowed_values, name, value)
            except ApiValueError:
                self.__dict__["_data_store"][name] = value
                self._unparsed = True
                return

        self.set_attribute(name, value)

    def get(self, name, default=None):
        """Returns the value of an attribute or some default value if the attribute was not set."""
        if name in self.required_properties:
            return self.__dict__[name]

        return self.__dict__["_data_store"].get(name, default)

    def __getitem__(self, name):
        """Get the value of an attribute using square-bracket notation: `instance[attr]`."""
        if name in self:
            return self.get(name)

        raise ApiAttributeError(
            "{0} has no attribute '{1}'".format(type(self).__name__, name), [e for e in (self._path_to_item, name) if e]
        )

    def __contains__(self, name):
        """Used by `in` operator to check if an attribute value was set in an instance: `'attr' in instance`."""
        if name in self.required_properties:
            return name in self.__dict__

        return name in self.__dict__["_data_store"]

    def to_str(self):
        """Returns the string representation of the model"""
        return str(self.value)

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, self.__class__):
            return False

        this_val = self._data_store["value"]
        that_val = other._data_store["value"]
        return this_val == that_val


class ModelNormal(OpenApiModel):
    """
    The parent class of models whose type == object in their swagger/openapi.
    """

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_spec_property_naming",
            "_path_to_item",
            "_configuration",
            "_unparsed",
        ]
    )

    def __setitem__(self, name, value):
        """Set the value of an attribute using square-bracket notation: `instance[attr] = val`."""
        if name in self.required_properties:
            self.__dict__[name] = value
            return

        self.set_attribute(name, value)

    def get(self, name, default=None):
        """Returns the value of an attribute or some default value if the attribute was not set."""
        if name in self.required_properties:
            return self.__dict__[name]

        return self.__dict__["_data_store"].get(name, default)

    def __getitem__(self, name):
        """Get the value of an attribute using square-bracket notation: `instance[attr]`."""
        if name in self:
            return self.get(name)

        raise ApiAttributeError(
            "{0} has no attribute '{1}'".format(type(self).__name__, name), [e for e in (self._path_to_item, name) if e]
        )

    def __contains__(self, name):
        """Used by `in` operator to check if an attribute value was set in an instance: `'attr' in instance`."""
        if name in self.required_properties:
            return name in self.__dict__

        return name in self.__dict__["_data_store"]

    def to_dict(self):
        """Returns the model properties as a dict"""
        return model_to_dict(self, serialize=False)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, self.__class__):
            return False

        if not set(self._data_store.keys()) == set(other._data_store.keys()):
            return False
        for _var_name, this_val in self._data_store.items():
            that_val = other._data_store[_var_name]
            if this_val != that_val:
                return False
        return True

    def __init__(self, kwargs):
        super().__init__(kwargs)
        for var_name, var_value in kwargs.items():
            if (
                var_name not in self.attribute_map
                and self._configuration is not None
                and self._configuration.discard_unknown_keys
                and self.additional_properties_type is None
            ):
                if self._spec_property_naming:
                    # If it's returned from the API, store it if we need to send it back
                    self.__dict__["_data_store"][var_name] = var_value
                continue
            setattr(self, var_name, var_value)
            if not self._spec_property_naming and var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute.")


class ModelComposed(OpenApiModel):
    """
    The parent class of models whose type == object in their swagger/openapi
    and have oneOf.

    When one sets a property we use var_name_to_model_instances to store the value in
    the correct class instances + run any type checking + validation code.
    When one gets a property we use var_name_to_model_instances to get the value
    from the correct class instances.
    This allows multiple composed schemas to contain the same property with additive
    constraints on the value.

    :var _composed_schemas: Stores the oneOf classes.
    :type _composed_schemas: dict
    :var _composed_instances: Stores a list of instances of the composed schemas
        defined in _composed_schemas. When properties are accessed in the self instance,
        they are returned from the self._data_store or the data stores in the instances
        in self._composed_schemas.
    :type _composed_schemas: list
    :var _var_name_to_model_instances: Map between a variable name on self and
        the composed instances (self included) which contain that data.
    :type _var_name_to_model_instances: dict
    """

    required_properties = set(
        [
            "_data_store",
            "_check_type",
            "_spec_property_naming",
            "_path_to_item",
            "_configuration",
            "_composed_instances",
            "_var_name_to_model_instances",
            "_additional_properties_model_instances",
            "_unparsed",
        ]
    )

    def __init__(self, kwargs):
        super().__init__(kwargs)
        constant_args = {
            "_check_type": self._check_type,
            "_path_to_item": self._path_to_item,
            "_spec_property_naming": self._spec_property_naming,
            "_configuration": self._configuration,
        }
        composed_info = validate_get_composed_info(constant_args, kwargs, self)
        self._composed_instances = composed_info[0]
        self._var_name_to_model_instances = composed_info[1]
        self._additional_properties_model_instances = composed_info[2]
        self._unparsed = any(
            isinstance(composed_instance, UnparsedObject) for composed_instance in self._composed_instances
        )

    def __setitem__(self, name, value):
        """Set the value of an attribute using square-bracket notation: `instance[attr] = val`."""
        if name in self.required_properties:
            self.__dict__[name] = value
            return

        # Set attribute on composed instances
        for model_instance in self._composed_instances:
            setattr(model_instance, name, value)
        if name not in self._var_name_to_model_instances:
            # we assigned an additional property
            self.__dict__["_var_name_to_model_instances"][name] = self._composed_instances + [self]
        return None

    __unset_attribute_value__ = object()

    def get(self, name, default=None):
        """Returns the value of an attribute or some default value if the attribute was not set."""
        if name in self.required_properties:
            return self.__dict__[name]

        # get the attribute from the correct instance
        model_instances = self._var_name_to_model_instances.get(name)
        values = []
        # A composed model stores self and child (oneof) models under
        # self._var_name_to_model_instances.
        # Any property must exist in self and all model instances
        # The value stored in all model instances must be the same
        if model_instances:
            for model_instance in model_instances:
                if name in model_instance._data_store:
                    v = model_instance._data_store[name]
                    if v not in values:
                        values.append(v)
        len_values = len(values)
        if len_values == 0:
            return default
        elif len_values == 1:
            return values[0]
        elif len_values > 1:
            raise ApiValueError(
                "Values stored for property {0} in {1} differ when looking "
                "at self and self's composed instances. All values must be "
                "the same".format(name, type(self).__name__),
                [e for e in (self._path_to_item, name) if e],
            )

    def __getitem__(self, name):
        """Get the value of an attribute using square-bracket notation: `instance[attr]`."""
        value = self.get(name, self.__unset_attribute_value__)
        if value is self.__unset_attribute_value__:
            raise ApiAttributeError(
                "{0} has no attribute '{1}'".format(type(self).__name__, name),
                [e for e in (self._path_to_item, name) if e],
            )
        return value

    def __contains__(self, name):
        """Used by `in` operator to check if an attribute value was set in an instance: `'attr' in instance`."""

        if name in self.required_properties:
            return name in self.__dict__

        model_instances = self._var_name_to_model_instances.get(name, self._additional_properties_model_instances)

        if model_instances:
            for model_instance in model_instances:
                if name in model_instance._data_store:
                    return True

        return False

    def to_dict(self):
        """Returns the model properties as a dict"""
        return model_to_dict(self, serialize=False)

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def get_oneof_instance(self):
        """Returns the oneOf instance"""
        return self._composed_instances[0]

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, self.__class__):
            return False

        if not set(self._data_store.keys()) == set(other._data_store.keys()):
            return False
        for _var_name, this_val in self._data_store.items():
            that_val = other._data_store[_var_name]
            if this_val != that_val:
                return False
        return True


COERCION_INDEX_BY_TYPE = {
    ModelComposed: 0,
    ModelNormal: 1,
    ModelSimple: 2,
    none_type: 3,  # The type of 'None'.
    list: 4,
    dict: 5,
    float: 6,
    int: 7,
    bool: 8,
    datetime: 9,
    date: 10,
    str: 11,
    file_type: 12,  # 'file_type' is an alias for the built-in 'file' or 'io.IOBase' type.
}

# these are used to limit what type conversions we try to do
# when we have a valid type already and we want to try converting
# to another type
UPCONVERSION_TYPE_PAIRS = (
    (str, datetime),
    (str, date),
    (int, float),  # A float may be serialized as an integer, e.g. '3' is a valid serialized float.
    (list, ModelComposed),
    (dict, ModelComposed),
    (bool, ModelComposed),
    (str, ModelComposed),
    (int, ModelComposed),
    (float, ModelComposed),
    (list, ModelComposed),
    (list, ModelNormal),
    (dict, ModelNormal),
    (bool, ModelSimple),
    (str, ModelSimple),
    (int, ModelSimple),
    (float, ModelSimple),
    (list, ModelSimple),
)

COERCIBLE_TYPE_PAIRS = {
    False: (  # client instantiation of a model with client data
        # (dict, ModelComposed),
        # (list, ModelComposed),
        # (dict, ModelNormal),
        # (list, ModelNormal),
        # (str, ModelSimple),
        # (int, ModelSimple),
        # (float, ModelSimple),
        # (list, ModelSimple),
        # (str, int),
        # (str, float),
        # (str, datetime),
        # (str, date),
        # (int, str),
        # (float, str),
    ),
    True: (  # server -> client data
        (dict, ModelComposed),
        (list, ModelComposed),
        (dict, ModelNormal),
        (list, ModelNormal),
        (bool, ModelSimple),
        (str, ModelSimple),
        (int, ModelSimple),
        (float, ModelSimple),
        (list, ModelSimple),
        # (str, int),
        # (str, float),
        (str, datetime),
        (str, date),
        # (int, str),
        # (float, str),
        (str, file_type),
    ),
}


def get_simple_class(input_value):
    """Returns an input_value's simple class that we will use for type checking.

    :param input_value: The item for which we will return the simple class.
    :type input_value: class/class_instance
    """
    if isinstance(input_value, type):
        # input_value is a class
        return input_value
    elif isinstance(input_value, tuple):
        return tuple
    elif isinstance(input_value, list):
        return list
    elif isinstance(input_value, dict):
        return dict
    elif input_value is None:
        return none_type
    elif isinstance(input_value, file_type):
        return file_type
    elif isinstance(input_value, bool):
        # this must be higher than the int check because
        # isinstance(True, int) == True
        return bool
    elif isinstance(input_value, int):
        return int
    elif isinstance(input_value, datetime):
        # this must be higher than the date check because
        # isinstance(datetime_instance, date) == True
        return datetime
    elif isinstance(input_value, date):
        return date
    elif isinstance(input_value, str):
        return str
    return type(input_value)


def check_allowed_values(allowed_values, input_variable, input_values):
    """Raises an exception if the input_values are not allowed.

    :type allowed_values: set
    :param input_variable: The name of the input variable.
    :type input_variable: str
    :param input_values: The values that we are checking to see if they are in
        allowed_values.
    :type input_values: list/str/int/float/date/datetime
    """
    if isinstance(input_values, list) and not set(input_values).issubset(allowed_values):
        invalid_values = (", ".join(map(str, set(input_values) - allowed_values)),)
        raise ApiValueError(
            "Invalid values for `%s` [%s], must be a subset of [%s]"
            % (input_variable, invalid_values, ", ".join(str(v) for v in allowed_values))
        )
    elif isinstance(input_values, dict) and not set(input_values.keys()).issubset(allowed_values):
        invalid_values = ", ".join(map(str, set(input_values.keys()) - allowed_values))
        raise ApiValueError(
            "Invalid keys in `%s` [%s], must be a subset of [%s]"
            % (input_variable, invalid_values, ", ".join(str(v) for v in allowed_values))
        )
    elif not isinstance(input_values, (list, dict)) and input_values not in allowed_values:
        raise ApiValueError(
            "Invalid value for `%s` (%s), must be one of %s" % (input_variable, input_values, allowed_values)
        )


def is_json_validation_enabled(schema_keyword, configuration=None):
    """
    Returns True if JSON schema validation is enabled for the specified
    validation keyword. This can be used to skip JSON schema structural validation
    as requested in the configuration.

    :param schema_keyword: The name of a JSON schema validation keyword.
    :type schema_keyword: string
    :param configuration: The configuration instance.
    :type configuration: Configuration
    """
    return (
        configuration is None
        or not hasattr(configuration, "_disabled_client_side_validations")
        or schema_keyword not in configuration._disabled_client_side_validations
    )


def check_validations(validations, input_variable, input_values, configuration=None):
    """Raises an exception if the input_values are invalid.

    :param validations: The validation dictionary.
    :type validations: dict
    :param input_variable: The name of the input variable.
    :type input_variable: str
    :param input_values: The values that we are checking.
    :type input_values: list/str/int/float/date/datetime
    :param configuration: The configuration instance.
    :type configuration: Configuration
    """
    if input_values is None:
        return

    if (
        is_json_validation_enabled("multipleOf", configuration)
        and "multiple_of" in validations
        and isinstance(input_values, (int, float))
        and not (float(input_values) / validations["multiple_of"]).is_integer()
    ):
        # Note 'multipleOf' will be as good as the floating point arithmetic.
        raise ApiValueError(
            "Invalid value for `%s`, value must be a multiple of " "`%s`" % (input_variable, validations["multiple_of"])
        )

    if (
        is_json_validation_enabled("maxLength", configuration)
        and "max_length" in validations
        and len(input_values) > validations["max_length"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, length must be less than or equal to "
            "`%s`" % (input_variable, validations["max_length"])
        )

    if (
        is_json_validation_enabled("minLength", configuration)
        and "min_length" in validations
        and len(input_values) < validations["min_length"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, length must be greater than or equal to "
            "`%s`" % (input_variable, validations["min_length"])
        )

    if (
        is_json_validation_enabled("maxItems", configuration)
        and "max_items" in validations
        and len(input_values) > validations["max_items"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, number of items must be less than or "
            "equal to `%s`" % (input_variable, validations["max_items"])
        )

    if (
        is_json_validation_enabled("minItems", configuration)
        and "min_items" in validations
        and len(input_values) < validations["min_items"]
    ):
        raise ValueError(
            "Invalid value for `%s`, number of items must be greater than or "
            "equal to `%s`" % (input_variable, validations["min_items"])
        )

    items = ("exclusive_maximum", "inclusive_maximum", "exclusive_minimum", "inclusive_minimum")
    if any(item in validations for item in items):
        if isinstance(input_values, list):
            max_val = max(input_values)
            min_val = min(input_values)
        elif isinstance(input_values, dict):
            max_val = max(input_values.values())
            min_val = min(input_values.values())
        else:
            max_val = input_values
            min_val = input_values

    if (
        is_json_validation_enabled("exclusiveMaximum", configuration)
        and "exclusive_maximum" in validations
        and max_val >= validations["exclusive_maximum"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, must be a value less than `%s`"
            % (input_variable, validations["exclusive_maximum"])
        )

    if (
        is_json_validation_enabled("maximum", configuration)
        and "inclusive_maximum" in validations
        and max_val > validations["inclusive_maximum"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, must be a value less than or equal to "
            "`%s`" % (input_variable, validations["inclusive_maximum"])
        )

    if (
        is_json_validation_enabled("exclusiveMinimum", configuration)
        and "exclusive_minimum" in validations
        and min_val <= validations["exclusive_minimum"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, must be a value greater than `%s`"
            % (input_variable, validations["exclusive_maximum"])
        )

    if (
        is_json_validation_enabled("minimum", configuration)
        and "inclusive_minimum" in validations
        and min_val < validations["inclusive_minimum"]
    ):
        raise ApiValueError(
            "Invalid value for `%s`, must be a value greater than or equal "
            "to `%s`" % (input_variable, validations["inclusive_minimum"])
        )
    flags = validations.get("regex", {}).get("flags", 0)
    if (
        is_json_validation_enabled("pattern", configuration)
        and "regex" in validations
        and not re.search(validations["regex"]["pattern"], input_values, flags=flags)
    ):
        err_msg = r"Invalid value for `%s`, must match regular expression `%s`" % (
            input_variable,
            validations["regex"]["pattern"],
        )
        if flags != 0:
            # Don't print the regex flags if the flags are not
            # specified in the OAS document.
            err_msg = r"%s with flags=`%s`" % (err_msg, flags)
        raise ApiValueError(err_msg)


def order_response_types(required_types):
    """Returns the required types sorted in coercion order.

    :param required_types: Collection of classes or instance of
        list or dict with class information inside it.
    :type required_types: list/tuple

    :return: Coercion order sorted collection of classes or instance
        of list or dict with class information inside it.
    :rtype: list
    """

    def index_getter(class_or_instance):
        if isinstance(class_or_instance, list):
            return COERCION_INDEX_BY_TYPE[list]
        elif isinstance(class_or_instance, dict):
            return COERCION_INDEX_BY_TYPE[dict]
        elif inspect.isclass(class_or_instance) and issubclass(class_or_instance, ModelComposed):
            return COERCION_INDEX_BY_TYPE[ModelComposed]
        elif inspect.isclass(class_or_instance) and issubclass(class_or_instance, ModelNormal):
            return COERCION_INDEX_BY_TYPE[ModelNormal]
        elif inspect.isclass(class_or_instance) and issubclass(class_or_instance, ModelSimple):
            return COERCION_INDEX_BY_TYPE[ModelSimple]
        elif class_or_instance in COERCION_INDEX_BY_TYPE:
            return COERCION_INDEX_BY_TYPE[class_or_instance]
        raise ApiValueError("Unsupported type: %s" % class_or_instance)

    sorted_types = sorted(required_types, key=index_getter)
    return sorted_types


def remove_uncoercible(required_types_classes, current_item, spec_property_naming, must_convert=True):
    """Only keeps the type conversions that are possible.

    :param required_types_classes: Classes that are required, these should be
        ordered by COERCION_INDEX_BY_TYPE.
    :type required_types_classes: tuple
    :param spec_property_naming: True if the variable names in the input data
        are serialized names as specified in the OpenAPI document.  False if the
        variables names in the input data are python variable names in PEP-8 snake
        case.
    :type spec_property_naming: bool
    :param current_item: The current item (input data) to be converted.

    :param must_convert: If True the item to convert is of the wrong type and
        we want a big list of coercibles if False, we want a limited list of coercibles.
    :type must_convert: bool

    :return: The remaining coercible required types, classes only.
    :rtype: list
    """
    current_type_simple = get_simple_class(current_item)

    results_classes = []
    for required_type_class in required_types_classes:
        # convert our models to OpenApiModel
        required_type_class_simplified = required_type_class
        if isinstance(required_type_class_simplified, type):
            if issubclass(required_type_class_simplified, ModelComposed):
                required_type_class_simplified = ModelComposed
            elif issubclass(required_type_class_simplified, ModelNormal):
                required_type_class_simplified = ModelNormal
            elif issubclass(required_type_class_simplified, ModelSimple):
                required_type_class_simplified = ModelSimple

        if required_type_class_simplified == current_type_simple:
            # don't consider converting to one's own class
            continue

        class_pair = (current_type_simple, required_type_class_simplified)
        if must_convert and class_pair in COERCIBLE_TYPE_PAIRS[spec_property_naming]:
            results_classes.append(required_type_class)
        elif class_pair in UPCONVERSION_TYPE_PAIRS:
            results_classes.append(required_type_class)
    return results_classes


def get_possible_classes(cls, from_server_context):
    possible_classes = [cls]
    if from_server_context:
        return possible_classes
    if issubclass(cls, ModelComposed):
        possible_classes.extend(composed_model_input_classes(cls))
    return possible_classes


def get_required_type_classes(required_types_mixed, spec_property_naming):
    """Converts the tuple required_types into a tuple and a dict described below.

    :param required_types_mixed: Will contain either classes or instance of
        list or dict.
    :type required_types_mixed: tuple/list
    :param spec_property_naming: if True these values came from the server, and
        we use the data types in our endpoints.  If False, we are client side and we
        need to include oneOf classes inside the data types in our endpoints.
    :type spec_property_naming: bool

    :return (valid_classes, dict_valid_class_to_child_types_mixed):
        valid_classes (tuple): The valid classes that the current item should be.
        dict_valid_class_to_child_types_mixed (dict):

            valid_class (class): This is the key.
            child_types_mixed (list/dict/tuple): Describes the valid child types.

    :rtype: tuple
    """
    valid_classes = []
    child_req_types_by_current_type = {}
    for required_type in required_types_mixed:
        if isinstance(required_type, list):
            valid_classes.append(list)
            child_req_types_by_current_type[list] = required_type
        elif isinstance(required_type, tuple):
            valid_classes.append(tuple)
            child_req_types_by_current_type[tuple] = required_type
        elif isinstance(required_type, dict):
            valid_classes.append(dict)
            child_req_types_by_current_type[dict] = required_type[str]
        else:
            valid_classes.extend(get_possible_classes(required_type, spec_property_naming))
    return tuple(valid_classes), child_req_types_by_current_type


def change_keys_js_to_python(input_dict, model_class):
    """
    Converts from javascript_key keys in the input_dict to python_keys in
    the output dict using the mapping in model_class.
    If the input_dict contains a key which does not declared in the model_class,
    the key is added to the output dict as is. The assumption is the model_class
    may have undeclared properties (additionalProperties attribute in the OAS
    document).
    """
    if issubclass(model_class, ModelComposed):
        attribute_map = {}
        for t in model_class._composed_schemas.get("oneOf", ()):
            if issubclass(t, OpenApiModel):
                attribute_map.update(t.attribute_map)
    elif not getattr(model_class, "attribute_map", None):
        return input_dict
    else:
        attribute_map = model_class.attribute_map
    output_dict = {}
    reversed_attr_map = {value: key for key, value in attribute_map.items()}
    for javascript_key, value in input_dict.items():
        python_key = reversed_attr_map.get(javascript_key)
        if python_key is None:
            # if the key is unknown, it is in error or it is an
            # additionalProperties variable
            python_key = javascript_key
        output_dict[python_key] = value
    return output_dict


def get_type_error(var_value, path_to_item, valid_classes, key_type=False):
    error_msg = type_error_message(
        var_name=path_to_item[-1], var_value=var_value, valid_classes=valid_classes, key_type=key_type
    )
    return ApiTypeError(error_msg, path_to_item=path_to_item, valid_classes=valid_classes, key_type=key_type)


def deserialize_primitive(data, klass, path_to_item):
    """Deserializes string to primitive type.

    :type data: str/int/float
    :param klass: The class to convert to.
    :type klass: str/class

    :rtype: int, float, str, bool, date, datetime
    """
    additional_message = ""
    try:
        if klass in {datetime, date}:
            additional_message = (
                "If you need your parameter to have a fallback "
                "string value, please set its type as `type: {}` in your "
                "spec. That allows the value to be any type. "
            )
            if klass == datetime:
                if len(data) < 8:
                    raise ValueError("This is not a datetime")
                # The string should be in iso8601 datetime format.
                parsed_datetime = parse(data)
                date_only = (
                    parsed_datetime.hour == parsed_datetime.minute == parsed_datetime.second == 0
                    and parsed_datetime.tzinfo is None
                    and 8 <= len(data) <= 10
                )
                if date_only:
                    raise ValueError("This is a date, not a datetime")
                return parsed_datetime
            elif klass == date:
                if len(data) < 8:
                    raise ValueError("This is not a date")
                return parse(data).date()
        else:
            converted_value = klass(data)
            if isinstance(data, str) and klass == float:
                if str(converted_value) != data:
                    # '7' -> 7.0 -> '7.0' != '7'
                    raise ValueError("This is not a float")
            return converted_value
    except (OverflowError, ValueError) as ex:
        # parse can raise OverflowError
        raise ApiValueError(
            "{0}Failed to parse {1} as {2}".format(additional_message, repr(data), klass.__name__),
            path_to_item=path_to_item,
        ) from ex


def deserialize_model(model_data, model_class, path_to_item, check_type, configuration, spec_property_naming):
    """Deserializes model_data to model instance.

    :param model_data: Data to instantiate the model.
    :type model_data: int/str/float/bool/none_type/list/dict
    :param model_class: The model class.
    :type model_class: OpenApiModel
    :param path_to_item: Path to the model in the received data.
    :type path_to_item: list
    :param check_type: Whether to check the data tupe for the values in
        the model.
    :type check_type: bool
    :param configuration: The instance to use to convert files.
    :type configuration: Configuration
    :param spec_property_naming: True if the variable names in the input
        data are serialized names as specified in the OpenAPI document.
        False if the variables names in the input data are python
        variable names in PEP-8 snake case.
    :type spec_property_naming: bool

    :return: The model instance.
    """

    kw_args = dict(
        _check_type=check_type,
        _path_to_item=path_to_item,
        _configuration=configuration,
        _spec_property_naming=spec_property_naming,
    )

    if issubclass(model_class, ModelSimple):
        return model_class(model_data, **kw_args)
    elif isinstance(model_data, list):
        if issubclass(model_class, ModelComposed) and allows_single_value_input(model_class):
            return model_class(model_data, **kw_args)
        else:
            return model_class(*model_data, **kw_args)
    if isinstance(model_data, dict):
        kw_args.update(change_keys_js_to_python(model_data, model_class))
        return model_class(**kw_args)
    elif isinstance(model_data, PRIMITIVE_TYPES):
        return model_class(model_data, **kw_args)


def deserialize_file(response_data, temp_folder_path, content_disposition=None):
    """Deserializes body to file.

    Saves response body into a file in a temporary folder, using the filename
    from the `Content-Disposition` header if provided.

    :param response_data: The file data to write.
    :type response_data: str
    :param temp_folder_path: The directory in which the client creates temporary files.
    :type temp_folder_path: str
    :param content_disposition: The value of the Content-Disposition
        header.
    :type content_disposition: str

    :return: The deserialized file which is open. The user is responsible for
        closing and reading the file.
    :rtype: file_type
    """
    fd, path = tempfile.mkstemp(dir=temp_folder_path)
    os.close(fd)
    os.remove(path)

    if content_disposition:
        filename = re.search(r'filename=[\'"]?([^\'"\s]+)[\'"]?', content_disposition).group(1)
        path = os.path.join(os.path.dirname(path), filename)

    with open(path, "wb") as f:
        if isinstance(response_data, str):
            # change str to bytes so we can write it
            response_data = response_data.encode("utf-8")
        f.write(response_data)

    f = open(path, "rb")
    return f


def attempt_convert_item(
    input_value,
    valid_classes,
    path_to_item,
    configuration,
    spec_property_naming,
    key_type=False,
    must_convert=False,
    check_type=True,
):
    """
    :param input_value: The data to convert.
    :param valid_classes: The classes that are valid.
    :param path_to_item: The path to the item to convert.
    :type path_to_item: list
    :param configuration: The instance to use to convert files.
    :type configuration: Configuration
    :param spec_property_naming: True if the variable names in the input data
        are serialized names as specified in the OpenAPI document.  False if the
        variables names in the input data are python variable names in PEP-8 snake
        case.
    :type spec_property_naming: bool
    :param key_type: If True we need to convert a key type (not supported)
    :type key_type: bool
    :param must_convert: If True we must convert.
    :type must_convert: bool
    :param check_type: If True we check the type or the returned data in
        ModelComposed/ModelNormal/ModelSimple instances.
    :type check_type: bool
    """
    valid_classes_ordered = order_response_types(valid_classes)
    valid_classes_coercible = remove_uncoercible(valid_classes_ordered, input_value, spec_property_naming)
    if not valid_classes_coercible or key_type:
        # we do not handle keytype errors, json will take care
        # of this for us
        if configuration is None or not configuration.discard_unknown_keys:
            raise get_type_error(input_value, path_to_item, valid_classes, key_type=key_type)
    for valid_class in valid_classes_coercible:
        try:
            if issubclass(valid_class, OpenApiModel):
                return deserialize_model(
                    input_value, valid_class, path_to_item, check_type, configuration, spec_property_naming
                )
            elif valid_class == file_type:
                return deserialize_file(input_value, configuration.temp_folder_path)
            return deserialize_primitive(input_value, valid_class, path_to_item)
        except (ApiTypeError, ApiValueError, ApiKeyError) as conversion_exc:
            if must_convert:
                raise conversion_exc
            # if we have conversion errors when must_convert == False
            # we ignore the exception and move on to the next class
            continue
    if must_convert:
        raise get_type_error(input_value, path_to_item, valid_classes, key_type=key_type)
    # we were unable to convert, must_convert == False
    return input_value


def is_type_nullable(input_type):
    """
    Returns True if None is an allowed value for the specified input_type.

    A type is nullable if at least one of the following conditions is True:

        1. The OAS 'nullable' attribute has been specified,
        2. The type is the 'null' type,
        3. The type is a oneOf composed schema, and a child schema is
           the 'null' type.

    :param input_type: The class of the input_value that we are checking.
    :type input_type: type

    :rtype: bool
    """
    if input_type is none_type:
        return True
    if issubclass(input_type, OpenApiModel) and input_type._nullable:
        return True
    if issubclass(input_type, ModelComposed):
        # If oneOf, check if the 'null' type is one of the allowed types.
        for t in input_type._composed_schemas.get("oneOf", ()):
            if is_type_nullable(t):
                return True
    return False


def is_valid_type(input_class_simple, valid_classes):
    """
    :param input_class_simple: The class of the input_value that we are checking.
    :type input_class_simple: class:
    :param valid_classes: The valid classes that the current item should be.
    :type valid_classes: tuple

    :rtype: bool
    """
    valid_type = input_class_simple in valid_classes
    if not valid_type and (issubclass(input_class_simple, OpenApiModel) or input_class_simple is none_type):
        for valid_class in valid_classes:
            if input_class_simple is none_type and is_type_nullable(valid_class):
                # Schema is oneOf and the 'null' type is one of the allowed types.
                return True
            if issubclass(valid_class, OpenApiModel):
                continue
    return valid_type


def validate_and_convert_types(
    input_value, required_types_mixed, path_to_item, spec_property_naming, check_type, configuration=None
):
    """Raises a TypeError is there is a problem, otherwise returns value.

    :param input_value: The data to validate/convert.
    :param required_types_mixed: A list of valid classes, or a list tuples of
        valid classes, or a dict where the value is a tuple of value classes.
    :type required_types_mixed: list/dict/tuple
    :param path_to_item: The path to the data being validated this stores a
        list of keys or indices to get to the data being validated.
    :type path_to_item: list
    :param spec_property_naming: True if the variable names in the input
        data are serialized names as specified in the OpenAPI document.  False
        if the variables names in the input data are python variable names in PEP-8
        snake case.
    :type spec_property_naming: bool
    :param check_type: If True, type will be checked and conversion
        will be attempted.
    :type check_type: bool
    :param configuration:: The configuration class to use when converting
        file_type items.
    :type configuration: Configuration

    :return: The correctly typed value.

    :raise: ApiTypeError
    """
    results = get_required_type_classes(required_types_mixed, spec_property_naming)
    valid_classes, child_req_types_by_current_type = results

    input_class_simple = get_simple_class(input_value)
    valid_type = is_valid_type(input_class_simple, valid_classes)
    if not valid_type:
        # if input_value is not valid_type try to convert it
        return attempt_convert_item(
            input_value,
            valid_classes,
            path_to_item,
            configuration,
            spec_property_naming,
            must_convert=True,
            check_type=check_type,
        )

    # input_value's type is in valid_classes
    if len(valid_classes) > 1 and configuration:
        # there are valid classes which are not the current class
        valid_classes_coercible = remove_uncoercible(
            valid_classes, input_value, spec_property_naming, must_convert=False
        )
        if valid_classes_coercible:
            return attempt_convert_item(
                input_value,
                valid_classes_coercible,
                path_to_item,
                configuration,
                spec_property_naming,
                check_type=check_type,
            )

    if child_req_types_by_current_type == {}:
        # all types are of the required types and there are no more inner
        # variables left to look at
        return input_value
    inner_required_types = child_req_types_by_current_type.get(type(input_value))
    if inner_required_types is None:
        # for this type, there are not more inner variables left to look at
        return input_value
    if isinstance(input_value, list):
        if input_value == []:
            # allow an empty list
            return input_value
        result = []
        for index, inner_value in enumerate(input_value):
            inner_path = list(path_to_item)
            inner_path.append(index)
            result.append(
                validate_and_convert_types(
                    inner_value,
                    inner_required_types,
                    inner_path,
                    spec_property_naming,
                    check_type,
                    configuration=configuration,
                )
            )
        return result
    elif isinstance(input_value, dict):
        if input_value == {}:
            # allow an empty dict
            return input_value
        result = {}
        for inner_key, inner_val in input_value.items():
            inner_path = list(path_to_item)
            inner_path.append(inner_key)
            if get_simple_class(inner_key) != str:
                raise get_type_error(inner_key, inner_path, valid_classes, key_type=True)
            result[inner_key] = validate_and_convert_types(
                inner_val,
                inner_required_types,
                inner_path,
                spec_property_naming,
                check_type,
                configuration=configuration,
            )
        return result
    return input_value


def model_to_dict(model_instance, serialize=True):
    """Returns the model properties as a dict.

    :param model_instance: The model instance that will be converted to a dict.
    :param serialize: If True, the keys in the dict will be values from
        attribute_map.
    :type serialize: bool
    """
    result = {}

    model_instances = [model_instance]
    if model_instance._composed_schemas:
        model_instances.extend(model_instance._composed_instances)
    seen_json_attribute_names = set()
    used_fallback_python_attribute_names = set()
    py_to_json_map = {}
    for model_instance in model_instances:
        for attr, value in model_instance._data_store.items():
            if serialize:
                # we use get here because additional property key names do not
                # exist in attribute_map
                try:
                    attr = model_instance.attribute_map[attr]
                    py_to_json_map.update(model_instance.attribute_map)
                    seen_json_attribute_names.add(attr)
                except KeyError:
                    used_fallback_python_attribute_names.add(attr)
            if isinstance(value, list):
                if not value:
                    # empty list or None
                    result[attr] = value
                else:
                    res = []
                    for v in value:
                        if isinstance(v, PRIMITIVE_TYPES) or v is None:
                            res.append(v)
                        elif isinstance(v, ModelSimple):
                            res.append(v.value)
                        elif isinstance(v, OpenApiModel):
                            res.append(model_to_dict(v, serialize=serialize))
                        else:
                            res.append(v)
                    result[attr] = res
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], model_to_dict(item[1], serialize=serialize))
                        if hasattr(item[1], "_data_store")
                        else item,
                        value.items(),
                    )
                )
            elif isinstance(value, ModelSimple):
                result[attr] = value.value
            elif hasattr(value, "_data_store"):
                result[attr] = model_to_dict(value, serialize=serialize)
            else:
                result[attr] = value
    if serialize:
        for python_key in used_fallback_python_attribute_names:
            json_key = py_to_json_map.get(python_key)
            if json_key is None:
                continue
            if python_key == json_key:
                continue
            json_key_assigned_no_need_for_python_key = json_key in seen_json_attribute_names
            if json_key_assigned_no_need_for_python_key:
                del result[python_key]

    return result


def type_error_message(var_value=None, var_name=None, valid_classes=None, key_type=None):
    """
    :param var_value: The variable which has the type error.
    :param var_name: The name of the variable which has the type error.
    :type var_name: str
    :param valid_classes: The accepted classes for current_item's value.
    :type valid_classes: tuple
    :param key_type: False if our value is a value in a dict True if it is a
        key in a dict False if our item is an item in a list.
    :type key_type: bool
    """
    key_or_value = "value"
    if key_type:
        key_or_value = "key"
    valid_classes_phrase = get_valid_classes_phrase(valid_classes)
    msg = "Invalid type for variable '{0}'. Required {1} type {2} and " "passed type was {3}".format(
        var_name,
        key_or_value,
        valid_classes_phrase,
        type(var_value).__name__,
    )
    return msg


def get_valid_classes_phrase(input_classes):
    """Returns a string phrase describing what types are allowed."""
    all_class_names = [cls.__name__ for cls in input_classes]
    all_class_names.sort()
    if len(all_class_names) == 1:
        return "is {0}".format(all_class_names[0])
    return "is one of [{0}]".format(", ".join(all_class_names))


def get_oneof_instance(cls, model_kwargs, constant_kwargs, model_arg=None):
    """
    Find the oneOf schema that matches the input data (e.g. payload).
    If exactly one schema matches the input data, an instance of that schema
    is returned.
    If zero or more than one schema match the input data, an exception is raised.
    In OAS 3.x, the payload MUST, by validation, match exactly one of the
    schemas described by oneOf.

    :param cls: The class we are handling.
    :param model_kwargs: var_name to var_value.
        The input data, e.g. the payload that must match a oneOf schema
        in the OpenAPI document.
    :type model_kwargs: dict
    :param constant_kwargs: var_name to var_value
        args that every model requires, including configuration, server
        and path to item.
    :type constant_kwargs: dict
    :param model_arg: The value to assign to a primitive class or ModelSimple class.
        Notes:
        - this is only passed in when oneOf includes types which are not object
        - None is used to suppress handling of model_arg, nullable models are handled in __new__
    :type model_arg: int, float, bool, str, date, datetime, ModelSimple, None
    """
    if len(cls._composed_schemas["oneOf"]) == 0:
        return None

    oneof_instances = []
    # Iterate over each oneOf schema and determine if the input data
    # matches the oneOf schemas.
    for oneof_class in cls._composed_schemas["oneOf"]:
        # The composed oneOf schema allows the 'null' type and the input data
        # is the null value. This is a OAS >= 3.1 feature.
        if oneof_class is none_type:
            # skip none_types because we are deserializing dict data.
            # none_type deserialization is handled in the __new__ method
            continue

        single_value_input = allows_single_value_input(oneof_class)

        with suppress(Exception):
            if not single_value_input:
                if constant_kwargs.get("_spec_property_naming"):
                    oneof_instance = oneof_class(
                        **change_keys_js_to_python(model_kwargs, oneof_class), **constant_kwargs
                    )
                else:
                    oneof_instance = oneof_class(**model_kwargs, **constant_kwargs)
                if not oneof_instance._unparsed:
                    oneof_instances.append(oneof_instance)
            else:
                if issubclass(oneof_class, ModelSimple):
                    oneof_instance = oneof_class(model_arg, **constant_kwargs)
                    if not oneof_instance._unparsed:
                        oneof_instances.append(oneof_instance)
                elif oneof_class in PRIMITIVE_TYPES:
                    oneof_instance = validate_and_convert_types(
                        model_arg,
                        (oneof_class,),
                        constant_kwargs.get("_path_to_item", ()),
                        constant_kwargs.get("_spec_property_naming", False),
                        constant_kwargs.get("_check_type", True),
                        configuration=constant_kwargs.get("_configuration"),
                    )
                    oneof_instances.append(oneof_instance)
    if len(oneof_instances) != 1:
        return UnparsedObject(**model_kwargs)
    return oneof_instances[0]


def get_discarded_args(self, composed_instances, model_args):
    """
    Gathers the args that were discarded by configuration.discard_unknown_keys
    """
    model_arg_keys = model_args.keys()
    discarded_args = set()
    # arguments passed to self were already converted to python names
    # before __init__ was called
    for instance in composed_instances:
        all_keys = set(model_to_dict(instance, serialize=False).keys())
        js_keys = model_to_dict(instance).keys()
        all_keys.update(js_keys)
        discarded_keys = model_arg_keys - all_keys
        discarded_args.update(discarded_keys)
    return discarded_args


def validate_get_composed_info(constant_args, model_args, self):
    """
    For composed schemas, generate schema instances for all schemas in the
    oneOf definition. If additional properties are allowed, also assign
    those properties on all matched schemas that contain additionalProperties.
    Openapi schemas are python classes.

    Exceptions are raised if:
    - 0 or > 1 oneOf schema matches the model_args input data

    :param constant_args: These are the args that every model requires.
    :type constant_args: dict
    :param model_args: These are the required and optional spec args that
        were passed in to make this model.
    :type model_args: dict
    :param self: The class that we are instantiating.  This class contains
        self._composed_schemas.
    :type self: class

    :return:
        composed_instances (list): the composed instances which are not
            self
        var_name_to_model_instances (dict): a dict going from var_name
            to the model_instance which holds that var_name
            the model_instance may be self or an instance of one of the
            classes in self.composed_instances()
        additional_properties_model_instances (list): a list of the
            model instances which have the property
            additional_properties_type. This list can include self
    :rtype: list
    """
    # Create composed_instances
    composed_instances = []
    oneof_instance = get_oneof_instance(self.__class__, model_args, constant_args)
    if oneof_instance is not None:
        composed_instances.append(oneof_instance)

    additional_properties_model_instances = []
    if self.additional_properties_type is not None:
        additional_properties_model_instances = [self]

    discarded_args = get_discarded_args(self, composed_instances, model_args)

    # Map variable names to composed_instances
    var_name_to_model_instances = {}
    for prop_name in model_args:
        if prop_name not in discarded_args:
            var_name_to_model_instances[prop_name] = [self] + composed_instances

    return [composed_instances, var_name_to_model_instances, additional_properties_model_instances, discarded_args]


class UnparsedObject(ModelNormal):
    """A model for an oneOf we don't know about."""

    required_properties = set(
        [
            "_data_store",
            "_unparsed",
        ]
    )

    def __init__(self, **kwargs):

        self._data_store = {}
        self._unparsed = True

        for var_name, var_value in kwargs.items():
            self.__dict__[var_name] = var_value
            self.__dict__["_data_store"][var_name] = var_value


def get_attribute_from_path(obj, path, default=None):
    """Return an attribute at `path` from the passed object."""
    for elt in path.split("."):
        try:
            obj = obj[elt]
        except (KeyError, AttributeError):
            if default is None:
                raise
            return default
    return obj


def set_attribute_from_path(obj, path, value, params_map):
    """Set an attribute at `path` with the given value."""
    elts = path.split(".")
    last = elts.pop(-1)
    root = None
    for i, elt in enumerate(elts):
        if i:
            root = root.openapi_types[elt][0]
        else:
            root = params_map[elt]["openapi_types"][0]
        try:
            obj = obj[elt]
        except (KeyError, AttributeError):
            obj = root()
    obj[last] = value
