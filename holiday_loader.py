import json
import os
from datetime import date
from typing import Dict, Any, Optional, List
from pathlib import Path

class HolidayLoader:
    """节假日数据加载器"""
    
    def __init__(self, holiday_dir: str = "holiday"):
        """
        初始化节假日加载器
        
        Args:
            holiday_dir: 节假日数据文件目录
        """
        self.holiday_dir = Path(holiday_dir)
        self._holiday_cache = {}  # 缓存已加载的节假日数据
        
    def load_holiday_data(self, year: int) -> Dict[str, Any]:
        """
        加载指定年份的节假日数据
        
        Args:
            year: 年份
            
        Returns:
            节假日数据字典
        """
        # 检查缓存
        if year in self._holiday_cache:
            return self._holiday_cache[year]
        
        # 构建文件路径
        file_path = self.holiday_dir / f"{year}.json"
        
        if not file_path.exists():
            # 如果文件不存在，返回空数据
            return {"year": year, "days": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 缓存数据
                self._holiday_cache[year] = data
                return data
        except Exception as e:
            print(f"加载节假日数据失败 {year}: {e}")
            return {"year": year, "days": []}
    
    def is_holiday(self, check_date: date) -> Dict[str, Any]:
        """
        判断指定日期是否为节假日
        
        Args:
            check_date: 要检查的日期
            
        Returns:
            包含节假日信息的字典
        """
        year = check_date.year
        date_str = check_date.strftime("%Y-%m-%d")
        
        # 加载节假日数据
        holiday_data = self.load_holiday_data(year)
        days = holiday_data.get("days", [])
        
        # 查找匹配的日期
        for day_info in days:
            if day_info.get("date") == date_str:
                is_off_day = day_info.get("isOffDay", False)
                holiday_name = day_info.get("name", "")
                
                return {
                    "is_holiday": is_off_day,
                    "is_workday": not is_off_day,
                    "holiday_name": holiday_name,
                    "type": "holiday" if is_off_day else "workday",
                    "source": "official"
                }
        
        # 如果没有找到法定节假日，检查是否为周末
        weekday = check_date.weekday()
        is_weekend = weekday >= 5  # 5=周六, 6=周日
        
        return {
            "is_holiday": is_weekend,
            "is_workday": not is_weekend,
            "holiday_name": "周末" if is_weekend else None,
            "type": "weekend" if is_weekend else "workday",
            "source": "weekend"
        }
    
    def get_holiday_info(self, check_date: date) -> Dict[str, Any]:
        """
        获取指定日期的完整节假日信息
        
        Args:
            check_date: 要检查的日期
            
        Returns:
            完整的节假日信息
        """
        holiday_info = self.is_holiday(check_date)
        
        return {
            "date": check_date.strftime("%Y-%m-%d"),
            "year": check_date.year,
            "month": check_date.month,
            "day": check_date.day,
            "weekday": {
                "number": check_date.weekday(),
                "name": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][check_date.weekday()],
                "english": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][check_date.weekday()]
            },
            "is_holiday": holiday_info["is_holiday"],
            "is_workday": holiday_info["is_workday"],
            "holiday_name": holiday_info["holiday_name"],
            "holiday_type": holiday_info["type"],
            "source": holiday_info["source"],
            "day_of_year": check_date.timetuple().tm_yday,
            "week_of_year": check_date.isocalendar()[1]
        }
    
    def get_year_holidays(self, year: int) -> List[Dict[str, Any]]:
        """
        获取指定年份的所有节假日信息
        
        Args:
            year: 年份
            
        Returns:
            节假日信息列表
        """
        holiday_data = self.load_holiday_data(year)
        days = holiday_data.get("days", [])
        
        result = []
        for day_info in days:
            date_str = day_info.get("date")
            if date_str:
                try:
                    check_date = date.fromisoformat(date_str)
                    holiday_info = self.get_holiday_info(check_date)
                    result.append(holiday_info)
                except ValueError:
                    continue
        
        return result
    
    def get_available_years(self) -> List[int]:
        """
        获取可用的年份列表
        
        Returns:
            可用年份列表
        """
        years = []
        for file_path in self.holiday_dir.glob("*.json"):
            try:
                year = int(file_path.stem)
                years.append(year)
            except ValueError:
                continue
        
        return sorted(years)
    
    def reload_cache(self):
        """重新加载缓存"""
        self._holiday_cache.clear()

# 全局实例
holiday_loader = HolidayLoader() 