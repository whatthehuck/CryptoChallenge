#include <bits/stdc++.h>

using namespace std;
int p,q,n,e,d,np;
long long M=1;
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
void init(int x,int y)
{
    p=x;
    q=y;
    n=p*q;
    e=3;
    M*=n;
}
int pt[100][3];
void enc(string s,int now)                   //encryption of string
{
    for(int i=0; i<s.length(); i++)
    {
        pt[i][now] = rsaE((int)s[i]);
    }
}
string dec(int len,int now)                   //encryption of string
{
    string res="";
    for(int i=0; i<len; i++)
    {
        int tmp=rsaD(pt[i][now]);
        res+=(char)tmp;
        //printf("%d ",now);
    }
    return res;
}
int a[3];
int m[3];
int exgcd(int a,int b,int &x,int &y)
{
    if(b==0)
    {
        x=1;y=0;
        return a;
    }
    int r=exgcd(b,a%b,x,y);
    int t=x;
    x=y;
    y=(t-a/b*y);
    return r;
}

int china(int n)
{
    int ans=0;
    int x,y,d;
    for(int i=0;i<n;i++)
    {
        int mi=M/m[i];
        int x,y;
        d=exgcd(mi,m[i],x,y);
        ans=((long long)ans+(long long)a[i]*mi%M*x)%M;
    }
    while(ans<0)
        ans+=M;
    return ans;
}
int ans[100];

int e3(int x)
{
    for(int i=0;i<256;i++)
    {
        if((i*i*i)%M==x)
            return i;
    }
}
int main()
{
    string ct="c++ is a shabi language in crypto";
    init(17,11);
    m[0]=n;
    enc(ct,0);
    //cout<<dec(ct.length(),0)<<endl;
    init(23,29);
    m[1]=n;
    enc(ct,1);
    //cout<<dec(ct.length(),1)<<endl;
    init(41,5);
    m[2]=n;
    enc(ct,2);                                           //get the three results of encryption
    //cout<<dec(ct.length(),2)<<endl;
    string res="";

    for(int i=0;i<ct.length();i++)                       //start attack
    {
        for(int j=0;j<3;j++)
        {
            a[j]=pt[i][j];
        }
        ans[i]=china(3);                                 //use CRT to find the answer^3
        res+= e3(ans[i]);                                //find the root cube
    }
    cout<<res<<endl;
    return 0;
}
