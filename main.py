import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any, Optional

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.provider import ProviderRequest


@register(
    "astrbot_plugin_rawmessage_viewer",
    "xSapientia",
    "查看和展示 aiocqhttp 原始消息的插件",
    "0.0.1",
    "https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer"
)
class RawMessageViewerPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.plugin_data_dir = os.path.join("data", "plugin_data", "astrbot_plugin_rawmessage_viewer")
        self.cache_file = os.path.join(self.plugin_data_dir, "message_cache.json")
        self.message_cache: Dict[str, Any] = {}

        # 创建插件数据目录
        os.makedirs(self.plugin_data_dir, exist_ok=True)

        # 加载缓存
        self._load_cache()

        logger.info("RawMessage Viewer 插件已加载")

    def _load_cache(self):
        """加载消息缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.message_cache = json.load(f)
            except Exception as e:
                logger.error(f"加载消息缓存失败: {e}")
                self.message_cache = {}

    def _save_cache(self):
        """保存消息缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.message_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存消息缓存失败: {e}")

    @filter.command("rawmsg", alias={'查看原始消息', 'viewraw'})
    async def view_raw_message(self, event: AstrMessageEvent):
        """查看当前消息的原始内容

        显示 napcat 通过 aiocqhttp 传递的原始消息数据
        """
        if not self.config.get("enable_plugin", True):
            yield event.plain_result("插件未启用")
            return

        # 检查是否是 aiocqhttp 平台
        if event.get_platform_name() != "aiocqhttp":
            yield event.plain_result("此功能仅支持 QQ (aiocqhttp) 平台")
            return

        # 获取原始消息
        raw_message = event.message_obj.raw_message

        # 缓存消息
        message_id = str(event.message_obj.message_id)
        self.message_cache[message_id] = {
            "raw": raw_message,
            "time": datetime.now().isoformat(),
            "sender": event.get_sender_name(),
            "sender_id": event.get_sender_id()
        }

        # 限制缓存大小
        if len(self.message_cache) > 100:
            # 删除最早的消息
            oldest_key = min(self.message_cache.keys(),
                           key=lambda k: self.message_cache[k].get('time', ''))
            del self.message_cache[oldest_key]

        self._save_cache()

        # 构建显示内容
        if self.config.get("show_raw_json", False):
            # 显示完整 JSON
            result = f"【原始消息 JSON】\n```json\n{json.dumps(raw_message, ensure_ascii=False, indent=2)}\n```"
        else:
            # 显示格式化信息
            result = self._format_raw_message(raw_message)

        yield event.plain_result(result)

    @filter.command("rawhistory", alias={'原始消息历史'})
    async def view_raw_history(self, event: AstrMessageEvent):
        """查看最近的原始消息历史"""
        if not self.config.get("enable_plugin", True):
            yield event.plain_result("插件未启用")
            return

        if not self.message_cache:
            yield event.plain_result("暂无消息历史")
            return

        # 获取最近10条
        recent_messages = sorted(
            self.message_cache.items(),
            key=lambda x: x[1].get('time', ''),
            reverse=True
        )[:10]

        result = "【最近原始消息历史】\n"
        for msg_id, msg_data in recent_messages:
            time_str = msg_data.get('time', 'unknown')[:19]
            sender = msg_data.get('sender', 'unknown')
            result += f"\n时间: {time_str}\n发送者: {sender}\n消息ID: {msg_id}\n"
            result += "-" * 30 + "\n"

        yield event.plain_result(result)

    @filter.llm_tool(name="get_raw_message")
    async def get_raw_message_tool(self, event: AstrMessageEvent, message_id: str = None) -> MessageEventResult:
        """获取原始消息内容

        Args:
            message_id(string): 消息ID，不填则获取当前消息
        """
        if not self.config.get("enable_plugin", True):
            yield event.plain_result("插件未启用")
            return

        if message_id:
            # 从缓存获取
            if message_id in self.message_cache:
                msg_data = self.message_cache[message_id]
                result = self._format_raw_message(msg_data.get('raw', {}))
            else:
                result = f"未找到消息ID: {message_id}"
        else:
            # 获取当前消息
            if event.get_platform_name() == "aiocqhttp":
                raw_message = event.message_obj.raw_message
                result = self._format_raw_message(raw_message)
            else:
                result = "当前平台不支持查看原始消息"

        yield event.plain_result(result)

    @filter.on_llm_request()
    async def add_raw_message_prefix(self, event: AstrMessageEvent, req: ProviderRequest):
        """在 LLM 请求前添加原始消息信息"""
        if not self.config.get("enable_plugin", True):
            return

        if not self.config.get("enable_llm_prefix", True):
            return

        # 仅处理 aiocqhttp 平台
        if event.get_platform_name() != "aiocqhttp":
            return

        try:
            raw_message = event.message_obj.raw_message
            prefix = self._generate_llm_prefix(event, raw_message)

            # 长度限制
            max_length = self.config.get("max_prefix_length", 500)
            if max_length > 0 and len(prefix) > max_length:
                prefix = prefix[:max_length] + "...[已截断]"

            # 添加到系统提示
            if req.system_prompt:
                req.system_prompt = prefix + "\n" + req.system_prompt
            else:
                req.system_prompt = prefix

            logger.debug(f"已添加 RawMessage 前缀到 LLM 请求")

        except Exception as e:
            logger.error(f"添加 RawMessage 前缀失败: {e}")

    def _format_raw_message(self, raw_message: Dict[str, Any]) -> str:
        """格式化原始消息用于显示"""
        if not raw_message:
            return "无原始消息数据"

        result = "【原始消息信息】\n"

        # 基本信息
        result += f"消息ID: {raw_message.get('message_id', 'N/A')}\n"
        result += f"消息类型: {raw_message.get('message_type', 'N/A')}\n"
        result += f"时间戳: {raw_message.get('time', 'N/A')}\n"

        # 发送者信息
        sender = raw_message.get('sender', {})
        if sender:
            result += f"\n【发送者信息】\n"
            result += f"QQ号: {sender.get('user_id', 'N/A')}\n"
            result += f"昵称: {sender.get('nickname', 'N/A')}\n"
            result += f"群名片: {sender.get('card', 'N/A')}\n"
            result += f"性别: {sender.get('sex', 'N/A')}\n"
            result += f"年龄: {sender.get('age', 'N/A')}\n"
            result += f"头衔: {sender.get('title', 'N/A')}\n"
            result += f"等级: {sender.get('level', 'N/A')}\n"

        # 群信息
        if raw_message.get('group_id'):
            result += f"\n【群信息】\n"
            result += f"群号: {raw_message.get('group_id', 'N/A')}\n"

        # 消息内容
        result += f"\n【消息内容】\n"
        result += f"原始消息: {raw_message.get('raw_message', 'N/A')}\n"

        # 消息段
        message_segments = raw_message.get('message', [])
        if message_segments:
            result += f"\n【消息段详情】\n"
            for i, seg in enumerate(message_segments):
                seg_type = seg.get('type', 'unknown')
                seg_data = seg.get('data', {})
                result += f"段{i+1}: 类型={seg_type}"

                if seg_type == 'text':
                    result += f", 内容=\"{seg_data.get('text', '')}\""
                elif seg_type == 'image':
                    result += f", 图片URL={seg_data.get('url', 'N/A')}"
                elif seg_type == 'at':
                    result += f", @用户={seg_data.get('qq', 'N/A')}"
                elif seg_type == 'reply':
                    result += f", 回复消息ID={seg_data.get('id', 'N/A')}"

                result += "\n"

        return result

    def _generate_llm_prefix(self, event: AstrMessageEvent, raw_message: Dict[str, Any]) -> str:
        """生成 LLM 请求的前缀"""
        template = self.config.get("prefix_format",
            "【消息元数据】\n发送者: {sender_name} ({sender_id})\n群组: {group_name} ({group_id})\n时间: {time}\n消息类型: {message_type}\n原始内容: {raw_content}\n---\n")

        # 获取发送者信息
        sender = raw_message.get('sender', {})
        sender_name = sender.get('nickname', event.get_sender_name())
        sender_id = sender.get('user_id', event.get_sender_id())

        # 获取群组信息
        group_id = raw_message.get('group_id', '')
        group_name = f"群{group_id}" if group_id else "私聊"

        # 时间处理
        timestamp = raw_message.get('time', 0)
        time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else '未知'

        # 消息类型
        message_type = raw_message.get('message_type', 'unknown')

        # 原始内容
        raw_content = raw_message.get('raw_message', '')

        # 替换模板变量
        prefix = template.format(
            sender_name=sender_name,
            sender_id=sender_id,
            group_name=group_name,
            group_id=group_id,
            time=time_str,
            message_type=message_type,
            raw_content=raw_content
        )

        return prefix

    async def terminate(self):
        """插件卸载时的清理工作"""
        self._save_cache()

        if self.config.get("delete_data_on_uninstall", False):
            try:
                # 删除插件数据目录
                if os.path.exists(self.plugin_data_dir):
                    shutil.rmtree(self.plugin_data_dir)
                    logger.info(f"已删除插件数据目录: {self.plugin_data_dir}")

                # 删除配置文件
                config_file = os.path.join("data", "config", "astrbot_plugin_rawmessage_viewer_config.json")
                if os.path.exists(config_file):
                    os.remove(config_file)
                    logger.info(f"已删除配置文件: {config_file}")

            except Exception as e:
                logger.error(f"删除插件数据失败: {e}")

        logger.info("RawMessage Viewer 插件已卸载")
