Tracer
======

Tracer is a command-line program that performs a route trace to a specified node and displays a hop, IP address, ASN, country, and provider table. This project was developed by Vladislav Zubkov, a 2nd-year student of Mathematics and Computer Science at the Institute of Mathematics and Mechanics.

Installation
------------

To use Tracer, you need to have Python 3 installed on your machine. Then, you can simply download or clone the repository and run the tracer.py file.

Usage
-----

To run Tracer, navigate to the directory containing tracer.py in your terminal and enter the following command:

phpCopy code

```bash
python tracer.py <destination>
```

Replace `<destination>` with the destination node's IP address or domain name.

Example Output
--------------

After running Tracer, you will see an output similar to the following:
```bash

Tracing a route:
  
+-----+----------------+--------------+---------+----------------------+
| hop |       ip       |     asn      | country |       provider       |
+-----+----------------+--------------+---------+----------------------+
|  1  |  192.168.3.1   |      -       |    -    |          -           |
|  2  | 10.242.255.255 |      -       |    -    |          -           |
|  3  |  10.7.32.185   |      -       |    -    |          -           |
|  4  |  10.7.32.170   |      -       |    -    |          -           |
|  5  | 91.221.180.30  |    13094     |    RU   |        SFO-IX        |
|  6  | 93.158.172.23  | 13238 208722 |    RU   | YANDEX-93-158-172-22 |
|  7  | 93.158.172.21  | 13238 208722 |    RU   | YANDEX-93-158-172-20 |
|  8  |  5.255.255.77  | 13238 208722 |    RU   |   YANDEX-5-255-255   |
+-----+----------------+--------------+---------+----------------------+

Tracing completed.
```
The table displays the hop number, IP address, ASN (Autonomous System Number), country, and provider for each step in the route trace.