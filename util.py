import numpy as np

length = 582
problems_arr = ['Gas', 'Mid-Low Reservoir Pressure', 'Fine Sands', 'Fishing Problem', 'Casing Damaged', 'Sand', '-', 'Tight Formation', 'Fines Migration', 'Scale', 'Sand Erosion', 'Low Reservoir Pressure', 'Hi TM', 'Low Influx', 'Corrosive']
pumps_arr = ['Q20', 'Q08', 'QM265', 'QN55', 'QM200', 'RC1000', 'DN1750', 'SN3600', 'QN70', 'Q10', 'QN120']
platforms_arr = ['AIDA A', 'ARYANI AC', 'ATTI AC', 'CINTA A', 'CINTA B', 'CINTA C', 'CINTA D', 'CINTA E', 'CINTA F', 'CINTA G', 'CINTA H', 'E.RAMA AC', 'FARIDA-A', 'FARIDA-B', 'FARIDA-C', 'GITA A', 'INDRI A', 'INTAN A', 'INTAN AC', 'INTAN B', 'KARMILA A', 'KARTINI AC', 'KITTY A', 'KRISNA A', 'KRISNA B', 'KRISNA C', 'KRISNA D', 'KRISNA E', 'LIDYA AC', 'LITA AC', 'N.WANDA BC', 'N.WANDA-A(MONOPOD)', 'NE.INTAN', 'NE.INTAN AC', 'NORA', 'RAMA A', 'RAMA B', 'RAMA C', 'RAMA D', 'RAMA E', 'RAMA F', 'RAMA G', 'RAMA H', 'RAMA I', 'S.ZELDA AC', 'SELATAN A', 'SUNDARI A', 'SUNDARI B', 'SURATMI AC', 'SW.WANDA-A(MONOPOD)', 'TERESIA AC', 'TITI A', 'VITA AC', 'WANDA', 'WIDURI A', 'WIDURI B', 'WIDURI C', 'WIDURI DC', 'WIDURI E', 'WIDURI F', 'WIDURI G', 'WIDURI H', 'WIDURI-D', 'WINDRI AC', 'YANI-A', 'YANI-AC', 'YVONE A', 'YVONE B', 'ZELDA A', 'ZELDA B', 'ZELDA C', 'ZELDA D', 'ZELDA-E']
wells_arr = ['AIDA-01', 'AIDA-02', 'AIDA-03', 'AIDA-04', 'AIDA-05', 'AIDA-07', 'AIDA-09', 'AIDA-13', 'AIDA-14', 'AIDA-15', 'ARYA-C1', 'ARYA-C2', 'ARYA-C6', 'ATTA-C1', 'ATTA-C8', 'ATTA-CAN A', 'CINA-03', 'CINA-04ST', 'CINA-08', 'CINA-10ST', 'CINA-11ST', 'CINA-12', 'CINB-05', 'CINC-01', 'CINC-03', 'CINC-05S', 'CINC-06', 'CINC-07', 'CINC-10', 'CINC-11', 'CINC-12', 'CIND-02', 'CIND-04', 'CIND-07', 'CIND-10', 'CIND-11ST', 'CIND-12', 'CIND-14', 'CIND-15', 'CIND-CAN A', 'CIND-CAN B', 'CINE-01', 'CINE-03', 'CINE-09', 'CINE-11', 'CINE-12', 'CINE-13', 'CINF-01', 'CINF-05', 'CINF-08', 'CINF-11', 'CINF-12', 'CINF-14', 'CINF-15', 'CINF-CAN A', 'CING-03', 'CING-08', 'CING-12', 'CING-13', 'CING-14', 'CING-15', 'CING-CAN A', 'CINH-01', 'CINH-04', 'CINH-06', 'CINH-CAN A', 'CINH-CAN B', 'ERMA-C10ST', 'ERMA-C4', 'FARA-02', 'FARA-02:TA', 'FARA-04', 'FARA-04:TA', 'FARA-07', 'FARA-07:TA', 'FARA-14', 'FARB-01', 'FARB-02', 'FARB-07', 'FARB-08', 'FARB-10', 'FARB-10:TA', 'FARB-12', 'FARB-12:TA', 'FARB-13', 'FARB-13:TA', 'FARB-15', 'FARB-CAN A', 'FARB-CAN B', 'FARC-01', 'FARC-01:TA', 'FARC-10', 'FARC-11', 'FARC-11:TA', 'GITA-01', 'GITA-09', 'GITA-10', 'GITA-11', 'GITA-12', 'GITA-18', 'INDA-02', 'INDA-05', 'INDA-11', 'INDA-24', 'INDA-25', 'INTA-04', 'INTA-05', 'INTA-08', 'INTA-16', 'INTA-18', 'INTA-C22', 'INTA-C23', 'INTB-01', 'INTB-02', 'INTB-04', 'KARA-14', 'KITA-07', 'KRIA-01', 'KRIA-03', 'KRIA-05', 'KRIA-06', 'KRIA-07', 'KRIA-09', 'KRIA-14', 'KRIB-01', 'KRIB-03', 'KRIB-04', 'KRIB-06', 'KRIB-07', 'KRIC-01', 'KRIC-02', 'KRIC-04', 'KRIC-08', 'KRID-02', 'KRID-03', 'KRID-06S', 'KRID-07', 'KRID-08', 'KRID-09', 'KRID-15', 'KRID-16', 'KRIE-01', 'KRIE-02', 'KRIE-07', 'KRTA-C01', 'KRTA-C03', 'KRTA-C04', 'KRTA-C06', 'KRTA-C07', 'LIDA-C02', 'LIDA-C06', 'LIDA-C07', 'LIDA-C08', 'LITA-C03', 'LITA-C04', 'NEIA-01', 'NEIA-02', 'NEIA-03ST', 'NEIA-04ST', 'NEIA-05', 'NEIA-06', 'NEIA-08ST', 'NEIA-09ST', 'NEIA-10', 'NEIA-11', 'NEIA-12', 'NEIA-14', 'NEIA-15', 'NEIA-24ML', 'NEIA-C17', 'NEIA-C18', 'NEIA-C19', 'NEIA-C20', 'NEIA-C21', 'NEIA-C25', 'NEIA-C26', 'NEIA-C27ST', 'NEIA-C28', 'NORA-01', 'NORA-02', 'NORA-03', 'NORA-04', 'NWAA-C2S', 'NWAA-C2S:TA', 'NWAA-C3', 'NWAA-C4', 'NWAA-CAN A', 'NWAA-CAN B', 'NWAB-C7', 'RAMA-01', 'RAMA-04', 'RAMA-05', 'RAMA-CAN A', 'RAMB-01', 'RAMB-05', 'RAMB-06', 'RAMB-10', 'RAMB-11', 'RAMC-01', 'RAMC-06', 'RAMC-07', 'RAMC-14', 'RAMC-CAN', 'RAMD-02', 'RAMD-08', 'RAMD-09', 'RAMD-12', 'RAMD-13', 'RAME-01', 'RAME-02', 'RAME-03', 'RAME-06', 'RAME-CAN A', 'RAMF-01', 'RAMF-02', 'RAMF-03ST', 'RAMF-06', 'RAMF-08', 'RAMF-11', 'RAMF-13', 'RAMF-14', 'RAMF-15', 'RAMF-17H', 'RAMF-CAN', 'RAMG-01', 'RAMG-02', 'RAMG-07', 'RAMG-10', 'RAMG-11', 'RAMG-CAN A', 'RAMH-02', 'RAMH-04', 'RAMH-08', 'RAMH-CAN A', 'RAMI-02', 'RAMI-03', 'RAMI-08', 'RAMI-CAN A', 'SELA-01', 'SELA-02', 'SELA-03', 'SELA-09', 'SELA-10', 'SUNA-06', 'SUNA-10', 'SUNA-11', 'SUNA-13', 'SUNB-01', 'SUNB-02', 'SUNB-04', 'SUNB-05', 'SUNB-08', 'SURA-C01', 'SURA-C02', 'SURA-C03H', 'SURA-C04', 'SWWA-C1', 'SWWA-C2', 'SWWA-C5', 'SWWA-C5:TA', 'SWWA-C8', 'SWWA-C9', 'SZEA-C1', 'SZEA-C10', 'SZEA-C11', 'SZEA-C6', 'SZEA-C8', 'SZEA-C9', 'TERA-C4', 'TERA-C6', 'TERA-CAN A', 'TERA-CAN B', 'TITA-02', 'TITA-05', 'TITA-15', 'VITA-C01', 'VITA-C02', 'VITA-C03', 'VITA-C04', 'VITA-CAN A', 'VITA-CAN B', 'WANA-01', 'WANA-02', 'WANA-03', 'WANA-06', 'WANA-09', 'WANA-10', 'WANA-11', 'WANA-12', 'WIDA-01', 'WIDA-02S', 'WIDA-03', 'WIDA-04', 'WIDA-05', 'WIDA-07', 'WIDA-08', 'WIDA-09', 'WIDA-10', 'WIDA-11', 'WIDA-14', 'WIDA-15', 'WIDA-16', 'WIDA-18S', 'WIDA-19', 'WIDA-20', 'WIDA-22', 'WIDA-24', 'WIDA-25', 'WIDA-26', 'WIDA-27', 'WIDA-28', 'WIDA-32', 'WIDA-35', 'WIDA-36ST', 'WIDA-37', 'WIDA-39', 'WIDA-CAN A', 'WIDA-CAN B', 'WIDB-01', 'WIDB-02ST', 'WIDB-04', 'WIDB-07', 'WIDB-08', 'WIDB-10', 'WIDB-15', 'WIDB-16', 'WIDB-17', 'WIDB-18', 'WIDB-22', 'WIDB-23', 'WIDB-24', 'WIDB-25', 'WIDB-29', 'WIDB-31', 'WIDB-32', 'WIDB-33', 'WIDB-34', 'WIDB-35', 'WIDB-36', 'WIDB-CAN A', 'WIDB-CAN B', 'WIDC-03', 'WIDC-04', 'WIDC-05', 'WIDC-06', 'WIDC-07', 'WIDC-08', 'WIDC-09', 'WIDC-12', 'WIDC-13', 'WIDC-16', 'WIDC-17', 'WIDC-18', 'WIDC-19', 'WIDC-22', 'WIDC-25', 'WIDC-30', 'WIDC-31', 'WIDC-32', 'WIDC-33', 'WIDC-34', 'WIDC-35', 'WIDC-36', 'WIDC-37', 'WIDC-39', 'WIDC-41', 'WIDC-CAN A', 'WIDC-CAN B', 'WIDD-01', 'WIDD-02', 'WIDD-03', 'WIDD-04', 'WIDD-05', 'WIDD-07', 'WIDD-08ST', 'WIDD-09', 'WIDD-09:TA', 'WIDD-11', 'WIDD-12', 'WIDD-15', 'WIDD-16', 'WIDD-20', 'WIDD-21', 'WIDD-22', 'WIDD-23', 'WIDD-25', 'WIDD-26', 'WIDD-28', 'WIDD-29', 'WIDD-31', 'WIDD-44', 'WIDD-48', 'WIDD-C17', 'WIDD-C38', 'WIDD-C41', 'WIDD-C42', 'WIDD-CA34', 'WIDD-CAN A', 'WIDD-CAN B', 'WIDE-02', 'WIDE-03', 'WIDE-04', 'WIDE-08', 'WIDE-10', 'WIDE-11', 'WIDE-12', 'WIDE-13', 'WIDE-14', 'WIDE-16', 'WIDE-19', 'WIDE-20', 'WIDF-01', 'WIDF-07', 'WIDG-01', 'WIDG-03', 'WIDG-05', 'WIDG-06', 'WIDG-08', 'WIDG-09', 'WIDH-04', 'WIDH-07', 'WIDH-08', 'WIDH-10', 'WIDH-11', 'WIDH-12', 'WIDH-13', 'WIDH-15', 'WIDH-16', 'WINA-C06', 'WINA-C12', 'WINA-C13', 'WINA-C15S', 'WINA-C17ST', 'WINA-C19', 'WINA-C2', 'WINA-C20', 'WINA-C21', 'WINA-C22', 'WINA-CAN A', 'WINA-CAN B', 'YANA-C01', 'YANA-C06', 'YANA-C08', 'YANA-C09', 'YANA-C11', 'YANA-C11:BW', 'YANA-C12', 'YVOA-05', 'YVOA-06', 'YVOA-10', 'YVOA-12', 'YVOA-CAN A', 'YVOB-03', 'YVOB-04', 'YVOB-08', 'YVOB-10', 'YVOB-14', 'YVOB-15', 'ZELA-02', 'ZELA-06', 'ZELA-08', 'ZELA-CAN A', 'ZELB-01', 'ZELB-04', 'ZELB-07', 'ZELB-08', 'ZELC-09', 'ZELC-13', 'ZELC-14', 'ZELD-01', 'ZELD-05', 'ZELD-11', 'ZELD-12', 'ZELE-02', 'ZELE-06', 'ZELE-07', 'ZELE-07:TA', 'ZELE-10', 'ZELE-11']
vendors_arr = ['Vendor_Powerlift', 'Vendor_Reda']

