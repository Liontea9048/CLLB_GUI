#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include "NoticeNKFADC500_1CH.h"

#define PC_DRAM_SIZE      (10)                      // available PC DRAM size in Mbyte
#define DATA_ARRAY_SIZE   (PC_DRAM_SIZE*1024*1024)  // array size in byte
#define MAX_SIZE          (PC_DRAM_SIZE*1024)       // array size in kilobyte

int main(int argc, char *argv[]) 
{

  struct timeval tv;
  
  // variables for daq code
  int run;			// DAQ status, 1 = running, 0 = stopped
  int data_size;		// data size
  char *data;			// data array
  FILE *fadc_fp;		// FADC data file pointer
  FILE *psd_fp;			// PSD data file pointer
  char fadc_filename[256] = {0};	// fadc data file name
  char psd_filename[256] = {0};	// psd data file name

  long long livetime;		// DAQ livetime
  int fadc_event_num;	        // # of fadc events taken
  int psd_event_num;	        // # of psd events taken

  char ip[256] = {0};
  char isoTope[11] = {0};
  int tcp_Handle = 0;
  int daq_mode = 0;

  if (argc < 3) {
    printf("enter IP address : ");
    scanf("%s", ip);
    printf("enter IsoTope : ");
    scanf("%s", isoTope);
    printf("enter DAQ mode (0 = charge only, 1 = waveform too) : ");
    scanf("%d", &daq_mode);
    printf("\n");
    printf("isoTope %s\n",isoTope);
  } else {
    sprintf(ip, "%s", argv[1]);
    sprintf(isoTope, "%s", argv[2]);
    daq_mode = atoi(argv[3]);
    printf("\n");
    printf("isoTope %s\n",isoTope);
  }

  // real time
  double start_Time, finish_Time;
  double duration_Time, dead_Time;
  
  // assign data array
  data = malloc(DATA_ARRAY_SIZE);

  // set filename  
  printf("\n");
  printf("isoTope %s\n\n",isoTope);
  //  sprintf(fadc_filename, "nkfadc500_fadc.dat"); // set fadc data file name here
  //  sprintf(psd_filename, "nkfadc500_psd.dat");   // set psd data file name here
  sprintf(fadc_filename, "nkfadc500_fadc_%s.dat", isoTope); // set fadc data file name here
  sprintf(psd_filename, "nkfadc500_psd_%s.dat", isoTope);   // set psd data file name here

  printf("\n");
  printf("isoTope %s\n\n",isoTope);

  printf("fadc_filename %s\n",fadc_filename);
  printf("psd_filename %s\n",psd_filename);
  printf("\n");
  
  // real time
  //  start_Time = clock();
  gettimeofday(&tv, NULL);
  start_Time = (tv.tv_sec)*1000 + (tv.tv_usec)/1000;
  
  // open NKFADC500
  tcp_Handle = NKFADC500_1CHopen(ip);

  // reset NKFADC500
  NKFADC500_1CHreset(tcp_Handle);

  // start DAQ
  NKFADC500_1CHstart(tcp_Handle);

  // open data file 
  if (daq_mode) fadc_fp = fopen(fadc_filename, "wb");
  psd_fp = fopen(psd_filename, "wb");

  run = 1;

  while (run) {

    if (daq_mode) {
      // check fadc data size
      data_size = NKFADC500_1CHread_DATASIZE(tcp_Handle);
      //if (!data_size) NKFADC500_1CHsend_TRIG(tcp_Handle);

      // if there are data, read them
      if (data_size) {
        // set limit for data sump size at one time, define it with PC_DRAM_SIZE 
        if (data_size > MAX_SIZE) data_size = MAX_SIZE;

        // read data
        NKFADC500_1CHread_DATA(tcp_Handle, data_size, data);

        // write data to data file
        fwrite(data, 1, data_size * 1024, fadc_fp);
      
        // print livetime and event #. If faster DAQ is necessary,
	// livetime reading can be omitted
        livetime = NKFADC500_1CHread_LIVETIME(tcp_Handle);
        fadc_event_num = NKFADC500_1CHread_EVENT_NUMBER(tcp_Handle);

	printf("%d FADC event are taken @ %f sec.\n", fadc_event_num, livetime/1E+09);
	//printf("%d FADC event are taken @ %lld ns.\n", fadc_event_num, livetime);
      }
      // if there are no data, check if run is ended. This can be used for PSD DAQ 
      //    else {
      //      run = NKFADC500_1CHread_RUN(tcp_Handle); 
      //    }
    }
    
    // check PSD data size to be read
    data_size = NKFADC500_1CHread_PSD_DATASIZE(tcp_Handle);

    // if there are data, read them
    if (data_size) {
      //printf("PSD data size = %d\n", data_size);
      // read data
      NKFADC500_1CHread_PSD_DATA(tcp_Handle, data_size, data);
      
      // write data to data file
      fwrite(data, 1, data_size * 16, psd_fp);

      // print livetime and event #. If faster DAQ is necessary,
      // livetime reading can be omitted
      livetime = NKFADC500_1CHread_LIVETIME(tcp_Handle);
      psd_event_num = NKFADC500_1CHread_PSD_EVENT_NUMBER(tcp_Handle);

      //printf("%d PSD event are taken @ %f sec.\n", psd_event_num, livetime/1E+09);
      //printf("%d PSD event are taken @ %lld ns.\n", psd_event_num, livetime);

    } else {
      run = NKFADC500_1CHread_RUN(tcp_Handle); 
    }

  } // while (run) {

  // write end of file
  data[0] = 0;
  if (daq_mode) fwrite(data, 1, 1, fadc_fp);
  fwrite(data, 1, 1, psd_fp);

  // close data file
  if (daq_mode) fclose(fadc_fp);
  fclose(psd_fp);
    
  // print # of events taken
  livetime = NKFADC500_1CHread_LIVETIME(tcp_Handle);

  fadc_event_num = NKFADC500_1CHread_EVENT_NUMBER(tcp_Handle);
  psd_event_num = NKFADC500_1CHread_PSD_EVENT_NUMBER(tcp_Handle);

  printf("\n\n");
  printf("FADC evt# = %d, livetime = %f sec.\n", fadc_event_num, livetime/1E+09);
  printf("PSD evt# = %d, livetime = %f sec.\n", psd_event_num, livetime/1E+09);
  //  printf("FADC evt# = %d, livetime = %lld\n", fadc_event_num, livetime);
  //  printf("PSD evt# = %d, livetime = %lld\n", psd_event_num, livetime);

  // reset NKFADC500
  NKFADC500_1CHreset(tcp_Handle);

  // close NKFADC500
  NKFADC500_1CHstop(tcp_Handle);

  // real time
  //  finish_Time = clock();
  gettimeofday(&tv, NULL);
  finish_Time = (tv.tv_sec)*1000 + (tv.tv_usec)/1000;
  duration_Time = (finish_Time - start_Time)/1000;
  dead_Time = (duration_Time - livetime/1E+09)/duration_Time;

  printf("realtime = %f sec. ; deadtime = %f\n", duration_Time, dead_Time);
  
  return 0;	
}

