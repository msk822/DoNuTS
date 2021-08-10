import datetime
import gc
import json
import os
import sqlite3
import sys
import time
import tkinter as tk
from tkinter import messagebox

import pandas as pd
import pydicom

import DataBase
import donuts_datasets
import funcs

sys.path.append("./")


def main():
    # tkでモダリティーを選択する
    MODALITY = funcs.select_modality()

    if MODALITY in ["CT", "NM", "ANGIO", "PT"]:
        print("{} が選択されました".format(MODALITY))
    else:
        print("Auto Mode が選択されました")

    # コンソールの作成
    # console_root = tk.Tk()
    # console_root.title("Modalityを選択")
    # console_root.geometry("500x400")
    
    # button_exit = tk.Button(console_root,
    #                         text='終了',
    #                         command=lambda: sys.exit(0))
    # button_exit.pack(padx=5, pady=10)
    # button_exit.update()
    
    print("{} が選択されました".format(MODALITY))
    # label1 = tk.Label(console_root,
    #                   text=MODALITY + "が選択されました")
    # label1.pack(padx=5, pady=5)

    # label2 = tk.Label(console_root,
    #                   text='**************************処理開始****************************')
    # label2.pack(padx=5, pady=5)

    print('**************************処理開始****************************')
    # desktop_dir = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '/Desktop'
    desktop_dir = os.path.expanduser("~") + '/Desktop'
    dicom_directory = funcs.select_directory(desktop_dir)

    # DICOMファイルを取得
    dicom_files = funcs.get_dicom_files(dicom_directory)

    # RDSR, Modalityのファイルを分割
    if int(len(dicom_files)) == 0:
        messagebox.showerror('エラー', 'DICOMファイルが存在しません')
        sys.exit(0)

    else:
        if MODALITY != "Auto":
            rdsr_files_dict, modality_files_dict = funcs.separate_dicom_files(dicom_files=dicom_files,
                                                                    MODALITY=MODALITY)

        else:
            rdsr_files_dict, modality_files_dict = funcs.separate_rdsr_dicom_files_and_identify_each_modality(
                dicom_files=dicom_files)
            
            
        print("見つかったRDSRファイル : {}".format(funcs.show_len_identified(rdsr_files_dict)))
        # label3 = tk.Label(console_root,
        #                     text="見つかったRDSRファイル : " + funcs.show_len_identified(rdsr_files_dict))
        # label3.pack(padx=5, pady=5)
        # label3.update()
        
        if MODALITY != "Auto":
            print("見つかったRDSRファイル : {}".format(funcs.show_len_identified(modality_files_dict)))
            # label4 = tk.Label(console_root,
            #                     text="見つかったModalityファイル : " + funcs.show_len_identified(modality_files_dict))
            # label4.pack(padx=5, pady=5)
            # label4.update()



    num_rdsr = funcs.count_rdsr(rdsr_files_dict)
    if num_rdsr == 0:
        messagebox.showerror('エラー', 'RDSRファイルが存在しません')
        sys.exit(0)

    elif num_rdsr == 0 and funcs.count_rdsr(modality_files_dict) == 0:
        messagebox.showerror('エラー', '処理可能なファイルが見つかりません．\nプログラムを終了します.')
        sys.exit()
            

    del dicom_files, num_rdsr
    gc.collect()
    
    # RDSRの処理
    # ここにデータを書き込む
    rdsr_data = []
    new_data_cnt = 0
    duplicate_data_cnt = 0
    
    for _modality in rdsr_files_dict:
        
        # PT, NMの情報（RadionuclideTotalDose）をmodality_fileから取得
        if _modality in ['PT', 'NM']:
            
            try:
                # {uniuqecode:DOSE}
                RadionuclideTotalDose_dict = funcs.extract_RadionuclideTotalDose(modality_files_dict, _modality)
            except:
                pass
            
        
        
        if _modality != 'Unknown':
            
            # モダリティ別のrdsr_filesを取得
            rdsr_files = rdsr_files_dict[_modality]
            
            # テンプレートファイルを読み込む
            try:
                # if MODALITY == 'Auto':
                #     _M = 'Auto'
                # else:
                #     _M = _modality
                _M = _modality
                temp_dict = donuts_datasets.return_json_temprate(MODALITY=_M)
            except:
                print("テンプレートファイルを読み込めません．")
                sys.exit(0)
            
            if len(rdsr_files) !=0:
                # RDSRのメイン処理
                try:
                    # 各データのevent数をリストで保存
                    events_dict = funcs.get_events_from_rdsr(rdsr_files, MODALITY=_modality)
                    #     >>>  {'0':'3',
                    #     >>>   '1':'6'}
                
                
                    # total_events = funcs.calc_total_event(events_dict)
                    # Acquisition データの取得
                    Acquisition_set = []
                    for r in rdsr_files:
                        Acquisition_set.append(
                            funcs.separate_Acquisition(r, MODALITY=_modality))

                    i = 0
                    # ファイルとその照射回数を読み込む
                    for r, c1, event_key in zip(rdsr_files, Acquisition_set, events_dict.keys()):
                        event_cnt = int(events_dict[event_key])  # 3, 6 int

                        # 照射回数分だけデータを書き込む
                        # 情報をtemp_dictに書き込んでいき，ループするたびにrdsr_dataに追加．
                        # ループがひとつ終了するとtemp_dictの値を削除し，再び書き込んでいく．
                        for e_c in range(event_cnt):
                            c2 = c1[e_c]  # c2:pydicom.dataelem.DataElement
                            if _modality in ["CT", "PT"]:
                                try:
                                    # acquisition
                                    acquisition_value = funcs.extract_data_from_CT_Acquisition(
                                        temp_dict, c2)
                                except:
                                    pass
                            elif _modality == "ANGIO":
                                # ANGIOのAcquisition を取得する
                                try:
                                    acquisition_value = funcs.extract_data_from_angio_Acquisition(
                                        temp_dict, c2)
                                except:
                                    pass
                            elif _modality == "NM":
                                pass
                            
                            
                            # Acquisition data を書き込む
                            temp_dict.update(acquisition_value)
                            
                            
                            # header情報を書き込む
                            for data_key in temp_dict.keys():
                                try:
                                    value = str(getattr(r, data_key))
                                    temp_dict[data_key] = value
                                except:
                                    pass    
                            temp_dict['Identified Modality'] = _modality
                            
                            if _modality in ['PT', 'NM']:
                                try:
                                    # temp_dictにRadionuclideTotalDoseを書き込む
                                    each_unique_code = str(r.PatientID) + str(r.StudyDate)
                                    for u_c in RadionuclideTotalDose_dict.keys():
                                        if u_c == each_unique_code:
                                            temp_dict['RadionuclideTotalDose'] = RadionuclideTotalDose_dict[u_c]
                                except:
                                    pass
                                
                            if _modality in ["CT", "PT"]:
                                CTDoseLengthProductTotal = funcs.extract_CT_Dose_Length_Product_Total(rdsr_files=r)
                                temp_dict['CTDoseLengthProductTotal'] = CTDoseLengthProductTotal
                            
                            temp_dict['PRIMARY KEY'] = str(i) + '_' + temp_dict['SOPInstanceUID']
                            # rdsr_dataに取得した値を追加
                            rdsr_data.append(temp_dict.copy())
                            
                            # PRIMARY_KEYが同じデータを書き込もうとするとエラーになるため，tryで行う．
                            try:
                                write_list = [v for v in temp_dict.values()]
                                DATABASE = DataBase.WriteDB(MODALITY=_modality)
                                DATABASE.main(data=write_list)
                                new_data_cnt += 1
                            except :
                                duplicate_data_cnt += 1
                            
                            # temp_dictのclear
                            temp_dict = funcs.clear_dict_value(temp_dict)
                            i += 1
                            
                            
                            
                    
                        
                except:
                    pass
            
           
                # RDSRファイル数が0でmodality_fileが0でないとき（NMなど）
            elif len(rdsr_files_dict[_modality])==0 and len(modality_files_dict[_modality])!=0:
                # header情報のみを書き込む
                for i,m in enumerate(modality_files_dict[_modality]):
                    
                    # headerを書き込む
                    for data_key in temp_dict.keys():
                        try:
                            value = str(getattr(m, data_key))
                            temp_dict[data_key] = value
                        except:
                            pass    
                    temp_dict['Identified Modality'] = _modality
                    
                    # temp_dictにRadionuclideTotalDoseを書き込む
                    each_unique_code = str(m.PatientID) + str(m.StudyDate)
                    for u_c in RadionuclideTotalDose_dict.keys():
                        if u_c == each_unique_code:
                            temp_dict['RadionuclideTotalDose'] = RadionuclideTotalDose_dict[u_c]
                    
                    temp_dict['PRIMARY KEY'] = str(i) + '_' + temp_dict['SOPInstanceUID']
                    # rdsr_dataに取得した値を追加
                    rdsr_data.append(temp_dict.copy())
                    
                    # PRIMARY_KEYが同じデータを書き込もうとするとエラーになるため，tryで行う．
                    try:
                        write_list = [v for v in temp_dict.values()]
                        DATABASE = DataBase.WriteDB(MODALITY=_modality)
                        DATABASE.main(data=write_list)
                        DATABASE.close()
                        new_data_cnt += 1
                    except :
                        duplicate_data_cnt += 1
                    
                    # temp_dictのclear
                    temp_dict = funcs.clear_dict_value(temp_dict)
                    i += 1
                    
                    # temp_dictのclear
                    temp_dict = funcs.clear_dict_value(temp_dict)
                    
            else:
                 pass

    del rdsr_files_dict,modality_files_dict,rdsr_files,temp_dict,_modality
    gc.collect()
    
    # for _modality in modality_files_dict:
        
        
    all_dict = donuts_datasets.return_json_temprate(MODALITY="Auto")
    DATABASE = DataBase.WriteDB(MODALITY="Auto")
    for each_rdsr_data in rdsr_data:
        all_dict.update(each_rdsr_data)

        write_list = [v for v in all_dict.values()]
        DATABASE.main(data=write_list)
    DATABASE.close()

    # jsonおよびcsvとしてデータを保存
    save_name = './Resources/' + MODALITY + '_out_'
    
    file_name_json = save_name + str(datetime.date.today()) + ".json"
    file_name_csv = save_name + str(datetime.date.today()) + ".csv"

    # json
    with open(file_name_json, mode='wt', encoding='utf-8') as file:
        json.dump(rdsr_data, file, ensure_ascii=False, indent=1)

    # csv
    df = pd.read_json(file_name_json)
    df.to_csv(file_name_csv, encoding='utf-8')
    
    del df
    gc.collect()

    print('********************RDSRファイルの処理完了********************')
    print("新規データ:{}件".format(new_data_cnt))
    print("重複データ:{}件".format(duplicate_data_cnt))
    print("5秒後に終了します.")
    time.sleep(5)
    # label5 = tk.Label(console_root,
    #                   text='********************RDSRファイルの処理完了********************')
    # label5.pack(padx=5, pady=5)
    # label5.update()

    # EXCELのパス ユーザーごとに異なる
    # EXCEL_PATH = "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE"
    # buton_csv = tk.Button(console_root,
    #                       text='csvを開く',
    #                       command=lambda: subprocess.run([EXCEL_PATH, file_name_csv]))
    # buton_csv.pack(padx=5, pady=5)
    # buton_csv.update()

    

    # console_root.mainloop()




if __name__ == '__main__':
    main()
