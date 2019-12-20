from groundwork.patterns import GwCommandsPattern
from groundwork_database.patterns import GwSqlPattern

from .models.models import get_classes


class CompeteDatabasePattern(GwSqlPattern, GwCommandsPattern):

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super(CompeteDatabasePattern, self).__init__(*args, **kwargs)

        if not hasattr(self.app, "compete_mgt"):
            self.app.compete_mgt = CmStore(self)

        self.compete_mgt = self.app.compete_mgt


class CmStore:

    def __init__(self, plugin):
        self._plugin = plugin
        self._app = plugin.app
        self._log = plugin.log

        self.models = CmDatabaseModels(plugin)


class CmDatabaseModels:

    def __init__(self, plugin):
        self._plugin = plugin
        self.all = []

        self.db = self._plugin.databases.get(self._plugin.app.config.get('CM_DATABASE_NAME'))
        if self.db is None:
            self.db = self._plugin.databases.register(self._plugin.app.config.get('CM_DATABASE_NAME'),
                                                      self._plugin.app.config.get('CM_DATABASE_CONNECTION'),
                                                      self._plugin.app.config.get('CM_DATABASE_DESCRIPTION'))

        classes = get_classes(self.db)

        for key, clazz in classes.items():
            self.db.classes.register(clazz)
            setattr(self, key, clazz)
            self.all.append(clazz)

        self.db.create_all()