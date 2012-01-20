import re, telnetlib, sys

class MemcachedStats:

    _client = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')
    _stat_regex = re.compile(ur"STAT (.*) (.*)\r")

    def __init__(self, host='localhost', port='11211'):
        self._host = host
        self._port = port

    @property
    def client(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)
        return self._client

    def command(self, cmd):
        ' Write a command to telnet and return the response '
        self.client.write("%s\n" % cmd)
        return self.client.read_until('END')

    def key_details(self, sort=True):
        ' Return a list of tuples containing keys and details '
        cmd = 'stats cachedump %s 100'
        keys = [key for id in self.slab_ids()
            for key in self._key_regex.findall(self.command(cmd % id))]
        if sort:
            return sorted(keys)
        else:
            return keys

    def keys(self, sort=True):
        ' Return a list of keys in use '
        return [key[0] for key in self.key_details(sort=sort)]

    def slab_ids(self):
        ' Return a list of slab ids in use '
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        ' Return a dict containing memcached stats '
        return dict(self._stat_regex.findall(self.command('stats')))

#def main(argv=None):
#    if not argv:
#        argv = sys.argv
#    host = argv[1] if len(argv) >= 2 else '127.0.0.1'
#    port = argv[2] if len(argv) >= 3 else '11211'
#    import pprint
#    m = MemcachedStats(host, port)
#    pprint.pprint(m.keys())

if __name__ == '__main__':
#    main()
    host = '192.168.1.220'
    port = '11211'
    split = 20111215
    argv = sys.argv
    if len(argv) >= 2:
        host = argv[1]
    if len(argv) >= 3:
        port = argv[2]
    if len(argv) >= 4:
        split = int(argv[3])
    import memcache,json
    mc = memcache.Client(['%s:%s'%(host,port)], debug=1)
#    import pprint
    m = MemcachedStats(host, port)
#    splitDate = time.strptime('20110109', "%Y%m%d")
    for i in range(2):
        for key in m.keys():
            if key.startswith('PytempId_'):
    #            print '%s: %s'%(key,mc.get(key))
                try:
                    pyObj = json.loads(mc.get(key))
                    if pyObj:
                        dateStr = pyObj.get('0',None)
                        if dateStr:
            #                lastDate = time.strptime(dateStr, "%Y%m%d")
                            lastDate = int(dateStr)
    #                        print lastDate
                            if lastDate<split:
                                print 'key: %s   date: %d'%(key,lastDate)
                                print mc.get(key)
                                print mc.delete(key,0)
                except:
                    print 'pyObj:%s'%mc.get(key)
