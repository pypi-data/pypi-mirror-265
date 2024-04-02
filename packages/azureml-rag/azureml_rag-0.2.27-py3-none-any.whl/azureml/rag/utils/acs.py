# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Functions for interacting with AzureSearch."""

import functools
from importlib.util import find_spec, module_from_spec


def _get_azuresearch_module_instance():
    import langchain_core.pydantic_v1

    original_root_validator = langchain_core.pydantic_v1.root_validator
    try:
        langchain_core.pydantic_v1.root_validator = functools.partial(langchain_core.pydantic_v1.root_validator, allow_reuse=True)

        module_spec = find_spec('langchain.vectorstores.azuresearch')
        azuresearch = module_from_spec(module_spec)
        module_spec.loader.exec_module(azuresearch)

        del azuresearch.AzureSearchVectorStoreRetriever

        return azuresearch
    finally:
        langchain_core.pydantic_v1.root_validator = original_root_validator
