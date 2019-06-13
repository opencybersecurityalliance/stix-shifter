from abc import ABCMeta, abstractmethod


class BaseDataMapper(object, metaclass=ABCMeta):

    @abstractmethod
    def fetch_mapping(self):
        """
        Fetches STIX-to-datasource mapping JSON from the module's from_stix_map.json file
        """
        pass

    @abstractmethod
    def map_field(self, stix_object_name, stix_property_name):
        """
        Maps the STIX object:property pair to any matching data source fields. 
        Mapping is based on a JSON object defined in the data source DataMapper class
        :param stix_object_name: STIX object (ie. url)
        :type stix_object_name: str
        :param stix_property_name: STIX property associated to the object (ie. value)
        :type stix_property_name: str
        :return: A list of 0 or more data source fields that map to a combination of stix_object_name and stix_property_name
        :rtype: list
        """
        pass
