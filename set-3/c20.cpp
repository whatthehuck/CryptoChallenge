#include <bits/stdc++.h>
using namespace std;
int to[256];
int s[100][500];
int ta[500];
int ok[100][500];
int ans[500];
int main()
{
    for(int i=0; i<10; i++)
    {
        to['0'+i]=i;
    }
    for(int i=0; i<7; i++)
    {
        to['a'+i]=10+i;
    }
    //freopen("in.txt","r",stdin);
    freopen("in2.txt","r",stdin);   //use c18.py we got the ciphertext and saved them in in2.txt
    char c;
    int len;
    for(int i=0; i<60; i++)
    {
        int k=0;
        int now=0;
        while(scanf("%c",&c),c!='\n')
        {
            if(k%2)
            {
                now=now*16+to[c];
                if(i<59)
                {
                    s[i][k/2]=now;
                }
                else
                {
                    ta[k/2]=now;
                }
            }
            else
            {
                now=to[c];
            }
            k++;
        }
        if(i==59)
            len=k/2;
//        for(int j=0; j<k/2; j++)
//        {
//            printf("%d %d\n",s[i][j],isalpha(s[i][j]));
//        }
    }
    for(int i=0; i<60; i++)
    {
        for(int k=0; k<len; k++)
        {
            ok[i][k]=1;
        }
        for(int j=0; j<60; j++)
        {
            if(j==i)
                continue;
            for(int k=0; k<len; k++)
            {
                //ok[i][k]=(ok[i][k]&&(isalpha(s[i][k]^s[j][k])||((s[i][j]^s[j][k])==32)));
                ok[i][k]+=(bool)(isalpha(s[i][k]^s[j][k])||((s[i][j]^s[j][k])==32));
            }
        }

    }
    int p[500];
    int l[500];
    memset(l,-1,sizeof(l));
    for(int k=0; k<len; k++)
    {
        for(int i=0;i<60;i++)
        {
            if(ok[i][k]>l[k])
            {
                l[k]=ok[i][k];
                p[k]=i;
            }
        }
        int ttt=1;
        if(l[k]>42)
           ans[k]=(s[p[k]][k]^ta[k]^32);
    }
    char ss[500];
    for(int i=0;i<len;i++)
    {
        if(ans[i])
            ss[i]=ans[i];
        else
            ss[i]=' ';
    }
    printf("%s",ss);
    return 0;
}
// the plaintext we find is "Fnd we ou ta here / Yo  wha  happened t   eAce?   Peacev"
// the correct plaintext is "And we outta here / Yo, what happened to peace? / Peace"
