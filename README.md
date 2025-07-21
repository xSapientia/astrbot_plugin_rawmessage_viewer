# astrbot_plugin_rawmessage_viewer

查看和展示 aiocqhttp 原始消息的插件，支持查看 RawMessage 内容并在 LLM 请求前添加到 Prompt

<div align="center">

[![Version](https://img.shields.io/badge/version-v0.0.1-blue.svg)](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer)
[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D3.4.0-green.svg)](https://github.com/Soulter/AstrBot)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

专门为开发者设计的调试工具插件，帮助查看和分析 QQ 消息的原始数据！

</div>

## ✨ 功能特性

- 🔍 **查看原始消息** - 实时查看 napcat 传递的 RawMessage 内容
- 📝 **LLM 前缀注入** - 自动在 LLM 请求前添加消息元数据
- 📊 **消息历史记录** - 缓存最近的原始消息供后续查看
- 🛠️ **函数调用支持** - 提供 get_raw_message 函数供 Bot 调用
- ⚙️ **高度可配置** - 支持自定义前缀格式和显示选项

## 🎯 使用方法

### 基础指令

| 指令 | 别名 | 说明 | 权限 |
|------|------|------|------|
| `/rawmsg` | `查看原始消息`, `viewraw` | 查看当前消息的原始内容 | 所有人 |
| `/rawhistory` | `原始消息历史` | 查看最近10条原始消息 | 所有人 |

### 函数调用

Bot 可以通过函数调用获取原始消息：
```
函数名: get_raw_message
参数: message_id (可选) - 消息ID，不填则获取当前消息
```

## ⚙️ 配置说明

插件支持在 AstrBot 管理面板中进行可视化配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_plugin` | bool | true | 插件总开关 |
| `enable_llm_prefix` | bool | true | 是否在 LLM 请求前添加原始消息信息 |
| `prefix_format` | text | 见下方 | LLM Prefix 格式模板 |
| `show_raw_json` | bool | false | 查看时是否显示完整 JSON |
| `max_prefix_length` | int | 500 | Prefix 最大长度限制 |
| `delete_data_on_uninstall` | bool | false | 卸载时是否删除数据 |

### 默认 Prefix 格式模板

```
【消息元数据】
发送者: {sender_name} ({sender_id})
群组: {group_name} ({group_id})
时间: {time}
消息类型: {message_type}
原始内容: {raw_content}
---
```

支持的变量：
- `{sender_name}` - 发送者昵称
- `{sender_id}` - 发送者 QQ 号
- `{group_name}` - 群名称
- `{group_id}` - 群号
- `{time}` - 消息时间
- `{message_type}` - 消息类型
- `{raw_content}` - 原始消息内容

## 📊 原始消息信息说明

插件可以展示的原始消息信息包括：

### 基本信息
- 消息 ID
- 消息类型（private/group）
- 时间戳

### 发送者信息
- QQ 号
- 昵称
- 群名片
- 性别
- 年龄
- 头衔
- 等级

### 消息内容
- 原始文本
- 消息段详情（文本、图片、@、回复等）

## 💾 数据存储

插件数据保存在以下位置：
- 消息缓存：`data/plugin_data/astrbot_plugin_rawmessage_viewer/message_cache.json`
- 插件配置：`data/config/astrbot_plugin_rawmessage_viewer_config.json`

## 🔧 高级用法

### 1. 调试消息结构
开发者可以通过查看原始消息了解 QQ 消息的完整结构，方便开发其他插件。

### 2. 增强 LLM 理解
通过在 LLM 请求前注入消息元数据，可以让 AI 更好地理解上下文，如：
- 识别用户身份
- 了解群组环境
- 获取时间信息

### 3. 消息分析
通过历史记录功能，可以分析消息模式和用户行为。

## 🐛 故障排除

### 插件无响应
1. 检查插件是否已启用
2. 确认使用的是 aiocqhttp 平台（QQ）
3. 查看 AstrBot 日志是否有错误信息

### 看不到原始消息
1. 确认消息来自 QQ 平台
2. 检查 `show_raw_json` 配置
3. 尝试使用 `/rawhistory` 查看历史

### LLM 前缀未生效
1. 检查 `enable_llm_prefix` 配置
2. 确认已配置大语言模型
3. 查看前缀长度是否超过限制

## 📝 更新日志

### v0.0.1 (2024-12-26)
- ✅ 实现查看原始消息功能
- ✅ 添加 LLM 前缀注入
- ✅ 实现消息历史缓存
- ✅ 添加函数调用支持
- ✅ 完善配置系统
- ✅ 优化数据清理机制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发计划

- [ ] 支持更多平台的原始消息查看
- [ ] 添加消息过滤和搜索功能
- [ ] 实现消息统计分析
- [ ] 支持导出消息数据

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

- **xSapientia** - *Initial work* - [GitHub](https://github.com/xSapientia)

## 🙏 致谢

- 感谢 [AstrBot](https://github.com/Soulter/AstrBot) 项目提供的优秀框架
- 感谢 [NapCat](https://github.com/NapNeko/NapCatQQ) 提供的 QQ 协议支持

---

<div align="center">

如果这个插件对你有帮助，请给个 ⭐ Star！

[报告问题](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer/issues) · [功能建议](https://github.com/xSapientia/astrbot_plugin_rawmessage_viewer/issues) · [查看更多插件](https://github.com/xSapientia)

</div>
