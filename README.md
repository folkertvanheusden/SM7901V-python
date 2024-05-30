This code is to retrieve dB measurements (audio level) from a SM7901V sensors.

I bought mine from https://nl.aliexpress.com/item/1005002395958513.html
When buying one, make sure you choose the right signal values. E.g. 3V when connecting to the serial port of a raspberry pi.

Datasheet: http://www.sonbus.com/upload/pdf/SM7901B.pdf?spm=a2g0o.detail.1000023.1.62e2Pyd8Pyd8bF&file=SM7901B.pdf

See the code for details (assumed is that you have basic understanding of the python language).
The code retrieves 5 seconds of measurements and then sends the statistics over those values to a MQTT server.


Released under the MIT license by Folkert van Heusden
