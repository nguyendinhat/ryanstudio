import json

try:
    with open('data\KerryExpress_van_chuyen_duong_bo.json', encoding='utf8') as data_file:
        data_object = json.load(data_file)
except IOError as e:
    print(e)
    exit(1)

def get_shipping_fee(ma_tinhthanh, kg):
    print(kg)
    base = 0
    upper = kg-20
    upper_fee = 0
    upper_sum = 0
    ma_khuvuc = None
    for zone_id  in data_object:        
        zone = data_object[zone_id]
        # print(zone)
        for city_id in zone["city"]:
            if city_id == ma_tinhthanh:
                ma_khuvuc = zone_id
    
    print(ma_khuvuc)
    if kg <= 20:
        if kg <= 5:
            return int(data_object[ma_khuvuc]["fee<20"]["<5"])
        else:
            return int(data_object[ma_khuvuc]["fee<20"]["5-20"])
    else:
        if kg <= 50:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["20-50"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 200:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["50-200"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 500:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["200-500"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 1000:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["500-1000"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 3000:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["1000-3000"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 5000:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["3000-5000"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        elif kg <= 10000:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"]["5000-10000"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum
        else:
            base = int(data_object[ma_khuvuc]["fee<20"]["5-20"])
            upper_fee = int(data_object[ma_khuvuc]["fee>20"][">10000"])
            i = 0
            while i < upper:
                upper_sum += upper_fee
                i += 1
            return base +upper_sum