import argparse
import logging
import os

from GithubCard import GithubCard

logging.basicConfig(level=logging.INFO,format='[%(asctime)s - %(levelname)s] %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='获取Github 项目简介卡片')

    # 添加参数步骤
    parser.add_argument('-r', '--repo',type=str,required=True,help='the repo name',dest='repo_name')
    parser.add_argument('-o','--output',type=str,required=False,help='output file name, optional, default is img/owner_repo.svg',dest='output_name')

    # 解析参数步骤  
    args = parser.parse_args()
    repo_name = args.repo_name
    card = GithubCard.generateSvg(repo_name=repo_name,svg_name=args.output_name)