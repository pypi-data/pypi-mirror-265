import re
import argparse
from enum import Enum
from loguru import logger
from fdp_msg_check import utils

class MessageType(Enum):
    Unknown = 0
    NewOrder = 1
    OrderAccepted = 2
    OrderRejected = 3
    OrderCanceled = 4
    TradeReport = 5
    TradeReportConfirmation = 6

tag_to_name = {
    1: "Account",
    6: "AvgPx",
    8: "BeginString",
    9: "BodyLength",
    10: "CheckSum",
    11: "ClOrdID",
    14: "CumQty",
    17: "ExecID",
    20: "ExecTransType",
    31: "LastPx",
    32: "LastQty",
    34: "MsgSeqNum",
    35: "MsgType",
    37: "OrderID",
    38: "OrderQty",
    39: "OrdStatus",
    40: "OrdType",
    44: "Price",
    47: "Rule80A",
    48: "SecurityID",
    49: "SenderCompID",
    52: "SendingTime",
    54: "Side",
    55: "Symbol",
    56: "TargetCompID",
    58: "Text",
    59: "TimeInForce",
    60: "TransactTime",
    76: "ExecBroker",
    109: "ClientID",
    110: "MinQty",
    150: "ExecType",
    151: "LeavesQty",
    167: "SecurityType",
    198: "SecondaryOrderID",
    375: "ContraBroker",
    527: "SecondaryExecID",
    583: "ClOrdLinkID",
    851: "LastLiquidityInd",
    8031: "PrimaryLastPx",
    8032: "PrimaryBidPx",
    8033: "PrimaryAskPx",
    8051: "RoutingDecisionTime",
    8060: "OrderClassification",
    8169: "FsxTransactTime",
    8174: "SelfTradePreventionId",
    8465: "JSCCAccountNo",
}


class FIXMessage:
    def __init__(self, message_str: str):
        self.fields = {}
        self.parse_message(message_str)

    def parse_message(self, message_str: str):
        parts = message_str.split("|")
        for part in parts:
            if "=" in part:
                tag_str, value = part.split("=")
                tag = int(tag_str)
                if tag in tag_to_name:
                    self.fields[tag_to_name[tag]] = value
                else:
                    logger.error(f"Unknown or unsupported tag: {tag_str}")
                    continue

    def __str__(self):
        return "\n".join([f"{name}: {value}" for name, value in self.fields.items()])
    
    def avgpx_check(self):
        pass


def parse_message(line: str) -> FIXMessage:
    line = utils.replace_x01(line)
    line = utils.extract_fix_msg(line)
    if line is None or line == "":
        return None
    return FIXMessage(line)

def detect_message_type(line: str) -> MessageType:
    line = utils.replace_x01(line)
    msg_str = utils.extract_fix_msg(line)
    
    if re.search(r'\|35=D\|', msg_str):
        return MessageType.NewOrder
    
    if re.search(r'\|49=FSX_(SIT|UAT|PROD)_FDP\|', msg_str) and re.search(r'\|35=8\|', msg_str): 
        if re.search(r'\|20=0\|', msg_str):
            if re.search(r'\|39=0\|', msg_str):
                return MessageType.OrderAccepted
            elif re.search(r'\|39=8\|', msg_str):
                return MessageType.OrderRejected
            elif re.search(r'\|39=4\|', msg_str):
                return MessageType.OrderCanceled
            elif re.search(r'\|39=[12]\|', msg_str):
                return MessageType.TradeReport
        elif re.search(r'\|20=2\|', msg_str) and re.search(r'\|39=[12]\|', msg_str):
            return MessageType.TradeReportConfirmation
        else:
            return MessageType.Unknown
    else:
        return MessageType.Unknown

def not_check(msg: str) -> bool:
    return True

def normal_check(msg: FIXMessage) -> bool:
    if not msg.avgpx_check():
        return False
    return True

def check_order_accepted(msg: str) -> bool:
    fix_msg = parse_message(msg)
    return normal_check(fix_msg)

def check_order_rejected(msg: str) -> bool:
    fix_msg = parse_message(msg)
    return normal_check(fix_msg)

def check_order_canceled(msg: str) -> bool:
    fix_msg = parse_message(msg)
    return normal_check(fix_msg)

def check_trade_report(msg: str) -> bool:
    fix_msg = parse_message(msg)
    return normal_check(fix_msg)

def check_trade_report_confirmation(msg: str) -> bool:
    fix_msg = parse_message(msg)
    return normal_check(fix_msg)

check_functions = {
    MessageType.Unknown: not_check, 
    MessageType.NewOrder: not_check,
    MessageType.OrderAccepted: check_order_accepted,
    MessageType.OrderRejected: check_order_rejected,
    MessageType.OrderCanceled: check_order_canceled,
    MessageType.TradeReport: check_trade_report,
    MessageType.TradeReportConfirmation: check_trade_report_confirmation,
}

def check_log(log_filename: str) -> bool:
    try:
        result = True
        with open(log_filename, 'r') as file:
            for line in file:
                msg_type = detect_message_type(line)
                res = check_functions[msg_type](line)
                if not res:
                    result = False
                    msg = utils.extract_fix_msg(utils.replace_x01(line))
                    logger.error(f"Failed: {msg_type}, {msg}")
        return result  
    except FileNotFoundError:
        logger.error(f"File {log_filename} Not Found")
        return False
    except Exception as e:
        logger.error(f"Open {log_filename}, Exception: {e}")
        return False


def main():
    # 创建命令行解析器
    parser = argparse.ArgumentParser(description='FDP message Checker')
    parser.add_argument('log_filename', type=str, help='Path to the log file')

    # 解析命令行参数
    args = parser.parse_args()

    check_log(args.log_filename)

if __name__ == "__main__":
    main()