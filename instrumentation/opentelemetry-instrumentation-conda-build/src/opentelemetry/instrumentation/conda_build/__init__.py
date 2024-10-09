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

The OpenTelemetry ``conda-build`` integration traces recipe
rendering, environment creation, and resource usage during build

Usage
-----

.. code-block:: python

    from conda-build import api
    from opentelemetry.instrumentation.conda_build import CondaBuildInstrumentor

    CondaBuildInstrumentor().instrument()

    api.build(".")

API
---
"""
# pylint: disable=no-value-for-parameter

import logging
import os
from typing import Collection

import conda_build
import conda_build.api
import conda_build.metadata
import conda_build.render
from wrapt import wrap_function_wrapper as _wrap

from opentelemetry import propagate
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.conda_build.package import _instruments
from opentelemetry.instrumentation.conda_build.version import __version__
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import Span, SpanKind, get_tracer
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


logger = logging.getLogger(__name__)

ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME = "conda-build.package_name"
ATTRIBUTE_CONDA_BUILD_RECIPE_PATH = "conda-build.recipe_path"
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
        "conda_build.api.render",
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
            "conda_build.api.build",
            kind=SpanKind.INTERNAL,
    ) as span:
        if span.is_recording():
            pass
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
            # span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_get_contents(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
        "conda_build.MetaData._get_contents",
        kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_parse_again(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
        "conda_build.MetaData.parse_again",
        kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_get_recipe_text(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.MetaData.get_recipe_text",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_get_output_metadata(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.MetaData.get_output_metadata",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)

@_with_tracer_wrapper
def _wrap_get_used_vars(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.MetaData.get_used_vars",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, instance.dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, instance.meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_get_env_dependencies(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.render.get_env_dependencies",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, args[0].dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, args[0].meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_execute_download_actions(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.render.execute_download_actions",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, args[0].dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, args[0].meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_get_upstream_pins(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.render.get_upstream_pins",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, args[0].dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, args[0].meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_add_upstream_pins(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.render.add_upstream_pins",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, args[0].dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, args[0].meta_path)
        return wrapped(*args, **kwargs)


@_with_tracer_wrapper
def _wrap_finalize_metadata(tracer, wrapped, instance, args, kwargs):
    with tracer.start_as_current_span(
            "conda_build.render.finalize_metadata",
            kind=SpanKind.INTERNAL,
    ) as span:
        # if span.is_recording():
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_PACKAGE_NAME, args[0].dist())
        #     span.set_attribute(ATTRIBUTE_CONDA_BUILD_RECIPE_PATH, args[0].meta_path)
        return wrapped(*args, **kwargs)


class CondaBuildInstrumentor(BaseInstrumentor):
    """An instrumentor for conda-build

    See `BaseInstrumentor`
    """
    root_span: Span | None = None

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

        carrier = {"traceparent": os.getenv("TRACEPARENT")}
        print("carrier: %s", carrier)
        ctx = TraceContextTextMapPropagator().extract(carrier)
        print("extracted context: %s", ctx)

        self.root_span = tracer.start_span("conda-build root process", context=ctx)

        _wrap(conda_build.api, "render", _wrap_render(tracer))
        _wrap(conda_build.api, "build", _wrap_build(tracer))

        _wrap(conda_build.metadata, "MetaData._get_contents", _wrap_get_contents(tracer))
        _wrap(conda_build.metadata, "MetaData.parse_again", _wrap_parse_again(tracer))
        _wrap(conda_build.metadata, "MetaData.get_recipe_text", _wrap_get_recipe_text(tracer))
        _wrap(conda_build.metadata, "MetaData.get_output_metadata", _wrap_get_output_metadata(tracer))
        _wrap(conda_build.metadata, "MetaData.get_used_vars", _wrap_get_used_vars(tracer))

        _wrap(conda_build.render, "get_env_dependencies", _wrap_get_env_dependencies(tracer))
        _wrap(conda_build.render, "execute_download_actions", _wrap_execute_download_actions(tracer))
        _wrap(conda_build.render, "get_upstream_pins", _wrap_get_upstream_pins(tracer))
        _wrap(conda_build.render, "add_upstream_pins", _wrap_add_upstream_pins(tracer))
        _wrap(conda_build.render, "finalize_metadata", _wrap_finalize_metadata(tracer))

    def _uninstrument(self, **kwargs):
        unwrap(conda_build.metadata.MetaData, "parse_again")
        unwrap(conda_build.metadata.MetaData, "_get_contents")
        unwrap(conda_build.metadata.MetaData, "get_recipe_text")
        unwrap(conda_build.metadata.MetaData, "get_output_metadata")
        unwrap(conda_build.metadata.MetaData, "get_used_vars")
        if self.root_span:
            self.root_span.end()
