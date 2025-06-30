from datetime import datetime, date
from typing import Dict, Any

# 中国节假日数据（2024-2025年）
HOLIDAYS_2024 = {
    "2024-01-01": {"name": "元旦", "type": "holiday"},
    "2024-02-10": {"name": "春节", "type": "holiday"},
    "2024-02-11": {"name": "春节", "type": "holiday"},
    "2024-02-12": {"name": "春节", "type": "holiday"},
    "2024-02-13": {"name": "春节", "type": "holiday"},
    "2024-02-14": {"name": "春节", "type": "holiday"},
    "2024-02-15": {"name": "春节", "type": "holiday"},
    "2024-02-16": {"name": "春节", "type": "holiday"},
    "2024-02-17": {"name": "春节", "type": "holiday"},
    "2024-02-18": {"name": "春节", "type": "holiday"},
    "2024-04-04": {"name": "清明节", "type": "holiday"},
    "2024-04-05": {"name": "清明节", "type": "holiday"},
    "2024-04-06": {"name": "清明节", "type": "holiday"},
    "2024-05-01": {"name": "劳动节", "type": "holiday"},
    "2024-05-02": {"name": "劳动节", "type": "holiday"},
    "2024-05-03": {"name": "劳动节", "type": "holiday"},
    "2024-05-04": {"name": "劳动节", "type": "holiday"},
    "2024-05-05": {"name": "劳动节", "type": "holiday"},
    "2024-06-10": {"name": "端午节", "type": "holiday"},
    "2024-09-15": {"name": "中秋节", "type": "holiday"},
    "2024-09-16": {"name": "中秋节", "type": "holiday"},
    "2024-09-17": {"name": "中秋节", "type": "holiday"},
    "2024-10-01": {"name": "国庆节", "type": "holiday"},
    "2024-10-02": {"name": "国庆节", "type": "holiday"},
    "2024-10-03": {"name": "国庆节", "type": "holiday"},
    "2024-10-04": {"name": "国庆节", "type": "holiday"},
    "2024-10-05": {"name": "国庆节", "type": "holiday"},
    "2024-10-06": {"name": "国庆节", "type": "holiday"},
    "2024-10-07": {"name": "国庆节", "type": "holiday"},
    # 调休工作日
    "2024-02-04": {"name": "春节调休", "type": "workday"},
    "2024-02-18": {"name": "春节调休", "type": "workday"},
    "2024-04-07": {"name": "清明节调休", "type": "workday"},
    "2024-04-28": {"name": "劳动节调休", "type": "workday"},
    "2024-05-11": {"name": "劳动节调休", "type": "workday"},
    "2024-09-14": {"name": "中秋节调休", "type": "workday"},
    "2024-09-29": {"name": "国庆节调休", "type": "workday"},
    "2024-10-12": {"name": "国庆节调休", "type": "workday"},
}

HOLIDAYS_2025 = {
    "2025-01-01": {"name": "元旦", "type": "holiday"},
    "2025-01-28": {"name": "春节", "type": "holiday"},
    "2025-01-29": {"name": "春节", "type": "holiday"},
    "2025-01-30": {"name": "春节", "type": "holiday"},
    "2025-01-31": {"name": "春节", "type": "holiday"},
    "2025-02-01": {"name": "春节", "type": "holiday"},
    "2025-02-02": {"name": "春节", "type": "holiday"},
    "2025-02-03": {"name": "春节", "type": "holiday"},
    "2025-04-04": {"name": "清明节", "type": "holiday"},
    "2025-04-05": {"name": "清明节", "type": "holiday"},
    "2025-04-06": {"name": "清明节", "type": "holiday"},
    "2025-05-01": {"name": "劳动节", "type": "holiday"},
    "2025-05-02": {"name": "劳动节", "type": "holiday"},
    "2025-05-03": {"name": "劳动节", "type": "holiday"},
    "2025-05-04": {"name": "劳动节", "type": "holiday"},
    "2025-05-05": {"name": "劳动节", "type": "holiday"},
    "2025-06-29": {"name": "端午节", "type": "holiday"},
    "2025-10-01": {"name": "国庆节", "type": "holiday"},
    "2025-10-02": {"name": "国庆节", "type": "holiday"},
    "2025-10-03": {"name": "国庆节", "type": "holiday"},
    "2025-10-04": {"name": "国庆节", "type": "holiday"},
    "2025-10-05": {"name": "国庆节", "type": "holiday"},
    "2025-10-06": {"name": "国庆节", "type": "holiday"},
    "2025-10-07": {"name": "国庆节", "type": "holiday"},
    # 调休工作日（2025年数据可能不完整，仅供参考）
    "2025-01-26": {"name": "春节调休", "type": "workday"},
    "2025-02-08": {"name": "春节调休", "type": "workday"},
}

