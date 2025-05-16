#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JetBrains AI Assistant Quota Analyzer (CLI Version)
--------------------------------------------------
一个用于查看和分析JetBrains AI Assistant配额使用情况的命令行工具。
"""

import argparse
import json
import os
import platform
import socket
import sqlite3
import subprocess
import sys
import traceback
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

from translations import get_translations

# 语言设置
DEFAULT_LANGUAGE = "zh_cn"  # 默认使用中文
SUPPORTED_LANGUAGES = ["zh_cn", "en"]  # 支持的语言列表
current_language = DEFAULT_LANGUAGE

# 导入颜色支持
try:
    from colorama import init, Fore, Back, Style

    colorama_initialized = False


    def init_colorama():
        global colorama_initialized
        if not colorama_initialized:
            init(autoreset=True, strip=False)  # 确保颜色代码被正确处理
            colorama_initialized = True


    # 立即初始化 colorama
    init_colorama()


    # 定义颜色常量
    class Colors:
        HEADER = Fore.CYAN + Style.BRIGHT
        INFO = Fore.BLUE + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        ERROR = Fore.RED + Style.BRIGHT
        RESET = Style.RESET_ALL

        # 进度条颜色
        PROGRESS_LOW = Fore.GREEN
        PROGRESS_MEDIUM = Fore.YELLOW
        PROGRESS_HIGH = Fore.RED

        # 菜单颜色
        MENU_TITLE = Fore.CYAN + Style.BRIGHT
        MENU_ITEM = Fore.WHITE + Style.BRIGHT
        MENU_PROMPT = Fore.YELLOW + Style.BRIGHT

        # 其他样式
        BG_BLACK = Back.BLACK
        DIM = Style.DIM
        BOLD = Style.BRIGHT

        # 表格样式
        TABLE_HEADER = Fore.CYAN + Style.BRIGHT + Back.BLUE
        TABLE_ROW_ODD = Back.BLACK  # 奇数行使用黑色背景
        TABLE_ROW_EVEN = Back.BLUE + Style.DIM  # 偶数行使用暗蓝色背景
except ImportError:
    # 如果colorama不可用，使用空字符串作为替代
    class Colors:
        HEADER = INFO = SUCCESS = WARNING = ERROR = ""
        RESET = ""
        PROGRESS_LOW = PROGRESS_MEDIUM = PROGRESS_HIGH = ""
        MENU_TITLE = MENU_ITEM = MENU_PROMPT = ""
        BG_BLACK = ""
        DIM = ""
        BOLD = ""
        TABLE_HEADER = ""
        TABLE_ROW_ODD = ""
        TABLE_ROW_EVEN = ""

# 版本信息
VERSION = "1.0.0"

# 全局变量
LOCK_PORT = 12345  # 用于确保只有一个实例运行的端口

# 翻译字典，使用语义化键
TRANSLATIONS = get_translations()


def set_language(language: str):
    """设置当前语言"""
    global current_language
    if language in SUPPORTED_LANGUAGES:
        current_language = language
    else:
        current_language = DEFAULT_LANGUAGE


def get_language() -> str:
    """获取当前语言设置"""
    return current_language


def t(key: str, default: Optional[str] = None) -> str:
    """
    翻译函数：根据键获取当前语言的翻译文本
    
    Args:
        key: 翻译键
        default: 如果未找到翻译，返回的默认值
        
    Returns:
        翻译后的文本
    """
    if key in TRANSLATIONS and current_language in TRANSLATIONS[key]:
        return TRANSLATIONS[key][current_language]
    return default or key


def print_diagnostic_info():
    """打印诊断信息"""
    print(f"{Colors.HEADER}{t('environment_info')}{Colors.RESET}")
    print(f"{Colors.INFO}{t('operating_system')} {Colors.RESET}{platform.system()} {platform.release()}{Colors.RESET}")
    print(f"{Colors.INFO}{t('python_version')} {Colors.RESET}{platform.python_version()}{Colors.RESET}")
    print(f"{Colors.INFO}{t('sqlite_version')} {Colors.RESET}{sqlite3.sqlite_version}{Colors.RESET}")

    # 检查文件系统权限
    try:
        test_dir = os.path.join(os.path.expanduser("~"), ".test_jetbrains_quota")
        os.makedirs(test_dir, exist_ok=True)
        test_file = os.path.join(test_dir, "test_write.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        os.rmdir(test_dir)
        print(f"{Colors.INFO}{t('file_system_permissions')} {Colors.RESET}{t('normal')}{Colors.RESET}")
    except Exception as e:
        print(
            f"{Colors.INFO}{t('file_system_permissions')} {Colors.RESET}{t('error_with_msg').format(error=e)}{Colors.RESET}")


# 使用套接字实现单例模式
class SocketSingleInstance:
    """
    使用套接字实现单例模式，确保应用程序只有一个实例在运行
    """

    def __init__(self, port=LOCK_PORT):
        self.port = port
        self.sock = None
        self.locked = False
        self._try_lock()

    def _try_lock(self):
        """尝试获取锁"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('127.0.0.1', self.port))
            self.sock.listen(1)
            self.locked = True
            print(f"{Colors.INFO}{t('app_lock_success').format(port=self.port)}{Colors.RESET}")
        except socket.error as e:
            self.sock = None
            self.locked = False
            print(f"{Colors.INFO}{t('app_lock_failure').format(port=self.port, error=e)}{Colors.RESET}")

    def is_running(self):
        """检查应用程序是否已经在运行"""
        return not self.locked

    def release(self):
        """释放锁"""
        if self.sock:
            try:
                self.sock.close()
                print(f"{Colors.INFO}{t('app_lock_released').format(port=self.port)}{Colors.RESET}")
            except:
                pass
            self.sock = None
            self.locked = False

    def __del__(self):
        """析构函数，释放锁"""
        self.release()


# 进程检查和清理功能
def check_and_clean_processes():
    """检查并清理残留进程"""
    print(f"{Colors.INFO}{t('checking_processes_simple')}{Colors.RESET}")
    try:
        # 根据操作系统执行不同的命令
        if platform.system() == "Windows":
            # Windows
            cmd = f'netstat -ano | findstr ":{LOCK_PORT}"'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
            if output:
                print(f"{Colors.INFO}{t('found_processes_simple')}{Colors.RESET}")
                print(output)
                # 可以添加自动清理逻辑
            else:
                print(f"{Colors.INFO}{t('no_processes_found_simple')}{Colors.RESET}")
        elif platform.system() == "Darwin" or platform.system() == "Linux":
            # macOS or Linux
            cmd = f"lsof -i :{LOCK_PORT}"
            try:
                output = subprocess.check_output(cmd, shell=True).decode('utf-8')
                if output:
                    print(f"{Colors.INFO}{t('found_processes_simple')}{Colors.RESET}")
                    print(output)
                    # 可以添加自动清理逻辑
                else:
                    print(f"{Colors.INFO}{t('no_processes_found_simple')}{Colors.RESET}")
            except subprocess.CalledProcessError:
                # 如果命令返回非零状态，通常意味着没有找到匹配的进程
                print(f"{Colors.INFO}{t('no_processes_found_simple')}{Colors.RESET}")
        else:
            print(f"{Colors.INFO}{t('unsupported_os').format(os=platform.system())}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.INFO}{t('process_check_failed').format(error=e)}{Colors.RESET}")
        traceback.print_exc()


