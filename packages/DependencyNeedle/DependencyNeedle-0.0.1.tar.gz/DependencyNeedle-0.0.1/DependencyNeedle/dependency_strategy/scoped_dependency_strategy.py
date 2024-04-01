from abc import ABC
from typing import Optional
from DependencyNeedle.dependency_strategy.\
    dependency_strategy_interface import IDependencyStrategyInterface


class ScopedDependencyStrategy(IDependencyStrategyInterface):
    """Scoped strategy for dependency building."""

    def _custom_post_build_strategy(self, interface: ABC,
                                    concrete_class: object,
                                    key_lookup: object) -> None:
        """Scoped post build strategy"""
        return None

    def _custom_pre_build_strategy(self,
                                   interface: ABC,
                                   key_lookup: object) -> Optional[object]:
        """Scoped pre build strategy"""
        return None
