from django.contrib.admin.models import LogEntry, LogEntryManager

UNKNOWN = 0
ACCEPT_PREREG = 10
REJECT_PREREG = 11
COMMENT_PREREG = 12

CONFIRM_SPAM = 20
CONFIRM_HAM = 21

NODE_REMOVED = 30
NODE_RESTORED = 31
CONTRIBUTOR_REMOVED = 32

USER_REMOVED = 40
USER_RESTORED = 41
USER_2_FACTOR = 42
USER_EMAILED = 43


def update_admin_log(user_id, object_id, object_repr, message, action_flag=UNKNOWN):
    OSFLogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=None,
        object_id=object_id,
        object_repr=object_repr,
        change_message=message,
        action_flag=action_flag
    )


class OSFLogEntryManager(LogEntryManager):
    pass


class OSFLogEntry(LogEntry):
    def message(self):
        return self.change_message
    message.allow_tags = True

    objects = OSFLogEntryManager()
