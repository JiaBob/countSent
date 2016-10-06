import re, os,chardet,time,datetime
import countlib

date=datetime.date.today()
wfile=open('countSentence.sql', 'w+')
sum=0
for root, dirs, files in os.walk(os.getcwd()):
   for file in files:
        if re.search('.txt$', file):
            path=os.path.join(root, file)
            if datetime.date.fromtimestamp(os.stat(path).st_ctime-1000)==date:
                _file=open(path, 'rb+')
                string=_file.read()
                coding=chardet.detect(string)['encoding']
                if coding:
                    string=string.decode(coding)
                else:
                    string=''
                result=countlib.countBoth_ch(string)
                #print("update logbook set file_entry='"+string+"' where uploadFile='"+str(file)+"';\n")
                wfile.write("update logbook set num_of_sent='"+str(result[0])+"',num_of_word='"+str(result[1])+"' where uploadFile='"+str(file)+"';\n")
                print(str(file))

wfile.close()
