import inspect
from collections import defaultdict

class Logger:
    _print_stats = defaultdict(int)
    
    @staticmethod
    def optimized_print(message):
        """优化的打印函数"""
        caller_frame = inspect.stack()[1]
        caller_location = f"{caller_frame.filename}:{caller_frame.lineno}"
        
        if Logger._print_stats[caller_location] == 0:
            print(message)
        Logger._print_stats[caller_location] += 1
        
        if Logger._print_stats[caller_location] % 10 == 0:
            print(f"调用位置 '{caller_location}' 的消息已打印 {Logger._print_stats[caller_location]} 次\n",message)