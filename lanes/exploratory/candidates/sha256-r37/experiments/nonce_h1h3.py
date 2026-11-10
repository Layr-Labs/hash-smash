import sys,json,hashlib
M=0xffffffff
def R(x,n):return(x>>n|x<<32-n)&M
def cr(n):
    x=1<<n.bit_length()//3+1
    while 1:
        y=(2*x+n//(x*x))//3
        if y>=x:return x
        x=y
P=[p for p in range(2,160)if all(p%q for q in range(2,p))][:37]
K=[cr(p<<96)&M for p in P]
V=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
def F(w,d,t):
    s=lambda v:R(v,7)^R(v,18)^v>>3
    return(s(w+d&M)-s(w))&M==t
def cv(m):
    W=list(m)
    for i in range(16,37):a,b=W[i-2],W[i-15];W.append(sum((R(a,17)^R(a,19)^a>>10,W[i-7],R(b,7)^R(b,18)^b>>3,W[i-16]))&M)
    a,b,c,d,e,f,g,h=V
    for i in range(37):
        t=h+(R(e,6)^R(e,11)^R(e,25))+(e&f^~e&g)+K[i]+W[i];u=(R(a,2)^R(a,13)^R(a,22))+(a&b^a&c^b&c)
        h,g,f,e,d,c,b,a=g,f,e,d+t&M,c,b,a,t+u&M
    return[x+y&M for x,y in zip(V,(a,b,c,d,e,f,g,h))]
J=lambda x,y,z:x&y^x&z^y&z
def run(q):
    o=[]
    for r in q["trials"]:
        n=[0]*6
        for i in range(150):
            s=hashlib.shake_256((r["seed"]+str(i)).encode()).digest(64)
            c=cv([int.from_bytes(s[j:j+4],"big")for j in range(0,64,4)]);x=c[0];n[0]+=1;p=F(0x716a554f-x&M,0xfbc00800,0x017f8000);n[1]+=p;k=0
            for a in(0xee534104,0xee534107,0xee53410c,0xee53410f):
                z=0x8f5a9ca1;e=a+0x92cedd4c&M;w=(0x0ea5c39d-c[1]+J(z,a,x)-(0x76760d10&e^~0x76760d10&(0x044dd43e-J(0x6effba9c,z,a)+x&M)))&M
                f=F(w,0x20000000,0x03c00800);n[2]+=f;k+=f
            n[3]+=k>1;n[4]+=p*(k>0);n[5]+=p*k
        o.append({"trial":r["trial"],"message_a_hex":None,"message_b_hex":None,"observations":dict(zip(("blocks","w7","w6","coW6","w7_and_w6","w7_w6_pairs"),n))})
    return{"schema_version":1,"trials":o}
sys.stdout.write(json.dumps(run(json.loads(sys.stdin.read()))))
