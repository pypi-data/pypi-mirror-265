from abc import ABC

from DependencyNeedle.lifetime_enums import LifeTimeEnums
from DependencyNeedle.dependency_strategy import (
    IDependencyStrategyInterface,
    ScopedDependencyStrategy,
    TransientDependencyStrategy,
    SingeltonDependencyStrategy
)


class Container:
    """Container used to build a class by automating the dependancy injection
    to obtain inversion of control"""

    def __init__(self):
        self.__interface_registery_lookup = {}
        self.__singleton_lookup = {}
        self.__transient_lookup = {}
        self.__lifetime_meta_lookup = {
            LifeTimeEnums.SINGLETON: self.__singleton_lookup,
            LifeTimeEnums.TRANSIENT: self.__transient_lookup,
            # Un-Used dictionary
            LifeTimeEnums.SCOPED: {}
        }
        self.__lifetime_strategy_lookup = {
            LifeTimeEnums.SINGLETON: SingeltonDependencyStrategy,
            LifeTimeEnums.TRANSIENT: TransientDependencyStrategy,
            # Un-Used dictionary
            LifeTimeEnums.SCOPED: ScopedDependencyStrategy
        }

    def __gaurd_build_unregistered_interface(self, interface: ABC):
        """Throw 'KeyError' exception if interface is not registered."""
        if interface not in self.__interface_registery_lookup:
            raise KeyError(f"Interface: {interface} is not registered.")

    def __assert_implementation(self, interface: ABC, concrete_class) -> None:
        """Assert that the concrete class implements the interface
        being registered.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :return: None
        """
        if interface not in concrete_class.__bases__:
            raise TypeError(f"Concrete class: {concrete_class}"
                            f" has to implement interface: {interface}.")

    def __assert_abstract_class(self, interface: ABC) -> None:
        """Assert that the interface being registered is an abstract class.

        :param interface: interface needed to be registered.
        :return: None
        """
        if ABC not in interface.__bases__:
            raise TypeError(f"Interface: {interface}"
                            f" has to be an abstract class.")

    def __assert_proper_enum_used(self, enum: LifeTimeEnums) -> None:
        """Assert that the enum being passed is valid.

        :param enum: enum used to register dependency.
        :return: None
        """
        if enum not in LifeTimeEnums.__members__.values():
            raise KeyError(f"Enum: {enum} does not exist in 'LifeTimeEnums'.")

    def register_interface(self, interface: ABC,
                           concrete_class,
                           life_time: LifeTimeEnums) -> None:
        """Register interface with a corresponding concrete class to use.

        :param interface: interface needed to be registered.
        :param concrete_class: concrete class implementing the interface.
        :param life_time: life time enum specifying the lifetime of the class.
        :return: None
        """
        self.__assert_abstract_class(interface)
        self.__assert_implementation(interface, concrete_class)
        self.__assert_proper_enum_used(life_time)
        strategy: IDependencyStrategyInterface = (
            self.__lifetime_strategy_lookup[life_time]
        )

        lookup = self.__lifetime_meta_lookup[life_time]
        self.__interface_registery_lookup[interface] = strategy(
            lookup, interface, concrete_class)

    def build(self, interface: ABC, key_lookup) -> object:
        """Build an interface by utilizing the registery lookup.

        :param interface: interface needed to be built
        :param key_lookup: key_lookup that might be used to lookup\
        registered interfaces.
        :return object: concrete class that implemenets that interface
        """
        self.__gaurd_build_unregistered_interface(interface)
        interface_to_build: IDependencyStrategyInterface = (
            self.__interface_registery_lookup[interface]
        )
        return interface_to_build.build(self.__interface_registery_lookup,
                                        key_lookup)

    def clear(self, key_lookup):
        """Clear created dependencies for specific key

        :param key_lookup: immutable key to delete from\
        transient lookup.
        """
        if key_lookup in self.__transient_lookup:
            del self.__transient_lookup[key_lookup]
