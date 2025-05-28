import json
from collections.abc import Generator
from datetime import date
from decimal import Decimal
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from loguru import logger

from libs.nlp_query import ConfigurationError, DatabaseError, DatabaseManager, DBConfig


class ExecSQLTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """处理工具调用"""
        try:
            res = self._process_query(tool_parameters)
            # yield self.create_json_message(data=res)
            result = (
                json.dumps(res["result"], ensure_ascii=False)
                if res.get("result")
                else None
            )
            yield self.create_text_message(text=result)
        except (ConfigurationError, DatabaseError) as e:
            logger.error(e)
            yield self.create_text_message(text=str(e))
        except Exception as e:
            logger.error(f"系统错误: {str(e)}")
            yield self.create_text_message(text=f"系统错误: {str(e)}")

    def _process_query(self, tool_parameters: dict[str, Any]) -> dict:
        """处理自然语言查询"""
        sql_query = tool_parameters.get("sql_query")

        # 初始化配置和管理器
        db_config = DBConfig(
            user=tool_parameters["db_user"],
            passwd=tool_parameters["db_passwd"],
            host=tool_parameters["db_host"],
            name=tool_parameters["db_name"],
            port=tool_parameters.get("db_port", 3306),
        )
        db_manager = DatabaseManager(db_config)
        with db_manager.get_engine() as engine:

            # 执行SQL查询
            results = db_manager.execute_sql(engine, sql_query)
            logger.info(f"SQL查询结果: {results}")

            # 将datetime.date对象转换为字符串
            for result in results:
                for key, value in result.items():
                    if isinstance(value, date):
                        result[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        result[key] = str(value)

            return {
                "sql": sql_query,
                "result": results,
            }