def get_pumps(desired_q):
    pumps = []
    if desired_q >= 200 and desired_q <= 1350:
        pumps.append('RC1000')
    if desired_q >= 400 and desired_q <= 1050:
        pumps.append('Q08')
    if desired_q >= 600 and desired_q <= 1250:
        pumps.append('Q10')
    if desired_q >= 1150 and desired_q <= 2050:
        pumps.append('Q20')
    if desired_q >= 1200 and desired_q <= 2050:
        pumps.append('DN1750')
    if desired_q >= 2250 and desired_q <= 5200:
        pumps.append('QN55')
    if desired_q >= 2400 and desired_q <= 4600:
        pumps.append('SN3600')
    if desired_q >= 3400 and desired_q <= 7900:
        pumps.append('QN70')
    if desired_q >= 6000 and desired_q <= 12800:
        pumps.append('QN120')
    if desired_q >= 12250 and desired_q <= 18000:
        pumps.append('QM200')
    if desired_q >= 14000 and desired_q <= 24000:
        pumps.append('QM265')
    return pumps

def get_model_input(desired_q, problems, pump_type, platform, well, vendor):
    data = np.zeros(length)
    data[0] = desired_q

    # initialize index
    i = 1

    # flag problems
    for pr in problems_arr:
        if pr in problems:
            data[i] = 1
        i += 1
    
    # flag pumps
    for pu in pumps_arr:
        if pu == pump_type:
            data[i] = 1
        i += 1

    # flag platforms
    for pl in platforms_arr:
        if pl == platform:
            data[i] = 1
        i += 1

    # flag wells
    for w in wells_arr:
        if w == well:
            data[i] = 1
        i += 1

    # flag vendor
    for v in vendors_arr:
        if v == vendor:
            data[i] = 1
        i += 1
    
    assert i == length - 1
    return data

def get_model_input_arr(desired_q, problems, pumps, platform, well, vendor):
    data = []
    for pump in pumps:
        temp = get_model_input(desired_q, problems, pump, platform, well, vendor)
        data.append(temp)
    return data