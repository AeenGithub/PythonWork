"""Optimized version of gaokao/main.py with improved structure and error handling"""

import sys
import logging
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

class GaokaoScraper:
    def __init__(self):
        self.conn = self._create_db_connection()
        self.cur = self.conn.cursor()
        self._validate_files()

    def _create_db_connection(self) -> sqlite3.Connection:
        """Create and return a database connection"""
        try:
            conn = sqlite3.connect(DATA_PATH)
            conn.execute("PRAGMA journal_mode=WAL")
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

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
        """Generate JavaScript code for encryption"""
        return f"""
j = "{init_url}"
t = {{"SIGN": "D23ABC@#56", str: j.replace(/^\/|https?:\/\/\/?/, "")}}
result = chook(360)(v(t))
result
"""

    def gen_signsafe(self, page: int = 1) -> Optional[str]:
        """Generate signsafe parameter"""
        init_url = INIT_URL_TEMPLATE.format(page)
        new_part = self.generate_js_code(init_url)
        
        try:
            js_code = JS_FILE_PATH.read_text(encoding='utf-8') + '\n' + new_part
            return self.get_encrypt_value(js_code)
        except Exception as e:
            logger.error(f"Error generating signsafe: {e}")
            return None

    def get_page_json(self, page: int = 1) -> Optional[Tuple[List[Dict[str, Any]], int]]:
        """Get JSON data for a specific page"""
        logger.info(f"Getting page {page}...")
        
        # Generate signsafe parameter
        signsafe = self.gen_signsafe(page)
        if not signsafe:
            logger.error("Failed to generate signsafe parameter")
            return None

        # Prepare request data
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

        try:
            # Make API request
            url = INIT_URL_TEMPLATE.format(page) + "&signsafe=" + signsafe
            logger.debug(f"Making request to: {url}")
            
            response = requests.post(
                headers=HEADERS,
                url=url,
                json=json_data,
                timeout=30
            )
            
            # Check response status
            response.raise_for_status()
            logger.debug(f"Response status: {response.status_code}")
            
            # Parse JSON response
            res_json = response.json()
            logger.debug(f"Response JSON: {res_json}")
            
            # Check for API errors
            if res_json.get("code") == 403:
                logger.error("403 Forbidden - Access denied")
                return None
                
            if not res_json.get("data"):
                logger.error("No data in response")
                return None
                
            res_lst = res_json.get("data").get("item")
            res_num_found = res_json.get("data").get("num_found")
            
            if not res_lst or not res_num_found:
                logger.error("Missing required data fields in response")
                return None
                
            logger.info(f"Successfully got page {page} with {len(res_lst)} items")
            return res_lst, res_num_found
            
        except requests.RequestException as e:
            logger.error(f"Request failed for page {page}: {e}")
            return None

    def loop_get_json(self, start_page: int = 1) -> None:
        """Loop through all pages and save data to database"""
        try:
            page_result = self.get_page_json(start_page)
            if not page_result or not page_result[1]:
                logger.error("Failed to get initial page data or num_found is None")
                return
                
            res_lst_first, res_num_found = page_result
            df_first = pd.DataFrame(res_lst_first)
            df_first.to_sql("college", self.conn, if_exists="append", index=False)
            
            try:
                total_page = res_num_found // 20 + 1
            except TypeError:
                logger.error("Invalid num_found value, cannot calculate total pages")
                return
            for i in range(start_page + 1, total_page + 1):
                page_res = self.get_page_json(i)
                if page_res:
                    page_res_lst, _ = page_res
                    df = pd.DataFrame(page_res_lst)
                    df.to_sql("college", self.conn, if_exists="append", index=False)
                    logger.info(f"Page {i} done.")
                    
            logger.info("All pages done.")
        except Exception as e:
            logger.error(f"Error in loop_get_json: {e}")
            raise
        finally:
            self.conn.close()

if __name__ == "__main__":
    try:
        scraper = GaokaoScraper()
        scraper.loop_get_json(start_page=1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
