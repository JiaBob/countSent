import re, os,chardet

wfile=open('countSentence.sql', 'w+')
sum=0
for root, dirs, files in os.walk(os.getcwd()):
   for file in files:
        if re.search('.txt$', file):
            path=os.path.join(root, file)
            _file=open(path, 'rb+')
            string=_file.read()
            coding=chardet.detect(string)['encoding']
            if coding:
                string=string.decode(coding)
            else:
                string=''
            subsum=0
            phrase=0
            token=0
            for word in string:
                if re.match(r'[\u3002\uff01\uff1f]', word):
                    subsum+=1
                    token=1
                elif re.match(r'\n', word):
                    phrase+=1
                if re.match(r'\n', word) and token==1:
                    phrase-=1
                    token=0
            #print("update logbook set file_entry='"+string+"' where uploadFile='"+str(file)+"';\n")
            wfile.write("update logbook set num_of_sent='"+str(subsum)+"',num_of_word='"+str(phrase//2)+"' where uploadFile='"+str(file)+"';\n")
            print(str(file))

wfile.close()
