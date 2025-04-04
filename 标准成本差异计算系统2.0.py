"""
标准成本差异计算系统
版本: 1.2
功能说明:
1. 计算四种标准成本差异
2. 记录计算历史
3. 支持数据导出Excel
4. 参数配置管理
"""

import sys
from openpyxl import Workbook


# ==================== 标准参数配置类 ====================
class StandardParams:
    """
    存储系统标准参数的静态类
    所有参数使用类属性方式存储，便于集中管理
    参数说明：
    - HOURS: 每件产品标准工时(小时/件)
    - MATERIAL_USAGE: 每件产品标准材料用量(千克/件)
    - MATERIAL_PRICE: 标准材料单价(元/千克)
    - LABOR_RATE: 标准人工费率(元/小时)
    - VARIABLE_RATE: 变动制造费用标准费率(元/小时)
    - FIXED_RATE: 固定制造费用标准费率(元/小时)
    """
    HOURS = 2  # (小时/件)
    MATERIAL_USAGE = 5.5  # (千克/件)
    MATERIAL_PRICE = 2.2  # (元/千克)
    LABOR_RATE = 6  # (元/小时)
    VARIABLE_RATE = 3  # (元/小时)
    FIXED_RATE = 1.5  # (元/小时)


# ==================== 输入验证模块 ====================
def get_valid_input(prompt, input_type=float, min_val=None, max_val=None):
    """
    通用输入验证函数
    参数:
        prompt (str): 输入提示语
        input_type (type): 目标数据类型(float/int等)
        min_val (float): 允许的最小值
        max_val (float): 允许的最大值
    返回:
        value: 验证通过的有效值
    功能:
        1. 循环获取输入直到有效
        2. 检查数据类型有效性
        3. 检查数值范围有效性
        4. 提供友好的错误提示
    """
    while True:
        try:
            raw = input(prompt).strip()
            # 空值检查（特殊处理字符串类型）
            if input_type != str and not raw:
                raise ValueError("输入不能为空")

            value = input_type(raw)

            # 构建错误信息列表
            err_msg = []
            if min_val is not None and value < min_val:
                err_msg.append("不能小于{}".format(min_val))
            if max_val is not None and value > max_val:
                err_msg.append("不能大于{}".format(max_val))

            # 如果有错误则抛出异常
            if err_msg:
                raise ValueError("，".join(err_msg))

            return value
        except ValueError as e:
            print("输入错误：{}".format(str(e)))
        except Exception as e:
            print("发生未知错误：{}".format(str(e)))


# ==================== 成本计算模块 ====================
class CostCalculator:
    """
    成本差异计算器类
    包含各种成本差异计算的静态方法
    所有方法接收生产数量参数，返回差异计算结果
    """

    @staticmethod
    def material(cp_number):
        """
        计算直接材料成本差异
        公式：
            差异 = 实际用量 × 实际单价 - 标准用量 × 标准单价 × 产量
        参数:
            cp_number (int): 产品数量
        返回:
            float: 成本差异金额
        """
        sj_use = get_valid_input("实际耗用材料(千克): ", float, 0)
        cl_price = get_valid_input("材料实际单价(元/千克): ", float, 0)
        return sj_use * cl_price - StandardParams.MATERIAL_USAGE * StandardParams.MATERIAL_PRICE * cp_number

    @staticmethod
    def labor(cp_number):
        """
        计算直接人工成本差异
        公式：
            差异 = 实际工资总额 - 标准工时 × 标准费率 × 产量
        参数:
            cp_number (int): 产品数量
        返回:
            float: 成本差异金额
        """
        actual_wages = get_valid_input("实际支付工资总额(元): ", float, 0)
        return actual_wages - cp_number * StandardParams.HOURS * StandardParams.LABOR_RATE

    @staticmethod
    def variable(cp_number):
        """
        计算变动制造费用差异
        公式：
            差异 = 实际费用 - 标准工时 × 标准费率 × 产量
        参数:
            cp_number (int): 产品数量
        返回:
            float: 成本差异金额
        """
        actual_cost = get_valid_input("实际发生变动制造费用(元): ", float, 0)
        return actual_cost - cp_number * StandardParams.HOURS * StandardParams.VARIABLE_RATE

    @staticmethod
    def fixed(cp_number):
        """
        计算固定制造费用差异
        公式：
            差异 = 实际费用 - 标准工时 × 标准费率 × 产量
        参数:
            cp_number (int): 产品数量
        返回:
            float: 成本差异金额
        """
        actual_cost = get_valid_input("实际发生固定制造费用(元): ", float, 0)
        return actual_cost - cp_number * StandardParams.HOURS * StandardParams.FIXED_RATE


