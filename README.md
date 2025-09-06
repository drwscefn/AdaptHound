Making life a little easier with AdaptixC2 and BOFHound [https://github.com/coffeegist/bofhound]

Once you've run an ldapsearch query, feed the task ID to adapthound e.g. 

[06/09 20:32:50] [+] BOF finished
+--- Task [**7772bfe2**] closed ----------------------------------------------------------+

python3 adapthound.py </path/to/AdaptixC2/ (assuming your adaptixserver.db is in dist/data/adaptixserver.db)> <task ID e.g. 7772bfe2> <output>
