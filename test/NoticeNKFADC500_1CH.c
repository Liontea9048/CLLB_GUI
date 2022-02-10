#include <sys/time.h>
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

#include "NoticeNKFADC500_1CH.h"

// internal functions
int NKFADC500_1CHtransmit(int tcp_Handle, char *buf, int len);
int NKFADC500_1CHreceive(int tcp_Handle, char *buf, int len);
void NKFADC500_1CHwrite(int tcp_Handle, int address, int data);
int NKFADC500_1CHread(int tcp_Handle, int address);
void NKFADC500_1CHblockread(int tcp_Handle, int addr, int datasize, char *data);
void NKFADC500_1CHenter_BOOTLOADER(int tcp_Handle);
void NKFADC500_1CHexit_BOOTLOADER(int tcp_Handle);
void NKFADC500_1CHprogram_MCU(int tcp_Handle, int flag, int page, unsigned char *data);
void NKFADC500_1CHsend_ADCCAL(int tcp_Handle);
void NKFADC500_1CHsend_ADCRST(int tcp_Handle);
void NKFADC500_1CHwrite_ADCDLY(int tcp_Handle, int data);
void NKFADC500_1CHwrite_ADCALIGN(int tcp_Handle, int data);
int NKFADC500_1CHread_ADCSTAT(int tcp_Handle);
void NKFADC500_1CHwrite_DRAMDLY(int tcp_Handle, int ch, int data);
void NKFADC500_1CHwrite_BITSLIP(int tcp_Handle, int ch);
void NKFADC500_1CHwrite_DRAMTEST(int tcp_Handle, int data);
int NKFADC500_1CHread_DRAMTEST(int tcp_Handle, int ch);

// transmit characters to NKFADC500_1CH
int NKFADC500_1CHtransmit(int tcp_Handle, char *buf, int len)
{
  int result;
  int bytes_more;
  int  bytes_xferd;
  char *idxPtr;

  bytes_more = len;
  idxPtr = buf;
  bytes_xferd = 0;
  while (1) {
    idxPtr = buf + bytes_xferd;
    result=write (tcp_Handle, (char *) idxPtr, bytes_more);

    if (result<0) {
      printf("Could not write the rest of the block successfully, returned: %d\n",bytes_more);
      return -1;
    }
    
    bytes_xferd += result;
    bytes_more -= result;
    
    if (bytes_more <= 0)
      break;
  }

  return 0;
}

// receive characters from NKFADC500_1CH
int NKFADC500_1CHreceive(int tcp_Handle, char *buf, int len)
{
  int result;
  int accum;
  int space_left;
  int bytes_more;
  int buf_count;
  char *idxPtr;

  fd_set rfds;
//  struct timeval tval;

//  tval.tv_sec = MAX_TCP_READ;
//  tval.tv_usec = 0;

  FD_ZERO(&rfds);
  FD_SET(tcp_Handle, &rfds);

  if (buf==NULL)
    return -1;

  idxPtr = buf;

  buf_count = 0;
  space_left = len;
  while (1) {
    accum = 0;
    while (1) {
      idxPtr = buf + (buf_count + accum);
      bytes_more = space_left;
      
      if ((result = read(tcp_Handle, (char *) idxPtr, (bytes_more>2048)?2048:bytes_more)) < 0) {
        printf("Unable to receive data from the server.\n");
        return -1;
      }
      
      accum += result;
      if ((accum + buf_count) >= len)
	break;

      if(result<bytes_more) {
        printf("wanted %d got %d \n",bytes_more,result);
        return accum+buf_count;
      }
    }
    
    buf_count += accum;
    space_left -= accum;

    if (space_left <= 0)
      break;
  }

  return buf_count;
}

// write to NKFADC500_1CH
void NKFADC500_1CHwrite(int tcp_Handle, int address, int data)
{
  char tcpBuf[3];

  tcpBuf[0] = 1;
  tcpBuf[1] = address & 0xFF;
  tcpBuf[2] = data & 0xFF;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 3);
  
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// read from NKFADC500_1CH
int NKFADC500_1CHread(int tcp_Handle, int address)
{
  char tcpBuf[2];
  int data;

  tcpBuf[0] = 2;
  tcpBuf[1] = address & 0xFF;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 2);
  
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);

  data = tcpBuf[0] & 0xFF;

  return data;
}

