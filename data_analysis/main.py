import joblib
import pyubx2
if __name__ == '__main__':
    data = joblib.load('./data_analysis/tagPosData_20220911-182703.pkl')
    print(data)