class QuotaInfo:
    """配额信息数据类"""

    def __init__(self):
        self.type = "Unknown"
        self.current = 0.0
        self.maximum = 0.0
        self.until = ""
        self.percentage = 0.0
        self.refill_type = "Unknown"
        self.next_refill = ""
        self.refill_amount = 0.0
        self.refill_duration = ""
        self.timestamp = datetime.now().isoformat()
        self.file_path = ""

    @classmethod
    def from_xml_file(cls, file_path):
        """从XML文件解析配额信息"""
        quota = cls()
        # 确保存储完整的绝对路径
        quota.file_path = os.path.abspath(file_path)

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 查找配额信息
            for option in root.findall(".//option"):
                if option.get("name") == "quotaInfo":
                    quota_info_str = option.get("value")
                    quota_info_str = quota_info_str.replace("&#10;", "\n").replace("&quot;", "\"")
                    quota_info = json.loads(quota_info_str)

                    quota.type = quota_info.get("type", "Unknown")
                    quota.current = float(quota_info.get("current", "0"))
                    quota.maximum = float(quota_info.get("maximum", "0"))
                    quota.until = quota_info.get("until", "")

                    # 计算百分比
                    if quota.maximum > 0:
                        quota.percentage = (quota.current / quota.maximum) * 100

                elif option.get("name") == "nextRefill":
                    refill_str = option.get("value")
                    refill_str = refill_str.replace("&#10;", "\n").replace("&quot;", "\"")

                    try:
                        refill_info = json.loads(refill_str)
                        quota.refill_type = refill_info.get("type", "Unknown")

                        if quota.refill_type != "Unknown":
                            quota.next_refill = refill_info.get("next", "")
                            quota.refill_amount = float(refill_info.get("amount", "0"))
                            quota.refill_duration = refill_info.get("duration", "")
                    except:
                        pass

            return quota
        except Exception as e:
            print(f"{Colors.INFO}{t('xml_parse_error').format(error=e)}{Colors.RESET}")
            return quota

    def to_dict(self):
        """转换为字典"""
        return {
            "type": self.type,
            "current": self.current,
            "maximum": self.maximum,
            "until": self.until,
            "percentage": self.percentage,
            "refill_type": self.refill_type,
            "next_refill": self.next_refill,
            "refill_amount": self.refill_amount,
            "refill_duration": self.refill_duration,
            "timestamp": self.timestamp,
            "file_path": self.file_path
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        quota = cls()
        quota.type = data.get("type", "Unknown")
        quota.current = data.get("current", 0.0)
        quota.maximum = data.get("maximum", 0.0)
        quota.until = data.get("until", "")
        quota.percentage = data.get("percentage", 0.0)
        quota.refill_type = data.get("refill_type", "Unknown")
        quota.next_refill = data.get("next_refill", "")
        quota.refill_amount = data.get("refill_amount", 0.0)
        quota.refill_duration = data.get("refill_duration", "")
        quota.timestamp = data.get("timestamp", datetime.now().isoformat())
        # 确保存储完整的绝对路径
        file_path = data.get("file_path", "")
        quota.file_path = os.path.abspath(file_path) if file_path else ""
        return quota


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        """初始化配置管理器"""
        # 获取应用程序路径
        self.app_path = self._get_app_path()

        # 尝试多个可能的配置目录
        self.config_dir = self._get_config_dir()

        # 确保目录存在
        try:
            os.makedirs(self.config_dir, exist_ok=True)
        except Exception as e:
            print(f"无法创建配置目录: {e}")
            # 如果无法创建目录，使用当前目录作为备选
            self.config_dir = os.path.abspath(".")

        # 配置文件路径
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.history_file = os.path.join(self.config_dir, "history.json")

    def print_config_paths(self):
        """打印配置路径信息"""
        print(f"{Colors.INFO}{t('app_path')} {Colors.RESET}{self.app_path}{Colors.RESET}")
        print(f"{Colors.INFO}{t('config_dir')} {Colors.RESET}{self.config_dir}{Colors.RESET}")
        print(f"{Colors.INFO}{t('config_file')} {Colors.RESET}{self.config_file}{Colors.RESET}")
        print(f"{Colors.INFO}{t('history_file')} {Colors.RESET}{self.history_file}{Colors.RESET}")

    def _get_app_path(self):
        """获取应用程序路径"""
        try:
            # 如果是PyInstaller打包的应用
            if getattr(sys, 'frozen', False):
                return os.path.dirname(sys.executable)
            # 否则使用脚本路径
            else:
                return os.path.dirname(os.path.abspath(__file__))
        except Exception as e:
            print(f"{Colors.INFO}{t('app_path_error').format(error=e)}{Colors.RESET}")
            return os.path.abspath(".")

    def _get_config_dir(self):
        """获取配置目录，尝试多个可能的位置"""
        # 尝试的路径列表，按优先级排序
        paths = [
            # 1. 用户主目录
            os.path.join(os.path.expanduser("~"), ".jetbrains_ai_quota_analyzer"),
            # 2. 应用程序目录
            os.path.join(self.app_path, "data"),
            # 3. 临时目录
            os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp",
                         "jetbrains_ai_quota_analyzer") if sys.platform == "win32" else
            os.path.join("/tmp", "jetbrains_ai_quota_analyzer") if sys.platform.startswith("linux") else
            os.path.join(os.path.expanduser("~"), "Library", "Caches",
                         "jetbrains_ai_quota_analyzer") if sys.platform == "darwin" else
            os.path.join(os.path.expanduser("~"), ".jetbrains_ai_quota_analyzer"),
            # 4. 当前目录
            os.path.abspath(".")
        ]

        # 尝试每个路径，返回第一个可写的路径
        for path in paths:
            try:
                # 尝试创建目录
                os.makedirs(path, exist_ok=True)
                # 尝试写入测试文件
                test_file = os.path.join(path, ".write_test")
                with open(test_file, "w") as f:
                    f.write("test")
                # 删除测试文件
                os.remove(test_file)
                return path
            except Exception as e:
                print(f"{Colors.INFO}{t('path_not_writable').format(path=path, error=e)}{Colors.RESET}")
                continue

        # 如果所有路径都失败，返回当前目录
        return os.path.abspath(".")

    def save_config(self, config):
        """保存配置"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def get_recent_paths(self):
        """获取最近使用的路径"""
        config = self.load_config()
        return config.get("recent_paths", [])

    def add_recent_path(self, path):
        """添加最近使用的路径"""
        config = self.load_config()
        recent_paths = config.get("recent_paths", [])

        # 如果路径已存在，则移除旧的
        if path in recent_paths:
            recent_paths.remove(path)

        # 添加到最前面
        recent_paths.insert(0, path)

        # 只保留最近的10个路径
        recent_paths = recent_paths[:10]

        config["recent_paths"] = recent_paths
        self.save_config(config)

    def save_history(self, quota_info):
        """保存历史记录"""
        history = self.load_history()
        history.append(quota_info.to_dict())

        # 只保留最近的100条记录
        history = history[-100:]

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def load_history(self):
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def get_unique_paths(self):
        """获取历史记录中的唯一路径"""
        history = self.load_history()
        paths = set()

        for item in history:
            path = item.get("file_path", "")
            if path:
                paths.add(path)

        return sorted(list(paths))

    def get_language(self):
        """获取语言设置"""
        config = self.load_config()
        return config.get("language", DEFAULT_LANGUAGE)

    def set_language(self, language: str):
        """设置语言"""
        if language not in SUPPORTED_LANGUAGES:
            language = DEFAULT_LANGUAGE

        config = self.load_config()
        config["language"] = language
        self.save_config(config)

    def get_recommended_paths(self, max_count=5):
        """获取推荐的历史路径，基于使用频率和最近使用情况
        
        Args:
            max_count: 最多返回的推荐路径数量
        
        Returns:
            推荐路径列表，按推荐度排序
        """
        # 获取历史记录
        history = self.load_history()

        # 获取最近使用的路径
        recent_paths = self.get_recent_paths()

        # 统计每个路径的使用频率
        path_frequency = {}
        for item in history:
            path = item.get("file_path", "")
            if path:
                path_frequency[path] = path_frequency.get(path, 0) + 1

        # 如果没有历史记录，返回空列表
        if not path_frequency:
            return []

        # 计算推荐得分：结合使用频率和最近使用情况
        path_scores = {}
        max_frequency = max(path_frequency.values()) if path_frequency else 1

        for path, freq in path_frequency.items():
            # 基础分数：使用频率的归一化值（0-1之间）
            base_score = freq / max_frequency

            # 最近使用加成：如果在最近使用列表中，根据位置给予额外加分
            recency_bonus = 0
            if path in recent_paths:
                # 最近使用列表中的位置（0是最近的）
                position = recent_paths.index(path)
                # 位置越靠前，加分越多（最大加分为1，随位置递减）
                recency_bonus = 1 * (1 - position / len(recent_paths)) if len(recent_paths) > 0 else 0

            # 总分 = 使用频率分数 + 最近使用加成
            # 权重可以调整：这里使用频率占60%，最近使用占40%
            path_scores[path] = base_score * 0.6 + recency_bonus * 0.4

        # 按得分排序，返回推荐路径
        recommended_paths = sorted(path_scores.items(), key=lambda x: x[1], reverse=True)
        return [path for path, score in recommended_paths[:max_count]]


class DatabaseManager:
    """数据库管理器"""

    def __init__(self, config_manager):
        """初始化数据库管理器"""
        self.config_manager = config_manager
        self.db_file = os.path.join(config_manager.config_dir, "database.db")
        self.conn = None
        self.connected = False

        # 初始化数据库
        self._connect_db()
        if self.connected:
            self.init_db()
            self._migrate_from_json()

    def _connect_db(self):
        """连接数据库"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.connected = True
            print(f"{Colors.INFO}{t('db_connected').format(path=self.db_file)}{Colors.RESET}")
        except sqlite3.Error as e:
            self.connected = False
            print(f"{Colors.INFO}{t('db_connect_failed').format(error=e)}{Colors.RESET}")
            # 尝试使用内存数据库作为备选
            try:
                self.conn = sqlite3.connect(":memory:")
                self.connected = True
                print(f"{Colors.INFO}{t('use_memory_db')}{Colors.RESET}")
            except sqlite3.Error as e2:
                print(f"{Colors.INFO}{t('memory_db_failed').format(error=e2)}{Colors.RESET}")

    def ensure_connection(self):
        """确保数据库连接有效，如果无效则尝试重新连接"""
        try:
            # 尝试执行一个简单的查询来测试连接
            if self.conn:
                self.conn.cursor().execute("SELECT 1")
                return True
        except sqlite3.Error:
            self.connected = False

        # 如果连接无效，尝试重新连接
        if not self.connected:
            self._connect_db()
            if self.connected:
                self.init_db()

        return self.connected

    def init_db(self):
        """初始化数据库，创建表结构"""
        if not self.ensure_connection():
            print(f"{Colors.INFO}{t('db_init_failed')}{Colors.RESET}")
            return False

        try:
            cursor = self.conn.cursor()
            # 创建历史记录表
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS history
                           (
                               id
                                   INTEGER
                                   PRIMARY
                                       KEY
                                   AUTOINCREMENT,
                               type
                                   TEXT,
                               current
                                   REAL,
                               maximum
                                   REAL,
                               until
                                   TEXT,
                               percentage
                                   REAL,
                               refill_type
                                   TEXT,
                               next_refill
                                   TEXT,
                               refill_amount
                                   REAL,
                               refill_duration
                                   TEXT,
                               timestamp
                                   TEXT,
                               file_path
                                   TEXT
                           )
                           ''')

            # 创建配置表
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS config
                           (
                               id
                                   INTEGER
                                   PRIMARY
                                       KEY
                                   AUTOINCREMENT,
                               key
                                   TEXT
                                   UNIQUE,
                               value
                                   TEXT
                           )
                           ''')

            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"{Colors.INFO}{t('db_init_error').format(error=e)}{Colors.RESET}")
            return False

    def _migrate_from_json(self):
        """从JSON文件迁移数据到SQLite"""
        if not self.ensure_connection():
            return

        # 检查是否已经有数据
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM history")
        count = cursor.fetchone()[0]

        # 如果已经有数据，不进行迁移
        if count > 0:
            return

        # 从JSON文件加载历史记录
        history = self.config_manager.load_history()
        if not history:
            return

        print(f"{Colors.INFO}{t('migrate_from_json').format(count=len(history))}{Colors.RESET}")

        # 插入历史记录
        try:
            for item in history:
                self.save_history_item(QuotaInfo.from_dict(item))
            print(f"{Colors.INFO}{t('migration_complete')}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.INFO}{t('migration_failed').format(error=e)}{Colors.RESET}")

    def save_history_item(self, quota_info):
        """保存单个历史记录项"""
        if not self.ensure_connection():
            print(f"{Colors.INFO}{t('save_history_failed')}{Colors.RESET}")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                           INSERT INTO history
                           (type, current, maximum, until, percentage, refill_type,
                            next_refill, refill_amount, refill_duration, timestamp, file_path)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''', (
                               quota_info.type, quota_info.current, quota_info.maximum,
                               quota_info.until, quota_info.percentage, quota_info.refill_type,
                               quota_info.next_refill, quota_info.refill_amount,
                               quota_info.refill_duration, quota_info.timestamp, quota_info.file_path
                           ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"{Colors.INFO}{t('save_record_failed').format(error=e)}{Colors.RESET}")
            return False

    def load_history(self, limit=50, file_path=None):
        """从数据库加载历史记录"""
        if not self.ensure_connection():
            print(f"{Colors.INFO}{t('load_history_failed')}{Colors.RESET}")
            return []

        try:
            cursor = self.conn.cursor()

            if file_path:
                # 检查是否是目录，如果是则使用 LIKE 进行模糊匹配
                if os.path.isdir(file_path):
                    # 确保目录路径以 / 结尾，以便正确匹配子路径
                    dir_path = os.path.join(file_path, '')  # 添加路径分隔符
                    cursor.execute('''
                                   SELECT *
                                   FROM history
                                   WHERE file_path LIKE ? || '%'
                                   ORDER BY timestamp DESC
                                   LIMIT ?
                                   ''', (dir_path, limit))
                else:
                    # 精确匹配文件路径
                    cursor.execute('''
                                   SELECT *
                                   FROM history
                                   WHERE file_path = ?
                                   ORDER BY timestamp DESC
                                   LIMIT ?
                                   ''', (file_path, limit))
            else:
                # 加载所有记录
                cursor.execute('''
                               SELECT *
                               FROM history
                               ORDER BY timestamp DESC
                               LIMIT ?
                               ''', (limit,))

            rows = cursor.fetchall()

            # 转换为QuotaInfo对象
            result = []
            for row in rows:
                data = {
                    "type": row[1],
                    "current": row[2],
                    "maximum": row[3],
                    "until": row[4],
                    "percentage": row[5],
                    "refill_type": row[6],
                    "next_refill": row[7],
                    "refill_amount": row[8],
                    "refill_duration": row[9],
                    "timestamp": row[10],
                    "file_path": row[11]
                }
                result.append(QuotaInfo.from_dict(data))

            return result
        except sqlite3.Error as e:
            print(f"{Colors.INFO}{t('load_records_failed').format(error=e)}{Colors.RESET}")
            return []

    def get_unique_paths(self):
        """获取历史记录中的唯一路径"""
        if not self.ensure_connection():
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                           SELECT DISTINCT file_path
                           FROM history
                           WHERE file_path != ''
                           ORDER BY file_path
                           ''')

            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print(f"{Colors.INFO}{t('get_paths_failed').format(error=e)}{Colors.RESET}")
            return []

    def clear_history(self, file_path=None):
        """
        清除历史记录
        
        Args:
            file_path (str, optional): 要清除的特定文件路径的历史记录。如果为None，则清除所有历史记录。
            
        Returns:
            bool: 操作是否成功
        """
        if not self.ensure_connection():
            error_msg = f"{Colors.ERROR}{t('save_history_failed')}{Colors.RESET}"
            print(error_msg)
            return False

        try:
            cursor = self.conn.cursor()

            # 检查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
            if not cursor.fetchone():
                print(f"{Colors.WARNING}{t('no_history_table')}{Colors.RESET}")
                return True

            # 获取记录数
            if file_path:
                cursor.execute('SELECT COUNT(*) FROM history WHERE file_path = ?', (file_path,))
                count = cursor.fetchone()[0]
                if count == 0:
                    print(f"{Colors.WARNING}{t('no_path_history').format(path=file_path)}{Colors.RESET}")
                    return True

                # 执行删除指定路径的历史记录
                cursor.execute('DELETE FROM history WHERE file_path = ?', (file_path,))
                success_msg = t('clear_success').format(message=t('clear_path_success').format(path=file_path))
            else:
                cursor.execute('SELECT COUNT(*) FROM history')
                count = cursor.fetchone()[0]
                if count == 0:
                    print(f"{Colors.INFO}{t('history_empty')}{Colors.RESET}")
                    return True

                # 执行删除所有历史记录
                cursor.execute('DELETE FROM history')
                success_msg = t('clear_all_success_count').format(count=count)

            self.conn.commit()

            # 验证删除结果
            if file_path:
                cursor.execute('SELECT COUNT(*) FROM history WHERE file_path = ?', (file_path,))
            else:
                cursor.execute('SELECT COUNT(*) FROM history')

            remaining = cursor.fetchone()[0]

            if remaining == 0 or (file_path and remaining < count):
                print(f"{Colors.SUCCESS}{success_msg}{Colors.RESET}")
                return True
            else:
                error_msg = f"{Colors.ERROR}{t('clear_history_db_error').format(count=remaining)}{Colors.RESET}"
                print(error_msg)
                if self.conn:
                    self.conn.rollback()
                return False

        except sqlite3.Error as e:
            error_msg = f"{Colors.ERROR}{t('clear_history_error').format(error=e)}{Colors.RESET}"
            print(error_msg)
            if self.conn:
                self.conn.rollback()
            return False
        except Exception as e:
            error_msg = f"{Colors.ERROR}{t('unexpected_error').format(error=e)}{Colors.RESET}"
            print(error_msg)
            if self.conn:
                self.conn.rollback()
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            try:
                self.conn.close()
                self.connected = False
                print(f"{Colors.INFO}{t('db_closed')}{Colors.RESET}")
            except sqlite3.Error as e:
                print(f"{Colors.INFO}{t('db_close_error').format(error=e)}{Colors.RESET}")