// block read from NKFADC500_1CH
void NKFADC500_1CHblockread(int tcp_Handle, int addr, int datasize, char *data)
{
  char tcpBuf[1024];

  tcpBuf[0] = 3;
  tcpBuf[1] = (addr >> 5) & 0x2;
  tcpBuf[2] = datasize & 0xFF;
  tcpBuf[3] = (datasize >> 8) & 0xFF;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 4);
  
  NKFADC500_1CHreceive(tcp_Handle, data, datasize);
}

// enter to bootloader
void NKFADC500_1CHenter_BOOTLOADER(int tcp_Handle)
{
  char tcpBuf[2];
	
  tcpBuf[0] = 31;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 1);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// exit out of bootloader
void NKFADC500_1CHexit_BOOTLOADER(int tcp_Handle)
{
  char tcpBuf[2];
	
  tcpBuf[0] = 30;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 1);
}

// program MCU flash memory page
void NKFADC500_1CHprogram_MCU(int tcp_Handle, int flag, int page, unsigned char *data)
{
  char tcpBuf[259];
  int i;
  
  tcpBuf[0] = 32;
  tcpBuf[1] = flag & 0xFF;
  tcpBuf[2] = page & 0xFF;
  for (i = 0; i < 256; i++)
    tcpBuf[i + 3] = data[i] & 0xFF;
  
  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 259);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// send ADC calibration signal
void NKFADC500_1CHsend_ADCCAL(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x2F, 0);
}

// send ADC reset signal
void NKFADC500_1CHsend_ADCRST(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x30, 0);
}

// write ADC calibration delay
void NKFADC500_1CHwrite_ADCDLY(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x31, data);
}

// write ADC test mode
void NKFADC500_1CHwrite_ADCALIGN(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x32, data);
}

// read ADC alignment status
int NKFADC500_1CHread_ADCSTAT(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x33, 0);
  return NKFADC500_1CHread(tcp_Handle, 0x33);
}

// write DRAM calibration delay
void NKFADC500_1CHwrite_DRAMDLY(int tcp_Handle, int ch, int data)
{
  if (ch)
    NKFADC500_1CHwrite(tcp_Handle, 0x35, data);
  else
    NKFADC500_1CHwrite(tcp_Handle, 0x34, data);
}

// write DRAM bitslip
void NKFADC500_1CHwrite_BITSLIP(int tcp_Handle, int ch)
{
  if (ch)
    NKFADC500_1CHwrite(tcp_Handle, 0x37, 0);
  else
    NKFADC500_1CHwrite(tcp_Handle, 0x36, 0);
}

// write DRAM test 
void NKFADC500_1CHwrite_DRAMTEST(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x38, data);
}

// read DRAM alignment
int NKFADC500_1CHread_DRAMTEST(int tcp_Handle, int ch)
{
  int addr;
  int data;
  int ival;

  if (ch)
    addr = 0x3C;
  else
    addr = 0x38;
  
  data = NKFADC500_1CHread(tcp_Handle, addr);
  ival = NKFADC500_1CHread(tcp_Handle, addr + 1);
  ival = ival << 8;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, addr + 2);
  ival = ival << 16;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, addr + 3);
  ival = ival << 24;
  data = data + ival;
  
  return data;
}

// ****************** end of internal functions ************************

