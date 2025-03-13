"""
namelist = ['直接材料成本差异', '直接人工标准成本差异', '变动制造费用成本差异','固定制造费用成本差异']
name = input('需要计算的标准成本差异:')
def Name(name):
    global C, cp_name
    if name in namelist:
        cp_name = input('请输入产品名称:')
        cp_number = int(input('输入生产该产品的数量:'))
        bz_time = 2
        if name == '直接材料标准成本差异':
            sj_use = float(input('实际耗用材料(单位：千克):'))
            cl_univalence = float(input('材料的单价:'))
            bz_use = 5.5
            bz_univalence = 2.2
            C = sj_use * cl_univalence - bz_use * bz_univalence * cp_number
        elif name == '直接人工标准成本差异':
            # cp_name = input('请输入产品名称:')
            # cp_number = int(input('输入生产该产品的数量:'))
            m = float(input('支付工资总额(单位:元)'))
            bz_mrate = 6
            C = m - cp_number * bz_time * bz_mrate
        elif name == '变动制造费用成本差异':
            VMC = float(input('实际发生变动制造费用(单位:元)'))
            bz_VMCrate = 3
            C = VMC - cp_number * bz_time * bz_VMCrate
        elif name == '固定制造费用成本差异':
            MC = float(input('实际发生固定制造费用(单位:元)'))
            bz_MCrate = 1.5
            C = MC - cp_number * bz_time * bz_MCrate
        return round(C, 2), cp_name,
C = list(Name(name))
print(f"{C[1]}{name}：\033[32m￥{C[0]:,.2f}\033[0m")  # 绿色显示总额
"""
import sys

# 标准参数配置（可根据需要修改）
STANDARD_HOURS = 2  # 标准工时
STANDARD_MATERIAL_USAGE = 5.5  # 标准材料用量（千克）
STANDARD_MATERIAL_PRICE = 2.2  # 标准材料单价（元/千克）
STANDARD_LABOR_RATE = 6  # 标准人工费率（元/小时）
STANDARD_VARIABLE_RATE = 3  # 变动制造费用标准费率（元/小时）
STANDARD_FIXED_RATE = 1.5  # 固定制造费用标准费率（元/小时）


def get_valid_input(prompt, input_type=float, min_val=None):
    """获取有效输入"""
    while True:
        try:
            value = input_type(input(prompt))
            if min_val is not None and value < min_val:
                print(f"输入值不能小于{min_val}，请重新输入")
                continue
            return value
        except ValueError:
            print("输入格式错误，请重新输入")


def calculate_material(cp_number):
    """处理直接材料成本差异"""
    sj_use = get_valid_input("实际耗用材料(千克): ", float, 0)
    cl_price = get_valid_input("材料实际单价(元/千克): ", float, 0)
    return sj_use * cl_price - STANDARD_MATERIAL_USAGE * STANDARD_MATERIAL_PRICE * cp_number


def calculate_labor(cp_number):
    """处理直接人工成本差异"""
    actual_wages = get_valid_input("实际支付工资总额(元): ", float, 0)
    return actual_wages - cp_number * STANDARD_HOURS * STANDARD_LABOR_RATE


def calculate_variable(cp_number):
    """处理变动制造费用差异"""
    actual_cost = get_valid_input("实际发生变动制造费用(元): ", float, 0)
    return actual_cost - cp_number * STANDARD_HOURS * STANDARD_VARIABLE_RATE


def calculate_fixed(cp_number):
    """处理固定制造费用差异"""
    actual_cost = get_valid_input("实际发生固定制造费用(元): ", float, 0)
    return actual_cost - cp_number * STANDARD_HOURS * STANDARD_FIXED_RATE


def main():
    """主程序"""
    cost_types = {'1': ('直接材料成本差异', calculate_material), '2': ('直接人工标准成本差异', calculate_labor),
        '3': ('变动制造费用成本差异', calculate_variable), '4': ('固定制造费用成本差异', calculate_fixed)}

    while True:
        print("\n标准成本差异计算系统")
        print("=" * 30)
        for k in cost_types:
            print(f"{k}. {cost_types[k][0]}")
        print("q. 退出系统")

        choice = input("\n请选择计算类型(输入编号): ").strip().lower()

        if choice == 'q':
            print("\n感谢使用，再见！")
            sys.exit()

        if choice not in cost_types:
            print("错误：无效的选项，请重新选择！")
            continue

        type_name, calculator = cost_types[choice]

        try:
            cp_name = input("请输入产品名称: ").strip()
            if not cp_name:
                raise ValueError("产品名称不能为空")

            cp_number = int(get_valid_input("生产数量(件): ", int, 1))

            variance = calculator(cp_number)

            print(f"\n{cp_name} {type_name}:")
            print(f"\033[32m￥{variance:+,.2f}\033[0m")  # 绿色显示，+号显示正负
            print("=" * 30)

        except Exception as e:
            print(f"发生错误：{str(e)}")


if __name__ == "__main__":
    main()