class QuotaAnalyzer:
    """配额分析器"""

    def __init__(self, db_manager):
        """初始化配额分析器"""
        self.db_manager = db_manager
        self.config_manager = db_manager.config_manager

    def _find_quota_file(self, directory):
        """在指定目录中查找配额文件"""
        # 检查是否是官方配置目录结构
        options_dir = os.path.join(directory, "options")
        if os.path.isdir(options_dir):
            quota_file = os.path.join(options_dir, "AIAssistantQuotaManager2.xml")
            if os.path.exists(quota_file):
                return quota_file

        # 如果不是官方目录结构，尝试直接查找XML文件
        for root, _, files in os.walk(directory):
            for file in files:
                if file == "AIAssistantQuotaManager2.xml":
                    return os.path.join(root, file)

        return None

    def analyze_file(self, file_or_dir_path):
        """
        分析指定文件或IDE数据目录的配额信息
        :param file_or_dir_path: 可以是以下任意一种：
           1. 配额文件完整路径 (如: /path/to/AIAssistantQuotaManager2.xml)
           2. IDE数据目录 (如: /Users/username/JetBrainsData/IDEA 或官方路径 ~/Library/Application Support/JetBrains/IntelliJIdea2024.1)
           3. 包含多个IDE配置的目录 (如: ~/Library/Application Support/JetBrains/)
        """
        try:
            # 如果路径为空，尝试自动查找
            if not file_or_dir_path:
                return self.find_and_analyze_quota_files(non_interactive=True)

            # 检查路径是否存在
            if not os.path.exists(file_or_dir_path):
                print(f"{Colors.INFO}{t('path_not_exist').format(path=file_or_dir_path)}{Colors.RESET}")
                return None

            # 如果是文件，直接使用
            if os.path.isfile(file_or_dir_path):
                file_path = file_or_dir_path
            # 如果是目录，尝试查找配额文件
            else:
                # 首先尝试在指定目录中查找
                file_path = self._find_quota_file(file_or_dir_path)

                # 如果没找到，且是官方配置目录结构，尝试查找子目录
                if not file_path and os.path.basename(file_or_dir_path) == "JetBrains":
                    for item in os.listdir(file_or_dir_path):
                        item_path = os.path.join(file_or_dir_path, item)
                        if os.path.isdir(item_path):
                            found = self._find_quota_file(item_path)
                            if found:
                                file_path = found
                                break

                if not file_path:
                    print(f"{Colors.INFO}{t('quota_file_not_found').format(path=file_or_dir_path)}{Colors.RESET}")
                    return None

            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"{Colors.INFO}{t('file_not_exist').format(path=file_path)}{Colors.RESET}")
                # 提示常见路径
                print(f"{Colors.INFO}{t('common_paths_hint')}{Colors.RESET}")
                print(
                    f"Windows: %APPDATA%\\JetBrains\\{t('product_placeholder')}\\options\\AIAssistantQuotaManager2.xml")
                print(
                    f"macOS: ~/Library/Application Support/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")
                print(f"Linux: ~/.config/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")
                return

            # 解析XML文件
            quota_info = QuotaInfo.from_xml_file(file_path)
            if not quota_info:
                return None

            # 保存到历史记录
            self.db_manager.save_history_item(quota_info)

            return quota_info

        except Exception as e:
            print(f"{Colors.INFO}{t('analyze_error').format(error=e)}{Colors.RESET}")
            traceback.print_exc()
            return None

    def _get_progress_bar(self, percentage, width=30):
        """
        生成一个带颜色的文本进度条
        :param percentage: 百分比值 (0-100)
        :param width: 进度条宽度（字符数）
        :return: 进度条字符串
        """
        # 根据百分比选择颜色和字符
        if percentage < 30:
            color = Colors.PROGRESS_LOW
            fill_char = '█'
            empty_char = '░'
        elif percentage < 70:
            color = Colors.PROGRESS_MEDIUM
            fill_char = '▓'
            empty_char = '░'
        else:
            color = Colors.PROGRESS_HIGH
            fill_char = '█'
            empty_char = '░'

        # 计算填充长度
        filled = int(width * percentage / 100)
        bar = f"{Colors.BG_BLACK}{color}{fill_char * filled}{Colors.RESET}{Colors.DIM}{empty_char * (width - filled)}{Colors.RESET}"

        # 添加百分比文本
        percent_text = f"{percentage:6.2f}%"

        # 组合进度条和百分比
        return f"{Colors.BOLD}{color}┃{bar}┃{Colors.RESET} {Colors.BOLD}{percent_text}{Colors.RESET}"

    def display_quota_info(self, quota_info):
        """显示配额信息"""
        print("\n" + Colors.HEADER + "=" * 60 + Colors.RESET)
        print(f"{Colors.INFO}{t('file_path')} {Colors.SUCCESS}{quota_info.file_path}{Colors.RESET}")

        # 根据使用百分比选择颜色
        if quota_info.percentage < 50:
            percentage_color = Colors.PROGRESS_LOW
        elif quota_info.percentage < 80:
            percentage_color = Colors.PROGRESS_MEDIUM
        else:
            percentage_color = Colors.PROGRESS_HIGH

        print(f"\n{Colors.HEADER}{t('quota_info')}{Colors.RESET}")
        print(f"{Colors.INFO}{t('quota_type')} {Colors.SUCCESS}{quota_info.type}{Colors.RESET}")
        print(f"{Colors.INFO}{t('current_usage')} {Colors.SUCCESS}{quota_info.current:.2f}{Colors.RESET}")
        print(f"{Colors.INFO}{t('max_limit')} {Colors.SUCCESS}{quota_info.maximum:.2f}{Colors.RESET}")
        print(f"{Colors.INFO}{t('usage_percentage')} {percentage_color}{quota_info.percentage:.2f}%{Colors.RESET}")
        print(f"{Colors.INFO}{t('valid_until')} {Colors.SUCCESS}{quota_info.until}{Colors.RESET}")

        print(f"\n{Colors.HEADER}{t('refill_info')}{Colors.RESET}")
        print(f"{Colors.INFO}{t('refill_type')} {Colors.SUCCESS}{quota_info.refill_type}{Colors.RESET}")
        print(f"{Colors.INFO}{t('next_refill')} {Colors.SUCCESS}{quota_info.next_refill}{Colors.RESET}")
        print(f"{Colors.INFO}{t('refill_amount')} {Colors.SUCCESS}{quota_info.refill_amount:.2f}{Colors.RESET}")
        print(f"{Colors.INFO}{t('refill_period')} {Colors.SUCCESS}{quota_info.refill_duration}{Colors.RESET}")

        print(f"\n{Colors.HEADER}{t('other_info')}{Colors.RESET}")
        print(f"{Colors.INFO}{t('timestamp')} {Colors.SUCCESS}{quota_info.timestamp}{Colors.RESET}")

        print("\n" + Colors.HEADER + "-" * 60 + Colors.RESET)

        # 显示进度条
        progress_bar = self._get_progress_bar(quota_info.percentage)
        print(f"\n{Colors.INFO}{t('usage_status')} {progress_bar}")

        # 等待用户按回车键继续
        if sys.stdin.isatty():  # 检查是否在交互式终端中运行
            input(f"\n{Colors.MENU_PROMPT}{t('press_enter')}{Colors.RESET}")
            print()  # 添加一个空行

    def display_history(self, file_path=None, limit=10):
        """显示历史记录"""
        history = self.db_manager.load_history(limit=limit, file_path=file_path)

        if not history:
            print(f"{Colors.INFO}{t('no_history')}{Colors.RESET}")
            return

        # 打印表头
        header = f"{Colors.TABLE_HEADER}{t('column_num'):<4} {t('column_time'):<25} {t('column_type'):<15} {t('column_usage'):<15} {t('column_current_max'):<20}"
        if file_path is None:
            header += f" {t('column_filepath')}"
        print(f"\n{header}{Colors.RESET}")
        print(f"{Colors.DIM}{'-' * 100}{Colors.RESET}")

        for i, item in enumerate(history, 1):
            # 根据使用率选择颜色
            if item.percentage < 30:
                percent_color = Colors.PROGRESS_LOW
            elif item.percentage < 70:
                percent_color = Colors.PROGRESS_MEDIUM
            else:
                percent_color = Colors.PROGRESS_HIGH

            # 格式化时间
            try:
                dt = datetime.fromisoformat(item.timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            except (ValueError, AttributeError):
                timestamp = str(item.timestamp)

            # 构建行
            row = f"{Colors.BOLD}{i:<4} {Colors.SUCCESS}{timestamp:<25} {item.type:<15} "
            row += f"{percent_color}{item.percentage:>6.2f}%{Colors.RESET} "
            row += f"{Colors.INFO}({item.current:>6.2f}/{item.maximum:<6.2f}){Colors.RESET}"

            # 如果不过滤路径，添加文件路径
            if file_path is None:
                # 显示完整路径
                row += f" {Colors.DIM}{item.file_path}{Colors.RESET}"

            # 交替行颜色
            if i % 2 == 0:
                row = f"{Colors.TABLE_ROW_EVEN}{row}{Colors.RESET}"
            else:
                row = f"{Colors.TABLE_ROW_ODD}{row}{Colors.RESET}"

            print(row)

        # 打印页脚
        print(f"{Colors.DIM}{'-' * 100}{Colors.RESET}")
        print(f"{Colors.INFO}{t('total_records').format(count=len(history))}{Colors.RESET}\n")

    def get_paths(self):
        """获取历史记录中的唯一路径"""
        return self.db_manager.get_unique_paths()

    def find_and_analyze_quota_files(self, non_interactive=False):
        """查找并分析配额文件"""
        # 查找配额文件
        quota_files = find_quota_files()

        if not quota_files:
            print(f"{Colors.INFO}{t('no_quota_file')}{Colors.RESET}")
            return

        print(f"{Colors.INFO}{t('found_quota_files').format(count=len(quota_files))}{Colors.RESET}")
        for i, file_path in enumerate(quota_files, 1):
            print(f"{i}. {file_path}")
        print()

        if non_interactive:
            # 非交互模式，分析所有文件
            print(f"{Colors.INFO}{t('auto_analyzing_all_files')}{Colors.RESET}")
            success_count = 0
            for file_path in quota_files:
                print(f"{Colors.INFO}{t('analyzing_file').format(path=file_path)}{Colors.RESET}")
                quota_info = self.analyze_file(file_path)
                if quota_info:
                    self.display_quota_info(quota_info)
                    success_count += 1
            print(f"\n{Colors.INFO}{t('analysis_success_count').format(count=success_count)}{Colors.RESET}")
        else:
            # 交互模式，让用户选择
            while True:
                choice = input(f"\n{t('select_file_to_analyze')}: ")

                if choice.lower() == 'q':
                    break

                if choice.lower() == 'a':
                    # 分析所有文件
                    success_count = 0
                    for file_path in quota_files:
                        print(f"{Colors.INFO}{t('analyzing_file').format(path=file_path)}{Colors.RESET}")
                        quota_info = self.analyze_file(file_path)
                        if quota_info:
                            self.display_quota_info(quota_info)
                            success_count += 1
                    print(f"\n{Colors.INFO}{t('analysis_success_count').format(count=success_count)}{Colors.RESET}")
                    break

                if choice.isdigit():
                    idx = int(choice)
                    if 1 <= idx <= len(quota_files):
                        file_path = quota_files[idx - 1]
                        print(f"{Colors.INFO}{t('analyzing_file').format(path=file_path)}{Colors.RESET}")
                        quota_info = self.analyze_file(file_path)
                        if quota_info:
                            self.display_quota_info(quota_info)
                    else:
                        print(f"{Colors.INFO}{t('invalid_option_simple')}{Colors.RESET}")
                else:
                    print(f"{Colors.INFO}{t('invalid_input_simple')}{Colors.RESET}")

    def close(self):
        """关闭资源"""
        pass  # 所有资源由db_manager关闭


class CommandLineInterface:
    """命令行界面"""

    def __init__(self, config_manager, db_manager):
        """初始化命令行界面"""
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.quota_analyzer = QuotaAnalyzer(self.db_manager)
        self.running = True
        # 检测是否在交互式环境中运行
        self.is_interactive = sys.stdin.isatty()

    def _safe_input(self, prompt):
        """安全的输入函数，处理EOF和KeyboardInterrupt异常"""
        if not self.is_interactive:
            print(f"{Colors.INFO}{t('non_interactive_warning')}{Colors.RESET}")
            print(f"{Colors.INFO}{t('use_command_line')}{Colors.RESET}")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -A --all")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/file.xml")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py --help")

            # 询问用户是否继续
            try:
                choice = input(f"{t('continue_prompt')} ")
                if choice.lower() != 'y':
                    return
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Colors.INFO}{t('eof_interrupt')}{Colors.RESET}")
                return

        try:
            # 添加颜色到提示符
            colored_prompt = f"{Colors.MENU_PROMPT}{prompt}{Colors.RESET}"
            return input(colored_prompt)
        except (EOFError, KeyboardInterrupt) as e:
            # 重新抛出异常，让上层处理
            raise e

    def show_menu(self):
        """显示主菜单"""
        print("\n" + Colors.HEADER + "=" * 60 + Colors.RESET)
        print(Colors.MENU_TITLE + t('app_title').center(60) + Colors.RESET)
        print(Colors.HEADER + "=" * 60 + Colors.RESET)
        print(f"{Colors.MENU_ITEM}1.{Colors.RESET} {t('menu_analyze_file')}")
        print(f"{Colors.MENU_ITEM}2.{Colors.RESET} {t('menu_auto_find')}")
        print(f"{Colors.MENU_ITEM}3.{Colors.RESET} {t('menu_view_history')}")
        print(f"{Colors.MENU_ITEM}4.{Colors.RESET} {t('menu_filter_history')}")
        print(f"{Colors.MENU_ITEM}5.{Colors.RESET} {t('menu_common_paths')}")
        print(f"{Colors.ERROR}6. {t('menu_clear_history')}{Colors.RESET}")
        print(f"{Colors.MENU_ITEM}7.{Colors.RESET} {t('menu_help')}")
        print(f"{Colors.MENU_ITEM}0.{Colors.RESET} {t('menu_exit')}")
        print("=" * 60)
        print(f"{Colors.INFO}{t('menu_hint')}{Colors.RESET}")

    def _get_path_with_recommendations(self, prompt=None):
        """
        获取带推荐路径的用户输入
        
        Args:
            prompt: 输入提示
            
        Returns:
            用户选择的文件路径，或None表示用户取消
        """
        if prompt is None:
            prompt = f"\n{t('enter_file_path_or_select')}: "

        # 获取推荐的历史路径
        recommended_paths = self.config_manager.get_recommended_paths(max_count=3)

        # 显示推荐的历史路径
        if recommended_paths:
            print(f"\n{Colors.HEADER}{t('recommended_paths')}{Colors.RESET}")
            for i, path in enumerate(recommended_paths, 1):
                print(f"{Colors.SUCCESS}{i}.{Colors.RESET} {path} {Colors.INFO}{t('recommended_tag')}{Colors.RESET}")

        # 获取用户输入
        while True:
            user_input = self._safe_input(prompt).strip()

            # 处理空输入
            if not user_input:
                return None

            # 处理推荐路径选择 (1, 2, 3)
            if user_input.isdigit():
                choice = int(user_input) - 1
                if 0 <= choice < len(recommended_paths):
                    return recommended_paths[choice]
                else:
                    print(f"{Colors.ERROR}{t('invalid_recommendation')}{Colors.RESET}")
                    continue

            # 处理普通路径
            if os.path.exists(user_input):
                return user_input

            # 路径不存在，显示错误信息
            print(f"{Colors.ERROR}{t('file_not_exist_error').format(path=user_input)}{Colors.RESET}")
            print(f"{Colors.INFO}{t('common_paths_hint')}{Colors.RESET}")
            print(f"Windows: %APPDATA%\\JetBrains\\{t('product_placeholder')}\\options\\AIAssistantQuotaManager2.xml")
            print(
                f"macOS: ~/Library/Application Support/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")
            print(f"Linux: ~/.config/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")

            # 询问是否重试
            choice = self._safe_input(f"{t('retry_prompt')} ").strip().lower()
            if choice != '' and choice != 'y':
                return None

    def _analyze_file(self):
        """分析单个文件"""
        file_path = self._get_path_with_recommendations(f"\n{t('enter_file_path_or_select')}: ")
        if not file_path:
            print(f"{Colors.INFO}{t('no_file_path')}{Colors.RESET}")
            return

        # 分析文件
        print(f"{Colors.INFO}{t('analyzing_file').format(path=file_path)}{Colors.RESET}")
        quota_info = self.quota_analyzer.analyze_file(file_path)
        if quota_info:
            self.quota_analyzer.display_quota_info(quota_info)
            # 添加到最近使用的路径
            self.config_manager.add_recent_path(file_path)

    def _view_history(self):
        """查看历史记录"""
        # 获取推荐的历史路径
        recommended_paths = self.config_manager.get_recommended_paths(max_count=3)

        # 显示推荐的历史路径
        if recommended_paths:
            print(f"\n{Colors.HEADER}{t('recommended_paths_view')}{Colors.RESET}")
            for i, path in enumerate(recommended_paths, 1):
                print(f"{Colors.SUCCESS}{i}.{Colors.RESET} {path} {Colors.INFO}{t('recommended_tag')}{Colors.RESET}")

        # 获取要显示的记录数量
        limit_str = self._safe_input(f"\n{t('enter_record_limit_filter')}: ")

        # 处理推荐路径选择
        if limit_str.isdigit():
            choice = int(limit_str) - 1
            if 0 <= choice < len(recommended_paths):
                file_path = recommended_paths[choice]
                limit_str = self._safe_input(f"{t('enter_record_limit')}: ")
                limit = 10
                if limit_str.isdigit():
                    limit = int(limit_str)
                self.quota_analyzer.display_history(file_path=file_path, limit=limit)
                # 添加到最近使用的路径
                self.config_manager.add_recent_path(file_path)
                return

        # 显示所有历史记录
        limit = 10
        if limit_str.isdigit():
            limit = int(limit_str)
        self.quota_analyzer.display_history(limit=limit)

    def _clear_history(self):
        """清除历史记录"""
        # 获取所有路径
        paths = self.quota_analyzer.get_paths()

        if not paths:
            print(f"{Colors.INFO}{t('no_history')}{Colors.RESET}")
            return

        print(f"\n{t('choose_clear_range')}")
        print(f"{Colors.WARNING}1. {t('clear_all_history')}{Colors.RESET}")
        print(f"{Colors.MENU_ITEM}2. {t('clear_by_path')}{Colors.RESET}")
        print(f"{Colors.MENU_ITEM}0. {t('cancel_return')}{Colors.RESET}")

        choice = self._safe_input(f"\n{t('select_operation')}: ")

        if choice == "1":
            # 清除所有历史记录
            confirm = self._safe_input(f"{Colors.WARNING}{t('confirm_clear_all')}")
            if confirm.lower() == 'y':
                if self.db_manager.clear_history():
                    print(f"{Colors.SUCCESS}{t('clear_all_success')}{Colors.RESET}")
            else:
                print(f"{Colors.INFO}{t('operation_cancelled')}{Colors.RESET}")

        elif choice == "2":
            # 按路径清除历史记录
            print(f"\n{t('available_paths')}:")
            for i, path in enumerate(paths, 1):
                print(f"{i}. {path}")

            path_choice = self._safe_input(f"\n{t('select_path_clear')}")

            if path_choice == "0":
                print(f"{Colors.INFO}{t('operation_cancelled_simple')}{Colors.RESET}")
                return

            if path_choice.isdigit() and 0 < int(path_choice) <= len(paths):
                file_path = paths[int(path_choice) - 1]
                confirm = self._safe_input(
                    f"{Colors.WARNING}{t('confirm_clear_path').format(path=file_path)}"
                )
                if confirm.lower() == 'y':
                    if self.db_manager.clear_history(file_path=file_path):
                        print(f"{Colors.SUCCESS}{t('clear_path_success').format(path=file_path)}{Colors.RESET}")
                else:
                    print(f"{Colors.INFO}{t('operation_cancelled')}{Colors.RESET}")
            else:
                print(f"{Colors.ERROR}{t('invalid_choice')}{Colors.RESET}")

    def _filter_history(self):
        """按路径筛选历史记录"""
        paths = self.quota_analyzer.get_paths()

        if not paths:
            print(f"{Colors.INFO}{t('no_history')}{Colors.RESET}")
            return

        # 获取推荐的历史路径
        recommended_paths = self.config_manager.get_recommended_paths(max_count=3)

        # 显示推荐的历史路径
        if recommended_paths:
            print(f"\n{Colors.HEADER}{t('recommended_paths')}{Colors.RESET}")
            for i, path in enumerate(recommended_paths, 1):
                print(f"{Colors.SUCCESS}R{i}.{Colors.RESET} {path} {Colors.INFO}{t('recommended_tag')}{Colors.RESET}")

        # 显示所有可用的文件路径
        print(f"\n{Colors.HEADER}{t('all_available_paths')}{Colors.RESET}")
        for i, path in enumerate(paths, 1):
            # 检查是否是推荐路径
            if path in recommended_paths:
                print(
                    f"{Colors.MENU_ITEM}{i}.{Colors.RESET} {path} {Colors.SUCCESS}{t('recommended_tag')}{Colors.RESET}")
            else:
                print(f"{Colors.MENU_ITEM}{i}.{Colors.RESET} {path}")

        if len(paths) == 1:
            # 如果只有一个路径，直接使用
            file_path = paths[0]
            print(f"\n{t('only_one_path').format(path=file_path)}")

            limit_str = self._safe_input(f"{t('enter_record_limit')}: ")

            # 设置默认值
            limit = 10
            if limit_str and limit_str.isdigit():
                limit = int(limit_str)

            self.quota_analyzer.display_history(file_path=file_path, limit=limit)
        else:
            # 让用户选择路径
            while True:
                # 提示用户可以使用R1-R3选择推荐路径
                prompt = f"\n{t('select_path_number')}"
                if recommended_paths:
                    prompt += t('select_path_hint').format(count=len(recommended_paths))
                prompt += t('select_path_return')

                choice = self._safe_input(prompt)

                if choice == "0":
                    return

                # 处理推荐路径选择
                if choice.upper().startswith('R') and choice[1:].isdigit():
                    r_index = int(choice[1:]) - 1
                    if 0 <= r_index < len(recommended_paths):
                        file_path = recommended_paths[r_index]

                        limit_str = self._safe_input(f"{t('enter_record_limit')}: ")

                        # 设置默认值
                        limit = 10
                        if limit_str and limit_str.isdigit():
                            limit = int(limit_str)

                        self.quota_analyzer.display_history(file_path=file_path, limit=limit)

                        # 添加到最近使用的路径
                        self.config_manager.add_recent_path(file_path)

                        break
                    else:
                        print(f"{Colors.ERROR}{t('invalid_recommendation')}{Colors.RESET}")
                # 处理普通路径选择
                elif choice.isdigit() and 1 <= int(choice) <= len(paths):
                    file_path = paths[int(choice) - 1]

                    limit_str = self._safe_input(f"{t('enter_record_limit')}: ")

                    # 设置默认值
                    limit = 10
                    if limit_str and limit_str.isdigit():
                        limit = int(limit_str)

                    self.quota_analyzer.display_history(file_path=file_path, limit=limit)

                    # 添加到最近使用的路径
                    self.config_manager.add_recent_path(file_path)

                    break
                else:
                    print(f"{Colors.ERROR}{t('invalid_option')}{Colors.RESET}")

    def show_common_paths(self):
        """显示常见配额文件路径"""
        print(f"\n{Colors.HEADER}{t('common_paths_title')}{Colors.RESET}")

        print(f"\n{Colors.MENU_ITEM}1. {Colors.HEADER}{t('idea_paths')}{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/IntelliJIdea{t('version_placeholder')}/options/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/IntelliJIdea{t('version_placeholder')}/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/.IntelliJIdea{t('version_placeholder')}/config/options/AIAssistantQuotaManager2.xml{Colors.RESET}")

        print(f"\n{Colors.MENU_ITEM}2. {Colors.HEADER}{t('pycharm_paths')}{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/PyCharm{t('version_placeholder')}/options/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/PyCharm{t('version_placeholder')}/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/.PyCharm{t('version_placeholder')}/config/options/AIAssistantQuotaManager2.xml{Colors.RESET}")

        print(f"\n{Colors.MENU_ITEM}3. {Colors.HEADER}{t('webstorm_paths')}{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/WebStorm{t('version_placeholder')}/options/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/Library/Application Support/JetBrains/WebStorm{t('version_placeholder')}/AIAssistantQuotaManager2.xml{Colors.RESET}")
        print(
            f"   {Colors.INFO}~/.WebStorm{t('version_placeholder')}/config/options/AIAssistantQuotaManager2.xml{Colors.RESET}")

        print(f"\n{Colors.INFO}{t('paths_tip')}{Colors.RESET}")

    def show_help(self):
        """显示帮助信息"""
        print(f"\n{Colors.HEADER}{t('help_title')}{Colors.RESET}")

        print(f"\n{Colors.INFO}{t('usage_tip')}{Colors.RESET}")
        print(f"{t('application_description')}")

        print(f"\n{Colors.INFO}{t('key_features')}{Colors.RESET}")
        print(f"1. {t('feature_analyze')}")
        print(f"2. {t('feature_auto')}")
        print(f"3. {t('feature_history')}")
        print(f"4. {t('feature_clear')}")

        print(f"\n{Colors.INFO}{t('command_line_usage')}{Colors.RESET}")
        print(f"- {t('interactive_mode')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py -i")
        print(f"- {t('analyze_example')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/AIAssistantQuotaManager2.xml")
        print(f"- {t('auto_find_example')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py -A")
        print(f"- {t('view_history_example')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py -H")
        print(f"- {t('filter_history_example')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py -f /path/to/file.xml")
        print(f"- {t('common_paths_example')}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py --help-paths")

        print(f"\n{Colors.INFO}{t('language_settings')}{Colors.RESET}")
        print(f"{t('supported_languages_info').format(languages=', '.join(SUPPORTED_LANGUAGES))}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py --lang en")

        print(f"\n{Colors.INFO}{t('other_help')}{Colors.RESET}")
        print("  python JetBrainsAIQuotaAnalyzer_CLI.py --help")

        # 等待用户按回车键继续
        if sys.stdin.isatty():
            input(f"\n{Colors.MENU_PROMPT}{t('press_enter')}{Colors.RESET}")

    def run_interactive(self):
        """运行交互式界面"""
        print(f"{Colors.INFO}{t('welcome')}{Colors.RESET}")

        if not self.is_interactive:
            print(f"{Colors.INFO}{t('interactive_warning')}{Colors.RESET}")
            print(f"{Colors.INFO}{t('interactive_error')}{Colors.RESET}")
            print(f"{Colors.INFO}{t('use_command_line')}{Colors.RESET}")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -A --all")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/file.xml")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py --help")

            # 询问用户是否继续
            try:
                choice = input(f"{t('continue_prompt')} ")
                if choice.lower() != 'y':
                    return
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Colors.INFO}{t('eof_interrupt')}{Colors.RESET}")
                return

        while self.running:
            try:
                self.show_menu()
                choice = self._safe_input(f"{t('select_operation')} ")

                if choice == "0":
                    self.running = False
                    print(f"{Colors.INFO}{t('thank_you')}{Colors.RESET}")
                elif choice == "1":
                    self._analyze_file()
                elif choice == "2":
                    self.quota_analyzer.find_and_analyze_quota_files(non_interactive=not self.is_interactive)
                elif choice == "3":
                    self._view_history()
                elif choice == "4":
                    self._clear_history()
                elif choice == "5":
                    self._filter_history()
                elif choice == "6":
                    self.show_common_paths()
                elif choice == "7":
                    self.show_help()
                else:
                    print(f"{Colors.INFO}{t('invalid_option_retry_dot')}{Colors.RESET}")
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Colors.INFO}{t('operation_cancelled')}{Colors.RESET}")
                self.running = False
            except Exception as e:
                print(f"{Colors.INFO}{t('unexpected_error').format(error=e)}{Colors.RESET}")
                traceback.print_exc()

        # 关闭数据库连接
        self.db_manager.close()

    def run_with_args(self, args):
        """使用命令行参数运行"""
        if args.analyze:
            quota_info = self.quota_analyzer.analyze_file(args.analyze)
            if quota_info:
                self.quota_analyzer.display_quota_info(quota_info)

        elif args.auto_find:
            self.quota_analyzer.find_and_analyze_quota_files(non_interactive=args.all)

        elif args.history:
            limit = args.limit if args.limit else 10
            self.quota_analyzer.display_history(limit=limit)

        elif args.filter:
            limit = args.limit if args.limit else 10
            self.quota_analyzer.display_history(file_path=args.filter, limit=limit)

        else:
            # 如果没有提供参数，运行交互式界面
            self.run_interactive()

        # 关闭资源
        self.quota_analyzer.close()