// open NKFADC500_1CH
int NKFADC500_1CHopen(char *ip)
{
  struct sockaddr_in serv_addr;
  int tcp_Handle;
  const int disable = 1;
        
  serv_addr.sin_family      = AF_INET;
  serv_addr.sin_addr.s_addr = inet_addr(ip);
  serv_addr.sin_port        = htons(5000);
        
  if ( (tcp_Handle = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    printf("Can't open NKFADC500_1CH\n");
    return -1;
  }

  setsockopt(tcp_Handle, IPPROTO_TCP,TCP_NODELAY,(char *) &disable, sizeof(disable)); 

  if (connect(tcp_Handle, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
    printf("client: can't connect to server\n");
    printf("ip %s , port 5000 \n", ip);
    printf("error number is %d \n", connect(tcp_Handle, (struct sockaddr *) &serv_addr,sizeof(serv_addr)));

    return -2;
  } 
  
  return tcp_Handle;
}

// close NKFADC500_1CH
void NKFADC500_1CHclose(int tcp_Handle)
{
  close(tcp_Handle);
}

// unprotect flash memory
void NKFADC500_1CHenable_FLASH(int tcp_Handle)
{
  char tcpBuf[2];
	
  tcpBuf[0] = 21;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 1);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// protect flash memory
void NKFADC500_1CHfinish_FLASH(int tcp_Handle)
{
  char tcpBuf[2];
	
  tcpBuf[0] = 22;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 1);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// erase flash memory
void NKFADC500_1CHerase_FLASH(int tcp_Handle, int sector)
{
  char tcpBuf[2];
	
  tcpBuf[0] = 23;
  tcpBuf[1] = sector & 0xFF;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 2);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// write flash memory
void NKFADC500_1CHwrite_FLASH(int tcp_Handle, int sector, int addrH, char *data)
{
  char tcpBuf[259];
  int i;
	
  tcpBuf[0] = 24;
  tcpBuf[1] = sector & 0xFF;
  tcpBuf[2] = addrH & 0xFF;
	
  for (i = 0; i < 256; i++)
    tcpBuf[i + 3] = data[i] & 0xFF;

  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 259);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 1);
}

// read flash memory
void NKFADC500_1CHread_FLASH(int tcp_Handle, int sector, int addrH, char *data)
{
  char tcpBuf[256];
  int i;
	
  tcpBuf[0] = 25;
  tcpBuf[1] = sector & 0xFF;
  tcpBuf[2] = addrH & 0xFF;
	
  NKFADC500_1CHtransmit(tcp_Handle, tcpBuf, 3);
  NKFADC500_1CHreceive(tcp_Handle, tcpBuf, 256);
	
  for (i = 0; i < 256; i++)
    data[i] = tcpBuf[i] & 0xFF;
}

/*
// update MCU firmware
void NKFADC500_1CHupdate_MCU(int tcp_Handle, char *filename)
{
  FILE *fp;
  unsigned char rom[0xE000];
  int flag[0xE0];
  int i;
  char hbuf[100];
  int length;
  int address;
  int hdat;
  int page;

  // initialize flag
  for (i = 0; i < 0xE0; i++)
    flag[i] = 0;  
  
  // initialize data to 0xFF
  for (i = 0; i < 0xE000; i++)
    rom[i] = 0xFF;
  
  // open hex file
  fp = fopen(filename, "rt");

  length = 0x10;
  while(length) {
    fgets(hbuf, 80, fp);
    sscanf(hbuf + 1, "%2X", &length);
    sscanf(hbuf + 3, "%4X", &address);

    page = (address >> 8) & 0xFF;
    if (page < 0xE0) {
      flag[page] = 1;
	  
      for (i = 0; i < length; i++) {
        sscanf(hbuf + 9 + 2 * i, "%2X", &hdat);
        rom[address + i] = hdat & 0xFF;
      }
    }
  }		

  // close hex file
  fclose(fp);
  
  // update MCU
  // enter to bootloader
  NKFADC500_1CHenter_BOOTLOADER(tcp_Handle);
  
  // program flash memory
  for (page = 0; page < 0xE0; page++) {
    if (flag[page]) 
      NKFADC500_1CHprogram_MCU(tcp_Handle, flag[page], page, rom + page * 256);
  }
  
  // exit out of bootloader
  NKFADC500_1CHexit_BOOTLOADER(tcp_Handle);
}
*/

// reset data acquisition
void NKFADC500_1CHreset(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x00, 0);
}

// start data acquisition
void NKFADC500_1CHstart(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x01, 1);
}

// stop data acquisition
void NKFADC500_1CHstop(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x01, 0);
}

// read RUN status
int NKFADC500_1CHread_RUN(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x01);
}

// Read data size in kbyte
int NKFADC500_1CHread_DATASIZE(int tcp_Handle)
{
  int data;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x02, 0);
  data = NKFADC500_1CHread(tcp_Handle, 0x02);
  ival = NKFADC500_1CHread(tcp_Handle, 0x03);
  ival = ival << 8;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x04);
  ival = ival << 16;
  data = data + ival;
  
  return data;
}

// Read PSD data size
int NKFADC500_1CHread_PSD_DATASIZE(int tcp_Handle)
{
  int data;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x05, 0);
  data = NKFADC500_1CHread(tcp_Handle, 0x05);
  ival = NKFADC500_1CHread(tcp_Handle, 0x06);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// turn on/off DRAM, 0 = off, 1 = on
