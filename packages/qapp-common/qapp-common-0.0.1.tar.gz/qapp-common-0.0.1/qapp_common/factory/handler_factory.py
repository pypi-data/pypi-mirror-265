"""
    QApp Platform Project handler_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ..handler.handler import Handler
from ..config.logging_config import *


class HandlerFactory:
    @staticmethod
    def create_handler(
            event,
            circuit_preparation_fn,
            post_processing_fn,
    ) -> Handler:
        logger.debug("Create InvocationHandler")

        raise NotImplemented('[HandlerFactory] create_handler() method must be implemented')
