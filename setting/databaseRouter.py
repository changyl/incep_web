# -*- coding: utf-8 -*-
from django.conf import settings
# DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING

class modelsRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return 'default'

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        return 'default'

class ReportRouter(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return 'data_backup'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'data_backup'

    # def allow_relation(self, obj1, obj2, **hints):
    #     """
    #     Relations between objects are allowed if both objects are
    #     in the primary/replica pool.
    #     """
    #     db_list = ('primary', 'replica1', 'replica2')
    #     if obj1._state.db in db_list and obj2._state.db in db_list:
    #         return True
    #     return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True


class ExecuteRoutor(object):
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return 'review'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'review'
