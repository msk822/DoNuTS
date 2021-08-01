import os
import sys
import glob
import gc
import datetime

from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


import pydicom
import pandas as pd

import json
sys.path.append("./")


def select_directory(initial_path: str) -> str:
    """
    tkinterのGUIでDICOMが入ったディレクトリを指定させて、そのディレクトリのパスを出力

    Args:
        initial_path ([str]): desktop dir

    Returns:
        [str]: dicom dir which selected by tkinter
    """

    root_select_directory = tk.Tk()
    root_select_directory.withdraw()
    dicom_directory = tk.filedialog.askdirectory(
        initialdir=initial_path, title='DICOMファイルが含まれるフォルダを選択')
    return dicom_directory


def get_dicom_files(directory_path: str) -> list:
    """
    directory_pathを受け取り，DICOMファイルを読み取りリストにて出力．

    Args:
        directory (str): directory_path

    Returns:
        list: dcmreadで読み込まれたファイル
    """

    if directory_path == "":
        print("エラー!　選択されたディレクトリに問題があります.プログラムを終了します．")
        sys.exit(0)

    else:
        path_of_files = glob.glob(directory_path + '/**/*.dcm', recursive=True)
        dicom_files = []

        # dcmreadで読み込めたファイルのみdicom_filesに追加
        for p in tqdm(path_of_files, desc="データ読み込み中"):
            try:
                dicom_files.append(pydicom.dcmread(p))
            except:
                pass

        print("{}つのデータを読み込みました．".format(len(dicom_files)))

    return dicom_files


def separate_dicom_files(dicom_files: list, MODALITY: str) -> dict:
    """
    DICOMファイルを入力し、RDSRとPETに分割してリスト化し，dictで出力

    Args:
        dicom_files ([list]): list of pydicom files

    Returns:
        rdsr_files_dict, modality_files_dict [dict]: rdsr_files, modality_files
        
        return:
            {'MODALITY':[rdsr_files]}, {'MODALITY':[modality_files]}
    """

    rdsr_files = []
    modality_files = []

    for f in tqdm(dicom_files, desc='データを分割中'):
        try:
            if f.Modality == 'SR':  # f.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.67'
                rdsr_files.append(f)
            # ORIGINALである意味は？
            elif f.Modality == MODALITY and f.ImageType[0] == 'ORIGINAL':
                modality_files.append(f)
        except:
            pass
    
    rdsr_files_dict = {MODALITY:rdsr_files}
    modality_files_dict = {MODALITY:modality_files} 

    return rdsr_files_dict, modality_files_dict


def separate_rdsr_dicom_files_and_identify_each_modality(dicom_files: list) -> dict:
    """すべてのdicom fileを引数に，rdsrを分割し，モダリティーを判別する．

    Args:
        dicom_files (list): 読み込まれたすべてのdicom files

    Returns:
        dict: {
            MODALITY : rdsr_dicom,
            MODALITY : rdsr_dicom
            }
            
        dict: {
            MODALITY : modality_dicom,
            MODALITY : modality_dicom
            }
    """
    identified_rdsr_file_angio = []
    identified_rdsr_file_ct = []
    identified_rdsr_file_pt = []
    identified_rdsr_file_nm = []
    identified_rdsr_file_unknown = []
    
    modality_file_angio = []
    modality_file_ct = []
    modality_file_pt = []
    modality_file_nm = [] 
    modality_file_unknown = []

    find_keys = {
        "ANGIO": "Projection",
        "CT": "Tomography",
        "PT":"PET"
        # "NM":"none"
        }

    for each_file in dicom_files:
        # TODO: PETを追加する
        
        try:
            if each_file.Modality == "SR":
                
                try:
                    # CT,ANGIOのとき
                    modality_name = each_file[0x0040, 0xa730][0][0x0040, 0xa168][0][0x0008, 0x0104].value

                    if find_keys["ANGIO"] in modality_name:
                        identified_rdsr_file_angio.append(each_file)
                        
                    elif find_keys["CT"] in modality_name:
                        try:
                            if find_keys["PT"] in each_file[0x0008, 0x1030].value:
                                identified_rdsr_file_pt.append(each_file)
                            else:
                                identified_rdsr_file_ct.append(each_file)
                        except :
                            pass
                except:
                    identified_rdsr_file_unknown.append(each_file)
                    
            elif each_file.Modality == "CT":
                modality_file_ct.append(each_file)
            elif each_file.Modality == "XA":
                modality_file_angio.append(each_file)
            elif each_file.Modality == "PT":
                modality_file_pt.append(each_file)
            elif each_file.Modality == "NM":
                modality_file_nm.append(each_file)
            else:
                modality_file_unknown.append(each_file)
        except :
            pass
        
    out_rdsr_dict = {
        "ANGIO":identified_rdsr_file_angio,
        "CT":identified_rdsr_file_ct,
        "PT":identified_rdsr_file_pt,
        "NM":identified_rdsr_file_nm,
        "Unknown":identified_rdsr_file_unknown
        }
    out_modality_dict = {
        "ANGIO":modality_file_angio,
        "CT":modality_file_ct,
        "PT":modality_file_pt,
        "NM":modality_file_nm,
        "Unknown":modality_file_unknown
        }
    
    return out_rdsr_dict, out_modality_dict


