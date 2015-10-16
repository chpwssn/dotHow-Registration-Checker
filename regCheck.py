from optparse import OptionParser
import urllib, re, json

parser = OptionParser(__file__+" -d foo.how", version=__file__+" 1.0")
parser.add_option("-d", "--domain", dest="domain",help=".how domain name to check", metavar="foo.how")
(options, args) = parser.parse_args()

howre = re.compile(r'^[^.]*.how')

if not options.domain:
    print "No domain name supplied"
    quit(1)

if not howre.search(options.domain):
    print "Invalid domain format"
    quit(1)

checkres = urllib.urlopen("https://domain-registry.appspot.com/check?domain="+options.domain)
checkjson = json.loads(checkres.read())
if checkjson['status'] == "success":
    if checkjson['available']:
        if checkjson['tier'] == "premium":
            print options.domain+" is available but is premium tier."
        elif checkjson['tier'] == "standard":
            print options.domain+" is available and standard tier!"
        else:
            print options.domain+" is available but it's tier is unknown."
    else:
        print options.domain+" is taken. :("
else:
    print "I connected to the checking service but got an invalid response:"
    print checkjson
    quit(2)