def find_quota_files():
    """
    自动查找系统中的JetBrains AI Assistant配额文件
    返回找到的文件路径列表
    """
    quota_files = []

    # 根据操作系统确定JetBrains配置目录
    if platform.system() == "Windows":
        # Windows: %APPDATA%\JetBrains\<产品>\options\AIAssistantQuotaManager2.xml
        base_dir = os.path.join(os.environ.get("APPDATA", ""), "JetBrains")
    elif platform.system() == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/JetBrains/<产品>/options/AIAssistantQuotaManager2.xml
        base_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "JetBrains")
    else:  # Linux and others
        # Linux: ~/.config/JetBrains/<产品>/options/AIAssistantQuotaManager2.xml
        base_dir = os.path.join(os.path.expanduser("~"), ".config", "JetBrains")

    # 如果基础目录不存在，返回空列表
    if not os.path.exists(base_dir):
        print(f"{Colors.INFO}{t('jetbrains_dir_not_found').format(path=base_dir)}{Colors.RESET}")
        return quota_files

    # 遍历基础目录下的所有子目录
    try:
        for product_dir in os.listdir(base_dir):
            product_path = os.path.join(base_dir, product_dir)

            # 检查是否是目录
            if not os.path.isdir(product_path):
                continue

            # 构建可能的配额文件路径
            quota_file = os.path.join(product_path, "options", "AIAssistantQuotaManager2.xml")

            # 检查文件是否存在
            if os.path.exists(quota_file):
                quota_files.append(quota_file)
    except Exception as e:
        print(f"{Colors.INFO}{t('find_quota_files_error').format(error=e)}{Colors.RESET}")

    return quota_files


