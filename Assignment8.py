from PIL import Image

def process(inp,out,key):
    img=Image.open(inp).convert("RGB")
    w,h=img.size
    px=img.load()
    for x in range(w):
        for y in range(h):
            r,g,b=px[x,y]
            px[x,y]=(r^key,g^key,b^key)
    img.save(out)

print("1 Encrypt")
print("2 Decrypt")
print("3 Exit")

while True:
    c=input("Choice: ")
    if c=="1":
        i=input("Input PNG: ")
        o=input("Output PNG: ")
        k=int(input("Key: "))
        process(i,o,k)
        print("Saved",o)
    elif c=="2":
        i=input("Input PNG: ")
        o=input("Output PNG: ")
        k=int(input("Key: "))
        process(i,o,k)
        print("Saved",o)
    elif c=="3":
        break
    else:
        print("Invalid")
