import logging
import os
import requests
from typing import Union
from urllib.parse import urlparse

from utils.GithubCardSvg import GithubCardSvg
from utils.GithubInfo import GithubInfo

class GithubCard:
    base = 'https://api.github.com/repos/{}'
    def __init__(self,repo_name=Union[str,None]):
        pass

    @classmethod
    def __getInfo(cls,url):
        headers = {'Content-Type': 'charset=utf-8'}
        response = requests.get(url,headers=headers)
        if response.status_code != 200:
            err = response.json().get('message')
            raise Exception(f'get repo info fail!, url:{url}, status code:{response.status_code}, err msg:{err}')
        
        info = response.json()
        return GithubInfo(info)

    @staticmethod
    def is_valid_url(url:str):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @classmethod
    def generateSvg(cls,repo_name:str,svg_name:Union[str,None]):
        url = cls.base.format(repo_name)
        if cls.is_valid_url(url) is False:
            logging.ERROR(f'repo format error: {repo_name}')
            raise ValueError(f'repo format error: {repo_name}')
        
        info = cls.__getInfo(url)
        logging.info(f'get github info:\n{info}')
        # 创建svg图像
        svg = GithubCardSvg.create_svg(info)
        if svg_name is None:
            if os.path.exists('img') is False:
                os.mkdir('img')
            svg_name_list = repo_name.split('/')
            svg_name = '_'.join(svg_name_list)
            svg_name = svg_name + '.svg'
            svg_name = os.path.join('img',svg_name)
        logging.info(f'saving svg file as {svg_name}...')
        with open(svg_name,'w',encoding='utf-8') as f:
            f.write(svg)
        return svg
