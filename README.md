## chat2db

**Author:** slp
**Version:** 0.0.3
**Type:** tool


## 项目描述

chat2db 是一个智能的文本到SQL转换工具，它利用自然语言处理技术，使用户能够通过直观的文本查询方式，快速、准确地从关系数据库中检索所需信息。该工具显著降低了数据库查询的门槛，提升了数据访问的效率和便捷性。

## 主要特性

- 自然语言转SQL：支持将自然语言查询转换为准确的SQL语句
- 多模型支持：支持多种LLM模型，包括OpenAI、通义和智谱等
- 数据库兼容：支持MySQL等主流关系型数据库
- 灵活配置：提供丰富的配置选项，包括数据库连接、模型选择等
- 错误处理：完善的错误处理机制，提供清晰的错误提示

## 准备

1. 安装 Dify 插件开发脚手架工具
   访问 Dify Plugin CLI 项目地址，下载并安装最新版本号和对应操作系统的工具。
   本文以装载 M 系列芯片的 macOS 为例。下载 dify-plugin-darwin-arm64 文件后，赋予其执行权限。
   ```bash
   chmod +x dify-plugin-darwin-arm64
   ```
   运行以下命令检查安装是否成功。
   ```bash
      ./dify-plugin-darwin-arm64 version
   ```
   运行成功后，将显示当前安装的 Dify 插件开发脚手架工具的版本号。

## 安装说明

1. 克隆项目到本地：
```bash
git clone [repository_url]
cd text2sql
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 调试项目
前往“插件管理”页获取远程服务器地址和调试 Key。
![前往“插件管理”页，点击“获取远程服务器地址和调试 Key”按钮。](https://docs.dify.ai/~gitbook/image?url=https%3A%2F%2Fassets-docs.dify.ai%2F2024%2F12%2F053415ef127f1f4d6dd85dd3ae79626a.png&width=768&dpr=4&quality=100&sign=1c835148&sv=2)
回到插件项目，拷贝 .env.example 文件并重命名为 .env，将获取的远程服务器地址和调试 Key 等信息填入其中。
.env 文件：
    ```bash
    INSTALL_METHOD=remote
    REMOTE_INSTALL_HOST=localhost
    REMOTE_INSTALL_PORT=5003
    REMOTE_INSTALL_KEY=****-****-****-****-****
    ```
    运行 python -m main 命令启动插件。在插件页即可看到该插件已被安装至 Workspace 内，团队中的其他成员也可以访问该插件。
    ![团队中的其他成员也可以访问该插件](https://docs.dify.ai/~gitbook/image?url=https%3A%2F%2Fassets-docs.dify.ai%2F2024%2F12%2Fec26e5afc57bbfeb807719638f603807.png&width=768&dpr=1&quality=100&sign=573525e7&sv=2)

4. 打包发布
   运行以下插件打包命令：
   ```bash
   dify plugin package ./your_plugin_project
   ```
   运行命令后将在当前路径下生成以 .difypkg 后缀结尾的文件。

## 使用方法

1. 配置数据库连接信息：
   - 数据库主机地址
   - 端口号
   - 用户名
   - 密码
   - 数据库名称

2. 配置模型参数：
   - 选择模型类型（openai/tongyi/zhipu）
   - 配置模型名称（可选）
   - 设置模型参数

3. 发送查询：
   - 使用自然语言描述您的查询需求
   - 系统将自动转换为SQL并执行查询
   - 返回查询结果



## 错误处理

工具提供了两种主要的异常类型：

- ConfigurationError：配置相关错误
- DatabaseError：数据库操作错误

系统会提供清晰的错误信息，帮助快速定位和解决问题。


## 贡献指南

欢迎提交问题报告和改进建议。如果您想贡献代码，请：

1. Fork 项目
2. 创建您的特性分支
3. 提交您的改动
4. 确保代码符合项目规范
5. 提交 Pull Request

## 许可证

[待补充]



