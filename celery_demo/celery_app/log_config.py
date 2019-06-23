import logging
import os.path
import time
from colorama import Fore,Style
import sys

"""
定义输出的颜色debug--white，info--green，warning/error/critical--red
:param msg: 输出的log文字
:return:
"""
class Logger(object):
    def __init__(self,logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger:  定义对应的程序模块名name，默认为root
        """
        # 创建一个logger
        self.logger = logging.getLogger(name = logger)

        # 指定最低的日志级别 critical > error > warning > info > debug
        self.logger.setLevel(logging.DEBUG)

        # 定义格式
        formatter = logging.Formatter("%(asctime)s - %(message)s")

        # 在控制台中输出
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)

        # 在文件中输出(如果有必要的话，要改colorama)
        """
        rq = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        log_path = os.getcwd() + "/logs/"
        log_name = log_path + rq + ".log"
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        """

        # 文件输出        
        #self.logger.addHandler(fh)文件输出

    def debug(self,msg):
        self.logger.debug(Style.BRIGHT + "[一般] - " + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        self.logger.info(Fore.BLUE + "[蓝色] - " + str(msg) + Style.RESET_ALL)
 
    def warning(self, msg):
        self.logger.warning(Fore.YELLOW + "[黄色] - " + str(msg) + Style.RESET_ALL)
 
    def error(self, msg):
        self.logger.error(Fore.CYAN + "[橙色] - " + str(msg) + Style.RESET_ALL)
 
    def critical(self, msg):
        self.logger.critical(Fore.RED  + "[红色] - " + str(msg) + Style.RESET_ALL)

# Create a logger object.
# 注意：此处不使用celery自带的logging模块，因为找不到到底它设置的入口在哪儿

#logger = logging.getLogger(__name__) 
#设置logger

#logger.setLevel(level=logging.INFO) 
#INFO级别的信息，就要输出

#formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
#只需要输出时间和信息

#handler = logging.StreamHandler()
#设置stdout的handler对象

#handler.setFormatter(formatter)
#handler加载格式

#logger.addHandler(handler)
#把handler加载进logger里

#formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(name)s - %(message)s")

