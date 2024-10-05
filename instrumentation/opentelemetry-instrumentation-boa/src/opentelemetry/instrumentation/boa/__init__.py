# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

Usage
-----

The OpenTelemetry ``boa`` integration traces recipe
rendering, environment creation, and resource usage during build

Usage
-----

.. code-block:: python

    from boa.cli.mambabuild import api
    from opentelemetry.instrumentation.boa import BoaInstrumentor

    BoaInstrumentor().instrument()

    api.build(".")

API
---
"""
# pylint: disable=no-value-for-parameter

import logging
from typing import Collection

import boa
import boa.cli
import boa.cli.mambabuild
import boa.core.metadata
import boa.core.render
from wrapt import wrap_function_wrapper as _wrap

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.boa.package import _instruments
from opentelemetry.instrumentation.boa.version import __version__
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, get_tracer

logger = logging.getLogger(__name__)

ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME = "boa.package_name"
ATTRIBUTE_CONDA_BUILD_RECIPE_PATH = "boa.recipe_path"
DEFAULT_TEMPLATE_NAME = "<memory>"


def _with_tracer_wrapper(func):
    """Helper for providing tracer for wrapper functions."""

    def _with_tracer(tracer):
        def wrapper(wrapped, instance, args, kwargs):
            return func(tracer, wrapped, instance, args, kwargs)

        return wrapper

    return _with_tracer

@_with_tracer_wrapper
def _wrap_render(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
        "boa.api.render",
        kind=SpanKind.INTERNAL,
    ) as span:
        if span.is_recording():
            pass
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_build(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "boa.api.build",
            kind=SpanKind.INTERNAL,
    ) as span:
        if span.is_recording():
            pass
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


class BoaInstrumentor(BaseInstrumentor):
    """An instrumentor for boa

    See `BaseInstrumentor`
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(
            __name__,
            __version__,
            tracer_provider,
            schema_url="https://opentelemetry.io/schemas/1.11.0",
        )

        _wrap(boa.cli.mambabuild.api, "render", _wrap_render(tracer))
        _wrap(boa.cli.mambabuild.api, "build", _wrap_build(tracer))

    def _uninstrument(self, **kwargs):
        unwrap(boa.cli.mambabuild.api, "render")
        unwrap(boa.cli.mambabuild.api, "build")
