import requests
import pandas as pd
import json
import sqlite3 as sql3

def get_college_info(college_id, conn):
	headers = {
		"accept": "application/json, text/plain, */*",
		"accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6",
		"cache-control": "no-cache",
		"origin": "https://www.gaokao.cn",
		"pragma": "no-cache",
		"priority": "u=1, i",
		"referer": "https://www.gaokao.cn/",
		"sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Windows"',
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-site",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
	}

	params = {"a": "www.gaokao.cn"}

	try:
		# print(f"正在获取学校信息: {college_id}")
		response = requests.get(
			f"https://static-data.gaokao.cn/www/2.0/school/{college_id}/info.json",
			params=params,
			headers=headers,
			timeout=10
		)
		response.raise_for_status()
		
		res_data = response.json().get("data")
		if not res_data:
			print(f"警告: 学校 {college_id} 返回空数据")
			return None
			
		# print(json.dumps(res_data, indent=2, ensure_ascii=False))
		return {
			k: str(v) if not isinstance(v, (str, int, float)) else v
			for k, v in res_data.items()
		}
		
	except requests.exceptions.RequestException as e:
		print(f"请求失败: {e}")
		return None
	except json.JSONDecodeError:
		print(f"响应不是有效的JSON: {response.text[:200]}")
		return None

def main():
	try:
		conn = sql3.connect(r"D:\SQLBASE\sdata.db")
		cur = conn.cursor()
		
		# 获取学校ID列表
		cur.execute("SELECT school_id FROM college")
		school_ids = [row[0] for row in cur.fetchall()]

		# 从college_info表中获取学校ID列表
		cur.execute("SELECT distinct school_id FROM college_info")	
		school_infos = [int(row[0]) for row in cur.fetchall()]
		for index_id, college_id in enumerate(school_ids):
			if college_id in school_infos:
				print(f"{index_id}: 学校信息已存在: {college_id}")
				continue	# 如果学校信息已存在，则跳过
			else:
				print(f"{index_id}: 学校信息不存在, 开始获取: {college_id}")
				data = get_college_info(college_id, conn)
				if data:
					df = pd.DataFrame([data])
					df.to_sql("college_info", conn, if_exists="append", index=False)
					print(f"{index_id}: 学校信息已成功保存到数据库: {college_id}")
				
	except requests.exceptions.RequestException as e:
		print(f"请求失败: {e}")
		
	except sql3.Error as e:
		print(f"数据库错误: {e}")
	finally:
		if conn:
			conn.commit()
			conn.close()
			print("数据库连接已关闭")

if __name__ == "__main__":
	main()
