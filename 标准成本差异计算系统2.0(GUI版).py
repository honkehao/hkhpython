"""
标准成本差异计算系统（完整版）
版本: 3.0
功能说明：
1. 可视化GUI操作界面
2. 支持四种成本差异计算
3. 历史记录管理与Excel导出
4. 系统参数配置与实时修改
5. 完善的输入验证机制
"""

import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook

# ==================== 标准参数配置类 ====================
class StandardParams:
    """
    系统标准参数存储类
    使用类属性保存参数，支持动态修改
    参数说明：
    - HOURS: 标准工时（小时/件）
    - MATERIAL_USAGE: 标准材料用量（千克/件）
    - MATERIAL_PRICE: 标准材料单价（元/千克）
    - LABOR_RATE: 标准人工费率（元/小时）
    - VARIABLE_RATE: 变动制造费率（元/小时）
    - FIXED_RATE: 固定制造费率（元/小时）
    """
    HOURS = 2.0
    MATERIAL_USAGE = 5.5
    MATERIAL_PRICE = 2.2
    LABOR_RATE = 6.0
    VARIABLE_RATE = 3.0
    FIXED_RATE = 1.5


# ==================== 历史记录管理类 ====================
class HistoryManager:
    """历史记录管理类，负责存储和导出计算记录"""

    def __init__(self):
        """初始化历史记录存储结构"""
        self.records = []
        self.headers = ["序号", "产品名称", "产品数量", "计算类型", "结果"]

    def add_record(self, product_name, quantity, calc_type, result):
        """
        添加新记录
        :param product_name: 产品名称（字符串）
        :param quantity: 生产数量（整数）
        :param calc_type: 计算类型（字符串）
        :param result: 计算结果（浮点数）
        """
        self.records.append({
            "产品名称": product_name,
            "产品数量": quantity,
            "计算类型": calc_type,
            "结果": result
        })

    def export_excel(self, filename="历史记录.xlsx"):
        """
        导出历史记录到Excel文件
        :param filename: 导出文件名
        :return: 导出成功返回True，否则返回False
        """
        try:
            wb = Workbook()
            ws = wb.active
            ws.append(self.headers)
            for idx, record in enumerate(self.records, 1):
                ws.append([idx, record["产品名称"], record["产品数量"],
                          record["计算类型"], record["结果"]])
            # 自动调整列宽
            for col in ws.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                ws.column_dimensions[col[0].column_letter].width = max_length + 2
            wb.save(filename)
            return True
        except Exception as e:
            return False


# ==================== 参数修改对话框类 ====================
class ParamEditDialog(tk.Toplevel):
    """参数修改对话框，用于编辑系统标准参数"""

    def __init__(self, parent):
        """
        初始化对话框
        :param parent: 父窗口对象
        """
        super().__init__(parent)
        self.title("修改系统参数")
        self.parent = parent
        self.params_config = [
            ("标准工时（小时/件）", "HOURS", float, 0.1),
            ("标准材料用量（千克/件）", "MATERIAL_USAGE", float, 0.1),
            ("标准材料单价（元/千克）", "MATERIAL_PRICE", float, 0),
            ("标准人工费率（元/小时）", "LABOR_RATE", float, 0),
            ("变动制造费率（元/小时）", "VARIABLE_RATE", float, 0),
            ("固定制造费率（元/小时）", "FIXED_RATE", float, 0)
        ]
        self.entries = {}
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        """创建界面组件"""
        for idx, (label_text, attr_name, data_type, min_val) in enumerate(self.params_config):
            # 创建带当前值的标签
            current_value = getattr(StandardParams, attr_name)
            lbl_text = "{label} [当前值: {value:.2f}]".format(
                label=label_text,
                value=current_value
            )
            lbl = ttk.Label(self, text=lbl_text)

            # 创建输入框
            entry = ttk.Entry(self)
            entry.insert(0, str(current_value))
            self.entries[attr_name] = (entry, data_type, min_val)

            # 网格布局
            lbl.grid(row=idx, column=0, padx=5, pady=5, sticky=tk.E)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky=tk.W)

        # 操作按钮
        self.btn_confirm = ttk.Button(self, text="确认修改", command=self._validate_input)
        self.btn_cancel = ttk.Button(self, text="取消", command=self.destroy)

    def _setup_layout(self):
        """布局管理"""
        self.btn_confirm.grid(row=len(self.params_config), column=0, pady=10, sticky=tk.E)
        self.btn_cancel.grid(row=len(self.params_config), column=1, pady=10, sticky=tk.W)

    def _validate_input(self):
        """输入验证与处理"""
        try:
            for attr_name, (entry, data_type, min_val) in self.entries.items():
                input_value = entry.get().strip()
                if not input_value:
                    raise ValueError("参数值不能为空")

                # 类型转换验证
                try:
                    converted_value = data_type(input_value)
                except ValueError:
                    raise ValueError("请输入有效的{}值".format(data_type.__name__))

                # 范围验证
                if converted_value < min_val:
                    raise ValueError("数值不能小于 {:.2f}".format(min_val))

                # 更新参数
                setattr(StandardParams, attr_name, converted_value)

            messagebox.showinfo("成功", "参数修改已生效")
            self.destroy()
            self.parent.show_params()  # 刷新参数显示
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))


