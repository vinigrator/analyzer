# coding: utf-8

import os
import netaddr
import random
import collections
from arg_parser.parser import createParser
from PIL import Image, ImageDraw #Подключим необходимые библиотеки. 

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    countL = int(namespace.num) #Считываем количество файлов статистики
    fn = namespace.name
    #print namespace
    if not os.path.exists("dir_" + fn):
        os.mkdir("dir_" + fn)
    if not os.path.exists("dir_adp_" + fn):
        os.mkdir("dir_adp_" + fn)

    fs = countL + 3
    color = (255, 255, 255)
    width = 256**2	#2**scaleW
    koefH = 100
    space = 30
    height = (koefH+space)*fs

    imgPIX = []
    allAdr = set([])
    for j in range(fs):
        imgPIX.append(collections.defaultdict(set))
        #for i in range(256):
        #    imgPIX[j].append(set([]))

    r = lambda: random.randint(0,255)
    #all_ip = []
    colors = []
    for k in range(fs):
        colors.append((r(),r(),r()))

    for i in range(countL):
        with open("log\\" + fn + "_" + str(i + 1)) as f:
            for line in f:
                ip = line[:-1].split('.')
                imgnum = ip[0] + "." + ip[1]
                if not (ip[0] + "." + ip[1] in imgPIX[i]):
                    imgPIX[i].update({imgnum : set([])})
                allAdr.add(imgnum)
                ip[0] = '0'
                ip[1] = '0'
                startpx = int(netaddr.IPAddress((".".join(ip)).strip('.')))
                imgPIX[i][imgnum].add(startpx)

    if not namespace.adp:
        #агрегаты над множествами
        for k in allAdr:
            imgPIX[countL][k] = imgPIX[0][k]
            imgPIX[countL+1][k] = imgPIX[0][k]
            imgPIX[countL + 2][k] = imgPIX[0][k]
            for i in range(1,countL):
                imgPIX[countL][k] = imgPIX[countL][k] & imgPIX[i][k]
                imgPIX[countL+2][k] = imgPIX[countL+2][k] | imgPIX[i][k]
                imgPIX[countL+1][k] = (imgPIX[countL+1][k] ^ imgPIX[i][k]) - imgPIX[countL][k] #^ imgPIX[fs-2][k])

        imgPIX.append(collections.defaultdict())
        for k in allAdr:
            imgPIX[fs].update({k:{}})
            for ip in imgPIX[countL][k]:
                nip = ip >> 7
                if nip in imgPIX[fs][k] :
                    imgPIX[fs][k][nip] += 1
                else:
                    imgPIX[fs][k][nip] = 1

        imgPIX.append(collections.defaultdict())
        for k in allAdr:
            imgPIX[fs+1].update({k: {}})
            for ip in imgPIX[countL+1][k]:
                nip = ip >> 7
                if nip in imgPIX[fs+1][k] :
                    imgPIX[fs+1][k][nip] += 1
                else:
                    imgPIX[fs+1][k][nip] = 1

        if namespace.print_length_list:
            for i in range(fs):
                ipsinscan = 0
                for ips in imgPIX[i]:
                    ipsinscan += len(imgPIX[i][ips])
                if i < countL:
                    print u"Сканирование №" + str(i+1) + ": " + str(ipsinscan)
                elif i == countL:
                    print u"Пересчение сканирований: " + str(ipsinscan)
                elif i == countL + 1:
                    print u"Симметричная разница сканирований: " + str(ipsinscan)
                elif i == countL + 2:
                    print u"Объединение сканирований: " + str(ipsinscan)


    if not namespace.adp:
        with open("dir_" + fn +"/analysis.txt","w") as f:
            for k in allAdr:
                for ip in imgPIX[fs+1][k]:
                    if ((ip in imgPIX[fs][k]) and imgPIX[fs+1][k][ip] > 9):
                    #if (ip in imgPIX[fs][k]) and (imgPIX[fs+1][k][ip] > imgPIX[fs][k][ip]) and (abs(int(imgPIX[fs+1][k][ip]) - int(imgPIX[fs][k][ip])) > 3) :
                        stroka = u"Аномалия! файл:\t" + str(k) + u"\tблок " + str(netaddr.IPAddress(ip << 7)) + u".\t\tРазных:\t" + str(
                            imgPIX[fs + 1][k][ip]) + u".\tОдинаковых:\t" + str(imgPIX[fs][k][ip]) + u"\n"
                        f.write(stroka.encode('utf-8'))
                    elif not(ip in imgPIX[fs][k]) and (imgPIX[fs+1][k][ip] > 10):
                        stroka = u"Аномалия! файл:\t" + str(k) + u"\tблок " + str(netaddr.IPAddress(ip << 7))  + u".\t\tРазных:\t" + str(
                            imgPIX[fs + 1][k][ip]) + u".\tОдинаковых:\t0" + u"\n"
                        f.write(stroka.encode('utf-8'))
                    #elif (imgPIX[fs+1][k][ip] > 10):
                    #    stroka = u"Аномалия! файл:\t" + str(k) + u"\tблок " + str(ip << 7) + u".\tРазных:\t" + str(
                    #        imgPIX[fs + 1][k][ip]) + u".\tОдинаковых:\t0" + u"\n"
                    #    f.write(stroka.encode('utf-8'))
                    #elif ((ip in imgPIX[fs][k]) and (abs(int(imgPIX[fs+1][k][ip]) - int(imgPIX[fs][k][ip])) > 3)):
                    #    stroka = u"Аномалия! файл:\t" + str(k) + u"\tблок " + str(netaddr.IPAddress(ip << 7))  + u".\t\tРазных:\t" + str(
                    #        imgPIX[fs + 1][k][ip]) + u".\tОдинаковых:\t" + str(imgPIX[fs][k][ip]) + u"\n"
                    #    f.write(stroka.encode('utf-8'))

    if namespace.adp:
        w = 2 ** 12+16
        h = 2 ** 12+16
        img = Image.new('RGB', (w, h), color)
        draw = ImageDraw.Draw(img)
        for col in range(256, 2 ** 12+16, 257):
            draw.line((col, 0, col, h), (255, 0, 0))
            draw.line((0, col, w, col), (255, 0, 0))
        for i in allAdr:
            numLine = 0
            for ip in imgPIX[numLine][i]:
                numSQ = int(i.split(".")[1])
                fname = i.split(".")[0]
                '''
                coor = str(netaddr.IPAddress(ip)).split('.')
                strFullIP = str(i) + "." + coor[2] + "." + coor[3]
                ip = strFullIP.split(".")
                fname = ip[0]
                ip[0] = "0"
                intIP = int(netaddr.IPAddress(".".join(ip)))
                '''
                coor = str(netaddr.IPAddress(ip)).split('.')
                shiftX = (numSQ % 15) * 257
                shiftY = (numSQ / 16) * 257
                x = int(coor[3]) + shiftX #& (2**12-1)
                y = int(coor[2]) + shiftY #>> 12

                draw.point((x,y), (0, 0, 0))
                #draw.line((ip, (numLine)*(koefH+1+space),ip, (numLine)*(koefH+1+space)+koefH), colors[numLine])
        img.save("dir_adp_" + fn + "/" + str(fname) + ".png", "PNG")
        del draw
        # print str(netaddr.IPAddress(i)) + " " + str(i)
        # print str(int(netaddr.IPAddress("0.0."+i))) + " " + str(ip)
        # draw.point((int(netaddr.IPAddress("0.0."+i)), int(ip)), colors[0])
        # draw.point((int(netaddr.IPAddress("0.0." + i)), int(ip)), (0,0,0))

    if not namespace.only_anomal_text:
        for i in allAdr:
            img = Image.new('RGB', (width, height), color)
            draw = ImageDraw.Draw(img)
            for col in range(0,256**2,128):
                draw.line((col, 0, col, width), (0,0,0))
                draw.text((col + 5, height-10),str(netaddr.IPAddress(col)).split('.',2)[2],  (0,0,0))
            for numLine in range(fs):
                for ip in imgPIX[numLine][i]:
                    draw.line((ip, (numLine)*(koefH+1+space),ip, (numLine)*(koefH+1+space)+koefH), colors[numLine])
                for col in range(0, 256 ** 2, 1000):
                    #str(netaddr.IPAddress(col))
                    if numLine < countL:
                        draw.text((col , (numLine)*(koefH+1+space)+koefH+10), fn + "_" + str(numLine+1), colors[numLine])
                    elif numLine == countL:
                        draw.text((col, (numLine)*(koefH+1+space)+koefH+10), u"intersection:", colors[numLine])
                    elif numLine == countL+1:
                        draw.text((col , (numLine)*(koefH+1+space)+koefH+10), u"difference:", colors[numLine])
                    elif numLine == countL+2:
                        draw.text((col, (numLine)*(koefH+1+space)+koefH+10), u"union:", colors[numLine])
            img.save("dir_" + fn +"/" + str(i) + ".png", "PNG")
        del draw