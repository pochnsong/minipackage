#!/usr/bin/env python
#coding=utf8
import sys;
import os;
import base64;
#----------------------------------------------------
def format_argv(ss):
    _code="";
    _value="";
    i=0;
    while i<len(ss):
        if ss[i]=='=':
            _value=ss[i+1:];
            break;
        _code=_code+ss[i];
        i=i+1;
    return _code,_value;
#----------------------------------------------------
def format_info(_str):
    return _str.strip()[1:];
#----------------------------------------------------
def release_data(path):
    fi=file(sys.argv[0],"r");
    while True:
        text=fi.readline();
        if not text:break;
        if "###***JJDL_DATA_SPFSE***###"==text.strip():
            if len(path)==0:
                path=format_info(fi.readline());
            else:
                fi.readline();
            filename=format_info(fi.readline());
            size=format_info(fi.readline());
            _pd=100.0/float(size);
            _filename=path+"/"+filename;
            _filepath=os.path.split(_filename)[0];
            try:os.makedirs(path);
            except:pass;
            try:os.makedirs(_filepath);
            except:pass;
            fo=file(_filename,"wb");
            print "正在解压文件:",_filename;
            I=0;
            while True:
                text=fi.readline();
                if "###***JJDL_DATA_END***###"==text.strip():
                    fo.close();
                    os.chmod(_filename,0777);
                    print "\r完成度：100%";
                    break;
                text_data=base64.decodestring(text[1:].strip());
                fo.write(text_data);
                I=I+_pd;
                print "\r完成度：",int(I),"%",

    fi.close();
    return 0;
#----------------------------------------------------
def main():
    path="";
    for i in sys.argv[1:]:
        code,value=format_argv(i);
        if code=="--path":
            path=value;
        if code=="--version":
            print "1.0-(SPFSE)-2.6";
            exit();
    release_data(path);
#----------------------------------------------------
main();

