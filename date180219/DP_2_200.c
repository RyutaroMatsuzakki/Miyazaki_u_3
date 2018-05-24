#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define RAND_SEED 2014628
#define N_DATA 200

#define SIGMA 0.1 // 加わるノイズの標準偏差
#define P00 0.99 // 状態遷移確率の定義．P01 は 0→1 の遷移確率
#define P01 0.01
#define P10 0.03
#define P11 0.97

/* ここではグローバル変数を使う．コードを短くし，分かりやすくするため． */
int x[N_DATA]; // もともとの信号． 0 か 1
int xmap[N_DATA]; // 推定値． 0 か 1
double y[N_DATA];  // 観測データ

int xhat[N_DATA][2];  // xhat[2][b] = argmax_a { ( f[2][a] + h(a,b) } 教科書  p.218 参照
double f[N_DATA][2];

double nrnd();

void generate_x (){

    int i;

    if ( drand48() < 0.5 ){ //初期値設定
        x[0]=0;
    }
    else{
        x[0]=1;
    }

    for (i=1; i<N_DATA; i++){   //確立によって数値を遷移させていく
        if(x[i - 1] == 0){
            if(drand48() < P00){
                x[i] = 0;
            }
            else{
                x[i] = 1;
            }
        }
        else{
            if(drand48() < P11){
                x[i] = 1;
            }
            else{
                x[i] = 0;
            }
        }
    }

}

void generate_y (){

    int i;
    for (i=0; i<N_DATA; i++){
        y[i]=(double)x[i] + SIGMA * nrnd();
    }

}


void compute_xmap (){

    int i = 0;
    f[i][0] = -pow((y[i] - 0), 2);
    f[i][1] = -pow((y[i] - 1), 2);
    for (i=1; i<N_DATA; i++){
        f[i][0] = f[i - 1][0] - pow((y[i] - 0), 2) +log(P00);
        if(f[i - 1][1] - pow((y[i] - 0), 2) + log(P10) > f[i][0]){
            f[i][0]= f[i - 1][1] - pow((y[i] - 0), 2) + log(P10);
            xhat[i][0] = 1;
        }
        else{
            xhat[i][0] = 0;
        }
        f[i][1] = f[i - 1][0] - pow((y[i] - 1), 2) + log(P01);
        if(f[i - 1][1] - pow((y[i] - 1), 2) + log(P11) > f[i][1]){
            f[i][1] = f[i - 1][1] - pow((y[i] - 1), 2) + log(P11);
            xhat[i][1] = 1;
        }
        else{
            xhat[i][1] = 0;
        }
    }
    if(f[i-1][0] > f[i-1][1]){
        xmap[i-1] = 0;
    }
    else{
        xmap[i-1] = 1;
    }
    for(i=199; i > 0; i--){
        xmap[i-1] = xhat[i][xmap[i]];
        /*printf("%d:xhat0= %d\n", i, xhat[i][0]);
        */
    }

}

void show_resuls(){

    int i;
    for (i=0; i<N_DATA; i++){
        printf("%d\t%d\t%.8lf\t%d\n",i+1, x[i],y[i],xmap[i] );
    }

}



/* 標準正規分布にしたがう擬似乱数の生成 */
double nrnd(){
    static int sw=0;
    static double r1,r2,s;

    if (sw==0){
        sw=1;
        do {
            r1=2.0*drand48()-1.0;
            r2=2.0*drand48()-1.0;
            s=r1*r1+r2*r2;
        } while (s>1.0 || s==0.0);
        s=sqrt(-2.0*log(s)/s);
        return(r1*s);
    }
    else {
        sw=0;
        return(r2*s);
    }
}


int main ( int argc , char * argv []){

    srand48(RAND_SEED); /* 擬似乱数の種を設定 */

/* 問題を作る（200 個のデータ生成） */
    generate_x ();
    generate_y ();

/* 復元する */
    compute_xmap ();

/* 結果を表示する */
    show_resuls();


    return 0;
}
