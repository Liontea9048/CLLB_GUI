#define MAX_TCP_CONNECT         5       /* time in secs to get a connection */
#define MAX_TCP_READ            3       /* time in secs to wait for the DSO
                                           to respond to a read request */
#define BOOL                    int
#define TRUE                    1
#define FALSE                   0

#ifdef __cplusplus
extern "C" {
#endif

extern int NKFADC500_1CHopen(char *ip);
extern void NKFADC500_1CHclose(int tcp_Handle);
extern void NKFADC500_1CHenable_FLASH(int tcp_Handle);
extern void NKFADC500_1CHfinish_FLASH(int tcp_Handle);
extern void NKFADC500_1CHerase_FLASH(int tcp_Handle, int sector);
extern void NKFADC500_1CHwrite_FLASH(int tcp_Handle, int sector, int addrH, char *data);
extern void NKFADC500_1CHread_FLASH(int tcp_Handle, int sector, int addrH, char *data);
//extern void NKFADC500_1CHupdate_MCU(int tcp_Handle, char *filename);
extern void NKFADC500_1CHreset(int tcp_Handle);
extern void NKFADC500_1CHstart(int tcp_Handle);
extern void NKFADC500_1CHstop(int tcp_Handle);
extern int NKFADC500_1CHread_RUN(int tcp_Handle);
extern int NKFADC500_1CHread_DATASIZE(int tcp_Handle);
extern int NKFADC500_1CHread_PSD_DATASIZE(int tcp_Handle);
extern void NKFADC500_1CHwrite_DRAMON(int tcp_Handle, int data);
extern int NKFADC500_1CHread_DRAMON(int tcp_Handle);
extern int NKFADC500_1CHread_MID(int tcp_Handle);
extern void NKFADC500_1CHwrite_HV(int tcp_Handle, float data);
extern float NKFADC500_1CHread_HV(int tcp_Handle);
extern void NKFADC500_1CHwrite_DACOFF(int tcp_Handle, int data);
extern int NKFADC500_1CHread_PED(int tcp_Handle);
extern void NKFADC500_1CHmeasure_PED(int tcp_Handle);
extern void NKFADC500_1CHwrite_ACQUISITION_TIME(int tcp_Handle, long long data);
extern long long NKFADC500_1CHread_LIVETIME(int tcp_Handle);
extern void NKFADC500_1CHwrite_AMODE(int tcp_Handle, int data);
extern int NKFADC500_1CHread_AMODE(int tcp_Handle);
extern void NKFADC500_1CHwrite_POL(int tcp_Handle, int data);
extern int NKFADC500_1CHread_POL(int tcp_Handle);
extern void NKFADC500_1CHwrite_PSW(int tcp_Handle, int data);
extern int NKFADC500_1CHread_PSW(int tcp_Handle);
extern void NKFADC500_1CHwrite_THR(int tcp_Handle, int data);
extern int NKFADC500_1CHread_THR(int tcp_Handle);
extern void NKFADC500_1CHwrite_RL(int tcp_Handle, int data);
extern int NKFADC500_1CHread_RL(int tcp_Handle);
extern void NKFADC500_1CHwrite_DLY(int tcp_Handle, int data);
extern int NKFADC500_1CHread_DLY(int tcp_Handle);
extern void NKFADC500_1CHwrite_TAILDLY(int tcp_Handle, int data);
extern int NKFADC500_1CHread_TAILDLY(int tcp_Handle);
extern void NKFADC500_1CHwrite_FRT(int tcp_Handle, float data);
extern float NKFADC500_1CHread_FRT(int tcp_Handle);
extern void NKFADC500_1CHwrite_PTRIG(int tcp_Handle, int data);
extern int NKFADC500_1CHread_PTRIG(int tcp_Handle);
extern void NKFADC500_1CHsend_TRIG(int tcp_Handle);
extern int NKFADC500_1CHread_EVENT_NUMBER(int tcp_Handle);
extern int NKFADC500_1CHread_PSD_EVENT_NUMBER(int tcp_Handle);
extern void NKFADC500_1CHread_DATA(int tcp_Handle, int data_size, char *data);
extern void NKFADC500_1CHread_PSD_DATA(int tcp_Handle, int data_size, char *data);
extern void NKFADC500_1CHalign_ADC(int tcp_Handle);
extern void NKFADC500_1CHalign_DRAM(int tcp_Handle);

#ifdef __cplusplus
}
#endif




