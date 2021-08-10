import sqlite3

class WriteDB():
    def __init__(self, MODALITY:str):
        self.MODALITY = MODALITY
        self.DBNAME = './Resources/DONUTS.db'
        self.MODALITY = MODALITY
        
        self.conn = sqlite3.connect(self.DBNAME)
        self.cursor = self.conn.cursor()
        
    def insertdb(self, table, data):
        # table に接続，存在しなかったらtableを作成
        if table == 'CT':
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table + 
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    AcquisitionProtocol TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL
                                )
                                """ )
        
        elif table == 'ANGIO':
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table + 
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    Projection_X_Ray TEXT NULL  ,
                                    Irradiation_Event_X_Ray_Data TEXT NULL  ,
                                    Acquisition_Plane TEXT NULL  ,
                                    Irradiation_Event Type TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    Reference_Point_Definition TEXT NULL  ,
                                    Dose_Area_Product TEXT NULL  ,
                                    Dose__RP_ TEXT NULL  ,
                                    Collimated_Field_Area TEXT NULL  ,
                                    Positioner_Primary_Angle TEXT NULL  ,
                                    Positioner_Secondary_Angle TEXT NULL  ,
                                    Distance_Source_to_Detector TEXT NULL  ,
                                    Table_Longitudinal_Position TEXT NULL  ,
                                    Table_Lateral_Position TEXT NULL  ,
                                    Table_Height_Position TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    X_Ray_Tube_Current TEXT NULL  ,
                                    Focal_Spot_Size TEXT NULL 
                                )
                                """ )
            
        elif table in ['PT', 'NM']:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table + 
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    AcquisitionProtocol TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL,
                                    RadionuclideTotalDose TEXT NULL
                                )
                                """ )
            
        elif table == "Auto":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table + 
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    Projection_X_Ray TEXT NULL  ,
                                    Irradiation_Event_X_Ray_Data TEXT NULL  ,
                                    Acquisition_Plane TEXT NULL  ,
                                    Irradiation_Event Type TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    Reference_Point_Definition TEXT NULL  ,
                                    Dose_Area_Product TEXT NULL  ,
                                    Dose__RP_ TEXT NULL  ,
                                    Collimated_Field_Area TEXT NULL  ,
                                    Positioner_Primary_Angle TEXT NULL  ,
                                    Positioner_Secondary_Angle TEXT NULL  ,
                                    Distance_Source_to_Detector TEXT NULL  ,
                                    Table_Longitudinal_Position TEXT NULL  ,
                                    Table_Lateral_Position TEXT NULL  ,
                                    Table_Height_Position TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    X_Ray_Tube_Current TEXT NULL  ,
                                    Focal_Spot_Size TEXT NULL,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    AcquisitionProtocol TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL,
                                    RadionuclideTotalDose TEXT NULL
                                )
                                """ )
        
        
        
        # column名をlistとして取得
        table_cursor = self.conn.execute('SELECT * FROM ' + table)
        names = list(map(lambda x: x[0], table_cursor.description))
        
        # データを挿入するためのタプルを作成 (?,?,?,...)
        t = ['']
        for i in range(len(names)):
            if i==0:
                txt = '?'
            else:
                txt = ',?'
            t[0] += txt
        tu = tuple(t)
        tu = '(' + tu[0] + ')'
        
        
        sql =  "INSERT INTO " + table + " VALUES " + tu
        data = tuple(data)
        self.conn.execute(sql, data)
        self.conn.commit()
        
    def main(self, data:list):
        self.insertdb(table=self.MODALITY, data=data)
    
    def close(self):
        self.conn.close()