def get_app_lock():
    """获取应用程序锁，确保只有一个实例在运行"""
    try:
        # 创建套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', LOCK_PORT))
        # 保存套接字引用，防止被垃圾回收
        global app_lock_socket
        app_lock_socket = sock
        print(f"{Colors.INFO}{t('app_lock_success').format(port=LOCK_PORT)}{Colors.RESET}")

        # 检查并清理残留进程
        check_and_clean_processes()

        return True
    except socket.error:
        print(f"{Colors.INFO}{t('app_lock_failure_simple').format(port=LOCK_PORT)}{Colors.RESET}")
        return False


def release_app_lock():
    """释放应用程序锁"""
    global app_lock_socket
    if 'app_lock_socket' in globals() and app_lock_socket:
        app_lock_socket.close()
        print(f"{Colors.INFO}{t('app_lock_released').format(port=LOCK_PORT)}{Colors.RESET}")


def create_argument_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(description=t('app_description'))

    # 基本选项
    parser.add_argument("-i", "--interactive", action="store_true", help=t('menu_analyze_file'))
    parser.add_argument("--help-paths", action="store_true", help=t('menu_common_paths'))

    # 分析选项
    parser.add_argument("-a", "--analyze", metavar="PATH", help=t('menu_analyze_file'))
    parser.add_argument("-A", "--auto-find", action="store_true", help=t('menu_auto_find'))
    parser.add_argument("--all", action="store_true", help=t('auto_analyze'))

    # 历史记录选项
    parser.add_argument("-H", "--history", action="store_true", help=t('menu_view_history'))
    parser.add_argument("-l", "--limit", type=int, default=10, help=t('enter_record_limit'))
    parser.add_argument("-f", "--filter", metavar="PATH", help=t('menu_filter_history'))

    # 语言选项
    parser.add_argument("--lang", choices=SUPPORTED_LANGUAGES, default=None,
                        help=t('set_language_option').format(languages=', '.join(SUPPORTED_LANGUAGES)))

    # 版本信息
    parser.add_argument("-v", "--version", action="version", version=t('version_info').format(version=VERSION))

    return parser


