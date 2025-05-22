from collections.abc import Generator
from datetime import date
from decimal import Decimal
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from loguru import logger

from libs.nlp_query import (
    ConfigurationError,
    DatabaseError,
    DatabaseManager,
    DBConfig,
    NLPQueryProcessor,
)


class Chat2DBTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """处理工具调用"""
        try:
            res = self._process_query(tool_parameters)
            yield self.create_json_message(json=res)
        except (ConfigurationError, DatabaseError) as e:
            yield self.create_text_message(text=str(e))
        except Exception as e:
            yield self.create_text_message(text=f"系统错误: {str(e)}")

    def _process_query(self, tool_parameters: dict[str, Any]) -> dict:
        """处理自然语言查询"""
        # 初始化配置和管理器
        db_config = DBConfig(
            user=tool_parameters["db_user"],
            passwd=tool_parameters["db_passwd"],
            host=tool_parameters["db_host"],
            name=tool_parameters["db_name"],
            port=tool_parameters.get("db_port", 3306),
        )
        db_manager = DatabaseManager(db_config)
        nlp_processor = NLPQueryProcessor(self.session.model)

        query = tool_parameters.get("query")
        model_config = tool_parameters.get("model")
        generate_sql_prompt = tool_parameters.get("generate_sql_prompt")

        with db_manager.get_engine() as engine:
            # 获取表结构信息
            table_info = db_manager.get_table_info(engine)
            params = {
                "table_info": table_info,
                "query": query,
                "model_config": model_config,
            }
            generate_sql_prompt and params.update({"sql_query_prompt": generate_sql_prompt})
            # 生成SQL查询
            sql_query = nlp_processor.generate_sql(**params)
            logger.info(f"SQL查询语句: {sql_query}")

            # 执行SQL查询
            results = db_manager.execute_sql(engine, sql_query)
            logger.info(f"SQL查询结果: {results}")
            # 处理不可序列号的字段
            for result in results:
                for key, value in result.items():
                    if isinstance(value, date):
                        result[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        result[key] = str(value)

            # 生成自然语言回答
            answer = nlp_processor.generate_answer(
                table_info, query, sql_query, results, model_config
            )
            logger.info(f"自然语言回答: {answer}")
            return {
                "query": query,
                "sql": sql_query,
                "result": results,
                "answer": answer,
            }
