import re
from loguru import logger

def replace_x01(input_line: str) -> str:
    return input_line.replace('\x01', '|')

def extract_fix_msg(input_line: str) -> str:
    match = re.search(r'8=FIX.+?\|10=.+?\|', input_line)
    if match:
        return match.group()
    else:
        return ""
    
def price_check(price: str, is_prod: bool) -> bool:
    try:
        price_float = float(price)
        return True
    except ValueError:
        logger.error(f"Invalid price. price: {price}")
        return False

def int_check(input: str, is_prod: bool) -> bool:
    try:
        input_int = int(input)
        return True
    except ValueError:
        logger.error("Invalid int")
        return False

def side_check(side: str, is_prod: bool) -> bool:
    return side == '1' or side == '2'

def symbol_check(symbol: str, is_prod: bool) -> bool:
    # 定义正则表达式模式，匹配 9 位数字
    pattern = r'^\d{9}$'
    
    # 使用正则表达式进行匹配
    if re.match(pattern, symbol):
        return True
    else:
        logger.error("Invalid symbol. Symbol must be a 9-digit number.")
        return False

def time_check(time_str: str, is_prod: bool) -> bool:
    # 定义正则表达式模式，匹配指定的时间格式
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$'
    
    # 使用正则表达式进行匹配
    if re.match(pattern, time_str):
        return True
    else:
        logger.error("Invalid time format. Time must be in the format: YYYY-MM-DD HH:MM:SS.sssssssss")
        return False