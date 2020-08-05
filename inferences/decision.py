NG_dict = dict(
    Nama='Cacat',
    bbox=[1, 3],
    pengikut=0,
    bagian=0
)


def final_decision(bbox_list, NG_list, isClassi=False, conf_list=None):
    Final = [NG_dict]
    for i in range(len(NG_list)):  # pembagi section
        # if not i==1:
        # 	continue
        # if i==4 or i == 5:
        #	continue
        sl = NG_list[i]
        bl = bbox_list[i]
        ng_bagian = i + 1
        # slist1, ...
        for j in range(len(sl)):  # pembagi frame
            sli = sl[j]
            bli = bl[j]
            # [['kurokawa_forging'],['OK']....]
            for k in range(len(sli)):  # pembagi ng type
                tipeNG = sli[k]
                if tipeNG == "OK":
                    continue
                ## khusus klasifikasi
                if isClassi:
                    conf = conf_list[i][j][k]
                    if conf < 0.4:
                        continue
                try:
                    bbox_ng = [bli[k][1], bli[k][3], bli[k][0], bli[k][2]]
                except:
                    continue
                isNew = True
                for l in Final:
                    if tipeNG == l['Nama'] and ng_bagian == l['bagian']:
                        # print(bbox_ng[0], 'vs', l['bbox'][0])
                        # print(bbox_ng[1], 'vs', l['bbox'][1])
                        if bbox_ng[0] > l['bbox'][0] and bbox_ng[1] < l['bbox'][1]:
                            if bbox_ng[2] > l['bboxY'][0] and bbox_ng[3] < l['bboxY'][1]:  # kasus salah scratch
                                aR = (bbox_ng[1] - bbox_ng[0]) / (bbox_ng[3] - bbox_ng[2])  # aspect ratio
                                if aR > 5:
                                    l['pengikut'] = -2
                            # print('masuk')
                            l['pengikut'] += 1
                            isNew = False
                        elif bbox_ng[0] > l['bbox'][0] or bbox_ng[1] < l['bbox'][1]:  ### x,p,y,q
                            qx = (l['bbox'][1] - bbox_ng[0])
                            py = (bbox_ng[0] - l['bbox'][1])
                            union = abs(qx - py)
                            intersect = min(qx, py)
                            iou = intersect / union
                            if iou > 0.3:
                                l['pengikut'] += 1
                                isNew = False

                if isNew == True:
                    # print('ga masuk')
                    newNG = dict(
                        Nama=tipeNG,
                        bbox=[bbox_ng[0] - 80, bbox_ng[1] + 80],
                        bboxY=[bbox_ng[2] - 50, bbox_ng[3] + 50],
                        pengikut=1,
                        bagian=ng_bagian)
                    Final.append(newNG)

    # print(Final)
    list_type_NG = []
    list_pengikut_NG = []
    list_bagian_NG = []
    for it in Final:
        # print(it)
        # if it['pengikut']>=2 and (it['Nama']=='keropos' or it['Nama']=='dakon'):# and it['pengikut']<10:
        #	list_type_NG.append(it['Nama'])
        #	list_pengikut_NG.append(it['pengikut'])
        #	list_bagian_NG.append(it['bagian'])
        #	print(it)
        if it['pengikut'] >= 3:  # and (it['Nama']=='kurokawa_forging' or it['Nama']=='scratch'):# and it['pengikut']<10:
            list_type_NG.append(it['Nama'])
            list_pengikut_NG.append(it['pengikut'])
            list_bagian_NG.append(it['bagian'])
            print(it)

    # if it['bagian']==2:
    # print(it)

    return list_type_NG, list_pengikut_NG, list_bagian_NG
