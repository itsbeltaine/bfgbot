from contextlib import contextmanager
from psycopg2.extensions import cursor
import psycopg2.extras
from psycopg2 import sql

from bfgbot.discord_classes import Discord_Handle


class BFG_Bot_DB_Parameters:
    host: str = ""
    port: str = ""
    database: str = ""
    user: str = ""
    password: str = ""

    def __init__(
        self,
        host: str,
        port: str,
        database: str,
        user: str,
        password: str,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password


class BFG_Bot_DB_Client:
    params: BFG_Bot_DB_Parameters = None
    _conn = None

    def __init__(self, params: BFG_Bot_DB_Parameters):
        self.params = params

    def _get_cursor(self) -> cursor:
        if self._conn is None:
            self._conn = psycopg2.connect(
                host=self.params.host,
                port=self.params.port,
                dbname=self.params.database,
                user=self.params.user,
                password=self.params.password,
            )

        return self._conn.cursor()

    def add_morceaux_robots(
        self, giver: Discord_Handle, receiver: Discord_Handle, morceaux: int
    ):
        query_string_audit = """
            WITH myconstants (giver, receiver, morceaux, timenow) AS (
                VALUES(
                    %(giver)s,
                    %(receiver)s,
                    %(morceaux)s,
                    now() at TIME zone 'UTC'
                )
            )
            INSERT INTO mr.event (
                discord_id_giver,
                event_time,
                discord_id_receiver,
                robot_received
            )
            SELECT
                giver,
                timenow,
                receiver,
                morceaux
            FROM
                myconstants
            """

        query_string_total_given = """
            INSERT INTO mr.total (
                discord_id,
                discord_global_name,
                total_given
            )
            VALUES (
                %(giver_id)s,
                %(giver_name)s,
                %(morceaux)s
            )
            ON CONFLICT (discord_id)
            DO
                UPDATE
                SET total_given =
                    mr.total.total_given + excluded.total_given
            """

        query_string_total_received = """
            INSERT INTO mr.total (
                discord_id,
                discord_global_name,
                total,
                total_received
            )
            VALUES (
                %(receiver_id)s,
                %(receiver_name)s,
                %(morceaux)s,
                %(morceaux)s
            )
            ON CONFLICT (discord_id)
            DO
                UPDATE
                    SET total_received =
                    mr.total.total_received + excluded.total_received,
                    total = mr.total.total + excluded.total
            """

        query_audit = sql.SQL(query_string_audit)
        query_total_given = sql.SQL(query_string_total_given)
        query_total_received = sql.SQL(query_string_total_received)

        with self._get_cursor() as curs:
            curs.execute(
                query_audit,
                {
                    "giver": giver.discord_id,
                    "receiver": receiver.discord_id,
                    "morceaux": morceaux,
                },
            )

            curs.execute(
                query_total_given,
                {
                    "giver_id": giver.discord_id,
                    "giver_name": giver.global_name,
                    "morceaux": morceaux,
                },
            )

            curs.execute(
                query_total_received,
                {
                    "receiver_id": receiver.discord_id,
                    "receiver_name": receiver.global_name,
                    "morceaux": morceaux,
                },
            )

            self._conn.commit()
