from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Optional
from urllib import parse

import sqlparse
from dify_plugin.entities.model.message import SystemPromptMessage, UserPromptMessage
from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from libs.prompts import CUSTOM_PROMPT, CUSTOM_PROMPT_SQLQUERY

# from langchain_community.utilities import SQLDatabase
from libs.sql_database import SQLDatabase


class ConfigurationError(Exception):
    """配置错误异常"""

    pass


class DatabaseError(Exception):
    """数据库操作异常"""

    pass


@dataclass
class DBConfig:
    user: str
    passwd: str
    host: str
    name: str
    port: int = 3306
    engine: str = "mysql+pymysql"

    def validate(self) -> None:
        """验证配置有效性"""
        if not all([self.user, self.host, self.name]):
            raise ConfigurationError("数据库配置信息不完整")
        if not 0 < self.port < 65536:
            raise ConfigurationError("无效的端口号")

    @property
    def connection_url(self) -> str:
        """生成数据库连接URL"""
        return (
            f"{self.engine}://{self.user}:{parse.quote(self.passwd)}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class DatabaseManager:
    """数据库管理类，负责处理数据库连接和查询"""

    def __init__(self, config: DBConfig) -> None:
        self.config = config
        self._engine: Optional[Engine] = None

    @contextmanager
    def get_engine(self) -> Generator[Engine, None, None]:
        """获取数据库引擎的上下文管理器"""
        if not self._engine:
            try:
                self._engine = create_engine(self.config.connection_url)
                yield self._engine
            except SQLAlchemyError as e:
                raise DatabaseError(f"数据库连接失败: {str(e)}") from e
            finally:
                if self._engine:
                    self._engine.dispose()
                    self._engine = None
        else:
            yield self._engine

    def get_table_info(self, engine: Engine) -> str:
        """获取数据库表结构信息"""
        return SQLDatabase(engine).get_table_info()

    def execute_sql(self, engine: Engine, sql_query: str) -> list[dict]:
        """执行SQL查询并返回结果"""
        try:
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                return [dict(row._mapping) for row in result]
        except SQLAlchemyError as e:
            raise DatabaseError(f"SQL执行失败: {str(e)}")


class NLPQueryProcessor:
    """自然语言查询处理器"""

    def __init__(self, session_model: Any) -> None:
        self.session_model = session_model

    @staticmethod
    def is_select_query(sql: str) -> bool:
        parsed = sqlparse.parse(sql)
        if not parsed:
            return False
        print(parsed[0].get_type())
        return parsed[0].get_type() == 'SELECT'

    def generate_sql(
        self,
        table_info: str,
        query: str,
        model_config: Any,
        sql_query_prompt: str = CUSTOM_PROMPT_SQLQUERY.format(top_k=5),
    ) -> str:
        """生成SQL查询语句"""
        context = f"表结构信息:\n{table_info}\n\n问题: {query}"
        response = self._invoke_model(sql_query_prompt, context, model_config)
        logger.info(f"Generate SQL LLM Response: {response.message.content}")
        sql_match = response.message.content.lower().split("sqlquery:")
        if len(sql_match) < 2:
            raise DatabaseError("无法生成有效的SQL查询")
        sql = sql_match[1].strip()
        if not self.is_select_query(sql):
            raise DatabaseError("禁止生成非查询以外的SQL语句")
        return sql

    def generate_answer(
        self,
        table_info: str,
        query: str,
        sql_query: str,
        results: list[dict],
        model_config: Any,
    ) -> str:
        """生成自然语言回答"""
        prompt = CUSTOM_PROMPT
        context = f"TableInfo:\n{table_info}\n\nQuestion: {query}, SQLQuery：{sql_query}, SQLResult: {results}"
        response = self._invoke_model(prompt, context, model_config)
        logger.info(f"Generate Answer LLM Response: {response.message.content}")
        return response.message.content.lower().split("answer:")[-1].strip()

    def _invoke_model(self, prompt: str, context: str, model_config: Any) -> Any:
        """调用模型进行推理"""
        return self.session_model.llm.invoke(
            model_config=model_config,
            prompt_messages=[
                SystemPromptMessage(content=prompt),
                UserPromptMessage(content=context),
            ],
            stream=False,
        )