def parse_arguments():
    """解析命令行参数"""
    parser = create_argument_parser()
    return parser.parse_args()


def print_help_paths():
    """打印常见配额文件路径帮助信息"""
    print(f"\n{Colors.INFO}{t('usage_tip')}{Colors.RESET}")
    print("1. " + t('analyze_example'))
    print("   python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/AIAssistantQuotaManager2.xml")
    print("2. " + t('auto_find_example'))
    print("   python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/IDE_Data")
    print("3. " + t('auto_find_example'))
    print("   python JetBrainsAIQuotaAnalyzer_CLI.py -A")

    print(f"\n{Colors.INFO}{t('common_paths_title')}{Colors.RESET}")
    print("- Windows:")
    print("  1. " + t('analyze_example'))
    print(f"     %APPDATA%\\JetBrains\\{t('product_placeholder')}\\options\\AIAssistantQuotaManager2.xml")
    print(
        f"     {t('example')}: C:\\Users\\{t('username')}\\AppData\\Roaming\\JetBrains\\PyCharm2024.1\\options\\AIAssistantQuotaManager2.xml")
    print("  2. " + t('auto_find_example'))
    print(f"     C:\\Users\\{t('username')}\\JetBrains\\{t('product_placeholder')}\\{t('version_placeholder')}")

    print(f"\n{Colors.INFO}- macOS:{Colors.RESET}")
    print("  1. " + t('analyze_example'))
    print(
        f"     ~/Library/Application Support/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")
    print(
        f"     {t('example')}: /Users/{t('username')}/Library/Application Support/JetBrains/PyCharm2024.1/options/AIAssistantQuotaManager2.xml")
    print("  2. " + t('auto_find_example'))
    print(f"     ~/Library/Application Support/JetBrains/{t('product_placeholder')}")

    print(f"\n{Colors.INFO}- Linux:{Colors.RESET}")
    print("  1. " + t('analyze_example'))
    print(f"     ~/.config/JetBrains/{t('product_placeholder')}/options/AIAssistantQuotaManager2.xml")
    print(
        f"     {t('example')}: /home/{t('username')}/.config/JetBrains/PyCharm2024.1/options/AIAssistantQuotaManager2.xml")
    print("  2. " + t('auto_find_example'))
    print(f"     ~/.config/JetBrains/{t('product_placeholder')}")

    print(f"\n{Colors.INFO}{t('paths_tip')}{Colors.RESET}")
    print("- PyCharm2024.1 (PyCharm)")
    print("- IntelliJIdea2024.1 (IntelliJ IDEA)")
    print("- WebStorm2024.1 (WebStorm)")
    print("- CLion2024.1 (CLion)")
    print(f"- {t('etc')}")


