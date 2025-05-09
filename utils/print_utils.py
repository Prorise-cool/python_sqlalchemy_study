"""
打印工具模块，提供彩色和结构化的打印函数。
"""

# ======== 彩色打印工具 ========
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}--- {text} ---{Colors.END}")

def print_subheader(text: str):
    print(f"\n{Colors.CYAN}{Colors.UNDERLINE}  {text}{Colors.END}")

def print_info(text: str):
    print(f"  {text}")

def print_success(text: str):
    print(f"{Colors.GREEN}  ✔ {text}{Colors.END}")

def print_warning(text: str):
    print(f"{Colors.WARNING}  ⚠️ [Warning] {text}{Colors.END}")

def print_error(text: str):
    print(f"{Colors.FAIL}  ❌ [Error] {text}{Colors.END}")

def print_sql(sql: str):
    print(f"{Colors.BLUE}    SQL: {sql.strip()}{Colors.END}")

def print_result_item(item, indent: int = 4):
    prefix = " " * indent
    if isinstance(item, dict):
        details = ", ".join([
            f"{Colors.BOLD}{key}{Colors.END}: {repr(value)}" for key, value in item.items()
        ])
        print(f"{prefix}Row({details})")
    else:
        print(f"{prefix}{repr(item)}")

# ======== END 彩色打印工具 ======== 