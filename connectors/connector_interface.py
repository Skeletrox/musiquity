import abc

class Connector(metacalass=abc.ABCMeta):

    @abc.abstractmethod
    def auth(self, **kwargs):
        """
            Interface for basic authentication to the database.
        """
        pass

    @abc.abstractmethod
    def create(self, **kwargs):
        """
            Interface for create operations (INSERT INTO)
        """
        pass

    @abc.abstractmethod
    def read(self, **kwargs):
        """
            Interface for read operations (SELECT ... FROM)
        """
        pass

    @abc.abstractmethod
    def update(self, **kwargs):
        """
            Interface for update operations (UPDATE ... SET ... WHERE ...)
        """
        pass

    @abc.abstractmethod
    def delete(self, **kwargs):
        """
            Inteface for delete operations (DROP / DELETE FROM)
        """
        pass

    @abc.abstractmethod
    def additional(self, **kwargs):
        """
            Interface for any additional methods the database may support
        """
        pass
