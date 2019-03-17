import uuid


class ValidationError(ValueError):
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


class UUID(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        if message is None:
            message = field.gettext('Invalid UUID.')
        if field.data:
            try:
                uuid.UUID(field.data)
            except ValueError:
                raise ValidationError(message)
