# astrbot_plugin_raw_message_viewer

查看和展示aiocqhttp平台原始消息内容的调试插件

<div align="center">

[![Version](https://img.shields.io/badge/version-v0.0.1-blue.svg)](https://github.com/xSapientia/astrbot_plugin_raw_message_viewer)
[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D3.4.0-green.svg)](https://github.com/Soulter/AstrBot)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

一个专为开发者设计的调试插件，帮助查看和分析 aiocqhttp 平台的原始消息内容！

</div>

## ✨ 功能特性

- 🔍 **查看原始消息**: 通过 LLM 函数调用查看最近一条消息的原始内容
- 📝 **自动插入提示**: 在每次 LLM 请求前自动插入原始消息内容
- 💾 **历史记录**: 自动保存最近 100 条消息的原始内容
- ⚙️ **灵活配置**: 支持开关功能、设置最大显示长度等

## 🎯 使用方法

### LLM 函数调用

当启用函数调用功能后，可以通过以下方式查看原始消息：

```
用户: 帮我查看一下原始消息内容
Bot: [调用 view_raw_message 函数]
```

### 自动插入原始消息

启用 `show_raw_message` 配置后，每次消息都会自动在 LLM 请求前插入原始内容：

```
<tip>
[aiocqhttp] RawMessage <Event, {'self_id': 1833235930, 'user_id': 2756189032, ...}>
</tip>
```

## ⚙️ 配置说明

插件支持在 AstrBot 管理面板中进行可视化配置：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_plugin` | bool | true | 插件总开关 |
| `show_raw_message` | bool | true | 是否在消息前显示原始内容 |
| `delete_data_on_uninstall` | bool | false | 卸载时是否删除插件数据 |
| `max_message_length` | int | 1000 | 原始消息最大显示长度（0表示不限制） |

## 💾 数据存储

插件数据保存在以下位置：
- 消息历史：`data/plugin_data/astrbot_plugin_raw_message_viewer/message_history.json`
- 插件配置：`data/config/astrbot_plugin_raw_message_viewer_config.json`

## 🔧 高级特性

### 消息历史记录
- 自动保存最近 100 条消息的原始内容
- 包含时间戳、发送者信息、消息类型等
- JSON 格式存储，方便查看和分析

### 平台兼容性
- 目前仅支持 aiocqhttp 平台（NapCat、Lagrange 等）
- 其他平台会自动忽略，不影响正常使用

## 🐛 故障排除

### 插件无响应
1. 检查插件是否已启用
2. 确认是否在 aiocqhttp 平台下使用
3. 查看 AstrBot 日志是否有错误信息

### 消息显示不完整
- 检查 `max_message_length` 配置
- 设置为 0 可显示完整消息

### 数据文件过大
- 插件自动只保留最近 100 条记录
- 可手动清理 `message_history.json` 文件

## 📝 更新日志

### v0.0.1 (2024-01-21)
- ✅ 实现查看原始消息的 LLM 函数
- ✅ 实现自动插入原始消息内容
- ✅ 添加消息历史记录功能
- ✅ 支持灵活的配置选项

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
- 感谢所有使用 aiocqhttp 平台的开发者

---

<div align="center">

如果这个插件对你有帮助，请给个 ⭐ Star！

[报告问题](https://github.com/xSapientia/astrbot_plugin_raw_message_viewer/issues) · [功能建议](https://github.com/xSapientia/astrbot_plugin_raw_message_viewer/issues) · [查看更多插件](https://github.com/xSapientia)

</div>