# ==================== 历史记录管理模块 ====================
class HistoryManager:
    """
    历史记录管理类
    功能：
    1. 存储计算记录
    2. 显示历史记录
    3. 导出Excel文件
    """

    def __init__(self):
        """初始化历史记录存储结构"""
        self.records = []  # 存储字典格式的记录
        self.headers = ["序号", "产品名称", "产品数量", "计算类型", "结果"]

    def add_record(self, cp_name, cp_number, calc_type, result):
        """
        添加新记录
        参数:
            cp_name (str): 产品名称
            cp_number (int): 产品数量
            calc_type (str): 计算类型名称
            result (float): 计算结果
        """
        self.records.append({"产品名称": cp_name, "产品数量": cp_number, "计算类型": calc_type, "结果": result})

    def show(self):
        """格式化显示历史记录"""
        print("\n【历史记录】")
        # 使用format进行列对齐格式化
        # {:<5}表示左对齐，占5字符宽度
        print("{:<5}{:<10}{:<10}{:<20}{:<15}".format(*self.headers))
        for idx, record in enumerate(self.records, 1):
            print("{:<5}{:<10}{:<10}{:<20}{:<+15,.2f}".format(idx, record["产品名称"], record["产品数量"], record["计算类型"],
                record["结果"]))

    def export_excel(self, filename="历史记录.xlsx"):
        """
        导出历史记录到Excel文件
        参数:
            filename (str): 导出文件名
        返回:
            bool: 导出是否成功
        """
        try:
            wb = Workbook()
            ws = wb.active

            # 设置标题行
            ws.append(self.headers)

            # 填充数据行
            for idx, record in enumerate(self.records, 1):
                ws.append([idx, record["产品名称"], record["产品数量"], record["计算类型"], record["结果"]])

            # 自动调整列宽（需要openpyxl 2.6+）
            for column in ws.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column[0].column_letter].width = adjusted_width

            wb.save(filename)
            return True
        except Exception as e:
            print("导出失败：{}".format(str(e)))
            return False


# ==================== 主程序模块 ====================
def main():
    """
    主程序入口函数
    功能：
    1. 显示系统菜单
    2. 处理用户输入
    3. 协调各模块工作
    """
    history = HistoryManager()  # 初始化历史记录管理器
    calc_map = {  # 计算类型映射表
        '1': ("直接材料成本差异", CostCalculator.material), '2': ("直接人工标准成本差异", CostCalculator.labor),
        '3': ("变动制造费用成本差异", CostCalculator.variable), '4': ("固定制造费用成本差异", CostCalculator.fixed)}

    while True:  # 主循环保持程序持续运行
        # 显示系统菜单
        print("\n{:=^30}".format(" 标准成本差异计算系统 "))
        # 打印计算类型选项
        for key in sorted(calc_map.keys()):
            print("{}. {}".format(key, calc_map[key][0]))
        # 打印系统功能选项
        print("{:<3}{}".format("q", "退出系统"))
        print("{:<3}{}".format("l", "查看历史记录"))
        print("{:<3}{}".format("c", "查看初始参数"))
        print("{:<3}{}".format("s", "导出历史记录"))

        # 获取用户输入
        choice = input("\n请选择操作编号: ").strip().lower()

        # 退出系统处理
        if choice == 'q':
            print("\n感谢使用，再见！")
            sys.exit()

        # 显示历史记录
        elif choice == 'l':
            history.show()

        # 显示参数配置
        elif choice == 'c':
            print("\n【系统参数配置】")
            params = [("标准工时", StandardParams.HOURS), ("标准材料用量", StandardParams.MATERIAL_USAGE),
                ("标准材料单价", StandardParams.MATERIAL_PRICE), ("标准人工费率", StandardParams.LABOR_RATE),
                ("变动制造费率", StandardParams.VARIABLE_RATE), ("固定制造费率", StandardParams.FIXED_RATE)]
            # 使用format对齐参数显示
            for name, value in params:
                print("{:<10}: {:<8}".format(name, value))

        # 导出Excel处理
        elif choice == 's':
            if history.export_excel():
                print("成功导出到 历史记录.xlsx")

        # 执行成本计算
        elif choice in calc_map:
            type_name, calculator = calc_map[choice]

            try:
                # 获取产品信息
                cp_name = input("请输入产品名称: ").strip()
                if not cp_name:
                    raise ValueError("产品名称不能为空")

                # 获取生产数量（至少1件）
                cp_number = int(get_valid_input("生产数量(件): ", int, 1))

                # 执行计算并存储结果
                result = calculator(cp_number)
                history.add_record(cp_name, cp_number, type_name, result)

                # 显示计算结果
                print("\n{0} {1}:".format(cp_name, type_name))
                # 使用ANSI转义码显示绿色文本，+号显示正负
                print("\033[32m￥{:+,.2f}\033[0m".format(result))
                print("{:=^30}".format(""))  # 分隔线

            except Exception as e:
                print("操作失败：{}".format(str(e)))

        # 无效选项处理
        else:
            print("无效的选项，请重新输入！")


# ==================== 程序启动 ====================
if __name__ == "__main__":
    """
    程序入口点说明：
    当直接运行本脚本时，执行main()函数
    当被其他模块导入时，不自动执行
    """
    main()