def print_environment_info():
    """打印环境信息"""
    print(f"\n{Colors.HEADER}{t('environment_info_detailed')}{Colors.RESET}")
    print(
        f"{Colors.INFO}{t('os_info_detailed').format(os=platform.system(), release=platform.release(), version=platform.version())}{Colors.RESET}")
    print(f"{Colors.INFO}{t('python_version_detailed').format(version=platform.python_version())}{Colors.RESET}")
    print(f"{Colors.INFO}{t('sqlite_version_detailed').format(version=sqlite3.sqlite_version)}{Colors.RESET}")
    print(f"{Colors.INFO}{t('app_path_detailed').format(path=os.path.abspath(__file__))}{Colors.RESET}")
    print(f"{Colors.INFO}{t('working_dir_detailed').format(path=os.getcwd())}{Colors.RESET}")
    print(f"{Colors.INFO}{t('home_dir_detailed').format(path=os.path.expanduser('~'))}{Colors.RESET}")
    print(
        f"{Colors.INFO}{t('temp_dir_detailed').format(path=os.path.abspath(os.getenv('TMPDIR', '/tmp')))}{Colors.RESET}")
    try:
        path_list = os.getenv('PATH', '').split(os.pathsep)
        print(f"{Colors.INFO}{t('path_var_detailed').format(path=path_list)}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}{t('env_var_error').format(error=e)}{Colors.RESET}")


