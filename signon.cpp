
#include <iostream>
using std::cout;
using std::endl;

#include <boost/asio.hpp>
using namespace::boost::asio;

#include "JetfileII.hpp"


void dump(unsigned char * buffer, size_t size)
{
	//cout.setf(ios::hex,ios::basefield);
	for(size_t sz = 0; sz < size; ++sz)
	{
		cout<<std::hex<<static_cast<int>(buffer[sz])<<"__";
	}
	cout<<endl;
};
 

int main(int argc, char* argv[])
{
	//Jetfile2::SignOffMsg msg;
	Jetfile2::SignOnMsg msg;
	cout<<"The size of msg is " << sizeof(msg)<<endl;
	cout<<"checksum of msg is " << msg.header.Checksum<<endl;

	serial_port_base::baud_rate BAUD(19200);
	serial_port_base::parity PARITY(serial_port_base::parity::none);
	serial_port_base::stop_bits STOP(serial_port_base::stop_bits::one);
	io_service io;
        serial_port port(io, "/dev/ttyS0");

        port.set_option(BAUD);
        port.set_option(PARITY);
        port.set_option(STOP);
	
	dump(reinterpret_cast<unsigned char*>(&msg),sizeof(msg));

        write(port, buffer(&msg,sizeof(msg)));
	
	return 0;
}