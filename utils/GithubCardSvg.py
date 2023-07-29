import base64
import logging
import re
import requests
from typing import Union

from .emoji import emoji
from .GithubInfo import GithubInfo
from .language_color import language_color_dict
from .svg_entities import svg_entities

class GithubCardSvg:

    star_info = (
        '<g transform="matrix(1,0,0,1,{icon_x},{icon_y})">'
        '<a target="_blank" href="{href}">'
        '<path fill="#656d76" stroke="none" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"></path>'
        '</a>'
        '</g>'        
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<a target="_blank" href="{href}">'
        '<text fill="#656d76" fill-opacity="1" stroke="none" x="{info_x}" y="{info_y}" font-family="sans-serif" '
        'font-size="12" font-weight="400" font-style="normal">{info}</text>'
        '</a>'
        '</g>'
    )

    fork_info = (
        '<g transform="matrix(1,0,0,1,{icon_x},{icon_y})">'
        '<a target="_blank" href="{href}">'
        '<path fill="#656d76" stroke="none" d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"></path>'
        '</a>'
        '</g>'
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<a target="_blank" href="{href}">'
        '<text fill="#656d76" fill-opacity="1" stroke="none" x="{info_x}" y="{info_y}" font-family="sans-serif" '
        'font-size="12" font-weight="400" font-style="normal">{info}</text>'
        '</a>'
        '</g>'
    )

    tag_info = (
        '<g transform="matrix(1,0,0,1,{icon_x},{icon_y})">'
        '<a target="_blank" href="{href}">'
        '<path fill="#656d76" stroke="none" d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.752 1.752 0 0 1 1 7.775Zm1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"></path>'
        '</a>'
        '</g>'
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<a target="_blank" href="{href}">'
        '<text fill="#656d76" fill-opacity="1" stroke="none" x="{info_x}" y="{info_y}" font-family="sans-serif" '
        'font-size="12" font-weight="400" font-style="normal">{info}</text>'
        '</a>'
        '</g>'
    )

    license_info = (
        '<g transform="matrix(1,0,0,1,{icon_x},{icon_y})">'
        '<a target="_blank" href="{href}">'
        '<path fill="#656d76" stroke="none" d="M8.75.75V2h.985c.304 0 .603.08.867.231l1.29.736c.038.022.08.033.124.033h2.234a.75.75 0 0 1 0 1.5h-.427l2.111 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.006.005-.01.01-.045.04c-.21.176-.441.327-.686.45C14.556 10.78 13.88 11 13 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L12.178 4.5h-.162c-.305 0-.604-.079-.868-.231l-1.29-.736a.245.245 0 0 0-.124-.033H8.75V13h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5V3.5h-.984a.245.245 0 0 0-.124.033l-1.289.737c-.265.15-.564.23-.869.23h-.162l2.112 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.016.015-.045.04c-.21.176-.441.327-.686.45C4.556 10.78 3.88 11 3 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L2.178 4.5H1.75a.75.75 0 0 1 0-1.5h2.234a.249.249 0 0 0 .125-.033l1.288-.737c.265-.15.564-.23.869-.23h.984V.75a.75.75 0 0 1 1.5 0Zm2.945 8.477c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L13 6.327Zm-10 0c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L3 6.327Z"></path>'
        '</a>'
        '</g>'
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<a target="_blank" href="{href}">'
        '<text fill="#656d76" fill-opacity="1" stroke="none" x="{info_x}" y="{info_y}" font-family="sans-serif" '
        'font-size="12" font-weight="400" font-style="normal">{info}</text>'
        '</a>'
        '</g>'
    )

    language = (
        '<circle cx="25" cy="{circle_y}" r="7" stroke="none" fill="{color}"></circle>'
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<text fill="#24292e" fill-opacity="1" stroke="none" x="{language_x}" y="{language_y}" font-family="sans-serif" '
        'font-size="12" font-weight="400" font-style="normal">{language}</text>'
        '</g>'
    )

    descript_element = (
        '<g fill="#586069" fill-opacity="1" stroke="#586069" stroke-opacity="1" '
        'stroke-width="1" stroke-linecap="square" stroke-linejoin="bevel" '
        'transform="matrix(1,0,0,1,0,0)">'
        '<text fill="#586069" fill-opacity="1" stroke="none" x="17" y="{y}" '
        'font-family="sans-serif" font-size="14" font-weight="550" font-style="normal">'
        '{content}</text></g>'
    )

    owner = (
        '<g transform="matrix(1,0,0,1,0,0)">'
        '<a target="_blank" href="{owner_href}">'
        '<circle cx="25" cy="56" r="12" stroke="#afb8c1" stroke-width="1.5" fill="none" />'
        '<image stroke="null" id="svg_1" height="24" width="24" x="13" y="44" clip-path="url(#circleClip)" href="data:image/png;base64,{img}"/>'
        '</a>'
        '</g>'
        '<g transform="matrix(1,0,0,1,25,0)">'
        '<a target="_blank" href="{owner_href}">'
        '<text fill="#000000" fill-opacity="1" stroke="none" xml:space="preserve" x="17" y="59.5" '
        'font-family="sans-serif" font-size="15" font-weight="540" font-style="normal">{owner}</text>'
        '</a>'
        '</g>'
    )

    repo = (
        '<g fill="#586069" fill-opacity="1" stroke="none" transform="matrix(1.25,0,0,1.25,18,18)">'
        '<path vector-effect="none" fill-rule="evenodd" d="M4,9 L3,9 L3,8 L4,8 L4,9 M4,6 L3,6 L3,7 L4,7 L4,6 M4,4 L3,4 L3,5 L4,5 L4,4 M4,2 L3,2 L3,3 L4,3 L4,2 M12,1 L12,13 C12,13.55 11.55,14 11,14 L6,14 L6,16 L4.5,14.5 L3,16 L3,14 L1,14 C0.45,14 0,13.55 0,13 L0,1 C0,0.45 0.45,0 1,0 L11,0 C11.55,0 12,0.45 12,1 M11,11 L1,11 L1,13 L3,13 L3,12 L6,12 L6,13 L11,13 L11,11 M11,1 L2,1 L2,10 L11,10 L11,1"></path>'
        '</g>'
        '<g fill="#0366d6" fill-opacity="1" stroke="#0366d6" stroke-opacity="1" stroke-width="1" '
        'stroke-linecap="square" stroke-linejoin="bevel" transform="matrix(1,0,0,1,25,0)">'
        '<a target="_blank" href="{repo_href}">'
        '<text fill="#0366d6" fill-opacity="1" stroke="none" xml:space="preserve" x="17" y="33" '
        'font-family="sans-serif" font-size="18" font-weight="630" '
        'font-style="normal">{repo_name}</text>'
        '</a>'
        '</g>'
    )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="422" height="{height}"\n\tversion="1.2" baseProfile="tiny" data-reactroot="">\n'
        '<defs>'
        '<clipPath id="circleClip">'
        '<circle cx="25" cy="56" r="12" />'
        '</clipPath>'
        '</defs>'
        '<g fill="none" stroke="black" stroke-width="1" fill-rule="evenodd" stroke-linecap="square" stroke-linejoin="bevel">'
        '<g fill="#ffffff" fill-opacity="1" stroke="none" transform="matrix(1,0,0,1,0,0)">'
        '<rect x="0" y="0" width="420" height="{height}"></rect>'
        '</g>'
        '<rect x="0" y="0" width="421" height="{height}" stroke="#eaecef" stroke-width="2"></rect>'
        '<g transform="matrix(1,0,0,1,0,-3)">{body}</g>'
        '</g>'
        '</svg>'
    )

    word_re = re.compile(r'[\u4e00-\u9fff]|[a-zA-Z0-9]+(?!=[\u4e00-\u9fff])|[^\u4e00-\u9fff\w\s]|\s',re.S)

    @staticmethod
    def __create_info(template:str, icon_x:int, icon_y:int,
                      info:str, href:str):
        info_x = icon_x + 21
        info_y = icon_y + 12
        next_x = info_x + 8*len(info)
        return template.format(icon_x = icon_x, icon_y = icon_y,
                               info_x = info_x, info_y = info_y, 
                               info = info, href = href),next_x

    @classmethod
    def __create_language(cls, circle_y:int, language:Union[str,None]):
        language_x = 35
        language_y = circle_y + 4
        if language is None:
            language = 'None'
            color = '#000000'
        else:
            color = language_color_dict.get(language,'#000000')
        en_char_len = 8
        cn_char_len = 16
        en_count = 0
        cn_count = 0
        for char in language:
            if '\u4e00' <= char <= '\u9fff':
                cn_count += 1
            else:
                en_count += 1
        next_x = cn_count*cn_char_len + en_count*en_char_len + language_x

        return cls.language.format(circle_y = circle_y, language_x = language_x,
                                   language_y = language_y, color = color, 
                                   language = language),next_x
    
    @staticmethod
    def __render_emoji(desc:str):
        # Split the string using lookbehind and lookahead regex pattern
        chunks = re.split(r'(?<=\s)|(?=\s)', desc)

        # Define a dictionary mapping symbols to emojis (assuming it's defined somewhere in the code)
        
        result = [emoji[chunk] if chunk in emoji else chunk for chunk in chunks]

        # Join the chunks to form the final string
        return "".join(result)
    
    
    @classmethod
    def __description_to_lines(cls,description:str):
        words = cls.word_re.findall(description)
        line = ""
        lines = []
        length = 0
        for word in words:
            line += word
            if ord(word)>255:
                length += 16
            else:
                length += 8*len(word)
            
            if length>380:
                lines.append(line)
                line = ""
                length=0
        if line != "":
            line = ''.join(svg_entities.get(c, c) for c in line)
            lines.append(line)
        return lines

    @classmethod
    def ___do_create_description(cls,description_lines:list):
        y = 86
        diff = 21
        desc = ''
        for line in description_lines:
            e = cls.descript_element.format(y = y, content = line)
            desc += e
            y += diff
        return desc, y - diff

    @classmethod
    def ___create_description(cls,description:str):
        desc_with_emoji = cls.__render_emoji(description)
        desc_lines = cls.__description_to_lines(desc_with_emoji)
        desc,last_desc_y= cls.___do_create_description(desc_lines)
        return desc,last_desc_y

    @classmethod
    def __create_owner(cls,img:bytes,href:str,owner:str):
        img_base64 = base64.b64encode(img).decode('utf-8')
        return cls.owner.format(img=img_base64,owner_href=href,owner=owner)

    @classmethod
    def __create_repo(cls,repo_href:str,repo_name:str):
        return cls.repo.format(repo_href=repo_href,repo_name=repo_name)

    @classmethod
    def create_svg(cls,info:GithubInfo):
        logging.info('构建repo')
        # 构建repo部分
        repo_part = cls.__create_repo(repo_href=info.repo_href,repo_name=info.repo_name)

        logging.info('构建owner')
        # 构建owner部分
        img_url = info.owner.img_url
        response = requests.get(img_url)
        if response.status_code !=200:
            raise Exception(f'download img error with code {response.status_code} and msg {response.text}')
        owner_part = cls.__create_owner(img = response.content,href = info.owner.home_page,owner=info.owner.uesr_name)

        logging.info('构建description')
        # 构建description部分
        desc_part,desc_last_y = cls.___create_description(description=info.description)
        language_y = desc_last_y + 18
        next_y = desc_last_y + 10
        # 构建language部分
        language_part,next_x = cls.__create_language(circle_y=language_y,language=info.language)

        logging.info('构建info')
        # 构建各个info部分
        ## star info
        star_part,next_x = cls.__create_info(template=cls.star_info,icon_x = next_x+16,icon_y = next_y,info=info.stars_count,href=info.star_href)
        ## fork info
        fork_part,next_x = cls.__create_info(template=cls.fork_info,icon_x = next_x+16,icon_y = next_y,info=info.forks_count,href=info.fork_href)
        ## tag info
        tag_part,next_x = cls.__create_info(template=cls.tag_info,icon_x = next_x+16, icon_y = next_y,info=info.tag_count,href = info.tag_href)
        ## license
        if info.license is not None:
            li = info.license
            license_part,next_x = cls.__create_info(template=cls.license_info,icon_x = next_x+16, icon_y=next_y,info=li,href=info.license_href)
        else:
            license_part = ''

        logging.info('生成svg')
        body_content = repo_part + owner_part + desc_part + language_part + star_part + fork_part + tag_part + license_part
        svg = cls.svg.format(body=body_content,height = desc_last_y+33)
        return svg

    @classmethod
    def test(cls,img:bytes,href:str,owner:str):
        return cls.__create_owner(img=img,href=href,owner=owner)
    
    