# astrbot_plugin_rawmessage_viewer

查看和记录消息平台原始消息的插件，支持查看 napcat 通过 aiocqhttp 传递的原始消息内容

<div align="center">

[![Version](https://img.shields.io/badge/version-v0.0.1-blue.svg)](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer)
[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D3.4.0-green.svg)](https://github.com/Soulter/AstrBot)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

让你能够深入了解消息平台传递的原始数据结构！

</div>

## ✨ 功能特性

- 🔍 **查看原始消息** - 使用指令查看当前消息的原始数据结构
- 📝 **自动插入显示** - 在每条消息前自动插入原始消息内容（可配置）
- 📊 **日志记录** - 在后台记录处理后的完整消息内容
- ⚙️ **灵活配置** - 支持开关自动插入和日志记录功能

## 🎯 使用方法

### 基础指令

| 指令 | 别名 | 说明 | 权限 |
|------|------|------|------|
| `/rawmessage` | `/rawmsg` | 查看当前消息的原始内容 | 所有人 |

### 使用示例

发送指令查看原始消息：
```
/rawmsg
```

自动插入效果示例：
```
[core.event_bus:50]: [aiocqhttp]
<tip>
[aiocqhttp] RawMessage <Event, {'self_id': , 'user_id': , 'time': , 'message_id': , 'message_seq': , 'real_id': , 'real_seq': '', 'message_type': 'group', 'sender': {'user_id': , 'nickname': '', 'card': '', 'role': 'member'}, 'font': 14, 'sub_type': 'normal', 'message': [{'type': 'text', 'data': {'text': ''}}], 'message_format': 'array', 'post_type': 'message', 'group_id': }>
</tip>
你好呀！
```

## ⚙️ 配置说明

插件支持在 AstrBot 管理面板中进行可视化配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_auto_insert` | bool | true | 是否在每条消息前自动插入原始消息内容 |
| `enable_logging` | bool | true | 是否在后台记录插入原始消息后的完整内容 |
| `delete_config_on_uninstall` | bool | false | 卸载插件时是否删除配置文件和数据 |

## 📊 支持的平台

目前主要支持以下平台的原始消息查看：
- ✅ **aiocqhttp** (napcat, lagrange 等)
- 🔄 其他平台（基础支持）

## 💾 数据存储

插件配置保存在：
- 配置文件：`data/config/astrbot_plugin_rawmessage_viewer_config.json`

## 🔧 高级特性

### 原始消息结构
对于 aiocqhttp 平台，原始消息通常包含以下信息：
- `self_id` - 机器人 QQ 号
- `user_id` - 发送者 QQ 号
- `message_id` - 消息 ID
- `message_type` - 消息类型（私聊/群聊）
- `sender` - 发送者信息
- `message` - 消息内容数组
- `group_id` - 群号（群消息时）

### 日志级别
- 插入原始消息使用 `info` 级别日志
- 错误信息使用 `error` 级别日志

## 🐛 故障排除

### 看不到原始消息
1. 检查是否启用了 `enable_auto_insert` 配置
2. 确认使用的是支持的平台（如 aiocqhttp）
3. 查看 AstrBot 日志是否有错误信息

### 消息显示异常
1. 检查原始消息格式是否正常
2. 确认插件版本与 AstrBot 版本兼容
3. 尝试重载插件

## 📝 更新日志

### v0.0.1 (2024-01-20)
- ✅ 实现查看原始消息指令
- ✅ 支持自动插入原始消息到消息前
- ✅ 添加日志记录功能
- ✅ 支持灵活的配置选项
- ✅ 支持卸载时清理数据

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本仓库
2. 创建新的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

- **xSapientia** - *Initial work* - [GitHub](https://github.com/xSapientia)

## 🙏 致谢

- 感谢 [AstrBot](https://github.com/Soulter/AstrBot) 项目提供的优秀框架
- 感谢所有提出建议和反馈的用户

---

<div align="center">

如果这个插件对你有帮助，请给个 ⭐ Star！

[报告问题](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer/issues) · [功能建议](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer/issues) · [查看更多插件](https://github.com/xSapientia)

</div>
