## This is to serialize the _id property of a MongoDB document to a usable model as the _id is a bson object
## Solution and code taken from:
## https://stackoverflow.com/questions/76686267/what-is-the-new-way-to-declare-mongo-objectid-with-pydantic-v2-0

from typing import Annotated, Any, Callable
from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

# Based on https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types
class ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:

        def validate_from_str(id_: str) -> ObjectId:
            return ObjectId(id_)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())


PydanticObjectId = Annotated[
    ObjectId, ObjectIdPydanticAnnotation
]

# class ObjectIdPydanticAnnotation:
#     def __init__(self, alias: str = None):
#         self.alias = alias
    
#     @classmethod
#     def validate_object_id(cls, v: Any, handler) -> ObjectId:
#         if isinstance(v, ObjectId):
#             return v

#         s = handler(v)
#         if ObjectId.is_valid(s):
#             return ObjectId(s)
#         else:
#             raise ValueError("Invalid ObjectId")

#     @classmethod
#     def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
#         assert source_type is ObjectId
#         return core_schema.no_info_wrap_validator_function(
#             cls.validate_object_id, 
#             core_schema.str_schema(), 
#             serialization=core_schema.to_string_ser_schema(),
#         )

#     @classmethod
#     def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
#         return handler(core_schema.str_schema())
