from __future__ import annotations

import functools
from typing import NoReturn

from procrastinate import blueprints

from . import exceptions


def _not_ready(_method: str, *args, **kwargs) -> NoReturn:
    base_text = (
        f"Cannot call procrastinate.contrib.app.{_method}() before "
        "the 'procrastinate.contrib.django' django app is ready."
    )
    details = (
        "If this message appears at import time, the app is not ready yet: "
        "move the corresponding code in an app's `AppConfig.ready()` method. "
        "If this message appears in an app's `AppConfig.ready()` method, "
        'make sure `"procrastinate.contrib.django"` appears before '
        "that app when ordering apps in the Django setting `INSTALLED_APPS`. "
        "Alternatively, use the Django setting "
        "PROCRASTINATE_ON_APP_READY (see the doc)."
    )
    raise exceptions.DjangoNotReady(base_text + "\n\n" + details)


class FutureApp(blueprints.Blueprint):
    _shadowed_methods = frozenset(
        [
            "__enter__",
            "__exit__",
            "_register_builtin_tasks",
            "_worker",
            "check_connection_async",
            "check_connection",
            "close_async",
            "close",
            "configure_task",
            "open_async",
            "open",
            "perform_import_paths",
            "run_worker_async",
            "run_worker",
            "schema_manager",
            "with_connector",
            "will_configure_task",
        ]
    )
    for method in _shadowed_methods:
        locals()[method] = functools.partial(_not_ready, method)
