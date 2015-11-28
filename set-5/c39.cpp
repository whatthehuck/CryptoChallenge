#include <bits/stdc++.h>

using namespace std;
int p,q,n,e,d,np;
bool vi[1000];
long long prime[1000]; //some primes
void setprime()                 //find some primes
{
    np=0;
    for(int i=2; i<=1000; i++)
    {
        if(vi[i]==0)
        {
            prime[np++]=i;
        }
        for(int j=0; j<np&&i*prime[j]<=1000; j++)
        {
            vi[i*prime[j]]=1;
            if(i%prime[j]==0)
                break;
        }
    }
}
int phi(int x)                                 //Euler function
{
    int res=x;
    for(int i=2; i*i<=x; i++)
    {
        if(x%i==0)
        {
            res=res-res/i;
            while(x%i==0)
                x/=i;
        }
    }
    if(x>1)
        res=res-res/x;
    return res;
}
int _pow(int a,int b,int mod)                   //quick power with mod
{
    int res=1;
    while(b)
    {
        if(b&1)
        {
            res=(long long)res*a%mod;
        }
        a=(long long)a*a%mod;
        b>>=1;
    }
    return res;
}
int rsaE(int x)                                 //the encryption of RSA
{
    return _pow(x,e,n);
}
int rsaD(int x)                                 //the decryption of RSA
{
    int ph=phi((p-1)*(q-1));
    d=_pow(e,ph-1,(p-1)*(q-1));
    return _pow(x,d,n);
}
void init()
{
    setprime();                        //get some primes
    int i=rand()%np;
    int j=rand()%np;
    while(i==j)
    {
        j=rand()%np;
    }
    p=prime[i];
    q=prime[j];                        //get two different primes p and q
    while((((p-1)*(q-1)%3)==0)||(p*q<256)    )      //indicate that (p-1)*(q-1) and 3 are coprime
    {
        i=rand()%np;
        j=rand()%np;
        while(i==j)
        {
            j=rand()%np;
        }
        p=prime[i];
        q=prime[j];
    }
    //cout<<p<<" "<<q<<endl;
    n=p*q;
    e=3;
}
int pt[100];
void enc(string s)                   //encryption of string
{
    for(int i=0; i<s.length(); i++)
    {
        //printf("%d ",s[i]);
        pt[i] = rsaE((int)s[i]);
    }
}
string dec(int len)                   //encryption of string
{
    string res="";
    for(int i=0; i<len; i++)
    {
        int now=rsaD(pt[i]);
        res+=(char)now;
        //printf("%d ",now);
    }
    return res;
}
int main()
{
    init();
    string ct="c++ is a shabi language in crypto";
    enc(ct);
    cout<<dec(ct.length())<<endl;
    return 0;
}