def separate_Acquisition(rdsr_file: pydicom.dataset.FileDataset, MODALITY: str) -> list:
    """RDSRファイルのデータを入力し，CTの線量情報が記載されたレベルのネストの情報を出力する

    Args:
        rdsr_file (pydicom.dataset.FileDataset): pydicom file
        MODALITY ([str]): MODALITY

    Returns:
        Acquisition [list]: 線量情報のリスト
    """

    Irradiation_Event_dict = {
        "CT": "113819",  # CT Acquisition
        "XR": "",
        "ANGIO": "113706",  # Irradiation Event X-Ray Data
        "PT": "113819"  # pst-ctと見なしてCTと同じ値にする
    }

    Acquisition = []
    for r in rdsr_file[0x0040, 0xa730].value:
        try:
            if r[0x0040, 0xa043][0][0x0008, 0x0100].value == Irradiation_Event_dict[MODALITY]:
                data = r[0x0040, 0xa730]
                Acquisition.append(r[0x0040, 0xa730])  # 照射イベントごとの線量情報
        except:
            pass
    return Acquisition
    # if r[0x0040, 0xa730][1][0x0040, 0xa043][0][0x0008, 0x0100].value == CTDoseLengthProductTotal_code:
    #                 CDLPT = r[0x0040, 0xa730][1][0x0040,
    #                                              0xa300][0][0x0040, 0xa30a].value


def extract_data_from_angio_Acquisition(tmp_dict: dict, Acquisition: pydicom.dataelem.DataElement) -> dict:
    """
    1つのANGIO Acquisitionを入力し，そのデータを辞書で返す

    Args:
        rdsr_col ([dict]): 辞書キー
        CTAcquisition ([pydicom.dataelem.DataElement]]): 一つ一つの線量情報が記載されたpydicom file

    Returns:
        [dict]: tmp_dict
    """
    # FIXME: 'Projection X-Ray', 'Irradiation Event X-Ray Data'は今回は取得しない
    xa_ev = {
        # dicom(0040, a730)[0](0040, a168)(0008, 0104).value
        'Projection X-Ray': '113704',
        'Irradiation Event X-Ray Data': '113706',

        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a168)[0](0008, 0104).value
        'Acquisition Plane': '113764',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a168)[0](0008, 0104).value
        'Irradiation Event Type': '113721',

        # ac  (0040, a043)[0](0008, 0100).value >>> (0040, a160).value
        'Acquisition Protocol': '125203',

        # ac  (0040, a043)[0](0008, 0100).value >>> (0040, a168)[0](0008, 0104).value
        'Reference Point Definition': '113780',

        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Dose Area Product': '122130',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Dose (RP)': '113738',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Collimated Field Area': '113790',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Positioner Primary Angle': '112011',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Positioner Secondary Angle': '112012',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Distance Source to Detector': '113750',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Table Longitudinal Position': '113751',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Table Lateral Position': '113752',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Table Height Position': '113753',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'KVP': '113733',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'X-Ray Tube Current': '113734',
        # ac (0040, a043)[0](0008, 0100).value >>> (0040, a300)[0](0040, a30a).value
        'Focal Spot Size': '113766'
    }

    # FILTER_TYPE_CODE = [0x0040, 0xa730][0]

    for nest0 in Acquisition:

        for xa_ev_key in xa_ev.keys():

            # このコード,interact_code_0 を探す
            interact_code_0 = nest0[0x0040, 0xa043][0][0x0008, 0x0100].value

            try:
                if interact_code_0 == xa_ev[xa_ev_key]:
                    if interact_code_0 in ['113764', '113721', '113780']:
                        tmp_dict[xa_ev_key] = nest0[0x0040,
                                                    0xa168][0][0x0008, 0x0104].value

                    elif interact_code_0 == '125203':
                        tmp_dict[xa_ev_key] = nest0[0x0040, 0xa160].value

                    elif interact_code_0 in ['122130', '113738', '113790', '112011', '112012', '113750', '113751', '113752', '113753', '113733',
                                             '113734', '113766']:
                        tmp_dict[xa_ev_key] = nest0[0x0040,
                                                    0xa300][0][0x0040, 0xa30a].value

            except:
                pass

    return tmp_dict


