"""Optimized version of gaokao/main.py with improved structure and error handling"""

import sys
import logging
import time
from typing import Optional, Tuple, List, Dict, Any
from ctypes import cdll, c_char_p, create_string_buffer
import requests
import sqlite3
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("gaokao_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DLL_PATH = Path("gaokao/bestV8_win64.dll")
JS_FILE_PATH = Path("gaokao/webspack_gaokao.js")
DATA_PATH = Path(r"D:\SQLBASE\sdata.db")
INIT_URL_TEMPLATE = (
    "https://api.eol.cn/web/api/?keyword=&page={}&province_id=&ranktype=&request_type=1"
    "&size=20&top_school_id=[1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375]"
    "&type=&uri=apidata/api/gkv3/school/lists"
)

HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.gaokao.cn',
    'priority': 'u=1, i',
    'referer': 'https://www.gaokao.cn/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
}

class DatabaseManager:
    """管理数据库连接和操作"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = self._create_db_connection()
        self.cur = self.conn.cursor()
        
    def _create_db_connection(self) -> sqlite3.Connection:
        """创建数据库连接"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=-10000")  # 10MB cache
            return conn
        except sqlite3.Error as e:
            logger.error(f"数据库连接错误: {e}")
            raise
            
    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> bool:
        """批量插入数据"""
        if not data:
            return False
            
        try:
            df = pd.DataFrame(data)
            df.to_sql(table_name, self.conn, if_exists="append", index=False)
            return True
        except Exception as e:
            logger.error(f"插入数据失败: {e}")
            return False
            
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class GaokaoScraper:
    """高考数据爬取器"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    def __init__(self):
        self._validate_files()
        self.db_manager = DatabaseManager(str(DATA_PATH))

    def _validate_files(self) -> None:
        """Validate required files exist"""
        if not DLL_PATH.exists():
            raise FileNotFoundError(f"DLL file not found: {DLL_PATH}")
        if not JS_FILE_PATH.exists():
            raise FileNotFoundError(f"JS file not found: {JS_FILE_PATH}")

    def get_encrypt_value(self, data: str) -> Optional[str]:
        """Encrypt data using V8 DLL"""
        if sys.platform != "win32":
            raise Exception("Only Windows system is supported")

        try:
            cur = cdll.LoadLibrary(str(DLL_PATH))
            result = bytes(20000)
            cur.runJs.argtypes = (c_char_p, c_char_p)
            cur.runJs(create_string_buffer(data.encode('utf8')), result)
            return result.rstrip(b"\x00").decode('utf-8')
        except Exception as e:
            logger.error(f"Error loading DLL or running JS: {e}")
            return None

    def generate_js_code(self, init_url: str) -> str:
        """生成用于加密的JavaScript代码"""
        return f"""
        j = "{init_url}"
        t = {{"SIGN": "D23ABC@#56", str: j.replace(/^\/|https?:\/\/\/?/, "")}}
        result = chook(360)(v(t))
        result
"""

    def gen_signsafe(self, page: int = 1) -> Optional[str]:
        """生成signsafe参数"""
        init_url = INIT_URL_TEMPLATE.format(page)
        new_part = self.generate_js_code(init_url)
        
        try:
            js_code = JS_FILE_PATH.read_text(encoding='utf-8') + '\n' + new_part
            return self.get_encrypt_value(js_code)
        except Exception as e:
            logger.error(f"Error generating signsafe: {e}")
            return None

    def get_page_json(self, page: int = 1) -> Optional[Tuple[List[Dict[str, Any]], int]]:
        """获取指定页面的JSON数据"""
        logger.info(f"开始获取第 {page} 页数据...")
        
        for attempt in range(self.MAX_RETRIES):
            try:
                signsafe = self.gen_signsafe(page)
                if not signsafe:
                    logger.error("生成signsafe参数失败")
                    return None

                json_data = {
                    'keyword': '',
                    'page': page,
                    'province_id': '',
                    'ranktype': '',
                    'request_type': 1,
                    'signsafe': signsafe,
                    'size': 20,
                    'top_school_id': '[1169,1159,435,457,436,589,459,3269,3117,434,1551,3374,3375]',
                    'type': '',
                    'uri': 'apidata/api/gkv3/school/lists',
                }

                url = INIT_URL_TEMPLATE.format(page) + "&signsafe=" + signsafe
                logger.debug(f"请求URL: {url}")
                
                response = requests.post(
                    headers=HEADERS,
                    url=url,
                    json=json_data,
                    timeout=30
                )
                
                response.raise_for_status()
                logger.debug(f"响应状态码: {response.status_code}")
                
                res_json = response.json()
                logger.debug(f"完整响应: {res_json}")
                
                if res_json.get("code") == 403:
                    logger.error("403 禁止访问 - 访问被拒绝")
                    return None
                    
                if not res_json.get("data"):
                    logger.error("响应中没有数据")
                    return None
                    
                res_lst = res_json.get("data").get("item")
                res_num_found = res_json.get("data").get("numFound")
                
                if not res_lst or not res_num_found:
                    logger.error(f"响应中缺少必要字段，完整响应: {res_json}")
                    return None
                    
                logger.info(f"成功获取第 {page} 页数据，共 {len(res_lst)} 条记录")
                return res_lst, res_num_found
                
            except requests.RequestException as e:
                logger.warning(f"第 {page} 页请求失败，尝试次数 {attempt + 1}/{self.MAX_RETRIES}: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                    continue
                logger.error(f"第 {page} 页请求最终失败: {e}")
                return None

    def loop_get_json(self, start_page: int = 1) -> None:
        """循环获取所有页面数据并保存到数据库"""
        try:
            with self.db_manager as db:
                page_result = self.get_page_json(start_page)
                if not page_result or not page_result[1]:
                    logger.error("获取初始页面数据失败或numFound为None")
                    return
                    
                res_lst_first, res_num_found = page_result
                
                if not db.insert_data("college", res_lst_first):
                    logger.error("插入第一页数据失败")
                    return
                
                try:
                    total_page = res_num_found // 20 + 1
                except TypeError:
                    logger.error("num_found值无效，无法计算总页数")
                    return
                    
                for i in range(start_page + 1, total_page + 1):
                    page_res = self.get_page_json(i)
                    if page_res:
                        page_res_lst, _ = page_res
                        if not db.insert_data("college", page_res_lst):
                            logger.error(f"插入第 {i} 页数据失败")
                            continue
                        logger.info(f"第 {i} 页完成")
                        
                logger.info("所有页面数据获取完成")
        except Exception as e:
            logger.error(f"loop_get_json 发生错误: {e}")
            raise

if __name__ == "__main__":
    try:
        scraper = GaokaoScraper()
        scraper.loop_get_json(start_page=1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
