# -*- coding: UTF-8 -*-

from django.db import models

def audit(cls):
    """
    Decorator de clase para que se actualice el campo last_user_id
    antes del save y ademas se guarde un registro de auditoria antes del delete.
    """
    old_save = cls.save
    old_delete = cls.delete
    def save(self, *arg, **kw):
        from middleware import get_current_user
        user = get_current_user()
        if user is not None:
            self.last_user_id = user.id
        return old_save(self, *arg, **kw)


    def delete(self, *arg, **kw):
        from middleware import get_current_user
        user = get_current_user()
        if user is not None:
            self.last_user_id = user.id
        cls.save(self)
        return old_delete(self, *arg, **kw)
    cls.save = save
    cls.delete = delete
    cls.last_user_id = models.IntegerField(null=True, blank=True, editable=False)
    return cls
