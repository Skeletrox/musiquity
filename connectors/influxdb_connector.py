from connectors.connector_interface import Connector
from influxdb import InfluxDBClient


class InfluxConnector(Connector):
    """
        Connector for Influx DB. Extends the abstract Connector class.
    """
    def auth(self, **kwargs):
        """
            Authenticates with an InfluxDB server
            kwarg params:
                host: The host the influxDB resides on
                port: The port number exposed
                database: The database to work on
                username: The username to use
                password: The password to use
        """
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", 8086)
        self.database = kwargs.get("database", None)
        self.username = kwargs.get("user", "root")
        self.password = kwargs.get("password", "root")

        self.client = InfluxDBClient(self.host, self.port, self.username,
                                     self.password, self.database)

    def create(self, **kwargs):
        """
            CREATEs something. Can create a database, or write a json body to measurement(s)
        """
        database_to_create = kwargs.get("database", None)
        if database_to_create is not None:
            self.client.create_database(database_to_create)
            return

        points_to_write = kwargs.get("points", None)
        if points_to_write is not None:
            self.client.write_points(points_to_write, database=self.database, time_precision=kwargs.get("time_precision", "s"), batch_size=kwargs.get("batch_size", 10000))

    def read(self, **kwargs):
        """
            READs something based on what kwargs sends, ideally a prepared query
        """
        query = kwargs.get("query", None)
        if query is not None:
            result = self.client.query(query, database=self.database)
            return result

    def update(self, **kwargs):
        """
            UPDATEs, works similar to read()
            TODO: cleanup if no change in code
        """
        return self.read(**kwargs)

    def delete(self, **kwargs):
        """
            DELETEs something. Database, measurement, query, whatever
        """
        database_to_delete = kwargs.get("database", None)
        if database_to_delete is not None:
            self.client.drop_database(database_to_delete)

        measurement_to_delete = kwargs.get("database", None)
        if measurement_to_delete is not None:
            self.client.drop_measurement(measurement_to_delete)

    def additional(self, **kwargs):
        
        # Switch a database
        database_to_switch_to = kwargs.get("database_switch", None)
        if database_to_switch_to is not None:
            self.client.switch_database(database_to_switch_to)
        pass