def L(x,n):
    return ((x<<n)&0xffffffff)|((x&0xffffffff)>>(32-n))

def sha1(m):
    h0=0x67452301
    h1=0xEFCDAB89
    h2=0x98BADCFE
    h3=0x10325476
    h4=0xC3D2E1F0
    ml=len(m)*8
    m=m.encode()
    m+=b'\x80'
    while ((len(m)*8)%512)!=448:
        m+=b'\x00'
    m+=ml.to_bytes(8,'big')
    for i in range(0,len(m),64):
        chunk=m[i:i+64]
        w=[0]*80
        for j in range(16):
            w[j]=int.from_bytes(chunk[j*4:j*4+4],'big')
        for j in range(16,80):
            w[j]=L(w[j-3]^w[j-8]^w[j-14]^w[j-16],1)
        a=h0
        b=h1
        c=h2
        d=h3
        e=h4
        for j in range(80):
            if j<20:
                f=(b&c)|((~b)&d)
                k=0x5A827999
            elif j<40:
                f=b^c^d
                k=0x6ED9EBA1
            elif j<60:
                f=(b&c)|(b&d)|(c&d)
                k=0x8F1BBCDC
            else:
                f=b^c^d
                k=0xCA62C1D6
            t=(L(a,5)+f+e+k+w[j])&0xffffffff
            e=d
            d=c
            c=L(b,30)
            b=a
            a=t
        h0=(h0+a)&0xffffffff
        h1=(h1+b)&0xffffffff
        h2=(h2+c)&0xffffffff
        h3=(h3+d)&0xffffffff
        h4=(h4+e)&0xffffffff
    return "".join(f"{x:08X}" for x in (h0,h1,h2,h3,h4))

msg=input("Enter the message to be hashed: ")
h=sha1(msg)
print("\nSHA-1 Hash of the message is:",h)
print("\nFirst 8 characters of the hash are:",h[:8])