def extract_data_from_CT_Acquisition(tmp_dict: dict, Acquisition: pydicom.dataelem.DataElement) -> dict:
    """
    1つのCT Acquisitionを入力し，そのデータを辞書で返す

    Args:
        rdsr_col ([dict]): 辞書キー
        CTAcquisition ([pydicom.dataelem.DataElement]]): 一つ一つの線量情報が記載されたpydicom file

    Returns:
        [dict]: tmp_dict
    """

    ct_ev = {
        'MeanCTDIvol': '113830',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'DLP': '113838',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'Comment': '121106',
        # [0x0040, 0xa430][0][0x0008, 0x0100].value >>> [0x0040, 0xa160].value

        'XRayModulationType': '113842',
        # [0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa160].value

        'CTDIwPhantomType': '113835',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa168][0][0x0008, 0x0104].value

        'AcquisitionProtocol': '125203',
        # [0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa160].value

        'TargetRegion': '123014',
        # [0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa168][0][0x0008, 0x0104].value

        'CTAcquisitionType': '113820',
        # [0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa168][0][0x0008, 0x0104].value

        'ProcedureContext': 'G-C32C',
        # [0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa168][0][0x0008, 0x0104].value

        'ExposureTime': '113824',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'ScanningLength': '113825',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'ExposedRange': '113899',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'NominalSingleCollimationWidth': '113826',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'NominalTotalCollimationWidth': '113827',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'PitchFactor': '113828',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa300][0][0x0040, 0xa30a].value

        # included CTXraySourceParameters_code
        'IdentificationoftheXRaySource': '113832',
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa160].value

        'KVP': '113733',  # included CTXraySourceParameters_code
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'MaximumXRayTubeCurrent': '113833',  # included CTXraySourceParameters_code
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'MeanXRayTubeCurrent': '113734',  # included CTXraySourceParameters_code
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'ExposureTimeperRotation': '113834',  # included CTXraySourceParameters_code
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa300][0][0x0040, 0xa30a].value

        'DeviceManufacturer': '113878',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa160].value

        'DeviceSerialNumber': '113880',
        # [0x0040, 0xa730][i][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa160].value

        'DLPNotificationValue': '113911',  # Cannot identify
        'CTDIvolNotificationValue': '113912',  # Cannot identify
        'ReasonforProceeding': '113907',  # Cannot identify
        "CTDoseLengthProductTotal":'113813'
        # [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa043][0][0x0008, 0x0100].value >>> [0x0040, 0xa730][i][0x0040, 0xa730][j][0x0040, 0xa300][0][0x0040, 0xa30a].value
    }

    for nest0 in Acquisition:
        # キー毎
        for ct_ev_key in ct_ev.keys():
            try:

                if ct_ev[ct_ev_key] in ['113842', '125203', '123014', '113820', 'G-C32C']:
                    interact_code_0 = nest0[0x0040,
                                            0xa043][0][0x0008, 0x0100].value
                    if interact_code_0 in ['113842', '125203']:
                        tmp_dict[ct_ev_key] = nest0[0x0040, 0xa160].value

                    elif interact_code_0 in ['123014', '113820', 'G-C32C']:
                        tmp_dict[ct_ev_key] = nest0[0x0040,
                                                    0xa168][0][0x0008, 0x0104].value

                elif ct_ev[ct_ev_key] in ['113835', '113830', '113838', '113824', '113825', '113899', '113826', '113827', '113828', '113878', '113880']:
                    try:
                        for nest1 in nest0[0x0040, 0xa730]:
                            if ct_ev[ct_ev_key] == nest1[0x0040, 0xa043][0][0x0008, 0x0100].value:
                                if ct_ev[ct_ev_key] in ['113835']:
                                    tmp_dict[ct_ev_key] = nest1[0x0040,
                                                                0xa168][0][0x0008, 0x0104].value

                                elif ct_ev[ct_ev_key] in ['113830', '113838', '113824', '113825', '113899', '113826', '113827', '113828']:
                                    tmp_dict[ct_ev_key] = nest1[0x0040,
                                                                0xa300][0][0x0040, 0xa30a].value

                                elif ct_ev[ct_ev_key] in ['113878', '113880']:
                                    tmp_dict[ct_ev_key] = nest1[0x0040,
                                                                0xa160].value
                    except :
                        pass

                elif ct_ev[ct_ev_key] in ['113832', '113733', '113833', '113734', '113834']:
                    try:
                        for nest1 in nest0[0x0040, 0xa730]:
                            try:
                                for nest2 in nest1[0x0040, 0xa730]:
                                    try:
                                        if ct_ev[ct_ev_key] == nest2[0x0040, 0xa043][0][0x0008, 0x0100].value:
                                            if ct_ev[ct_ev_key] in ['113832']:
                                                tmp_dict[ct_ev_key] = nest2[0x0040, 0xa160].value
                                                
                                            else:
                                                tmp_dict[ct_ev_key] = nest2[0x0040, 0xa300][0][0x0040, 0xa30a].value
                                    except :
                                        pass
                            except :
                                pass
                    except :
                        pass
            except:
                pass
        
        
    return tmp_dict

