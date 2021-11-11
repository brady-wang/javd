import os.path


def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


def getFileSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    print(os.path.isfile('./cili/all/youma/h.m.p.txt'))
    size = os.path.getsize("./cili/all/youma/d.txt")
    try:
        size = os.path.getsize("./cili/all/youma/d.txt")
        print(size)
        print(formatSize(size))
    except Exception as err:
        print(err)
