#include <string>

#include "mbed.h"

#define TRUE 1
#define FALSE 0 

//set up a timer for timing FFT's
Timer timer;

AnalogIn chan1(p18);
AnalogIn chan2(p19);
AnalogIn chan3(p20);

Serial pc(USBTX, USBRX);

string times;
string ch1;
string ch2;
string ch3;
char buffer [10];
string buf2str;
int getdata;

void callback() {
    // Note: you need to actually read from the serial to clear the RX interrupt
    pc.getc();
    getdata = TRUE;
}


int main() {
    //Prepare for burst mode on all ADC pins and set up interrupt handler (using ADC library from Simon Blandford
    timer.reset();
    timer.start();
    pc.baud(921600);
    pc.attach(&callback);
    while(1) {
        if (getdata == TRUE) {
            sprintf(buffer, "%f", timer.read());
            buf2str = buffer;
            times = buf2str;
            sprintf(buffer, "%f", chan1.read());
            buf2str = buffer;
            ch1 = buf2str;
            sprintf(buffer, "%f", chan2.read());
            buf2str = buffer;
            ch2 = buf2str;
            sprintf(buffer, "%f", chan3.read());
            buf2str = buffer;
            ch3 = buf2str;
    
            for(int x = 0; x<120; x++){
                wait(0.01);
                sprintf(buffer, "%f", timer.read());
                buf2str = buffer;
                times = times + "," + buf2str;
                sprintf(buffer, "%f", chan1.read());
                buf2str = buffer;
                ch1 = ch1 + "," + buf2str;
                sprintf(buffer, "%f", chan2.read());
                buf2str = buffer;
                ch2 = ch2 + "," + buf2str;
                sprintf(buffer, "%f", chan3.read());
                buf2str = buffer;
                ch3 = ch3 + "," + buf2str;
            } 
            printf("%s\r\n", times);
            printf("%s\r\n", ch1);
            printf("%s\r\n", ch2);
            printf("%s\r\n", ch3);
            getdata = FALSE;
        }
    }
    
}
