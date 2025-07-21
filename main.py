import os
import json
import shutil
from typing import Dict, Any
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.provider import ProviderRequest

@register(
    "astrbot_plugin_raw_message_viewer",
    "xSapientia",
    "查看和展示aiocqhttp平台原始消息内容的调试插件",
    "0.0.1",
    "https://github.com/xSapientia/astrbot_plugin_raw_message_viewer",
)
class RawMessageViewerPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.plugin_data_dir = os.path.join("data", "plugin_data", "astrbot_plugin_raw_message_viewer")

        # 确保插件数据目录存在
        os.makedirs(self.plugin_data_dir, exist_ok=True)

        logger.info("astrbot_plugin_raw_message_viewer 插件已加载")

    @filter.llm_tool(name="view_raw_message")
    async def view_raw_message(self, event: AstrMessageEvent) -> str:
        """查看最近一条消息的原始内容。

        Args:
            无参数
        """
        try:
            # 获取平台名称
            platform_name = event.get_platform_name()

            if platform_name != "aiocqhttp":
                return f"当前平台 {platform_name} 不是 aiocqhttp，无法查看原始消息"

            # 获取原始消息
            raw_message = event.message_obj.raw_message

            if raw_message:
                # 格式化输出
                formatted_message = self._format_raw_message(raw_message)

                # 保存到历史记录
                self._save_message_history(event, raw_message)

                return f"[aiocqhttp] 原始消息内容:\n{formatted_message}"
            else:
                return "未找到原始消息内容"

        except Exception as e:
            logger.error(f"查看原始消息时出错: {str(e)}")
            return f"查看原始消息失败: {str(e)}"

    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """在LLM请求前插入原始消息内容"""
        if not self.config.get("enable_plugin", True):
            return

        if not self.config.get("show_raw_message", True):
            return

        try:
            # 只处理aiocqhttp平台的消息
            if event.get_platform_name() != "aiocqhttp":
                return

            raw_message = event.message_obj.raw_message
            if not raw_message:
                return

            # 格式化原始消息
            formatted_message = self._format_raw_message(raw_message)

            # 根据配置截断消息
            max_length = self.config.get("max_message_length", 1000)
            if max_length > 0 and len(formatted_message) > max_length:
                formatted_message = formatted_message[:max_length] + "...(已截断)"

            # 在prompt前插入原始消息内容
            tip_content = f"\n<tip>\n[aiocqhttp] RawMessage {raw_message}\n</tip>\n"

            # 更新请求内容
            req.prompt = tip_content + req.prompt

            logger.debug(f"已在消息前插入原始内容")

        except Exception as e:
            logger.error(f"处理原始消息时出错: {str(e)}")

    def _format_raw_message(self, raw_message: Any) -> str:
        """格式化原始消息为可读字符串"""
        try:
            if isinstance(raw_message, dict):
                return json.dumps(raw_message, ensure_ascii=False, indent=2)
            else:
                return str(raw_message)
        except:
            return str(raw_message)

    def _save_message_history(self, event: AstrMessageEvent, raw_message: Any):
        """保存消息历史记录"""
        try:
            history_file = os.path.join(self.plugin_data_dir, "message_history.json")

            # 读取现有历史
            history = []
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)

            # 添加新记录
            history.append({
                "timestamp": event.message_obj.timestamp,
                "sender_id": event.get_sender_id(),
                "sender_name": event.get_sender_name(),
                "message_type": event.message_obj.type.name,
                "raw_message": raw_message if isinstance(raw_message, dict) else str(raw_message)
            })

            # 只保留最近100条
            if len(history) > 100:
                history = history[-100:]

            # 保存
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"保存消息历史时出错: {str(e)}")

    async def terminate(self):
        """插件卸载时的清理工作"""
        logger.info("astrbot_plugin_raw_message_viewer 插件正在卸载...")

        # 根据配置决定是否删除数据
        if self.config.get("delete_data_on_uninstall", False):
            try:
                # 删除插件数据目录
                if os.path.exists(self.plugin_data_dir):
                    shutil.rmtree(self.plugin_data_dir)
                    logger.info(f"已删除插件数据目录: {self.plugin_data_dir}")

                # 删除配置文件
                config_file = os.path.join("data", "config", "astrbot_plugin_raw_message_viewer_config.json")
                if os.path.exists(config_file):
                    os.remove(config_file)
                    logger.info(f"已删除配置文件: {config_file}")

            except Exception as e:
                logger.error(f"删除插件数据时出错: {str(e)}")

        logger.info("astrbot_plugin_raw_message_viewer 插件已卸载")
