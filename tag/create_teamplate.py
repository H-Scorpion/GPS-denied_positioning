from pyubx2 import UBXMessage, GET


def create_NAV_PVT (lat, lon, height):
    NAV_PVT_obj = UBXMessage(0x01, 0x07, GET, 
					iTOW=196806000, year=2022, month=5, 
					day=17, hour=6, min=6, second=36, 
					validDate=1, validTime=1, 
					fullyResolved=1, validMag=0, tAcc=10, nano=600130452, 
					fixType=3, gnssFixOk=1, difSoln=1, psmState=0, 
					headVehValid=0, carrSoln=0, confirmedAvai=0, 
					confirmedDate=0, confirmedTime=0, numSV=18, 
					lon = lon, lat = lat, height = height,
					# lon=121.5415504, lat=25.0187538, height=55280, 
					hMSL=38221, hAcc=3853, vAcc=5546, velN=-105, 
					velE=33, velD=-132, gSpeed=110, headMot=346.78089, 
					sAcc=964, headAcc=19.36601, pDOP=2.04, invalidLlh=0, 
					lastCorrectionAge=0, reserved0=2312952, 
					headVeh=0.0, magDec=0.0, magAcc=0.0)
    return NAV_PVT_obj


# msg_NAV_PVT = UBXMessage(0x01, 0x07, GET, 
# 					iTOW=196806000, year=2022, month=5, 
# 					day=17, hour=6, min=6, second=36, 
# 					validDate=1, validTime=1, 
# 					fullyResolved=1, validMag=0, tAcc=10, nano=600130452, 
# 					fixType=3, gnssFixOk=1, difSoln=1, psmState=0, 
# 					headVehValid=0, carrSoln=0, confirmedAvai=0, 
# 					confirmedDate=0, confirmedTime=0, numSV=18, 
# 					lon=121.5415504, lat=25.0187538, height=55280, 
# 					hMSL=38221, hAcc=3853, vAcc=5546, velN=-105, 
# 					velE=33, velD=-132, gSpeed=110, headMot=346.78089, 
# 					sAcc=964, headAcc=19.36601, pDOP=2.04, invalidLlh=0, 
# 					lastCorrectionAge=0, reserved0=2312952, 
# 					headVeh=0.0, magDec=0.0, magAcc=0.0)

msg_NAV_DOP = UBXMessage(0x01, 0x04, GET, 
					iTOW=196806000, gDOP=2.38, pDOP=2.04, 
					tDOP=1.22, vDOP=1.75, 
					hDOP=1.06, nDOP=0.77, 
					eDOP=0.73)

msg_NAV_TIMEGPS = UBXMessage(0x01, 0x20, GET, 
					iTOW=196806000, fTOW=125064, week=2210, 
					leapS=18, towValid=1, 
					weekValid=1, leapSValid=1, tAcc=10)

msg_MON_HW = UBXMessage(0x0a, 0x09, GET, 
					pinSel=b'\x00\xf4\x01\x00', pinBank=b'\x00\x00\x00\x00', 
					pinDir=b'\x00\x00\x01\x00', pinVal=b'\xef\xf7\x01\x00', 
					noisePerMS=104, agcCnt=1638, aStatus=2, aPower=1, 
					rtcCalib=1, safeBoot=0, jammingState=0, xtalAbsent=0, 
					reserved0=132, usedMask=b'\xff\xeb\x01\x00', VP_01=b'\n', 
					VP_02=b'\x0b', VP_03=b'\x0c', VP_04=b'\r', VP_05=b'\x0e', 
					VP_06=b'\x0f', VP_07=b'\x01', VP_08=b'\x00', VP_09=b'\x02', 
					VP_10=b'\x03', VP_11=b'\xff', VP_12=b'\x10', VP_13=b'\xff', 
					VP_14=b'\x12', VP_15=b'\x13', VP_16=b'6', VP_17=b'5', 
					jamInd=62, reserved1=24079, pinIrq=b'\x00\x00\x00\x00', 
					pullH=b'\x80\xf7\x01\x00', pullL=b'\x00\x00\x00\x00')

msg_MON_HW2 = UBXMessage(0x0a, 0x0b, GET, 
					ofsI=-42, magI=151, ofsQ=11, magQ=162, cfgSource=111, 
					reserved0=1800, lowLevCfg=4294967295, 
					reserved1=18446744073709551615, postStatus=0, reserved2=0)

# print(msg_MON_HW)