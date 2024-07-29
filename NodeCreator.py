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
from collections import OrderedDict
import threading


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("NodeCreator")

        # 设置窗口图标为 "logo.ico"
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, 'logo.ico')
        else:
            logo_path = 'logo.ico'
        self.window.iconbitmap(logo_path)

        # 原始节点输入框
        self.raw_node_label = tk.Label(window, text="原始节点")
        self.raw_node_label.grid(row=0, column=0, sticky='nsew')
        self.raw_node_text = tk.Text(window, height=10, undo=True)  # 启用撤销功能
        self.raw_node_text.grid(row=1, column=0, sticky='nsew')

        # IP列表输入框
        self.ip_list_label = tk.Label(window, text="IP列表")
        self.ip_list_label.grid(row=2, column=0, sticky='nsew')
        self.ip_list_text = tk.Text(window, height=10, undo=True)  # 启用撤销功能
        self.ip_list_text.grid(row=3, column=0, sticky='nsew')

        # IP类型下拉框
        self.ip_type_frame = tk.Frame(window)
        self.ip_type_frame.grid(row=4, column=0, sticky='nsew')
        self.ip_type_frame.columnconfigure(0, weight=1)

        self.inner_ip_type_frame = tk.Frame(self.ip_type_frame)
        self.inner_ip_type_frame.pack(anchor='center')

        self.ip_type_label = tk.Label(self.inner_ip_type_frame, text="IP类型：")
        self.ip_type_label.pack(side=tk.LEFT)

        self.ip_type_var = tk.StringVar(window)
        self.ip_type_var.set("自定义")
        self.ip_type_option = ttk.Combobox(self.inner_ip_type_frame, textvariable=self.ip_type_var,
                                           values=["自定义", "Cloudflare官方", "Cloudflare反代", "Cloudflare官方优选", "Cloudflare反代优选", "cfno1优选IP"], width=17)
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
        self.order_var.set("顺序")
        self.order_option = ttk.Combobox(self.inner_option_frame, textvariable=self.order_var, values=["顺序", "随机"],
                                         width=7)
        self.order_option.pack(side=tk.LEFT)

        self.result_num_label = tk.Label(self.inner_option_frame, text="   结果数量：")
        self.result_num_label.pack(side=tk.LEFT)

        self.result_num_entry = tk.Entry(self.inner_option_frame, width=10)
        self.result_num_entry.pack(side=tk.LEFT)

        self.space_label = tk.Label(self.inner_option_frame, text="   ")
        self.space_label.pack(side=tk.LEFT)

        # 生成节点按钮
        self.generate_button = tk.Button(self.inner_option_frame, text="点击生成节点", command=self.generate_nodes)
        self.generate_button.pack(side=tk.LEFT)

        # 生成节点输出框
        self.generated_node_label = tk.Label(window, text="生成节点")
        self.generated_node_label.grid(row=6, column=0, sticky='nsew')
        self.generated_node_text = tk.Text(window, height=20, state='disabled', undo=True)  # 启用撤销功能
        self.generated_node_text.grid(row=7, column=0, sticky='nsew')

        # 复制按钮
        self.copy_button = tk.Button(window, text="点击复制", command=self.copy_to_clipboard)
        self.copy_button.grid(row=8, column=0, sticky='nsew')

        # 设置网格权重
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=10)
        window.grid_rowconfigure(2, weight=1)
        window.grid_rowconfigure(3, weight=10)
        window.grid_rowconfigure(4, weight=1)
        window.grid_rowconfigure(5, weight=1)
        window.grid_rowconfigure(6, weight=1)
        window.grid_rowconfigure(7, weight=10)
        window.grid_rowconfigure(8, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # 绑定撤销快捷键
        self.bind_undo_redo()

        # 绑定空格键事件
        self.raw_node_text.bind("<space>", self.handle_space_press)
        self.ip_list_text.bind("<space>", self.handle_space_press)
        self.space_press_count = 0

    def bind_undo_redo(self):
        self.raw_node_text.bind("<Control-z>", lambda event: self.raw_node_text.edit_undo())
        self.raw_node_text.bind("<Control-y>", lambda event: self.raw_node_text.edit_redo())
        self.ip_list_text.bind("<Control-z>", lambda event: self.ip_list_text.edit_undo())
        self.ip_list_text.bind("<Control-y>", lambda event: self.ip_list_text.edit_redo())
        self.result_num_entry.bind("<Control-z>", lambda event: self.result_num_entry.delete(0, tk.END))  # 简单的撤销操作
        self.generated_node_text.bind("<Control-z>", lambda event: self.generated_node_text.edit_undo())
        self.generated_node_text.bind("<Control-y>", lambda event: self.generated_node_text.edit_redo())

        # 绑定粘贴事件，以便在粘贴前后添加撤销堆栈标记
        self.raw_node_text.bind("<Control-v>", self.handle_paste)
        self.ip_list_text.bind("<Control-v>", self.handle_paste)

    def handle_paste(self, event):
        widget = event.widget
        widget.edit_separator()  # 在粘贴前添加撤销堆栈标记
        widget.event_generate("<<Paste>>")
        widget.edit_separator()  # 在粘贴后添加撤销堆栈标记
        return "break"

    def handle_space_press(self, event):
        widget = event.widget
        cursor_index = widget.index(tk.INSERT)
        line_start = widget.index(f"{cursor_index} linestart")
        line_end = widget.index(f"{cursor_index} lineend")
        current_line = widget.get(line_start, line_end)

        if current_line.startswith("http://") or current_line.startswith("https://"):
            self.space_press_count += 1
            if self.space_press_count >= 3:
                self.space_press_count = 0
                try:
                    response = requests.get(current_line.strip())
                    response_content = response.text.strip()  # 使用 strip() 删除可能的尾随换行符或空格
                    widget.delete(line_start, line_end)
                    widget.insert(line_start, response_content)
                    # 直接设置光标位置到插入内容的末尾
                    widget.mark_set(tk.INSERT, f"{line_start}+{len(response_content)}c")
                except Exception as e:
                    messagebox.showerror("错误", f"无法获取URL内容: {e}")
        else:
            self.space_press_count = 0

    def update_ip_list(self, event):
        ip_type = self.ip_type_var.get()
        threading.Thread(target=self._update_ip_list_async, args=(ip_type,)).start()

    def _update_ip_list_async(self, ip_type):
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
                response = requests.get("https://ipdb.api.030101.xyz/?type=bestproxy&country=true")
                ip_list = response.text
            except:
                messagebox.showerror("错误", "无法获取IP列表，请手动输入")
                return
        elif ip_type == "cfno1优选IP":
            try:
                url = "https://cfno1.pages.dev/sub"
                response = requests.get(url)
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch URL: {url}")

                encoded_content = response.text.strip()
                decoded_content = base64.b64decode(encoded_content).decode('utf-8')

                pattern = re.compile(r'vless://[^\s@]+@(\d+\.\d+\.\d+\.\d+):(\d+)')
                matches = pattern.findall(decoded_content)

                ip_list = "\n".join([f"{ip}:{port} #{self.get_region(ip)}" for ip, port in matches])
            except Exception as e:
                messagebox.showerror("错误", f"无法获取IP列表: {e}")
                return
        else:
            ip_list = ""

        self.window.after(0, self._update_ip_list_ui, ip_list)

    def _update_ip_list_ui(self, ip_list):
        self.ip_list_text.delete('1.0', tk.END)
        self.ip_list_text.insert(tk.END, ip_list)

    def get_region(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode")
            if response.status_code == 200:
                data = response.json()
                return data.get("countryCode", "Unknown")
            else:
                return "Unknown"
        except Exception as e:
            return "Unknown"

    def generate_nodes(self):
        raw_node = self.raw_node_text.get("1.0", tk.END).strip()
        ip_list_input = self.ip_list_text.get("1.0", tk.END).strip()

        if not raw_node:
            messagebox.showerror("错误", "请输入节点")
            return
        if not ip_list_input:
            messagebox.showerror("错误", "请输入IP")
            return

        # 检查是否是URL
        if ip_list_input.startswith("http://") or ip_list_input.startswith("https://"):
            try:
                response = requests.get(ip_list_input)
                ip_list = response.text.strip().split('\n')
            except:
                messagebox.showerror("错误", "无法从URL获取IP列表，请检查URL")
                return
        else:
            ip_list = ip_list_input.split('\n')

        if raw_node.startswith("vmess://"):
            raw_node = raw_node.replace("vmess://", "").strip()
            raw_node = raw_node + '=' * ((4 - len(raw_node) % 4) % 4)
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

        expanded_ip_list = []
        for ip in ip_list:
            ip = ip.split('#')[0].strip()  # 忽略#及其之后的内容
            if not ip:
                continue
            if '*' in ip:
                for i in range(256):
                    expanded_ip_list.append(ip.replace('*', str(i)))
            elif '/' in ip:
                for ip in ipaddress.IPv4Network(ip):
                    expanded_ip_list.append(str(ip))
            else:
                expanded_ip_list.append(ip)

        # 如果结果数量大于IP列表中的IP总数，则使用IP列表中的IP总数
        if result_num > len(expanded_ip_list):
            result_num = len(expanded_ip_list)

        try:
            if protocol == "vmess":
                raw_node = base64.b64decode(raw_node).decode('utf-8')
                node = json.loads(raw_node)
                original_add = node['add']
                original_port = node['port']

                generated_nodes = OrderedDict()
                for i in range(result_num):
                    if order == '顺序':
                        ip_port = expanded_ip_list[i % len(expanded_ip_list)]
                    else:
                        ip_port = random.choice(expanded_ip_list)

                    ip, port = (ip_port.split(':') + [original_port])[:2]  # 分离IP和端口，如果没有端口则使用原来的端口
                    if ip.count(':') >= 2:  # 判断是否是IPv6地址
                        ip = '[' + ip + ']'
                    node['add'] = ip
                    node['port'] = port
                    if not node.get('host'):
                        node['host'] = original_add
                    node_key = "vmess://" + base64.b64encode(json.dumps(node).encode('utf-8')).decode('utf-8')
                    generated_nodes[node_key] = None

            elif protocol == "vless":
                pattern = re.compile(r'@([^:]+):(\d+)')
                match = pattern.search(raw_node)
                if not match:
                    messagebox.showerror("错误", "无法解析vless节点中的address和端口")
                    return
                original_address, original_port = match.groups()

                generated_nodes = OrderedDict()
                for i in range(result_num):
                    if order == '顺序':
                        ip_port_region = expanded_ip_list[i % len(expanded_ip_list)]
                    else:
                        ip_port_region = random.choice(expanded_ip_list)

                    ip_port, region = (ip_port_region.split('#') + [''])[:2]  # 分离IP和地区
                    ip, port = (ip_port.split(':') + [original_port])[:2]  # 分离IP和端口，如果没有端口则使用原来的端口
                    if ip.count(':') >= 2:  # 判断是否是IPv6地址
                        ip = '[' + ip + ']'
                    node_key = raw_node.replace(f"{original_address}:{original_port}", f"{ip}:{port}")
                    if region:
                        node_key += f" #{region}"
                    generated_nodes[node_key] = None

            self.generated_node_text.config(state='normal')
            self.generated_node_text.delete('1.0', tk.END)
            for node in generated_nodes.keys():
                self.generated_node_text.insert(tk.END, node + '\n')
            self.generated_node_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("错误", f"生成节点时出错: {e}")

    def copy_to_clipboard(self):
        generated_nodes = self.generated_node_text.get("1.0", tk.END).strip()
        if generated_nodes:
            self.window.clipboard_clear()
            self.window.clipboard_append(generated_nodes)
            node_count = len(generated_nodes.split('\n'))
            messagebox.showinfo("提示", f"已复制{node_count}条")
        else:
            messagebox.showerror("错误", "没有生成的节点可以复制")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
