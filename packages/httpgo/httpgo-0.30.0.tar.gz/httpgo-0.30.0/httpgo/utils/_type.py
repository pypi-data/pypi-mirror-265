import json, typer
from click import ParamType
from rich import print

# from pydantic import HttpUrl, validate_arguments


# @validate_arguments
# def url(value: HttpUrl) -> HttpUrl:
#     """自定义Url类型提示,
#        使用pydantic对入参进行验证

#     Args:
#         value (HttpUrl): 控制台入参


#     Returns:
#         HttpUrl: 校验后直接return
#     """
#     return value
class UrlType(ParamType):
    """URL类型提示"""

    name = "URL"

    # def url_check(self, url: str):
    #     """基本的检查url格式

    #     Args:
    #         url (str): URL

    #     Raises:
    #         UrlVerifyError: _description_

    #     Returns:
    #         _type_: _description_
    #     """
    #     url_pattern = re.compile(
    #         r"^(https?|ftp)://"  # 协议部分，支持 http、https、ftp
    #         r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # 域名部分
    #         r"localhost|"  # localhost
    #         r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # IP 地址
    #         r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # IPv6 地址
    #         r"(?::\d+)?"  # 端口部分
    #         r"(?:/?|[/?]\S+)$",  # 路径和查询字符串部分
    #         re.IGNORECASE,
    #     )
    #     if url_pattern.match(url):
    #         return url
    #     else:
    #         raise UrlVerifyError

    def convert(self, value, param, ctx):
        # try:
        #     return self.url_check(value)
        # except UrlVerifyError as e:
        #     print("[bold red]Error:[/bold red]", e)
        #     raise typer.Exit()
        return value


class NameValueType(ParamType):
    """键值类型提示"""

    name = "<NAME VALUE> ..."


class JsonType(ParamType):
    """JSON类型提示并解析"""

    name = "JSON"


    def convert(self, value, param, ctx):
        """转化json为dict"""
        try:
            dict_data = json.loads(value)
        except json.JSONDecodeError:
            print(f"[bold red]Error:[/bold red]  '--json' / '-j': 无效json格式")
            raise typer.Exit()
        else:
            return dict_data
