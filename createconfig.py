#!/usr/bin/env python
#coding=utf8

import sys;
import os;

#----------------------------------------------------
def info():
    try:
        _hpname=sys.path[0]+"/help/help.createconfig";
        fi=file(_hpname,"r");
    except:
        print "错误：未找到帮助文件！";
        return;

    text=fi.readlines();
    fi.close();
    for i in text:
        print i,

#----------------------------------------------------
def get_file_list(_p):
    res=[];
    if os.path.isdir(_p):
        list_dir=os.listdir(_p);
        for i in list_dir:
            res=res+get_file_list(_p+"/"+i);
    else:
        res.append(_p);

    return res;

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
def main():
    _filename="";
    _dir="";
    _T="false";
    _O="";
    _size=True;
    for i in sys.argv[1:]:
        code,value=format_argv(i);
        if code=="--script":
            _filename=value;
            continue;
        elif code=="--src":
            _dir=value;
            if not _filename:
                _filename="MINIPACKAGE_"+os.path.split(_dir)[1]+"_CONFIG";
            if not _O:
                _O="install_"+os.path.split(_dir)[1]+"_minipackage.py";
            continue;
        elif code=="--help":
            info();
            return 0; 
        elif code=="--T:":
            if value=="false":
                _T="false";
            elif value=="true":
                _T="true";
            else:
                print "警告！忽略无效的 T:值",value;
            continue;
        elif code=="--size":
            if value=="false" or value=="off":
                _size=False;
            elif value=="true" or value=="on":
                _size=True;
            else:
                print "警告！忽略无效的 T:值",value;
            continue;
        elif code=="--O:":
            _O=value;
            continue;
        else:
            print "警告！已忽略无效的参数",code;
            
    if len(_dir):
        try:
            if _filename[0:1]!="/":
                _filename=os.getcwd()+"/"+_filename;
            fo=file(_filename,"w");
        except:
            print "错误!文件写入错误",_filename;
            return 1;
        
        print "正在创建配置文件:",_filename;
        if os.path.isdir(_dir):
            _index=len(os.path.split(_dir)[0]);
            if _index:
                _index=_index+1;
        else:
            _index=len(os.path.split(_dir)[0]);
        fo.write("O:"+_O+"\n");
        fo.write("T:"+_T+"\n");
        print "正在获取文件列表...";
        size_all=0;
        for i in get_file_list(_dir):
            try:
                size=os.path.getsize(i);
            except:
                print "警告！忽略丢失文件:",i;
                continue;
            print "正在写入文件:",i;
            size_all=size_all+size;
            fo.write("S:"+i+"\n");
            if _size:fo.write("//sizeof: "+str(size)+" byte\n");
            fo.write("P:.\n");
            fo.write("F:"+i[_index:]+"\n");
            fo.write("E:\n");

        if _size:
            fo.write("//sizeof(all):"+str(size_all)+" byte\n");
            size_all=float(size_all)/1024.0;
            fo.write("//sizeof(all):%0.3f KB\n"%size_all);
            size_all=float(size_all)/1024.0;
            fo.write("//sizeof(all):%0.3f MB\n"%size_all);
            size_all=float(size_all)/1024.0;
            fo.write("//sizeof(all):%0.3f GB\n"%size_all);


        fo.close();
        print "完成!";
    else:
        print "迷你打包工具箱-自动配置工具 1.0-(SPFE)-2.6";
        print "请输入 --help 获取帮助";
    return 0;
#----------------------------------------------------
main();
