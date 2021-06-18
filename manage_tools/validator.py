from marshmallow import Schema, fields, INCLUDE, ValidationError


class ViaShareSchema(Schema):
    fb_id = fields.Str(required=False)
    password = fields.Str(required=False)
    secret_key = fields.Str(required=False)
    email = fields.Str(required=False)
    email_password = fields.Str(required=False)
    phone_number = fields.Str(required=False)
    cookies = fields.Str(required=False)


class CookiesSchema(Schema):
    used = fields.Bool(required=False)
    failed = fields.Bool(required=False)
