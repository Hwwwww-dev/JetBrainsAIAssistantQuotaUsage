# JetBrains AI Assistant 配额使用查看器

本项目帮助您查看 JetBrains AI Assistant 的配额使用情况。它提供了手动方法和脚本，方便您查看当前的配额状态。

## 免责声明

**本项目仅供交流学习使用。**

- 本工具与JetBrains公司没有官方关联，也未获得JetBrains的认可。
- 使用本工具时，用户必须遵守JetBrains的服务条款和使用政策。
- 请勿将本项目用于任何商业目的，或以违反适用法律法规的方式使用。
- 作者不对本工具的任何滥用或因使用本工具而产生的任何后果负责。
- 使用本项目风险自负。作者不对所提供信息的准确性或可靠性做任何保证。
- 本工具旨在帮助用户了解其配额使用情况，而非规避任何限制或约束。

## 手动方法

### 方法一：查看账户用量

您可以通过查看 `AIAssistantQuotaManager2.xml` 文件直接检查 AI Assistant 的配额使用情况。

#### 各操作系统的文件位置：

- **Windows**: `%APPDATA%\JetBrains\<IDE>\options\AIAssistantQuotaManager2.xml`
- **macOS**: `~/Library/Application Support/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`
- **Linux**: `~/.config/JetBrains/<IDE>/options/AIAssistantQuotaManager2.xml`

其中 `<IDE>` 是您特定的 JetBrains IDE（例如：IntelliJ IDEA 2025.1, WebStorm 2025.1 等）

### 方法二：查看刷新日志

您还可以通过在 IDE 日志文件中搜索关键字 "QuotaManager2" 来查看配额刷新日志。

#### 各操作系统的日志文件位置：

- **Windows**: `%APPDATA%\JetBrains\<IDE>\system\log\idea.log`
- **macOS**: `~/Library/Logs/JetBrains/<IDE>/idea.log`
- **Linux**: `~/.cache/JetBrains/<IDE>/log/idea.log`

## 使用脚本

本项目为Unix/Linux/macOS（bash）和Windows（cmd）提供了脚本，帮助您查看配额信息：

### 1. 查看当前配额使用情况

#### Unix/Linux/macOS系统：
```bash
./scripts/check_quota.sh <IDE基础路径>
```

#### Windows系统：
```cmd
scripts\check_quota.cmd <IDE基础路径>
```

示例：
```bash
./scripts/check_quota.sh /path/to/your/JetBrains/IDE
```

**注意**：请提供 JetBrains IDE 安装的基础路径。例如，如果您的配额文件位于 `/path/to/IDE/config/options/AIAssistantQuotaManager2.xml`，则提供 `/path/to/IDE` 作为参数。

### 2. 查看配额刷新日志

#### Unix/Linux/macOS系统：
```bash
./scripts/check_quota_logs.sh <IDE基础路径>
```

#### Windows系统：
```cmd
scripts\check_quota_logs.cmd <IDE基础路径>
```

示例：
```bash
./scripts/check_quota_logs.sh /path/to/your/JetBrains/IDE
```

**注意**：脚本期望以下结构：
- 配额文件位于：`<IDE基础路径>/config/options/AIAssistantQuotaManager2.xml`
- 日志文件位于：`<IDE基础路径>/system/log/idea.log`

## 输出示例

当您运行配额检查脚本时，您将看到类似以下的输出：

```
Analyzing AI Assistant quota usage from: /path/to/JetBrains/IDE/config/options/AIAssistantQuotaManager2.xml
------------------------------------------------------
Current Quota Status:
---------------------
Quota Status: Available
Current Usage: 1000000.0000 tokens
Maximum Quota: 2000000 tokens
Valid Until: 2026-06-01T00:00:00Z
Percentage Used: 50.00%

Next Quota Refill:
-----------------
Refill Type: Known
Next Refill Date: 2025-06-01T00:00:00.000Z
Refill Amount: 2000000 tokens
Refill Duration: PT720H
------------------------------------------------------
Note: This information is based on the local cache and may not reflect real-time usage.
```

## 理解输出内容

配额信息包括：
- **配额状态**：您的配额当前状态（可用、已用尽等）
- **当前使用量**：您当前已经使用的配额（以token为单位）
- **最大配额**：您的最大配额限制（以token为单位）
- **有效期至**：您当前配额的到期日期
- **使用百分比**：已使用的配额百分比
- **下次刷新日期**：配额将在何时刷新
- **刷新数量**：刷新时将添加多少token
- **刷新持续时间**：刷新的配额将持续多长时间

日志信息显示：
- 配额更新请求的时间
- 新的配额状态
- 刷新计划

## 要求

- Bash shell（适用于Unix/Linux/macOS）或命令提示符（适用于Windows）
- xmllint（用于bash脚本中的XML解析）
- grep（用于bash脚本中的日志搜索）
- PowerShell（用于Windows脚本中的HTML实体解码）

## 注意事项

- **Windows脚本**：Windows命令脚本（.cmd）尚未经过广泛测试。如果您在使用过程中遇到任何问题，请报告。

## 致谢

本项目在[Windsurf](http://windsurf.com)的协助下开发完成。
