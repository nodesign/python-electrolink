import os
from collections import namedtuple

def getFileList(arg):
    path = arg[0]
    return os.listdir(path)

def writeFile(arg):
    name = arg[0]
    data = arg[1]
    try :
        f = open(name, "w")
        f.write(data)
        f.close()
        return "OK"
    except :
        raise Exception("File can't be written")

def getFile(arg):
    name = arg[0]
    if (is_binary(name) is True):
        raise Exception("Oups! This is a binary file. Only text files are allowed!")
    else :
        f = open(name, "r")
        data = f.read()
        f.close()
        return data

def deleteFile(arg):
    name = arg[0]
    try :
        os.remove(name)
        return "OK"
    except :
        raise Exception("File don't exist or can't be removed")


def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    p = path[0]
    st = os.statvfs(p)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    rslt = {"total" : str(intWithSpaces(total/1000000))+"Mb", \
            "used"  : str(intWithSpaces(used/1000000))+"Mb", \
            "free"  : str(intWithSpaces(free/1000000))+"Mb"}

    return rslt

def intWithSpaces(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = " %03d%s" % (r, result)
        #result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

def is_binary(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
    @author: Trent Mick <TrentM@ActiveState.com>
    @author: Jorge Orpinel <jorge@orpinel.com>"""
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
    finally:
        fin.close()

    return False

callbacks = {
      "getFileList": {"call": getFileList,  "parameters": "path",       "description": "Get file list in directory"},
      "writeFile":   {"call": writeFile,    "parameters": "path, data", "description": "Write data in file"}, 
      "getFile":     {"call": getFile,      "parameters": "path",       "description": "Get file data"},
      "deleteFile":  {"call": deleteFile,   "parameters": "path",       "description": "Delete specified file"},
      "diskUsage":   {"call": disk_usage,   "parameters": "path",       "description": "Get disk space info"}
      }
