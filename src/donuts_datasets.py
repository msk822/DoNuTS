def return_json_temprate(MODALITY: str) -> dict:
    """テンプレート辞書を返す

    Args:
        MODALITY (str): MODALITY

    Returns:
        [dict]: temprate
    """
    header = {
        'PRIMARY KEY':' ',
        'Identified Modality':"",
        "SOPInstanceUID":" ",
        "StudyID":" ",
        "ManufacturerModelName": " ",
        "PatientID": " ",
        "StudyDate": " ",
        "PatientName": " ",
        "StudyDescription": " ",
        "PatientBirthDate": " ",
        "PatientSex": " ",
        "PatientAge": " ",
        "PatientSize": " ",
        "PatientWeight": " ",
        'AccessionNumber': ' '
    }

    if MODALITY == "CT":

        # ct_temp
        temp = {
            "MeanCTDIvol": " ",
            "DLP": " ",
            "Comment": " ",
            "XRayModulationType": " ",
            "CTDIwPhantomType": " ",
            "AcquisitionProtocol": " ",
            "TargetRegion": " ",
            "CTAcquisitionType": " ",
            "ProcedureContext": " ",
            "ExposureTime": " ",
            "ScanningLength": " ",
            "ExposedRange": " ",
            "NominalSingleCollimationWidth": " ",
            "NominalTotalCollimationWidth": " ",
            "PitchFactor": " ",
            "IdentificationoftheXRaySource": " ",
            "KVP": " ",
            "MaximumXRayTubeCurrent": " ",
            "MeanXRayTubeCurrent": " ",
            "ExposureTimeperRotation": " ",
            "DeviceManufacturer": " ",
            "DeviceSerialNumber": " ",
            "DLPNotificationValue": " ",
            "CTDIvolNotificationValue": " ",
            "ReasonforProceeding": " ",
            "CTDoseLengthProductTotal": " "
        }

    elif MODALITY == "ANGIO":

        # angio_temp
        temp = {
            'Projection X-Ray': ' ',
            'Irradiation Event X-Ray Data': ' ',
            'Acquisition Plane': ' ',
            'Irradiation Event Type': ' ',
            'Acquisition Protocol': ' ',
            'Reference Point Definition': ' ',
            'Dose Area Product': ' ',
            'Dose (RP)': ' ',
            'Collimated Field Area': ' ',
            'Positioner Primary Angle': ' ',
            'Positioner Secondary Angle': ' ',
            'Distance Source to Detector': ' ',
            'Table Longitudinal Position': ' ',
            'Table Lateral Position': ' ',
            'Table Height Position': ' ',
            'KVP': ' ',
            'X-Ray Tube Current': ' ',
            'Focal Spot Size': ' '
        }

    elif MODALITY in ["PT", "NM"]:

        # pet_temp
        temp = {
            "MeanCTDIvol": " ",
            "DLP": " ",
            "Comment": " ",
            "XRayModulationType": " ",
            "CTDIwPhantomType": " ",
            "AcquisitionProtocol": " ",
            "TargetRegion": " ",
            "CTAcquisitionType": " ",
            "ProcedureContext": " ",
            "ExposureTime": " ",
            "ScanningLength": " ",
            "ExposedRange": " ",
            "NominalSingleCollimationWidth": " ",
            "NominalTotalCollimationWidth": " ",
            "PitchFactor": " ",
            "IdentificationoftheXRaySource": " ",
            "KVP": " ",
            "MaximumXRayTubeCurrent": " ",
            "MeanXRayTubeCurrent": " ",
            "ExposureTimeperRotation": " ",
            "DeviceManufacturer": " ",
            "DeviceSerialNumber": " ",
            "DLPNotificationValue": " ",
            "CTDIvolNotificationValue": " ",
            "ReasonforProceeding": " ",
            "CTDoseLengthProductTotal": " ",
            "RadionuclideTotalDose": " "
        }

    
    elif MODALITY == 'Auto':
        temp = {
            'Identified Modality':"",
            'Projection X-Ray': ' ',
            'Irradiation Event X-Ray Data': ' ',
            'Acquisition Plane': ' ',
            'Irradiation Event Type': ' ',
            'Acquisition Protocol': ' ',
            'Reference Point Definition': ' ',
            'Dose Area Product': ' ',
            'Dose (RP)': ' ',
            'Collimated Field Area': ' ',
            'Positioner Primary Angle': ' ',
            'Positioner Secondary Angle': ' ',
            'Distance Source to Detector': ' ',
            'Table Longitudinal Position': ' ',
            'Table Lateral Position': ' ',
            'Table Height Position': ' ',
            'KVP': ' ',
            'X-Ray Tube Current': ' ',
            'Focal Spot Size': ' ',
            "MeanCTDIvol": " ",
            "DLP": " ",
            "Comment": " ",
            "XRayModulationType": " ",
            "CTDIwPhantomType": " ",
            "AcquisitionProtocol": " ",
            "TargetRegion": " ",
            "CTAcquisitionType": " ",
            "ProcedureContext": " ",
            "ExposureTime": " ",
            "ScanningLength": " ",
            "ExposedRange": " ",
            "NominalSingleCollimationWidth": " ",
            "NominalTotalCollimationWidth": " ",
            "PitchFactor": " ",
            "IdentificationoftheXRaySource": " ",
            "KVP": " ",
            "MaximumXRayTubeCurrent": " ",
            "MeanXRayTubeCurrent": " ",
            "ExposureTimeperRotation": " ",
            "DeviceManufacturer": " ",
            "DeviceSerialNumber": " ",
            "DLPNotificationValue": " ",
            "CTDIvolNotificationValue": " ",
            "ReasonforProceeding": " ",
            "CTDoseLengthProductTotal": " ",
            "RadionuclideTotalDose": " "
        }

    else:
        print("MODALITYが不正です")

    header.update(temp)
    return header
