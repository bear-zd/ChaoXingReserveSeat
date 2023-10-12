import js2py
def encode(roomId, day, starttime ,endtime, seatNum, token):
    with open("utils/encode.js","r+") as f:
        js_code = f.read()
    parm_dict = {"roomIdparm": roomId,
                 "dayparm": day,
                 "startTimeparm": starttime,
                 "endTimeparm": endtime,
                 "seatNumparm": seatNum,
                 "tokenparm": token}
    for i in parm_dict:
        js_code = js_code.replace(i, parm_dict[i])
    # print(js_code)
    result = js2py.eval_js(js_code)
    
    return result