# ==================== 主应用程序类 ====================
class CostAnalysisApp(tk.Tk):
    """主应用程序类，负责界面布局和功能协调"""

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.title("标准成本差异分析系统 v3.0")
        self.geometry("900x650")
        self.history = HistoryManager()
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        """创建界面组件"""
        # 工具栏
        self.toolbar = ttk.Frame(self)

        # 功能按钮
        self.btn_material = ttk.Button(
            self.toolbar,
            text="材料成本差异",
            command=lambda: self._show_calculator("材料")
        )
        self.btn_labor = ttk.Button(
            self.toolbar,
            text="人工成本差异",
            command=lambda: self._show_calculator("人工")
        )
        self.btn_variable = ttk.Button(
            self.toolbar,
            text="变动费用差异",
            command=lambda: self._show_calculator("变动")
        )
        self.btn_fixed = ttk.Button(
            self.toolbar,
            text="固定费用差异",
            command=lambda: self._show_calculator("固定")
        )

        # 系统功能按钮
        self.btn_history = ttk.Button(self.toolbar, text="历史记录", command=self._show_history)
        self.btn_export = ttk.Button(self.toolbar, text="导出Excel", command=self._export_data)
        self.btn_params = ttk.Button(self.toolbar, text="查看参数", command=self.show_params)
        self.btn_edit = ttk.Button(self.toolbar, text="修改参数", command=self._show_edit_dialog)
        self.btn_exit = ttk.Button(self.toolbar, text="退出系统", command=self.destroy)

        # 历史记录表格
        self.tree = ttk.Treeview(self, columns=self.history.headers, show="headings")
        for col in self.history.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

    def _setup_layout(self):
        """布局管理"""
        # 工具栏布局
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        buttons = [
            self.btn_material, self.btn_labor, self.btn_variable, self.btn_fixed,
            self.btn_history, self.btn_export, self.btn_params, self.btn_edit, self.btn_exit
        ]
        for btn in buttons:
            btn.pack(side=tk.LEFT, padx=2)

        # 历史记录表格
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _show_calculator(self, calc_type):
        """显示计算对话框"""
        dialog = CalculationDialog(self, calc_type)
        self.wait_window(dialog)
        if dialog.result:
            self.history.add_record(*dialog.result)
            self._update_history()
            result_msg = "产品：{0}\n类型：{1}\n差异金额：￥{2:+,.2f}".format(
                dialog.result[0],
                dialog.result[2],
                dialog.result[3]
            )
            messagebox.showinfo("计算结果", result_msg)

    def _update_history(self):
        """更新历史记录表格"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, record in enumerate(self.history.records, 1):
            self.tree.insert("", "end", values=(
                idx,
                record["产品名称"],
                record["产品数量"],
                record["计算类型"],
                "￥{:+,.2f}".format(record["结果"])
            ))

    def _show_history(self):
        """显示历史记录"""
        self._update_history()

    def _export_data(self):
        """导出数据到Excel"""
        if self.history.export_excel():
            messagebox.showinfo("导出成功", "已成功导出到 历史记录.xlsx")
        else:
            messagebox.showerror("导出失败", "导出过程中发生错误")

    def show_params(self):
        """显示当前系统参数"""
        params = [
            ("标准工时", StandardParams.HOURS),
            ("标准材料用量", StandardParams.MATERIAL_USAGE),
            ("标准材料单价", StandardParams.MATERIAL_PRICE),
            ("标准人工费率", StandardParams.LABOR_RATE),
            ("变动制造费率", StandardParams.VARIABLE_RATE),
            ("固定制造费率", StandardParams.FIXED_RATE)
        ]
        param_list = ["{0}: {1:.2f}".format(name, value) for name, value in params]
        messagebox.showinfo("系统参数", "\n".join(param_list))

    def _show_edit_dialog(self):
        """显示参数修改对话框"""
        ParamEditDialog(self)


# ==================== 计算对话框类 ====================
class CalculationDialog(tk.Toplevel):
    """成本计算对话框，用于收集计算参数"""

    def __init__(self, parent, calc_type):
        """
        初始化对话框
        :param parent: 父窗口对象
        :param calc_type: 计算类型（材料/人工/变动/固定）
        """
        super().__init__(parent)
        self.title("{0}成本差异计算".format(calc_type))
        self.calc_type = calc_type
        self.result = None
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        """创建界面组件"""
        # 公共字段
        self.lbl_product = ttk.Label(self, text="产品名称：")
        self.ent_product = ttk.Entry(self)

        self.lbl_quantity = ttk.Label(self, text="生产数量：")
        self.ent_quantity = ttk.Entry(self)

        # 根据计算类型创建特定字段
        if self.calc_type == "材料":
            self.lbl_field1 = ttk.Label(self, text="实际材料用量（kg）：")
            self.lbl_field2 = ttk.Label(self, text="实际材料单价（元/kg）：")
            self.ent_field1 = ttk.Entry(self)
            self.ent_field2 = ttk.Entry(self)
        else:
            self.lbl_field1 = ttk.Label(self, text="实际费用（元）：")
            self.ent_field1 = ttk.Entry(self)
            self.lbl_field2 = None
            self.ent_field2 = None

        self.btn_calculate = ttk.Button(self, text="计算", command=self._validate_input)

    def _setup_layout(self):
        """布局管理"""
        rows = [
            (self.lbl_product, self.ent_product),
            (self.lbl_quantity, self.ent_quantity),
            (self.lbl_field1, self.ent_field1)
        ]
        if self.calc_type == "材料":
            rows.append((self.lbl_field2, self.ent_field2))

        for i, (lbl, ent) in enumerate(rows):
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)
            ent.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)

        self.btn_calculate.grid(row=len(rows), columnspan=2, pady=10)

    def _validate_input(self):
        """输入验证与计算"""
        try:
            # 基础验证
            product_name = self.ent_product.get().strip()
            if not product_name:
                raise ValueError("产品名称不能为空")

            quantity = self._validate_number(self.ent_quantity.get(), int, 1)

            # 根据计算类型进行验证
            if self.calc_type == "材料":
                usage = self._validate_number(self.ent_field1.get(), float, 0)
                price = self._validate_number(self.ent_field2.get(), float, 0)
                result = usage * price - quantity * StandardParams.MATERIAL_USAGE * StandardParams.MATERIAL_PRICE
            elif self.calc_type == "人工":
                wages = self._validate_number(self.ent_field1.get(), float, 0)
                result = wages - quantity * StandardParams.HOURS * StandardParams.LABOR_RATE
            else:
                cost = self._validate_number(self.ent_field1.get(), float, 0)
                rate = StandardParams.VARIABLE_RATE if self.calc_type == "变动" else StandardParams.FIXED_RATE
                result = cost - quantity * StandardParams.HOURS * rate

            self.result = (
                product_name,
                quantity,
                "直接{0}成本差异".format(self.calc_type),
                result
            )
            self.destroy()
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))

    def _validate_number(self, value, data_type, min_val):
        """
        通用数字验证方法
        :param value: 输入值
        :param data_type: 目标数据类型
        :param min_val: 最小值
        :return: 转换后的有效值
        """
        value = value.strip()
        if not value:
            raise ValueError("数值不能为空")
        try:
            converted = data_type(value)
        except ValueError:
            raise ValueError("请输入有效的{}值".format(data_type.__name__))
        if converted < min_val:
            raise ValueError("数值不能小于 {}".format(min_val))
        return converted


# ==================== 程序入口 ====================
if __name__ == "__main__":
    app = CostAnalysisApp()
    app.mainloop()