#include <bits/stdc++.h>
using namespace std;


//写在前面
//此代码完全仿照网上的伪代码写出，内部的数学原理并不能看懂
long long mt[624];
int idx=0;
const long long l32=(1LL<<32)-1;
const long long l31=(1LL<<31)-1;
const long long nd32=(1LL<<32);
void ini(long long seed)                    //初始化函数，使用前需要调用
{
    idx=0;
    mt[0]=seed;
    for(int i=1;i<624;i++)
    {
        mt[i]=(1812433253LL*((mt[i-1]^(mt[i-1]>>30))+i))&(l32);
    }
}
void geneNum()                              //算法中的一些的数学变换
{
    for(int i=0;i<624;i++)
    {
        int y=(mt[i]&nd32)+((mt[(i+1)%624])&l31);
        mt[i]=mt[(i+397)%624]^(y>>1);
        if(y&1)
        {
            mt[i]^=(2567483615LL);
        }
    }
}
long long extNum()                          //提取得到的随机数
{
    if(idx==0)
    {
        geneNum();
    }
    long long y=mt[idx];
    y^=(y>>11);
    y^=((y<<7)&(2636928640LL));
    y^=((y<<15)&(4022730752LL));
    y^=(y>>18);
    idx=(idx+1)%624;
    return y;
}
int main()
{
    int seed =(rand()%961) + 40; //生成一个40到1000之间的随机seed
    ini(seed);                   //使用刚才生成的seed初始化mt19937
    int res=extNum();            //获得mt19937的一个输出
    for(int i=40;i<=1000;i++)    //暴力枚举40到1000之间的数  （可能为seed）
    {
        ini(i);
        int tmp=extNum();        //使用枚举的seed进行初始化并获得mt19937的一个输出
        if(res==tmp)
        {
            printf("the seed is %d\n",i);  //相等 则找到了seed.
        }
    }
    return 0;
}
