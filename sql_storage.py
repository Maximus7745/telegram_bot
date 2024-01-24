import pickle
from asyncio import Lock
from typing import Any, Dict, Optional

import aiomysql
from aiogram import Bot
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey


class MySQLStorage(BaseStorage):
    """
    MySQL storage backend for FSM.\n
    If database and table does not exist, it will be created automatically.
    """

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
    ) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self._lock = Lock()

    async def __execute(self, query: str, values: tuple = None, commit: bool = False):
        async with self._lock:
            await self.connect()
            await self.cursor.execute(query, values)
            if commit:
                await self.connection.commit()

    async def __create_tables(self) -> None:
        await self.cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{self.database}`;\n"
            f"USE `{self.database}`;\n"
            "CREATE TABLE IF NOT EXISTS `aiogram_fsm_states` ("
            "`chat_id` BIGINT NOT NULL,"
            "`user_id` BIGINT NOT NULL,"
            "`state` TEXT,"
            "PRIMARY KEY (`chat_id`)"
            ");\n"
            "CREATE TABLE IF NOT EXISTS `aiogram_fsm_data` ("
            "`chat_id` BIGINT NOT NULL,"
            "`user_id` BIGINT NOT NULL,"
            "`data` BLOB,"
            "PRIMARY KEY (`chat_id`)"
            ");"
        )

    async def connect(self) -> aiomysql.Connection:
        if self.connection is None:
            self.connection = await aiomysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.database,
            )
            self.cursor = await self.connection.cursor(aiomysql.DictCursor)
            await self.__create_tables()

        return self.connection

    async def close(self) -> None:
        if isinstance(self.connection, aiomysql.Connection):
            await self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        _state = state.state if isinstance(state, State) else state
        if _state is None:
            await self.__execute(
                "DELETE FROM `aiogram_fsm_states` WHERE `chat_id` = %s AND `user_id` = %s;",
                (key.chat_id, key.user_id),
                commit=True,
            )
            return

        await self.__execute(
            "INSERT INTO `aiogram_fsm_states` (`chat_id`, `user_id`, `state`) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE `state` = %s;",
            (key.chat_id, key.user_id, _state, _state),
            commit=True,
        )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        await self.__execute(
            "SELECT `state` FROM `aiogram_fsm_states` WHERE `chat_id` = %s AND `user_id` = %s;",
            (key.chat_id, key.user_id),
        )
        result = await self.cursor.fetchone()
        return result["state"] if result else None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        if not data:
            await self.__execute(
                "DELETE FROM `aiogram_fsm_data` WHERE `chat_id` = %s AND `user_id` = %s;",
                (key.chat_id, key.user_id),
                commit=True,
            )
            return

        serialized_data = pickle.dumps(data)
        await self.__execute(
            "INSERT INTO `aiogram_fsm_data` (`chat_id`, `user_id`, `data`) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE `data` = %s;",
            (key.chat_id, key.user_id, serialized_data, serialized_data),
            commit=True,
        )

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        await self.__execute(
            "SELECT `data` FROM `aiogram_fsm_data` WHERE `chat_id` = %s AND `user_id` = %s;",
            (key.chat_id, key.user_id),
        )
        result = await self.cursor.fetchone()
        return pickle.loads(result["data"]) if result else {}

    async def update_data(self, key: StorageKey, data: Dict[str, Any]) -> Dict[str, Any]:
        current_data = await self.get_data(key=key)
        current_data.update(data)
        await self.set_data(key=key, data=current_data)
        return current_data