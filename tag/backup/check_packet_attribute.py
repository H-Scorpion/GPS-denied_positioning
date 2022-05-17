import joblib

template_path = "../template/NAV-PVT_template.pkl"

pvt_obj =joblib.load(template_path)
att = dir(pvt_obj)
print(att)
print(pvt_obj.pDOP)
for attr in att:
    try:
        print(attr,":",getattr(pvt_obj,attr))
    except:
        print("can't find attribute"+ attr)