def main():
    """主函数"""
    try:
        # 创建配置管理器
        config_manager = ConfigManager()

        # 先检查命令行中是否指定了语言
        import sys
        for i, arg in enumerate(sys.argv[1:], 1):
            if arg == "--lang" and i < len(sys.argv):
                lang = sys.argv[i + 1]
                if lang in SUPPORTED_LANGUAGES:
                    set_language(lang)
            elif arg.startswith("--lang="):
                lang = arg.split("=")[1]
                if lang in SUPPORTED_LANGUAGES:
                    set_language(lang)

        # 如果命令行中未指定语言，从配置加载
        if not get_language() in SUPPORTED_LANGUAGES:
            set_language(config_manager.get_language())

        # 打印配置路径信息
        config_manager.print_config_paths()

        # 解析命令行参数
        args = parse_arguments()

        # 如果通过命令行指定了语言，保存到配置
        if args.lang:
            config_manager.set_language(args.lang)

        # 获取应用程序锁
        if not get_app_lock():
            sys.exit(1)

        # 打印诊断信息
        print_diagnostic_info()

        # 创建数据库管理器
        db_manager = DatabaseManager(config_manager)

        # 创建命令行界面
        cli = CommandLineInterface(config_manager, db_manager)

        try:
            # 处理命令行参数
            if args.help_paths:
                print_help_paths()
            elif args.interactive:
                cli.run_interactive()
            elif args.auto_find:
                cli.quota_analyzer.find_and_analyze_quota_files(non_interactive=args.all)
            elif args.analyze:
                quota_info = cli.quota_analyzer.analyze_file(args.analyze)
                if quota_info:
                    cli.quota_analyzer.display_quota_info(quota_info)
            elif args.history:
                limit = args.limit if args.limit else 10
                cli.quota_analyzer.display_history(limit=limit)
            elif args.filter:
                limit = args.limit if args.limit else 10
                cli.quota_analyzer.display_history(file_path=args.filter, limit=limit)
            else:
                # 如果没有提供参数，运行交互式界面
                cli.run_interactive()
        except KeyboardInterrupt:
            print(f"\n{t('operation_cancelled')}")
        except EOFError:
            print(f"\n{t('eof_interrupt')}")
            print(f"{t('use_command_line')}")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -A --all")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py -a /path/to/file.xml")
            print("  python JetBrainsAIQuotaAnalyzer_CLI.py --help")
        except Exception as e:
            print(f"{t('unexpected_error').format(error=e)}")
            print(f"{t('examples')}:")
            traceback.print_exc()

        # 关闭数据库连接
        db_manager.close()

        # 释放应用程序锁
        release_app_lock()
    except Exception as e:
        print(f"{t('unexpected_error').format(error=e)}")
        print(f"{t('examples')}:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
