from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from advanced_alchemy.exceptions import wrap_sqlalchemy_exception as _wrap_sqlalchemy_exception

if TYPE_CHECKING:
    from sqlalchemy.orm import InstrumentedAttribute

    from advanced_alchemy.base import ModelProtocol
    from advanced_alchemy.repository.typing import ModelT

# NOTE: For backward compatibility with Litestar - this is imported from here within the litestar codebase.
wrap_sqlalchemy_exception = _wrap_sqlalchemy_exception


def get_instrumented_attr(model: type[ModelProtocol], key: str | InstrumentedAttribute) -> InstrumentedAttribute:
    if isinstance(key, str):
        return cast("InstrumentedAttribute", getattr(model, key))
    return key


def model_from_dict(model: ModelT, **kwargs: Any) -> ModelT:
    """Return ORM Object from Dictionary."""
    data = {}
    for column_name in model.__mapper__.columns.keys():  # noqa: SIM118
        column_val = kwargs.get(column_name, None)
        if column_val is not None:
            data[column_name] = column_val
    return model(**data)  # type: ignore  # noqa: PGH003
