"""
    QApp Platform Project provider_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from abc import ABC, abstractmethod

from ..enum.provider_tag import ProviderTag
from ..enum.sdk import Sdk


class ProviderFactory(ABC):

    @abstractmethod
    def create_provider(self, provider_type: ProviderTag, sdk: Sdk, authentication: dict):
        """

        @param sdk:
        @param provider_type:
        @param authentication:
        @return:
        """

        raise NotImplemented('[ProviderFactory] create_provider() method must be implemented')