void NKFADC500_1CHwrite_DRAMON(int tcp_Handle, int data)
{
  int status;

  // turn on DRAM
  if (data) {
    // check DRAM is on
    status = NKFADC500_1CHread(tcp_Handle, 0x07);

    // when DRAM is on now, turn it off
    if (status)
      NKFADC500_1CHwrite(tcp_Handle, 0x07, 0);

    // turn on DRAM
    NKFADC500_1CHwrite(tcp_Handle, 0x07, 1);

    // wait for DRAM ready
    status = 0;
    while (!status)
      status = NKFADC500_1CHread(tcp_Handle, 0x07);
  }
  // trun off DRAM
  else 
    NKFADC500_1CHwrite(tcp_Handle, 0x07, 0);
}

// read DRAM status
int NKFADC500_1CHread_DRAMON(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x07);
}

// read module ID
int NKFADC500_1CHread_MID(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x08);
}

// write high voltage
void NKFADC500_1CHwrite_HV(int tcp_Handle, float data)
{
  float fval;
  int hval;
  int ival;

  fval = data;
  fval = fval * 2.0 + 0.0;
  hval = (int)(fval);
  if (hval < 0) 
    hval = 0;
  else if (hval > 4095)
    hval = 4095;

  ival = hval & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x09, ival);
  ival = (hval >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x0A, ival);
}

// read high voltage
float NKFADC500_1CHread_HV(int tcp_Handle)
{
  float data;
  int hval;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x22, 0x02);
  hval = NKFADC500_1CHread(tcp_Handle, 0x09);
  ival = NKFADC500_1CHread(tcp_Handle, 0x0A);
  ival = ival << 8;
  hval = hval + ival;

  data = hval;
  data = data * 0.03686 + 0.0;
  return data;
}

// write offset adjustment
void NKFADC500_1CHwrite_DACOFF(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x0B, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x0C, ival);
  sleep(1);
}

// read pedestal
int NKFADC500_1CHread_PED(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x0B);
  ival = NKFADC500_1CHread(tcp_Handle, 0x0C);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// measure pedestal
void NKFADC500_1CHmeasure_PED(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x0D, 0);
}

// write acquisition time
void NKFADC500_1CHwrite_ACQUISITION_TIME(int tcp_Handle, long long data)
{
  long long tval;
  int ival;

  tval = data / 8;
  ival = tval & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x0E, ival);
  ival = (tval >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x0F, ival);
  ival = (tval >> 16) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x10, ival);
  ival = (tval >> 24) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x11, ival);
  ival = (tval >> 32) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x12, ival);
}

// read DAQ livetime
long long NKFADC500_1CHread_LIVETIME(int tcp_Handle)
{
  long long data;
  long long lval;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x22, 0x04);
  ival = NKFADC500_1CHread(tcp_Handle, 0x0E);
  data = ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x0F);
  lval = ival;
  lval = lval << 8;
  data = data + lval;
  ival = NKFADC500_1CHread(tcp_Handle, 0x10);
  lval = ival;
  lval = lval << 16;
  data = data + lval;
  ival = NKFADC500_1CHread(tcp_Handle, 0x11);
  lval = ival;
  lval = lval << 24;
  data = data + lval;
  ival = NKFADC500_1CHread(tcp_Handle, 0x12);
  lval = ival;
  lval = lval << 32;
  data = data + lval;
  data = data * 8;

  return data;
}

// write ADC mode
void NKFADC500_1CHwrite_AMODE(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x13, data);
}

// read ADC mode
int NKFADC500_1CHread_AMODE(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x13);
}

// write input pulse polarity
void NKFADC500_1CHwrite_POL(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x14, data);
}

// read input pulse polarity
int NKFADC500_1CHread_POL(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x14);
}

// write pulse sum width
void NKFADC500_1CHwrite_PSW(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x15, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x16, ival);
}

// read pulse sum width
int NKFADC500_1CHread_PSW(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x15);
  ival = NKFADC500_1CHread(tcp_Handle, 0x16);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// write discriminator threshold
void NKFADC500_1CHwrite_THR(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x17, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x18, ival);
}

