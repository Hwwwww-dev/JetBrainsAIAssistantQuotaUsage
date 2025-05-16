#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""翻译字典模块，用于支持多语言"""

# 翻译字典，使用语义化键
TRANSLATIONS = {
    # 基础信息
    "environment_info": {
        "zh_cn": "环境信息:",
        "en": "Environment Info:"
    },
    "operating_system": {
        "zh_cn": "操作系统:",
        "en": "Operating System:"
    },
    "python_version": {
        "zh_cn": "Python版本:",
        "en": "Python Version:"
    },
    "sqlite_version": {
        "zh_cn": "SQLite版本:",
        "en": "SQLite Version:"
    },
    "file_system_permissions": {
        "zh_cn": "文件系统权限:",
        "en": "File System Permissions:"
    },
    "normal": {
        "zh_cn": "正常",
        "en": "Normal"
    },
    "error_with_msg": {
        "zh_cn": "异常 - {error}",
        "en": "Error - {error}"
    },
    
    # 应用程序锁
    "app_lock_success": {
        "zh_cn": "成功获取应用程序锁 (端口: {port})",
        "en": "Successfully acquired application lock (port: {port})"
    },
    "app_lock_failure": {
        "zh_cn": "无法获取应用程序锁 (端口: {port}): {error}，可能已有实例在运行",
        "en": "Failed to acquire application lock (port: {port}): {error}, another instance may be running"
    },
    "app_lock_released": {
        "zh_cn": "已释放应用程序锁 (端口: {port})",
        "en": "Released application lock (port: {port})"
    },
    
    # 进程相关
    "check_processes": {
        "zh_cn": "检查是否存在残留进程...",
        "en": "Checking for residual processes..."
    },
    "found_processes": {
        "zh_cn": "发现 {count} 个残留进程，正在清理...",
        "en": "Found {count} residual processes, cleaning up..."
    },
    "terminated_process": {
        "zh_cn": "已终止进程 {pid}",
        "en": "Terminated process {pid}"
    },
    "terminate_failed": {
        "zh_cn": "终止进程 {pid} 失败: {error}",
        "en": "Failed to terminate process {pid}: {error}"
    },
    "process_still_running": {
        "zh_cn": "进程 {pid} 仍在运行，尝试强制终止...",
        "en": "Process {pid} is still running, trying to forcefully terminate..."
    },
    "process_cleanup_complete": {
        "zh_cn": "进程清理完成",
        "en": "Process cleanup complete"
    },
    "no_process_found": {
        "zh_cn": "未发现残留进程",
        "en": "No residual processes found"
    },
    "process_check_failed": {
        "zh_cn": "进程检查失败: {error}",
        "en": "Process check failed: {error}"
    },
    
    # 解析错误
    "xml_parse_error": {
        "zh_cn": "解析XML文件时出错: {error}",
        "en": "Error parsing XML file: {error}"
    },
    
    # 配置管理
    "create_config_dir_error": {
        "zh_cn": "无法创建配置目录: {error}",
        "en": "Cannot create config directory: {error}"
    },
    "app_path": {
        "zh_cn": "应用程序路径:",
        "en": "Application Path:"
    },
    "config_dir": {
        "zh_cn": "配置目录:",
        "en": "Config Directory:"
    },
    "config_file": {
        "zh_cn": "配置文件:",
        "en": "Config File:"
    },
    "history_file": {
        "zh_cn": "历史文件:",
        "en": "History File:"
    },
    "app_path_error": {
        "zh_cn": "获取应用程序路径出错: {error}",
        "en": "Error getting application path: {error}"
    },
    "path_not_writable": {
        "zh_cn": "路径 {path} 不可写: {error}",
        "en": "Path {path} not writable: {error}"
    },
    
    # 数据库相关
    "db_connected": {
        "zh_cn": "成功连接到数据库: {path}",
        "en": "Successfully connected to database: {path}"
    },
    "db_connect_failed": {
        "zh_cn": "连接数据库失败: {error}",
        "en": "Failed to connect to database: {error}"
    },
    "use_memory_db": {
        "zh_cn": "使用内存数据库作为备选",
        "en": "Using in-memory database as fallback"
    },
    "memory_db_failed": {
        "zh_cn": "连接内存数据库也失败: {error}",
        "en": "Failed to connect to in-memory database: {error}"
    },
    "db_init_failed": {
        "zh_cn": "无法初始化数据库：连接失败",
        "en": "Cannot initialize database: connection failed"
    },
    "db_init_error": {
        "zh_cn": "初始化数据库失败: {error}",
        "en": "Failed to initialize database: {error}"
    },
    "migrate_from_json": {
        "zh_cn": "从JSON迁移 {count} 条历史记录到SQLite...",
        "en": "Migrating {count} history records from JSON to SQLite..."
    },
    "migration_complete": {
        "zh_cn": "迁移完成",
        "en": "Migration complete"
    },
    "migration_failed": {
        "zh_cn": "迁移数据失败: {error}",
        "en": "Data migration failed: {error}"
    },
    "save_history_failed": {
        "zh_cn": "无法保存历史记录：数据库连接失败",
        "en": "Cannot save history: database connection failed"
    },
    "save_record_failed": {
        "zh_cn": "保存历史记录失败: {error}",
        "en": "Failed to save history record: {error}"
    },
    "load_history_failed": {
        "zh_cn": "无法加载历史记录：数据库连接失败",
        "en": "Cannot load history: database connection failed"
    },
    "load_records_failed": {
        "zh_cn": "加载历史记录失败: {error}",
        "en": "Failed to load history records: {error}"
    },
    "get_paths_failed": {
        "zh_cn": "获取唯一路径失败: {error}",
        "en": "Failed to get unique paths: {error}"
    },
    "no_history_table": {
        "zh_cn": "历史记录表不存在，无需清除",
        "en": "History table does not exist, no need to clear"
    },
    "no_path_history": {
        "zh_cn": "未找到路径 '{path}' 的历史记录",
        "en": "No history records found for path '{path}'"
    },
    "history_empty": {
        "zh_cn": "历史记录已为空",
        "en": "History is already empty"
    },
    "clear_success": {
        "zh_cn": "{message}",
        "en": "{message}"
    },
    "db_closed": {
        "zh_cn": "数据库连接已关闭",
        "en": "Database connection closed"
    },
    "db_close_error": {
        "zh_cn": "关闭数据库连接时出错: {error}",
        "en": "Error closing database connection: {error}"
    },
    
    # 文件相关错误
    "path_not_exist": {
        "zh_cn": "错误: 路径不存在: {path}",
        "en": "Error: Path does not exist: {path}"
    },
    "quota_file_not_found": {
        "zh_cn": "在目录中未找到配额文件: {path}",
        "en": "Quota file not found in directory: {path}"
    },
    "file_not_exist": {
        "zh_cn": "错误: 文件不存在: {path}",
        "en": "Error: File does not exist: {path}"
    },
    "common_paths_hint": {
        "zh_cn": "提示: 常见的配额文件路径包括:",
        "en": "Hint: Common quota file paths include:"
    },
    "analyze_error": {
        "zh_cn": "分析文件时出错: {error}",
        "en": "Error analyzing file: {error}"
    },
    
    # 配额显示相关
    "file_path": {
        "zh_cn": "文件路径:",
        "en": "File path:"
    },
    "quota_info": {
        "zh_cn": "配额信息:",
        "en": "Quota information:"
    },
    "quota_type": {
        "zh_cn": "类型:",
        "en": "Type:"
    },
    "current_usage": {
        "zh_cn": "当前使用:",
        "en": "Current usage:"
    },
    "max_limit": {
        "zh_cn": "最大限制:",
        "en": "Maximum limit:"
    },
    "usage_percentage": {
        "zh_cn": "使用百分比:",
        "en": "Usage percentage:"
    },
    "valid_until": {
        "zh_cn": "有效期至:",
        "en": "Valid until:"
    },
    "refill_info": {
        "zh_cn": "补充信息:",
        "en": "Refill information:"
    },
    "refill_type": {
        "zh_cn": "补充类型:",
        "en": "Refill type:"
    },
    "next_refill": {
        "zh_cn": "下次补充:",
        "en": "Next refill:"
    },
    "refill_amount": {
        "zh_cn": "补充数量:",
        "en": "Refill amount:"
    },
    "refill_period": {
        "zh_cn": "补充周期:",
        "en": "Refill period:"
    },
    "other_info": {
        "zh_cn": "其他信息:",
        "en": "Other information:"
    },
    "timestamp": {
        "zh_cn": "时间戳:",
        "en": "Timestamp:"
    },
    "usage_status": {
        "zh_cn": "使用情况:",
        "en": "Usage status:"
    },
    "press_enter": {
        "zh_cn": "按回车键返回菜单...",
        "en": "Press Enter to return to menu..."
    },
    
    # 历史记录相关
    "no_history": {
        "zh_cn": "没有历史记录",
        "en": "No history records"
    },
    "total_records": {
        "zh_cn": "共显示 {count} 条记录",
        "en": "Displaying {count} records in total"
    },
    "no_quota_file": {
        "zh_cn": "未找到配额文件",
        "en": "No quota file found"
    },
    "found_quota_files": {
        "zh_cn": "找到 {count} 个配额文件:",
        "en": "Found {count} quota files:"
    },
    "auto_analyze": {
        "zh_cn": "自动分析所有文件...",
        "en": "Auto-analyzing all files..."
    },
    "analyzing_file": {
        "zh_cn": "分析文件: {path}",
        "en": "Analyzing file: {path}"
    },
    "invalid_option": {
        "zh_cn": "无效的选项",
        "en": "Invalid option"
    },
    "invalid_input": {
        "zh_cn": "无效的输入",
        "en": "Invalid input"
    },
    
    # 非交互式环境
    "non_interactive_warning": {
        "zh_cn": "警告: 在非交互式环境中运行，无法获取用户输入",
        "en": "Warning: Running in non-interactive environment, cannot get user input"
    },
    "use_command_line": {
        "zh_cn": "请使用命令行参数代替交互式模式，例如:",
        "en": "Please use command line arguments instead of interactive mode, for example:"
    },
    
    # 菜单相关
    "app_title": {
        "zh_cn": "JetBrains AI Assistant 配额分析器 (v1.0.0)",
        "en": "JetBrains AI Assistant Quota Analyzer (v1.0.0)"
    },
    "menu_analyze_file": {
        "zh_cn": "分析单个文件",
        "en": "Analyze single file"
    },
    "menu_auto_find": {
        "zh_cn": "自动查找并分析所有文件",
        "en": "Auto-find and analyze all files"
    },
    "menu_view_history": {
        "zh_cn": "查看历史记录",
        "en": "View history"
    },
    "menu_filter_history": {
        "zh_cn": "按路径筛选历史记录",
        "en": "Filter history by path"
    },
    "menu_common_paths": {
        "zh_cn": "显示常见路径",
        "en": "Show common paths"
    },
    "menu_clear_history": {
        "zh_cn": "清除历史记录 (删除数据)",
        "en": "Clear history (delete data)"
    },
    "menu_help": {
        "zh_cn": "帮助",
        "en": "Help"
    },
    "menu_exit": {
        "zh_cn": "退出",
        "en": "Exit"
    },
    "menu_hint": {
        "zh_cn": "提示: 输入数字选择操作，按Ctrl+C返回上一级",
        "en": "Hint: Enter a number to select an operation, press Ctrl+C to go back"
    },
    
    # 推荐路径相关
    "recommended_paths": {
        "zh_cn": "✨ 推荐的历史路径:",
        "en": "✨ Recommended history paths:"
    },
    "recommended_tag": {
        "zh_cn": "[推荐]",
        "en": "[Recommended]"
    },
    "invalid_recommendation": {
        "zh_cn": "无效的推荐路径编号，请重试",
        "en": "Invalid recommendation number, please try again"
    },
    "file_not_exist_error": {
        "zh_cn": "错误: 文件或目录不存在 - {path}",
        "en": "Error: File or directory does not exist - {path}"
    },
    "retry_prompt": {
        "zh_cn": "是否重试? (y/n, 默认y):",
        "en": "Retry? (y/n, default y):"
    },
    "no_file_path": {
        "zh_cn": "未提供文件路径",
        "en": "No file path provided"
    },
    
    # 清除历史记录相关
    "choose_clear_range": {
        "zh_cn": "请选择要清除的历史记录范围:",
        "en": "Please select the range of history to clear:"
    },
    "clear_all_history": {
        "zh_cn": "清除所有历史记录 (危险: 删除所有数据)",
        "en": "Clear all history (dangerous: delete all data)"
    },
    "clear_by_path": {
        "zh_cn": "按文件路径清除历史记录",
        "en": "Clear history by file path"
    },
    "cancel_return": {
        "zh_cn": "取消并返回",
        "en": "Cancel and return"
    },
    "select_operation": {
        "zh_cn": "选择操作",
        "en": "Select operation"
    },
    "confirm_clear_all": {
        "zh_cn": "确定要删除所有历史记录吗? 此操作不可恢复 (y/n): ",
        "en": "Are you sure you want to delete all history records? This action cannot be undone (y/n): "
    },
    "clear_all_success": {
        "zh_cn": "已成功清除所有历史记录",
        "en": "Successfully cleared all history records"
    },
    "operation_cancelled": {
        "zh_cn": "操作已取消",
        "en": "Operation cancelled"
    },
    "available_paths": {
        "zh_cn": "可用的文件路径",
        "en": "Available file paths"
    },
    "select_path_clear": {
        "zh_cn": "选择要清除历史记录的路径编号 (0表示取消): ",
        "en": "Select the path number to clear history (0 to cancel): "
    },
    "operation_cancelled_simple": {
        "zh_cn": "操作已取消",
        "en": "Operation cancelled"
    },
    "confirm_clear_path": {
        "zh_cn": "确定要删除路径 {path} 的历史记录吗? 此操作不可恢复 (y/n): ",
        "en": "Are you sure you want to delete history records for path {path}? This action cannot be undone (y/n): "
    },
    "clear_path_success": {
        "zh_cn": "已成功清除路径 {path} 的历史记录",
        "en": "Successfully cleared history records for path {path}"
    },
    "invalid_choice": {
        "zh_cn": "无效的选择",
        "en": "Invalid choice"
    },
    
    # 查看历史记录相关
    "recommended_paths_view": {
        "zh_cn": "✨ 推荐的历史路径 (可以直接输入编号进行选择):",
        "en": "✨ Recommended history paths (you can enter the number to select):"
    },
    "enter_record_limit_filter": {
        "zh_cn": "请输入要显示的记录数量，或选择推荐路径的编号 (默认10)",
        "en": "Please enter the number of records to display, or select a recommended path number (default 10)"
    },
    "enter_record_limit": {
        "zh_cn": "请输入要显示的记录数量 (默认10)",
        "en": "Please enter the number of records to display (default 10)"
    },
    
    # 筛选历史记录相关
    "all_available_paths": {
        "zh_cn": "所有可用的文件路径",
        "en": "All available file paths"
    },
    "only_one_path": {
        "zh_cn": "只有一个路径可选: {path}",
        "en": "Only one path available: {path}"
    },
    "select_path_number": {
        "zh_cn": "请选择文件路径编号",
        "en": "Please select a file path number"
    },
    "select_path_hint": {
        "zh_cn": " (或使用R1-R{count}选择推荐路径)",
        "en": " (or use R1-R{count} to select a recommended path)"
    },
    "select_path_return": {
        "zh_cn": " (输入0返回): ",
        "en": " (enter 0 to return): "
    },
    
    # 常见路径相关
    "common_paths_title": {
        "zh_cn": "常见配额文件路径:",
        "en": "Common quota file paths:"
    },
    "idea_paths": {
        "zh_cn": "IntelliJ IDEA:",
        "en": "IntelliJ IDEA:"
    },
    "pycharm_paths": {
        "zh_cn": "PyCharm:",
        "en": "PyCharm:"
    },
    "webstorm_paths": {
        "zh_cn": "WebStorm:",
        "en": "WebStorm:"
    },
    "paths_tip": {
        "zh_cn": "提示: 将 <版本> 替换为您的IDE版本号 (例如: 2023.1)",
        "en": "Tip: Replace <version> with your IDE version number (e.g., 2023.1)"
    },
    
    # 帮助相关
    "help_title": {
        "zh_cn": "帮助信息",
        "en": "Help Information"
    },
    "usage_tip": {
        "zh_cn": "使用说明:",
        "en": "Usage Instructions:"
    },
    "application_description": {
        "zh_cn": "本应用程序用于分析JetBrains AI Assistant配额使用情况",
        "en": "This application is used to analyze JetBrains AI Assistant quota usage"
    },
    "key_features": {
        "zh_cn": "主要功能:",
        "en": "Key Features:"
    },
    "feature_analyze": {
        "zh_cn": "分析单个配额文件",
        "en": "Analyze a single quota file"
    },
    "feature_auto": {
        "zh_cn": "自动查找并分析所有IDE的配额文件",
        "en": "Automatically find and analyze quota files for all IDEs"
    },
    "feature_history": {
        "zh_cn": "查看和筛选历史记录",
        "en": "View and filter history records"
    },
    "feature_clear": {
        "zh_cn": "清除历史记录",
        "en": "Clear history records"
    },
    "command_line_usage": {
        "zh_cn": "命令行使用方式:",
        "en": "Command Line Usage:"
    },
    "interactive_mode": {
        "zh_cn": "交互式模式:",
        "en": "Interactive Mode:"
    },
    "analyze_example": {
        "zh_cn": "分析指定文件:",
        "en": "Analyze Specified File:"
    },
    "auto_find_example": {
        "zh_cn": "自动查找所有配额文件:",
        "en": "Auto-find All Quota Files:"
    },
    "view_history_example": {
        "zh_cn": "查看历史记录:",
        "en": "View History:"
    },
    "filter_history_example": {
        "zh_cn": "按路径筛选历史记录:",
        "en": "Filter History by Path:"
    },
    "common_paths_example": {
        "zh_cn": "查看常见路径:",
        "en": "View Common Paths:"
    },
    "other_help": {
        "zh_cn": "更多帮助信息，请使用 --help 参数",
        "en": "For more help information, use the --help parameter"
    },
    "language_settings": {
        "zh_cn": "语言设置 (--lang):",
        "en": "Language Settings (--lang):"
    },
    "supported_languages_info": {
        "zh_cn": "支持的语言: {languages}",
        "en": "Supported languages: {languages}"
    },
    
    # 进程检查相关
    "checking_processes": {
        "zh_cn": "检查是否存在残留进程...",
        "en": "Checking for residual processes..."
    },
    "found_processes_info": {
        "zh_cn": "发现残留进程:",
        "en": "Found residual processes:"
    },
    "no_processes_found": {
        "zh_cn": "未发现残留进程",
        "en": "No residual processes found"
    },
    "process_check_error": {
        "zh_cn": "进程检查失败: {error}",
        "en": "Process check failed: {error}"
    },
    "unsupported_os": {
        "zh_cn": "不支持的操作系统: {os}",
        "en": "Unsupported operating system: {os}"
    },
    
    # 其他
    "app_description": {
        "zh_cn": "JetBrains AI Assistant 配额分析器",
        "en": "JetBrains AI Assistant Quota Analyzer"
    },
    "operation_cancelled": {
        "zh_cn": "操作已取消",
        "en": "Operation cancelled"
    },
    "eof_interrupt": {
        "zh_cn": "检测到EOF，可能在非交互式环境中运行",
        "en": "EOF detected, possibly running in a non-interactive environment"
    },
    "unexpected_error": {
        "zh_cn": "发生意外错误: {error}",
        "en": "Unexpected error occurred: {error}"
    },
    "examples": {
        "zh_cn": "示例",
        "en": "Examples"
    },
    
    # 文件分析相关的翻译键
    "auto_analyzing_all_files": {
        "zh_cn": "自动分析所有文件...",
        "en": "Auto-analyzing all files..."
    },
    "analysis_success_count": {
        "zh_cn": "成功分析了 {count} 个配额文件",
        "en": "Successfully analyzed {count} quota files"
    },
    "select_file_to_analyze": {
        "zh_cn": "请选择要分析的文件编号 (输入 'a' 分析所有, 'q' 返回)",
        "en": "Please select a file number to analyze (enter 'a' to analyze all, 'q' to return)"
    },
    "invalid_option_simple": {
        "zh_cn": "无效的选项",
        "en": "Invalid option"
    },
    "invalid_input_simple": {
        "zh_cn": "无效的输入",
        "en": "Invalid input"
    },

    # 进程检查相关的翻译键
    "checking_processes_simple": {
        "zh_cn": "检查是否存在残留进程...",
        "en": "Checking for residual processes..."
    },
    "found_processes_simple": {
        "zh_cn": "发现残留进程:",
        "en": "Found residual processes:"
    },
    "no_processes_found_simple": {
        "zh_cn": "未发现残留进程",
        "en": "No residual processes found"
    },
    "process_check_error_simple": {
        "zh_cn": "进程检查失败: {error}",
        "en": "Process check failed: {error}"
    },
    "unsupported_os_simple": {
        "zh_cn": "不支持的操作系统: {os}",
        "en": "Unsupported operating system: {os}"
    },

    # 环境信息相关的翻译键
    "environment_info_detailed": {
        "zh_cn": "环境信息:",
        "en": "Environment Information:"
    },
    "os_info_detailed": {
        "zh_cn": "操作系统: {os} {release} ({version})",
        "en": "Operating System: {os} {release} ({version})"
    },
    "python_version_detailed": {
        "zh_cn": "Python 版本: {version}",
        "en": "Python Version: {version}"
    },
    "sqlite_version_detailed": {
        "zh_cn": "SQLite 版本: {version}",
        "en": "SQLite Version: {version}"
    },
    "app_path_detailed": {
        "zh_cn": "应用程序路径: {path}",
        "en": "Application Path: {path}"
    },
    "working_dir_detailed": {
        "zh_cn": "当前工作目录: {path}",
        "en": "Current Working Directory: {path}"
    },
    "home_dir_detailed": {
        "zh_cn": "用户主目录: {path}",
        "en": "User Home Directory: {path}"
    },
    "temp_dir_detailed": {
        "zh_cn": "临时目录: {path}",
        "en": "Temporary Directory: {path}"
    },
    "path_var_detailed": {
        "zh_cn": "PATH 环境变量: {path}",
        "en": "PATH Environment Variable: {path}"
    },
    "env_var_error": {
        "zh_cn": "获取环境变量时出错: {error}",
        "en": "Error getting environment variables: {error}"
    },

    # 错误信息相关的翻译键
    "clear_history_db_error": {
        "zh_cn": "清除历史记录失败：仍有 {count} 条记录未删除",
        "en": "Failed to clear history: {count} records still remain"
    },
    "clear_history_error": {
        "zh_cn": "清除历史记录时出错: {error}",
        "en": "Error clearing history: {error}"
    },
    "clear_all_success_count": {
        "zh_cn": "已成功清除所有 {count} 条历史记录",
        "en": "Successfully cleared all {count} history records"
    },
    "unexpected_error": {
        "zh_cn": "发生意外错误: {error}",
        "en": "Unexpected error occurred: {error}"
    },

    # 其他交互式提示相关的翻译键
    "continue_prompt": {
        "zh_cn": "是否继续? (y/n):",
        "en": "Continue? (y/n):"
    },
    "welcome": {
        "zh_cn": "欢迎使用 JetBrains AI Assistant 配额分析器!",
        "en": "Welcome to JetBrains AI Assistant Quota Analyzer!"
    },
    "interactive_warning": {
        "zh_cn": "警告: 在非交互式环境中运行",
        "en": "Warning: Running in a non-interactive environment"
    },
    "interactive_error": {
        "zh_cn": "错误: 需要交互式终端支持, 无法获取用户输入",
        "en": "Error: Interactive terminal support required, cannot get user input"
    },
    "thank_you": {
        "zh_cn": "感谢使用 JetBrains AI Assistant 配额分析器!",
        "en": "Thank you for using JetBrains AI Assistant Quota Analyzer!"
    },
    "invalid_option_retry_dot": {
        "zh_cn": "无效的选项，请重试。",
        "en": "Invalid option, please try again."
    },
    "version_placeholder": {
        "zh_cn": "<版本>",
        "en": "<version>"
    },
    "product_placeholder": {
        "zh_cn": "<产品>",
        "en": "<product>"
    },

    # 路径显示相关的翻译键
    "app_lock_failure_simple": {
        "zh_cn": "无法获取应用程序锁 (端口: {port})",
        "en": "Failed to acquire application lock (port: {port})"
    },
    "jetbrains_dir_not_found": {
        "zh_cn": "未找到JetBrains目录: {path}",
        "en": "JetBrains directory not found: {path}"
    },
    "find_quota_files_error": {
        "zh_cn": "查找配额文件时出错: {error}",
        "en": "Error finding quota files: {error}"
    },
    "enter_file_path_or_select": {
        "zh_cn": "请输入文件路径或选择推荐路径",
        "en": "Please enter file path or select a recommended path"
    },
    
    # 帮助相关
    "help_title": {
        "zh_cn": "帮助信息",
        "en": "Help Information"
    },
    "usage_tip": {
        "zh_cn": "使用说明:",
        "en": "Usage Instructions:"
    },
    "application_description": {
        "zh_cn": "本应用程序用于分析JetBrains AI Assistant配额使用情况",
        "en": "This application is used to analyze JetBrains AI Assistant quota usage"
    },
    "key_features": {
        "zh_cn": "主要功能:",
        "en": "Key Features:"
    },
    "feature_analyze": {
        "zh_cn": "分析单个配额文件",
        "en": "Analyze a single quota file"
    },
    "feature_auto": {
        "zh_cn": "自动查找并分析所有IDE的配额文件",
        "en": "Automatically find and analyze quota files for all IDEs"
    },
    "feature_history": {
        "zh_cn": "查看和筛选历史记录",
        "en": "View and filter history records"
    },
    "feature_clear": {
        "zh_cn": "清除历史记录",
        "en": "Clear history records"
    },
    "command_line_usage": {
        "zh_cn": "命令行使用方式:",
        "en": "Command Line Usage:"
    },
    "interactive_mode": {
        "zh_cn": "交互式模式:",
        "en": "Interactive Mode:"
    },
    "analyze_example": {
        "zh_cn": "分析指定文件:",
        "en": "Analyze Specified File:"
    },
    "auto_find_example": {
        "zh_cn": "自动查找所有配额文件:",
        "en": "Auto-find All Quota Files:"
    },
    "view_history_example": {
        "zh_cn": "查看历史记录:",
        "en": "View History:"
    },
    "filter_history_example": {
        "zh_cn": "按路径筛选历史记录:",
        "en": "Filter History by Path:"
    },
    "common_paths_example": {
        "zh_cn": "查看常见路径:",
        "en": "View Common Paths:"
    },
    "other_help": {
        "zh_cn": "更多帮助信息，请使用 --help 参数",
        "en": "For more help information, use the --help parameter"
    },
    "language_settings": {
        "zh_cn": "语言设置 (--lang):",
        "en": "Language Settings (--lang):"
    },
    "supported_languages_info": {
        "zh_cn": "支持的语言: {languages}",
        "en": "Supported languages: {languages}"
    },
    
    # 进程检查相关
    "checking_processes": {
        "zh_cn": "检查是否存在残留进程...",
        "en": "Checking for residual processes..."
    },
    "found_processes_info": {
        "zh_cn": "发现残留进程:",
        "en": "Found residual processes:"
    },
    "no_processes_found": {
        "zh_cn": "未发现残留进程",
        "en": "No residual processes found"
    },
    "process_check_error": {
        "zh_cn": "进程检查失败: {error}",
        "en": "Process check failed: {error}"
    },
    "unsupported_os": {
        "zh_cn": "不支持的操作系统: {os}",
        "en": "Unsupported operating system: {os}"
    },
    
    # 其他
    "app_description": {
        "zh_cn": "JetBrains AI Assistant 配额分析器",
        "en": "JetBrains AI Assistant Quota Analyzer"
    },
    "operation_cancelled": {
        "zh_cn": "操作已取消",
        "en": "Operation cancelled"
    },
    "eof_interrupt": {
        "zh_cn": "检测到EOF，可能在非交互式环境中运行",
        "en": "EOF detected, possibly running in a non-interactive environment"
    },
    "unexpected_error": {
        "zh_cn": "发生意外错误: {error}",
        "en": "Unexpected error occurred: {error}"
    },
    "examples": {
        "zh_cn": "示例",
        "en": "Examples"
    },
    "username": {
        "zh_cn": "用户名",
        "en": "Username"
    },
    "etc": {
        "zh_cn": "等等...",
        "en": "etc..."
    },
    "column_num": {
        "zh_cn": "编号",
        "en": "Number"
    },
    "column_time": {
        "zh_cn": "时间",
        "en": "Time"
    },
    "column_type": {
        "zh_cn": "类型",
        "en": "Type"
    },
    "column_usage": {
        "zh_cn": "使用率",
        "en": "Usage"
    },
    "column_current_max": {
        "zh_cn": "当前/最大",
        "en": "Current/Max"
    },
    "column_filepath": {
        "zh_cn": "文件路径",
        "en": "File Path"
    },
    # 语言选项
    "set_language_option": {
        "zh_cn": "设置界面语言 (支持: {languages})",
        "en": "Set interface language (supported: {languages})"
    },
    
    # 版本信息
    "version_info": {
        "zh_cn": "JetBrains AI Assistant配额分析器 v{version}",
        "en": "JetBrains AI Assistant Quota Analyzer v{version}"
    }
}

def get_translations():
    """返回翻译字典"""
    return TRANSLATIONS