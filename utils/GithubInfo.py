import requests

from typing import Union


class OnwerInfo:
    def __init__(self,user_info_dict:dict[str,str]):
        self.uesr_name = user_info_dict['login']
        self.id = user_info_dict['id']
        self.home_page = user_info_dict['html_url']
        self.img_url = user_info_dict['avatar_url']

    def __repr__(self):
        attr_info = ''
        for attr in self.__dict__:
            attr_info += f'\n\t{attr} : {self.__dict__[attr]}'
        return attr_info
    
    def __str__(self):
        return self.__repr__()

class GithubInfo:

    def __init__(self,info_dict:dict):
        self.repo_name:str = info_dict['name']
        self.repo_href:str = info_dict['html_url']
        self.tag_href:str = self.repo_href + '/tags'
        self.star_href:str = self.repo_href + '/stargazers'
        self.fork_href:str = self.repo_href + '/forks'
        self.tag_count:str = self.__get_tag_count(info_dict['tags_url'])
        self.owner = OnwerInfo(info_dict['owner'])
        self.description:str = info_dict['description']
        self.stars_count:str = self.__get_count(info_dict['stargazers_count'])
        self.language:str = info_dict['language']
        self.forks_count:str = self.__get_count(info_dict['forks_count'])
        self.license: str = self.__dict_parser(info_dict['license'],'spdx_id')
        if self.license == 'NOASSERTION':
            self.license = 'Custom-License'
        self.license_href = '' if self.license is None else self.repo_href + '/blob/' + info_dict['default_branch'] + '/LICENSE'
        self.topics: list = info_dict['topics']
    
    def __get_tag_count(self,url:str):
        response = requests.get(url)
        return str(len(response.json()))
    
    @staticmethod
    def __get_count(value):

        def format_large_number(number):
            suffixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
            suffix_index = -1

            # 将 number 缩小到一定范围内，然后添加相应的后缀
            while number >= 1000 and suffix_index < len(suffixes) - 1:
                number /= 1000.0
                suffix_index += 1

            # 使用 round() 函数进行四舍五入并保留一位小数
            formatted_number = f"{round(number, 2)}{suffixes[suffix_index]}"
            return formatted_number
        
        if isinstance(value,str):
            value = int(value)
        
        if value<10000:
            return str(value)
        else:
            return format_large_number(value)
        
    @staticmethod
    def __dict_parser(param_dict:dict[str,str],key_in_dict:Union[list,str]):
        '''
        从字典解析参数
        - key_in_dict: 
          - list: 从字典中取多个参数，返回字典
          - str: 从字典中取单个参数，返回字符串
        - 若没有对应关键字则返回None
        '''
        if param_dict is None:
            return None
        if isinstance(key_in_dict,str):
            return param_dict.get(key_in_dict,None)
        elif isinstance(key_in_dict,list):
            param = dict()
            for key in key_in_dict:
                param[key] = param_dict.get(key,None)
            return param
    
    def __repr__(self):
        attr_info = ''
        for attr in self.__dict__:
            attr_info += f'{attr} : {self.__dict__[attr]}\n'
        return attr_info
    
    def __str__(self):
        return self.__repr__()