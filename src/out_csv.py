import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import sys

# 出力するモダリティを選択
def select_modality():
    selected_modality = []
    """
    modalityを選択する

    Returns:
        [str]]: selected_modality[0]  ["CT", "XR", "ANGIO","PT"]のいずれかひとつ
    """
    root = tk.Tk()
    root.title("出力するModalityを選択")
    root.geometry("400x300")

    M = tk.Label(text='')
    label1 = tk.Label(text="Modalityを選択")
    label1.pack(padx=5, pady=5)

    # ct
    ct_btn = tk.Button(text="CT",
                       command=lambda: [selected_modality.append("CT"),
                                        root.destroy()])
    ct_btn.pack(padx=5, pady=5)

    # ANGIO
    ct_btn = tk.Button(text="ANGIO",
                       command=lambda: [selected_modality.append("ANGIO"),
                                        root.destroy()])
    ct_btn.pack(padx=5, pady=5)

    # XR
    ct_btn = tk.Button(text="SPECT",
                       command=lambda: [selected_modality.append("NM"),
                                        root.destroy()])
    ct_btn.pack(padx=5, pady=5)

    # pet テキストはPETだが，PTとして
    ct_btn = tk.Button(text="PET",
                       command=lambda: [selected_modality.append("PT"),
                                        root.destroy()])
    ct_btn.pack(padx=5, pady=5)
    
    auto_btn = tk.Button(text="終了",
                         command=lambda: sys.exit(0))
    auto_btn.pack(padx=5, pady=10)

    
    root.mainloop()

    return selected_modality[0]

def main():
    
    DB_path = './Resources/DONUTS.db'
    conn = sqlite3.connect(DB_path)
    
    table = select_modality()
    SQL = 'SELECT * FROM ' + table
    
    
    df = pd.read_sql_query(SQL,conn)
    conn.close()
    
    # filename = filedialog.asksaveasfilename()
    filename = filedialog.asksaveasfilename(
    title = "名前を付けて保存",
    filetypes = [("csv", ".csv")], # ファイルフィルタ
    initialdir = "./", # 自分自身のディレクトリ
    defaultextension = "csv"
    )
    df.to_csv(filename, header=True, index=None)

if __name__ == '__main__':
    main()