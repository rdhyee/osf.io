# -*- coding: utf-8 -*-


def get_entry_point(user):
    """
    Given the user system_tags, return the user entry point (osf, osf4m, prereg, institution)
    In case of multiple entry_points existing in the system_tags, return only the first one.
    """
    entry_points = ['osf4m', 'prereg_challenge_campaign', 'institution_campaign']
    for i in user.system_tags:
        if i in entry_points:
            return i
    else:
        return 'osf'
