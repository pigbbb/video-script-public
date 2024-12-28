import requests
from langchain_community.utilities import WikipediaAPIWrapper

# 设置代理
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 自定义 WikipediaAPIWrapper 类
class CustomWikipediaAPIWrapper(WikipediaAPIWrapper):
    def run(self, query: str) -> str:
        try:
            # 设置代理和用户代理
            response = requests.get(
                url="https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "titles": query,
                    "prop": "extracts",  # 请求摘要信息
                    "exintro": True,  # 获取页面的简介（前几段）
                    "explaintext": True  # 返回纯文本格式的摘要
                },
                proxies=proxies,  # 使用代理
                #headers={"User-Agent": "MyPythonApp/1.0 (https://example.com/contact)"},

            )
            response.raise_for_status()
            result = response.json()
            print(result)
            pages = result.get("query", {}).get("pages", {})

            if pages:
                # 获取页面的信息
                page = list(pages.values())[0]
                title = page.get("title")
                extract = page.get("extract")

                # 检查是否获取到extract内容
                if extract:
                    return extract
                else:
                    return "No extract found"
            return "No pages found"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

# 查询函数
def search_wikipedia(subject):
    search = CustomWikipediaAPIWrapper()
    result = search.run(subject)
    return result

