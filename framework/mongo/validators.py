"""
Validators for use in ModularODM
"""
import collections
from modularodm.exceptions import ValidationError, ValidationValueError


def string_required(value):
    if value is None or value.strip() == '':
        raise ValidationValueError('Value must not be empty.')
    return True


def choice_in(choices, ignore_case=False):
    """
    Validate that the option provided is one of a restricted set of choices

    Returns a callable that can be used as a validator in ModularODM
    :param choices: An iterable of choices allowed for use
    :param bool ignore_case: If True, perform case-insensitive comparison (for strings) and otherwise match as-is
    :return:
    """

    if ignore_case:
        choice_set = frozenset(e.upper() if isinstance(e, basestring) else e
                               for e in choices)
    else:
        choice_set = frozenset(choices)

    def validator(value):

        if not isinstance(value, collections.Hashable):
            raise ValidationError('Must specify a single choice; value cannot be a collection')
        if ignore_case and isinstance(value, basestring):
            value = value.upper()

        if value in choice_set:
            return True
        else:
            raise ValidationValueError('Value must be one of these options: {}'.format(choices))
    return validator
