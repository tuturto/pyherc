cd ..
curl -O http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.13.3.tar.gz
gunzip sip-4.13.3.tar.gz
tar -xvf sip-4.13.3.tar
cd sip-4.13.3
python configure.py
make -j 4
sudo make install
cd ..
curl -O http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-4.9.4.tar.gz
gunzip PyQt-x11-gpl-4.9.4.tar.gz
tar -xvf PyQt-x11-gpl-4.9.4.tar
cd PyQt-x11-gpl-4.9.4
python configure.py --confirm-license
make -j 4
sudo make install
cd ../pyherc