// read discriminator threshold
int NKFADC500_1CHread_THR(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x17);
  ival = NKFADC500_1CHread(tcp_Handle, 0x18);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// write recording length
void NKFADC500_1CHwrite_RL(int tcp_Handle, int data)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x19, data);
}

// read recording length
int NKFADC500_1CHread_RL(int tcp_Handle)
{
  return NKFADC500_1CHread(tcp_Handle, 0x19);
}

// write input delay
void NKFADC500_1CHwrite_DLY(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1A, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1B, ival);
}

// read input delay
int NKFADC500_1CHread_DLY(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x1A);
  ival = NKFADC500_1CHread(tcp_Handle, 0x1B);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// write tail delay
void NKFADC500_1CHwrite_TAILDLY(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1C, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1D, ival);
}

// read tail delay
int NKFADC500_1CHread_TAILDLY(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x1C);
  ival = NKFADC500_1CHread(tcp_Handle, 0x1D);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// write neutron discriminator threshold
void NKFADC500_1CHwrite_FRT(int tcp_Handle, float data)
{
  float fval;
  int tval;
  int ival;

  fval = data * 1024.0;
  tval = (int)(fval);
  if (tval > 1023)
    tval = 1023;

  ival = tval & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1E, ival);
  ival = (tval >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x1F, ival);
}

// read neutron discriminator threshold
float NKFADC500_1CHread_FRT(int tcp_Handle)
{
  float data;
  int tval;
  int ival;

  tval = NKFADC500_1CHread(tcp_Handle, 0x1E);
  ival = NKFADC500_1CHread(tcp_Handle, 0x1F);
  ival = ival << 8;
  tval = tval + ival;

  data = tval;
  data = data / 1024.0;
  return data;
}

// write pedestal trigger interval in ms;
void NKFADC500_1CHwrite_PTRIG(int tcp_Handle, int data)
{
  int ival;

  ival = data & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x20, ival);
  ival = (data >> 8) & 0xFF;
  NKFADC500_1CHwrite(tcp_Handle, 0x21, ival);
}

// read pedestal trigger interval in ms;
int NKFADC500_1CHread_PTRIG(int tcp_Handle)
{
  int data;
  int ival;

  data = NKFADC500_1CHread(tcp_Handle, 0x20);
  ival = NKFADC500_1CHread(tcp_Handle, 0x21);
  ival = ival << 8;
  data = data + ival;
  
  return data;
}

// send trigger
void NKFADC500_1CHsend_TRIG(int tcp_Handle)
{
  NKFADC500_1CHwrite(tcp_Handle, 0x22, 0x01);
}

// read FADC event number
int NKFADC500_1CHread_EVENT_NUMBER(int tcp_Handle)
{
  int data;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x22, 0x08);
  data = NKFADC500_1CHread(tcp_Handle, 0x23);
  ival = NKFADC500_1CHread(tcp_Handle, 0x24);
  ival = ival << 8;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x25);
  ival = ival << 16;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x26);
  ival = ival << 24;
  data = data + ival;

  return data;
}

// read PSD event number
int NKFADC500_1CHread_PSD_EVENT_NUMBER(int tcp_Handle)
{
  int data;
  int ival;

  NKFADC500_1CHwrite(tcp_Handle, 0x22, 0x10);
  data = NKFADC500_1CHread(tcp_Handle, 0x27);
  ival = NKFADC500_1CHread(tcp_Handle, 0x28);
  ival = ival << 8;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x29);
  ival = ival << 16;
  data = data + ival;
  ival = NKFADC500_1CHread(tcp_Handle, 0x2A);
  ival = ival << 24;
  data = data + ival;

  return data;
}

// read FADC data
void NKFADC500_1CHread_DATA(int tcp_Handle, int data_size, char *data)
{
  int i;

  for (i = 0; i < data_size; i++)
    NKFADC500_1CHblockread(tcp_Handle, 0x80, 1024, data + i * 1024);
}

// read PSD data
void NKFADC500_1CHread_PSD_DATA(int tcp_Handle, int data_size, char *data)
{
  int nkbyte;
  int nbyte;
  int i;

  nkbyte = data_size / 64;
  nbyte = data_size % 64;
  nbyte = nbyte * 16;

  for (i = 0; i < nkbyte; i++)
    NKFADC500_1CHblockread(tcp_Handle, 0xC0, 1024, data + i * 1024);

  if (nbyte)
    NKFADC500_1CHblockread(tcp_Handle, 0xC0, nbyte, data + nkbyte * 1024);
}



