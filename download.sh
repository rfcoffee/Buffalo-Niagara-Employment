rm -rf raw_data/
git clone https://github.com/rfcoffee/Buffalo-Niagara-Employment/ raw_data
cd raw_data
rm *.csv

# file name: oes (Occupational Employment Statistics), m/n (May/November), 17 (2017), ma (Metropolitan and nonmetropolitana area)
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm17ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm16ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm15ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm14ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm13ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm12ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm11ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm10ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm09ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm08ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm07ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm06ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm05ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesn04ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm04ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesn03ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oesm03ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes02ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes01ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes00ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes99ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes98ma.zip
wget -q --show-progress https://www.bls.gov/oes/special.requests/oes97ma.zip

# unzip
for f in *.zip; do unzip -tq $f; unzip -oq $f; done
# remove zip files
rm *.zip