def is_holiday(check_date: date) -> Dict[str, Any]:
    """判断指定日期是否为节假日"""
    date_str = check_date.strftime("%Y-%m-%d")
    year = check_date.year
    
    # 选择对应年份的节假日数据
    if year == 2024:
        holidays = HOLIDAYS_2024
    elif year == 2025:
        holidays = HOLIDAYS_2025
    else:
        # 对于其他年份，只判断周末
        holidays = {}
    
    # 检查是否为法定节假日
    if date_str in holidays:
        holiday_info = holidays[date_str]
        return {
            "is_holiday": holiday_info["type"] == "holiday",
            "is_workday": holiday_info["type"] == "workday",
            "holiday_name": holiday_info["name"],
            "type": holiday_info["type"]
        }
    
    # 检查是否为周末
    weekday = check_date.weekday()
    is_weekend = weekday >= 5  # 5=周六, 6=周日
    
    return {
        "is_holiday": is_weekend,
        "is_workday": not is_weekend,
        "holiday_name": "周末" if is_weekend else None,
        "type": "weekend" if is_weekend else "workday"
    }

def get_time_info() -> Dict[str, Any]:
    """获取详细的时间信息"""
    now = datetime.now()
    today = now.date()
    
    # 获取节假日信息
    holiday_info = is_holiday(today)
    
    # 获取农历信息（简化版）
    lunar_info = get_lunar_date(today)
    
    return {
        "timestamp": now.isoformat(),
        "date": today.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "weekday": {
            "number": now.weekday(),
            "name": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
            "english": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][now.weekday()]
        },
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "microsecond": now.microsecond,
        "is_holiday": holiday_info["is_holiday"],
        "is_workday": holiday_info["is_workday"],
        "holiday_name": holiday_info["holiday_name"],
        "holiday_type": holiday_info["type"],
        "lunar_date": lunar_info,
        "season": get_season(now.month),
        "quarter": (now.month - 1) // 3 + 1,
        "day_of_year": now.timetuple().tm_yday,
        "week_of_year": now.isocalendar()[1]
    }

def get_lunar_date(solar_date: date) -> Dict[str, Any]:
    """获取农历日期信息（简化版）"""
    # 这里使用简化的农历计算，实际项目中可以使用专门的农历库
    # 如 chinese_calendar 或 lunar_python
    
    # 简化实现：返回基本信息
    return {
        "lunar_year": "甲辰年",  # 2024年
        "lunar_month": "五月",
        "lunar_day": "十五",
        "zodiac": "龙",
        "festival": get_lunar_festival(solar_date)
    }

def get_lunar_festival(solar_date: date) -> str:
    """获取农历节日"""
    month = solar_date.month
    day = solar_date.day
    
    festivals = {
        (1, 1): "元旦",
        (2, 10): "春节",
        (4, 4): "清明节",
        (5, 1): "劳动节",
        (6, 10): "端午节",
        (9, 15): "中秋节",
        (10, 1): "国庆节",
    }
    
    return festivals.get((month, day), "")

def get_season(month: int) -> str:
    """获取季节"""
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    else:
        return "冬季" 