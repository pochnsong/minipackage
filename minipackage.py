#!/usr/bin/env python
#coding=utf8
#version SPFSE
import sys;
import os;
import uuid;
import base64;
import py_compile;

def version():
    print "当前版本: 1.0-(SPFSE)-2.6";
#---------------------------------------------------------------
def info():
    try:
        _hpname=sys.path[0]+"/help/help.minipackage";
        fi=file(_hpname,"r");
    except:
        print "错误：未找到帮助文件！";
        return;

    text=fi.readlines();
    fi.close();
    for i in text:
        print i,
    
#---------------------------------------------------------------
#追加数据
#_file:头文件 
#_src_file:源文件
#_path:路径
#_filename:文件名
#_num：文件大小
#_pd:百分比

def append_data(_file,_src_file,_path,_filename):
    if not os.path.exists(_src_file):
        print "错误！文件",_src_file,"不存在!";
        return 2;

    print "正在处理文件：",_src_file;
    _size=float(os.stat(_src_file).st_size)//float(57)+1.0;
    _pd=100.0/_size;
    _size=str(_size);
    try:
        fi=file(_src_file,"rb");
        f=file(_file,"a");
    except:
        print "错误！文件读取错误!";
        return 1;
    f.write("\n###***JJDL_DATA_SPFSE***###\n");
    f.write("#"+_path+"\n");
    f.write("#"+_filename+"\n");
    f.write("#"+_size+"\n");

    _I=0;
    while True:
        text=fi.read(57);
        if not text:break;
        text_data="#"+base64.encodestring(text);
        f.write(text_data);
        _I=_I+_pd;
        if _I>100:_I=100;
        print "\r完成度：",int(_I),"%",
    f.write("###***JJDL_DATA_END***###");
    f.close();
    fi.close();
    print "\r完成度： 100 %";
    return 0;

#----------------------------------------------------
#----------------------------------------------------
def format_info(_str):
    return _str.strip()[1:];
#----------------------------------------------------
def release_data(FileIn,path):
    try:
        fi=file(FileIn,"r");
    except:
        print "错误！文件：",FileIn,"读取错误。";
        return 1;
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
                    print "\r完成度： 100 %";
                    break;
                text_data=base64.decodestring(text[1:].strip());
                fo.write(text_data);
                I=I+_pd;
                print "\r完成度：",int(I),"%",

    fi.close();
    return 0;
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
#---------------------------------------------------
def create_setup(_file,_datalist,_c):

    if _c:
        try:
            py_compile.compile(sys.path[0]+"/release_head.py");
            frel=file(sys.path[0]+"/release_head.pyc","r");
        except:
            print "错误！无法加载自解模块 release_head.pyc ";
            return 1;
    else:
        try:
            frel=file(sys.path[0]+"/release_head.py","r");
        except:
            print "错误！无法加载自解模块 release_head.py ";
            return 2;

    try:
        os.makedirs(os.path.split(_file)[0]);
    except:
        pass;
    try:
        f=file(_file,"w");
    except:
        print "错误！无法写入文件",_file;
        return 3;

    f.write(frel.read());
    f.close();
    frel.close();
    for I in _datalist:
        append_data(_file,I[0],I[1],I[2]);
    os.chmod(_file,0777);
    return 0;

#---------------------------------------------------
def script(_script_file):
    try:
        fi=file(_script_file,"r");
    except:
        print "脚本读取错误:",_script_file;
        return 1;
    ScriptList=[];
    _stype=False;
    filename="MINISetup_"+os.path.split(_script_file)[1]+".py";
    i=0;
    while True:
        text=fi.readline();i=i+1;
        if not text:break;
        text=text.strip();
        if not text:
            continue;
        elif text[0:2]=="//":
            continue;
        elif text[0:2]=="O:":
            filename=text[2:].strip();
        elif text[0:2]=="T:":
            if text[2:].strip()=="false":
                _stype=False;
            elif text[2:].strip()=="true":
                _stype=True;
            else:
                print "忽略警告！行号:",i,text,"; (T:)非标准的类型定义。已被定义成默认值 false";
                _stype=False;
        elif text[0:2]=="S:":
            _src=text[2:].strip();
            _P=".";
            _F=os.path.split(_src)[1];
            while True:
                text=fi.readline();i=i+1;
                if not text:
                    print "错误！行号:",i,"; 缺少结束符号 (E:)";
                    return 2;
                text=text.strip();
                if not text:
                    continue;
                elif text[0:2]=="//":
                    continue;
                elif text[0:2]=="E:":
                    ScriptList.append([_src,_P,_F]);
                    break;
                elif text[0:2]=="P:":
                    _P=text[2:].strip();
                elif text[0:2]=="F:":
                    _F=text[2:].strip();
                else:
                    print "错误！行号:",i,"; 无效的说明行",text;
                    return 2;
        else:
            print "错误！行号:",i,"; 缺少开始符号 (S:)",text;
            return 3;
    print filename;
    if filename[0:1]!="/":
        filename=os.getcwd()+"/"+filename;
    create_setup(filename,ScriptList,_stype);
    
#---------------------------------------------------
#---------------------------------------------------
def main():
    _S="";
    _P=".";
    _F="";
    _T=False;
    _script="";
    _path="";
    _release="";
    _add="";
    _new="";
    _info=True;
    for i in sys.argv[1:]:
        code,value=format_argv(i);
        if code=="--version":
            version();
            _info=False;
            continue;
        elif code=="--help":
            info();
            _info=False;
            continue;
        elif code=="--release":
            _release=value;
            continue;
        elif code=="--path":
            _path=value;
            continue;
        elif code=="--add":
            _add=value;
            continue;
        elif code=="--S:":
            _S=value;
            _F=os.path.split(_S)[1];
            continue;
        elif code=="--P:":
            _P=value;
            continue;
        elif code=="--F:":
            _F=value;
            continue;
        elif code=="--T:":
            if value=="true":
                _T=True;
            elif value=="false":
                _T=False;
            else:
                print "警告！无效的 T：值。已定义成默认值 true ";
            continue;
        elif code=="--new":
            _new=value;
            continue;
        elif code=="--script":
            _script=value;
            continue;
        else:
            print "警告：忽略无效的参数 ",code;

    if len(_script):
        script(_script);
        _info=False;

    if len(_release):
        release_data(_release,_path);
        _info=False;

    if len(_new):
        if len(_S):
            print "正在创建文件：",_new;
            create_setup(_new,[[_S,_P,_F]],_T);
        else:
            print "缺少源文件,请使用 --S: 添加源文件";
        _info=False;

    if len(_add):
        if len(_S):
            print "正在追加文件",_S,"到文件",_add;
            append_data(_add,_S,_P,_F);
        else:
            print "缺少源文件,请使用 --S: 添加源文件";
        _info=False;

    if _info:
        print "迷你打包工具箱 1.0-(SPFSE)\nminipackage 1.0-(SPFSE)";
        print "JJDL-二进制人类工作室";
        print "请使用 --help 获取帮助。";
    return 0;
#---------------------------------------------------
main();