def get_events_from_rdsr(rdsr_files: pydicom.dataset.FileDataset, MODALITY: str) -> dict:
    """曝射回数をRDSRからeventsとして読み取る

    rdsr_files[0x0040,0xa730]の中を繰り返し検索する

    Args:
        rdsr_files ([pydicom.dataset.FileDataset]): dcmreadで読み込まれたファイル
        MODALITY ([str]): MODALITY

    Returns:
        [dict]: 照射回数を返す
        dict[key] は読み込まれたrdsrファイルの順番

        >>> 手持ちデータのctの場合
                {'0' : '3',
                 '1' : '6'}

        >>> 手持ちデータのangioの場合
                {'0' : '14'}
                {'1' : '14'}
    """

    # 照射回数をEVENTとして取得し，events_dictの中に情報を入れる．

    events_dict = {}

    for file_cnt, rdsr_file in enumerate(rdsr_files):
        event_counts = 0  # ANGIOのため

        # key
        file_cnt_str = str(file_cnt)

        # 以下で照射回数を取得
        try:
            for r in rdsr_file[0x0040, 0xa730].value:

                if MODALITY in ["CT", "PT"]:

                    TotalNumberofIrradiationEvents_code = '113812'

                    try:
                        if r[0x0040, 0xa730][0][0x0040, 0xa043][0][0x0008, 0x0100].value == TotalNumberofIrradiationEvents_code:
                            events = r[0x0040, 0xa730][0][0x0040,
                                                        0xa300][0][0x0040, 0xa30a].value
                    except:
                        pass

                elif MODALITY == "ANGIO":

                    try:
                        if r[0x0040, 0xa043][0][0x0008, 0x0100].value == '113706':
                            event_counts += 1
                    except:
                        pass
                    events = event_counts

                elif MODALITY == "NM":
                    pass

                else:
                    pass

        except :
            pass
        
        each_event_dict = {file_cnt_str: str(events)}
        events_dict.update(each_event_dict)

    return events_dict


