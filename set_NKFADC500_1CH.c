#include <unistd.h>
#include <stdio.h>
#include "NoticeNKFADC500_1CH.h"

int main(int argc, char *argv[]) 
{
  //  long long acq_time = 1000000000; // acquisition time in ns, upto 2^40 ns
  long long acq_time = 600;    // acquisition time in sec
  float hv = 1000.0;                  // high voltage in volt, 0 ~ 2,000
  int rl = 16;	 // recording length: 1=128ns, 2=256ns, 3=512ns, 8=1us, 16=2us, 32=4us, 64=8us
  int ptrig_interval = 0;    // pedestal trigger interval in ms, 0 for disable
  int offset = 3500;         // ADC offset value (0~4095)
  int dly = 100;             // ADC waveform delay from trigger point (0 ~ 8,000)
  int thr = 100;	     // discrimination threshold, 1 ~ 4095
  int pol = 0;		     // input pulse polarity, 0 = negative, 1 = positive
  int psw = 250;	     // peak sum width in ns (8 ~ 8000 ns)
  int amode = 1;	     // ADC mode, 0 = raw, 1 = filtered
  int tail_dly = 80;         // peak to tail start delay, 0 ~ 8000 ns
  float frt = 0.1;           // tail/body ratio threshold
  FILE *fp;
  char ip[256];
  int tcp_Handle = 0;
  
  if (argc < 2) {
    printf("enter IP address : ");
    scanf("%s", ip);
  } else sprintf(ip, "%s", argv[1]);

  // read setup.txt
  fp = fopen("setup.txt", "rt");
  if (fp != NULL) {
    fscanf(fp, "%lld", &acq_time);
    fscanf(fp, "%f", &hv);
    fscanf(fp, "%d", &rl);
    fscanf(fp, "%d", &ptrig_interval);
    fscanf(fp, "%d", &offset);
    fscanf(fp, "%d", &dly);
    fscanf(fp, "%d", &thr);
    fscanf(fp, "%d", &pol);
    fscanf(fp, "%d", &psw);
    fscanf(fp, "%d", &amode);
    fscanf(fp, "%d", &tail_dly);
    fscanf(fp, "%f", &frt);
  }

  // open KFADC500_1CH
  tcp_Handle = NKFADC500_1CHopen(ip);

  // reset and initialize NKFADC500_1CH
  NKFADC500_1CHreset(tcp_Handle);
  NKFADC500_1CHalign_ADC(tcp_Handle);
  NKFADC500_1CHwrite_DRAMON(tcp_Handle, 1);
  NKFADC500_1CHalign_DRAM(tcp_Handle);

  // set NKFADC500_1CH
  NKFADC500_1CHwrite_ACQUISITION_TIME(tcp_Handle, (long long)(acq_time*1E+09));
  NKFADC500_1CHwrite_HV(tcp_Handle, hv);
  NKFADC500_1CHwrite_RL(tcp_Handle, rl);
  NKFADC500_1CHwrite_PTRIG(tcp_Handle, ptrig_interval);
  NKFADC500_1CHwrite_DACOFF(tcp_Handle, offset);
  NKFADC500_1CHmeasure_PED(tcp_Handle);
  NKFADC500_1CHwrite_DLY(tcp_Handle, dly);
  NKFADC500_1CHwrite_THR(tcp_Handle, thr);
  NKFADC500_1CHwrite_POL(tcp_Handle, pol);
  NKFADC500_1CHwrite_PSW(tcp_Handle, psw);
  NKFADC500_1CHwrite_AMODE(tcp_Handle, amode);
  NKFADC500_1CHwrite_TAILDLY(tcp_Handle, tail_dly);
  NKFADC500_1CHwrite_FRT(tcp_Handle, frt);

  // readback setting registers
  printf("module ID = %d\n", NKFADC500_1CHread_MID(tcp_Handle));
  printf("high voltage = %f\n", NKFADC500_1CHread_HV(tcp_Handle));
  printf("recording length = %d\n", NKFADC500_1CHread_RL(tcp_Handle));
  printf("dramon = %d\n", NKFADC500_1CHread_DRAMON(tcp_Handle));
  printf("pedestal trigger interval = %d ms\n", NKFADC500_1CHread_PTRIG(tcp_Handle));
  printf("pedestal = %d\n", NKFADC500_1CHread_PED(tcp_Handle));
  printf("dly = %d\n", NKFADC500_1CHread_DLY(tcp_Handle));
  printf("thr = %d\n", NKFADC500_1CHread_THR(tcp_Handle));
  printf("pol = %d\n", NKFADC500_1CHread_POL(tcp_Handle));
  printf("psw = %d\n", NKFADC500_1CHread_PSW(tcp_Handle));
  printf("amode = %d\n", NKFADC500_1CHread_AMODE(tcp_Handle));
  printf("tail delay = %d\n", NKFADC500_1CHread_TAILDLY(tcp_Handle));
  printf("tail/body ratio threshold = %f\n", NKFADC500_1CHread_FRT(tcp_Handle));

  // reset NKFADC500_1CH
  NKFADC500_1CHreset(tcp_Handle);

  // close NKFADC500_1CH
  NKFADC500_1CHclose(tcp_Handle);

  return 0;	
}

