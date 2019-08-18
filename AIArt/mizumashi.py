from PIL import Image
import os,glob,random,math,sys
import numpy as np

root_dir="./image/"
a = True if sys.argv[1]=="1" else False
categories=sys.argv[2:]
nb_classes = len(categories)
image_size=50

X=[]
Y=[]

def add_sample(cat,fname,is_train):
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size,image_size))
    data = np.asarray(img)
    X.append(data)
    Y.append(cat)
    if not a: return
    for ang in range(-40,40,2):
        img2 = img.rotate(ang)
        data = np.asarray(img2)
        X.append(data)
        Y.append(cat)
        img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)
        data = np.asarray(img2)
        X.append(data)
        Y.append(cat)


def make_sample(files,is_train):
    global X,Y
    X = []
    Y = []
    for cat, fname in files:
        print("[add] add sample ",cat,fname)
        add_sample(cat,fname,is_train)
    return np.array(X),np.array(Y)

allfiles = []
for idx, cat in enumerate(categories):
    image_dir=root_dir + cat
    files = glob.glob(image_dir + "/*.jpg")
    for f in files:
        allfiles.append((idx,f))

lens = len(allfiles)
random.shuffle(allfiles)
th = math.floor(len(allfiles) * 0.6)
train = allfiles[0:th]
test = allfiles[th:]
print("[add] train")
X_train,y_train = make_sample(train,True)
print("[add] test")
X_test,y_test = make_sample(test,True)
xy = (X_train,X_test,y_train,y_test)
print("[save] save")
np.save("./image/dogandcat.npy",xy)
print("[log] ok",lens ,"→",len(y_train))