def calc_total_event(events_dict: dict) -> int:
    """各照射回数の合計を求める

    Args:
        events_dict (dict):

    Returns:
        int: cnt
    """
    cnt = 0
    for key in events_dict.keys():
        n = int(events_dict[key])
        cnt = cnt + n
    return cnt


def extract_CT_Dose_Length_Product_Total(rdsr_files: pydicom.dataset.FileDataset) -> str:
    """
    RDSRからCT Dose Length Product Totalを抽出し，辞書で出力

    Args:
        rdsr_files ([pydicom.dataset.FileDataset]): dcmreadで読み込まれたファイル

    Returns:
        [str]: CT Dose Length Product Total
    """
    ''''''
    # CT Dose Length Product TotalのEV
    CTDoseLengthProductTotal_code = '113813'

    for _, r in enumerate(rdsr_files[0x0040, 0xa730].value):
        try:
            if r[0x0040, 0xa730][1][0x0040, 0xa043][0][0x0008, 0x0100].value == CTDoseLengthProductTotal_code:
                CDLPT = r[0x0040, 0xa730][1][0x0040,
                                             0xa300][0][0x0040, 0xa30a].value
        except:
            pass
    return CDLPT


def extract_data_from_rdsr_header(rdsr_header_col_names: list, rdsr_files: list, events: list) -> dict:
    """
    RDSRのヘッダーから情報を抽出し，辞書で出力

    Args:
        rdsr_header_col_names (list): [description]
        rdsr_files (list): [description]
        events (list): [description]

    Returns:
        dict: tmp_header_dictionary
    """

    # 空の辞書tmpを作成
    tmp_header_dictionary = {col: [] for col in rdsr_header_col_names}

    for num, rdsr in enumerate(rdsr_files):
        for eve in range(int(events[num])):
            for name in rdsr_header_col_names:
                try:
                    tmp_header_dictionary[name].append(
                        str(getattr(rdsr, name)))
                except:
                    tmp_header_dictionary[name].append(" ")
    return tmp_header_dictionary

def extract_RadionuclideTotalDose(modality_files_dict:dict, MODALITY)-> dict:
    """PT, NM　の RadionuclideTotalDoseを返す

    Args:
        modality_files_dict (dict): modality file dict

    Returns:
        dict: {
            "PatientID + StudyDate": DOSE
            "PatientID + StudyDate": DOSE
            }
    """    
    out_dict = {}
    for m in modality_files_dict[MODALITY]:
        try:
            unique_code = str(m.PatientID) + str(m.StudyDate)
            DOSE = m.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose
            temp_dict = {unique_code:DOSE}
            out_dict.update(temp_dict)
        except :
            pass
    return out_dict

selected_modality = []


def select_modality():
    """
    modalityを選択する

    Returns:
        [str]]: selected_modality[0]  ["CT", "XR", "ANGIO","PT"]のいずれかひとつ
    """
    root = tk.Tk()
    root.title("Modalityを選択")
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

    auto_btn = tk.Button(text="Auto",
                         command=lambda: [selected_modality.append("Auto"),
                                          root.destroy()])
    auto_btn.pack(padx=5, pady=5)

    list_value = tk.StringVar()
    lb = tk.Listbox(height=8, listvariable=list_value, selectmode="single")
    root.mainloop()

    return selected_modality[0]

def show_len_identified(dictinary: dict) -> str:
    """ユーザー向けに見つかったファイル数を返す

    Args:
        dictinary (dict): [description]

    Returns:
        str: modality:n
    """    
    txt = ''
    for M in dictinary:
        txt += str("\n{}:{}".format(M,len(dictinary[M])))
    
    return txt

def count_rdsr(dictinary: dict) -> int:
    """dict内のファイル数の総計を返す

    Args:
        dictinary (dict): [description]

    Returns:
        int: [description]
    """    
    cnt = 0
    for M in dictinary:
        cnt += len(dictinary[M])
    return cnt

def clear_dict_value(dict: dict) -> dict:
    """dictの値を ' ' にする

    Args:
        dict ([dict]): [description]

    Returns:
        [dict]: [description]
    """
    for key in dict.keys():
        dict[key] = ' '
    return dict
