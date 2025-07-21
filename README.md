from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from typing import Dict, Any
import json

@register(
    "astrbot_plugin_rawmessage_viewer",
    "xSapientia",
    "查看和记录消息平台原始消息的插件",
    "0.0.1",
    "https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer"
)
class RawMessageViewerPlugin(Star):
    def __init__(self, context: Context, config: Dict[str, Any] = None):
        super().__init__(context)
        self.config = config or {}
        self.enable_auto_insert = self.config.get("enable_auto_insert", True)
        self.enable_logging = self.config.get("enable_logging", True)
        self.delete_config_on_uninstall = self.config.get("delete_config_on_uninstall", False)
        logger.info("astrbot_plugin_rawmessage_viewer 插件已加载")

    @filter.command("rawmessage", alias={"rawmsg"})
    async def view_raw_message(self, event: AstrMessageEvent):
        """查看当前消息的原始内容"""
        try:
            # 获取原始消息
            raw_message = event.message_obj.raw_message
            platform_name = event.get_platform_name()

            # 格式化输出
            if platform_name == "aiocqhttp":
                output = f"[{platform_name}] RawMessage <{type(raw_message).__name__}"

                # 如果是字典类型，格式化显示
                if hasattr(raw_message, '__dict__'):
                    output += f", {raw_message.__dict__}>"
                elif isinstance(raw_message, dict):
                    output += f", {raw_message}>"
                else:
                    output += f", {str(raw_message)}>"

                yield event.plain_result(f"原始消息内容：\n{output}")
            else:
                yield event.plain_result(f"当前平台 [{platform_name}] 的原始消息：\n{str(raw_message)}")

        except Exception as e:
            logger.error(f"获取原始消息失败: {e}")
            yield event.plain_result(f"获取原始消息失败: {str(e)}")

    @filter.on_decorating_result()
    async def insert_raw_message(self, event: AstrMessageEvent):
        """在消息前插入原始消息内容"""
        if not self.enable_auto_insert:
            return

        try:
            platform_name = event.get_platform_name()

            # 只处理 aiocqhttp 平台
            if platform_name != "aiocqhttp":
                return

            # 获取原始消息
            raw_message = event.message_obj.raw_message

            # 格式化原始消息
            raw_msg_str = f"[{platform_name}] RawMessage <{type(raw_message).__name__}"
            if hasattr(raw_message, '__dict__'):
                raw_msg_str += f", {raw_message.__dict__}>"
            elif isinstance(raw_message, dict):
                raw_msg_str += f", {raw_message}>"
            else:
                raw_msg_str += f", {str(raw_message)}>"

            # 获取结果消息链
            result = event.get_result()
            if result and result.chain:
                # 在消息链开头插入原始消息
                from astrbot.api.message_components import Plain
                tip_content = f"\n<tip>\n{raw_msg_str}\n</tip>\n"
                result.chain.insert(0, Plain(tip_content))

                # 记录日志
                if self.enable_logging:
                    logger.info(f"已插入原始消息内容: {tip_content}")
                    logger.info(f"插入后的完整消息: {[str(comp) for comp in result.chain]}")

        except Exception as e:
            logger.error(f"插入原始消息失败: {e}")

    async def terminate(self):
        """插件卸载时的清理工作"""
        try:
            if self.delete_config_on_uninstall:
                # 删除配置文件
                import os
                config_path = f"data/config/astrbot_plugin_rawmessage_viewer_config.json"
                if os.path.exists(config_path):
                    os.remove(config_path)
                    logger.info(f"已删除配置文件: {config_path}")

                # 删除插件数据目录
                plugin_data_path = "data/plugin_data/astrbot_plugin_rawmessage_viewer"
                if os.path.exists(plugin_data_path):
                    import shutil
                    shutil.rmtree(plugin_data_path)
                    logger.info(f"已删除插件数据目录: {plugin_data_path}")

            logger.info("astrbot_plugin_rawmessage_viewer 插件已卸载")
        except Exception as e:
            logger.error(f"插件卸载时出错: {e}")
