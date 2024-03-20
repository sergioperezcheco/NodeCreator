import tkinter as tk
from tkinter import messagebox, ttk
import base64
import json
import random
import ipaddress
import sys
import os
import re
import requests


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("批量生成节点")

        # 设置窗口图标为 "logo.ico"
        if getattr(sys, 'frozen', False):
            # 如果程序是被打包的，则从程序的当前目录加载图标文件
            logo_path = os.path.join(sys._MEIPASS, 'logo.ico')
        else:
            # 如果程序是被直接运行的，则从脚本的目录加载图标文件
            logo_path = 'logo.ico'
        self.window.iconbitmap(logo_path)

        # 原始节点输入框
        self.raw_node_label = tk.Label(window, text="原始节点")
        self.raw_node_label.grid(row=0, column=0, sticky='nsew')
        self.raw_node_text = tk.Text(window, height=10)
        self.raw_node_text.grid(row=1, column=0, sticky='nsew')

        # IP列表输入框
        self.ip_list_label = tk.Label(window, text="IP列表")
        self.ip_list_label.grid(row=2, column=0, sticky='nsew')
        self.ip_list_text = tk.Text(window, height=10)
        self.ip_list_text.grid(row=3, column=0, sticky='nsew')

        # IP类型下拉框
        self.ip_type_frame = tk.Frame(window)
        self.ip_type_frame.grid(row=4, column=0, sticky='nsew')
        self.ip_type_frame.columnconfigure(0, weight=1)  # 设置权重

        self.inner_ip_type_frame = tk.Frame(self.ip_type_frame)
        self.inner_ip_type_frame.pack(anchor='center')  # 居中

        self.ip_type_label = tk.Label(self.inner_ip_type_frame, text="IP类型：")
        self.ip_type_label.pack(side=tk.LEFT)

        self.ip_type_var = tk.StringVar(window)
        self.ip_type_var.set("自定义")  # 默认值
        self.ip_type_option = ttk.Combobox(self.inner_ip_type_frame, textvariable=self.ip_type_var,
                                           values=["自定义", "Cloudflare官方", "Cloudflare反代", "Cloudflare官方优选", "Cloudflare反代优选"], width=17)
        self.ip_type_option.pack(side=tk.LEFT)
        self.ip_type_option.bind("<<ComboboxSelected>>", self.update_ip_list)

        # 下拉框和结果数量输入框
        self.option_frame = tk.Frame(window)
        self.option_frame.grid(row=5, column=0, sticky='nsew')

        self.inner_option_frame = tk.Frame(self.option_frame)
        self.inner_option_frame.pack(anchor='center')

        self.result_num_label = tk.Label(self.inner_option_frame, text="生成方式：")
        self.result_num_label.pack(side=tk.LEFT)

        self.order_var = tk.StringVar(window)
        self.order_var.set("顺序")  # 默认值
        self.order_option = ttk.Combobox(self.inner_option_frame, textvariable=self.order_var, values=["顺序", "随机"],
                                         width=7)
        self.order_option.pack(side=tk.LEFT)

        self.result_num_label = tk.Label(self.inner_option_frame, text="   结果数量：")
        self.result_num_label.pack(side=tk.LEFT)

        self.result_num_entry = tk.Entry(self.inner_option_frame, width=10)
        self.result_num_entry.pack(side=tk.LEFT)

        # 添加一个包含三个空格的标签
        self.space_label = tk.Label(self.inner_option_frame, text="   ")
        self.space_label.pack(side=tk.LEFT)

        # 生成节点按钮
        self.generate_button = tk.Button(self.inner_option_frame, text="点击生成节点", command=self.generate_nodes)
        self.generate_button.pack(side=tk.LEFT)

        # 生成节点输出框
        self.generated_node_label = tk.Label(window, text="生成节点")
        self.generated_node_label.grid(row=6, column=0, sticky='nsew')
        self.generated_node_text = tk.Text(window, height=20, state='disabled')
        self.generated_node_text.grid(row=7, column=0, sticky='nsew')

        # 复制按钮
        self.copy_button = tk.Button(window, text="复制", command=self.copy_to_clipboard)
        self.copy_button.grid(row=8, column=0, sticky='nsew')

        # 设置网格权重
        window.grid_rowconfigure(0, weight=1)  # 原始节点标签
        window.grid_rowconfigure(1, weight=10)  # 原始节点输入框
        window.grid_rowconfigure(2, weight=1)  # IP列表标签
        window.grid_rowconfigure(3, weight=10)  # IP列表输入框
        window.grid_rowconfigure(4, weight=1)  # IP类型下拉框
        window.grid_rowconfigure(5, weight=1)  # 下拉框和结果数量输入框
        window.grid_rowconfigure(6, weight=1)  # 生成节点标签
        window.grid_rowconfigure(7, weight=10)  # 生成节点输出框
        window.grid_rowconfigure(8, weight=1)  # 复制按钮
        window.grid_columnconfigure(0, weight=1)

    # 感谢https://github.com/ymyuuu/IPDB 这一项目提供的IP
    def update_ip_list(self, event):
        ip_type = self.ip_type_var.get()
        if ip_type == "Cloudflare官方":
            ip_list = "173.245.48.0/20\n103.21.244.0/22\n103.22.200.0/22\n103.31.4.0/22\n141.101.64.0/18\n108.162.192.0/18\n190.93.240.0/20\n188.114.96.0/20\n197.234.240.0/22\n198.41.128.0/17\n162.158.0.0/15\n104.16.0.0/13\n104.24.0.0/14\n172.64.0.0/13\n131.0.72.0/22"
        elif ip_type == "Cloudflare反代":
            try:
                response = requests.get("https://ipdb.api.030101.xyz/?type=proxy")
                ip_list = response.text
            except:
                messagebox.showerror("错误", "无法获取IP列表，请手动输入")
                return
        elif ip_type == "Cloudflare官方优选":
            try:
                response = requests.get("https://ipdb.api.030101.xyz/?type=bestcf")
                ip_list = response.text
            except:
                messagebox.showerror("错误", "无法获取IP列表，请手动输入")
                return
        elif ip_type == "Cloudflare反代优选":
            try:
                response = requests.get("https://ipdb.api.030101.xyz/?type=bestproxy")
                ip_list = response.text
            except:
                messagebox.showerror("错误", "无法获取IP列表，请手动输入")
                return
        else:
            ip_list = ""
        self.ip_list_text.delete('1.0', tk.END)
        self.ip_list_text.insert(tk.END, ip_list)

    def generate_nodes(self):
        # 获取原始节点和IP列表，处理字符串
        raw_node = self.raw_node_text.get("1.0", tk.END).strip()
        ip_list = self.ip_list_text.get("1.0", tk.END).strip().split('\n')

        if not raw_node:
            messagebox.showerror("错误", "请输入节点")
            return
        if not ip_list[0]:
            messagebox.showerror("错误", "请输入IP")
            return

        if raw_node.startswith("vmess://"):
            raw_node = raw_node.replace("vmess://", "").strip()  # 移除 "vmess://" 前缀
            raw_node = raw_node + '=' * ((4 - len(raw_node) % 4) % 4)  # 确保字符串长度是4的倍数
            protocol = "vmess"
        elif raw_node.startswith("vless://"):
            protocol = "vless"
        else:
            messagebox.showerror("错误", "只支持vmess和vless节点")
            return

        order = self.order_var.get()
        try:
            result_num = int(self.result_num_entry.get())
            if result_num <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "结果数量必须是正整数")
            return

        # 处理 IP 列表，支持 IP 地址段和通配符
        expanded_ip_list = []
        for ip in ip_list:
            if '*' in ip:  # 通配符
                for i in range(256):
                    expanded_ip_list.append(ip.replace('*', str(i)))
            elif '/' in ip:  # IP 地址段
                for ip in ipaddress.IPv4Network(ip):
                    expanded_ip_list.append(str(ip))
            else:  # 单个 IP 地址
                expanded_ip_list.append(ip)

        try:
            if protocol == "vmess":
                # 解析原始节点
                raw_node = base64.b64decode(raw_node).decode('utf-8')
                node = json.loads(raw_node)
                host = node['add']

                # 生成新节点
                generated_nodes = set()  # 使用集合自动移除重复项
                for i in range(result_num):
                    if order == '顺序':
                        ip = expanded_ip_list[i % len(expanded_ip_list)]
                    else:  # 随机
                        ip = random.choice(expanded_ip_list)

                    # 处理 IP 地址
                    if ':' in ip:  # IPv6
                        ip = '[' + ip + ']'
                    node['add'] = ip
                    node['host'] = host
                    generated_nodes.add("vmess://" + base64.b64encode(json.dumps(node).encode('utf-8')).decode('utf-8'))
            elif protocol == "vless":
                # 解析原始节点
                node = raw_node
                host = re.search(r'@(.+?):', node).group(1)

                # 生成新节点
                generated_nodes = set()  # 使用集合自动移除重复项
                for i in range(result_num):
                    if order == '顺序':
                        ip = expanded_ip_list[i % len(expanded_ip_list)]
                    else:  # 随机
                        ip = random.choice(expanded_ip_list)

                    # 处理 IP 地址
                    if ':' in ip:  # IPv6
                        ip = '[' + ip + ']'
                    generated_nodes.add(node.replace(host, ip))

            # 更新生成节点输出框
            self.generated_node_text.config(state='normal')
            self.generated_node_text.delete('1.0', tk.END)
            self.generated_node_text.insert(tk.END, '\n'.join(generated_nodes))
            self.generated_node_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def copy_to_clipboard(self):
        # 复制生成的节点到剪贴板
        generated_nodes = self.generated_node_text.get("1.0", tk.END).strip().split('\n')
        self.window.clipboard_clear()
        if generated_nodes == ['']:
            messagebox.showinfo("提示", "已复制0条")
        else:
            self.window.clipboard_append('\n'.join(generated_nodes))
            messagebox.showinfo("提示", f"已复制{len(generated_nodes)}条")


window = tk.Tk()
app = App(window)
window.mainloop()