// align ADC for NKFADC500
void NKFADC500_1CHalign_ADC(int tcp_Handle)
{
  int dly;
  int value;
  int count;
  int sum;
  int center;
  int gdly;
  int flag;

  NKFADC500_1CHsend_ADCRST(tcp_Handle);
  usleep(500000);
  NKFADC500_1CHsend_ADCCAL(tcp_Handle);
  NKFADC500_1CHwrite_ADCALIGN(tcp_Handle, 1);

  count = 0;
  sum = 0;
  flag = 0;

  for (dly = 0; dly < 32; dly++) {
    NKFADC500_1CHwrite_ADCDLY(tcp_Handle, dly);
    value = NKFADC500_1CHread_ADCSTAT(tcp_Handle);
      
    // count bad delay
    if (!value) {
      flag = 1;
      count = count + 1;
      sum = sum + dly;
    }
    else {
      if (flag) 
        dly = 32;
    }
  }

  // get bad delay center
  center = sum / count;

  // set good delay
  if (center < 11)
    gdly = center + 11;
  else
    gdly = center - 11;

  // set delay
  NKFADC500_1CHwrite_ADCDLY(tcp_Handle, gdly);
  printf("ADC calibration delay = %d\n", gdly);

  NKFADC500_1CHwrite_ADCALIGN(tcp_Handle, 0);
  NKFADC500_1CHsend_ADCCAL(tcp_Handle);
}

// align DRAM
void NKFADC500_1CHalign_DRAM(int tcp_Handle)
{
  int ch;
  int dly;
  int value;
  int flag;
  int count;
  int sum;
  int aflag;
  int gdly;
  int bitslip;

  // turn on DRAM    
  NKFADC500_1CHwrite_DRAMON(tcp_Handle, 1);

  // enter DRAM test mode
  NKFADC500_1CHwrite_DRAMTEST(tcp_Handle, 1);

  // send reset to iodelay  
  NKFADC500_1CHsend_ADCCAL(tcp_Handle);

  // fill DRAM test pattern
  NKFADC500_1CHwrite_DRAMTEST(tcp_Handle, 2);

  for (ch = 0; ch < 2; ch ++) {
    count = 0;
    sum = 0;
    flag = 0;

    // search delay
    for (dly = 0; dly < 32; dly++) {
      // set delay
      NKFADC500_1CHwrite_DRAMDLY(tcp_Handle, ch, dly);

      // read DRAM test pattern
      NKFADC500_1CHwrite_DRAMTEST(tcp_Handle, 3);
      value = NKFADC500_1CHread_DRAMTEST(tcp_Handle, ch);

      aflag = 0;
      if (value == 0xFFAA5500)
        aflag = 1;
      else if (value == 0xAA5500FF)
        aflag = 1;
      else if (value == 0x5500FFAA)
        aflag = 1;
      else if (value == 0x00FFAA55)
        aflag = 1;
    
      if (aflag) {
        count = count + 1;
        sum = sum + dly;
        if (count > 4)
          flag = 1; 
     }
      else {
        if (flag)
          dly = 32;
        else {
          count = 0;
          sum = 0;
        }
      }
    }

    // get bad delay center
    if (count)
      gdly = sum / count;
    else
      gdly = 9;

    // set delay
    NKFADC500_1CHwrite_DRAMDLY(tcp_Handle, ch, gdly);
  
    // get bitslip
    for (bitslip = 0; bitslip < 4; bitslip++) {
      // read DRAM test pattern
      NKFADC500_1CHwrite_DRAMTEST(tcp_Handle, 3);
      value = NKFADC500_1CHread_DRAMTEST(tcp_Handle, ch);

      if (value == 0xFFAA5500) {
        aflag = 1;
        bitslip = 4;
      }
      else {
        aflag = 0;
        NKFADC500_1CHwrite_BITSLIP(tcp_Handle, ch);
      }
    }

    if (aflag) 
      printf("DRAM(%d) is aligned, delay = %d\n", ch, gdly);
    else 
      printf("Fail to align DRAM(%d)!\n", ch);
  }

  // exit DRAM test mode
  NKFADC500_1CHwrite_DRAMTEST(tcp_Handle, 0);
}
