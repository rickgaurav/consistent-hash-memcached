# consistent-hash-memcached
Implementation of consistent hash algorithm.

PREREQUISITES:

1. apt-get install memcached
2. python-memcached==1.53
3. python2.7
4. You'll need to setup 8 running memcached instances on the following ports:
11211
11212
11213
11214
11215
11216
11217
11218

ASSUMPTIONS:

1. All the 8 memcached instances are running before running the program.

STEPS to run:

1. Create a virtual environment. 
2. pip install -r requirements.txt
3. python new_memcached.py
