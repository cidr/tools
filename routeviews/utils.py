from subprocess import Popen, PIPE, STDOUT

def check_output(args, shouldPrint=True):
    return check_both(args, shouldPrint)[0]

def check_both(args, shouldPrint=True, check=True):
    p = Popen(args,shell=True,stdout=PIPE,stderr=STDOUT)
    out, err = p.communicate()
    rc = p.returncode
    out = (out,"")
    out = (out, rc)
    if check and rc is not 0:
        #print "Error processes output: %s" % (out,)
        raise Exception("subprocess.CalledProcessError: Command '%s'" \
                            "returned non-zero exit status %s (%s)" % (args, rc, out[0]))
    return out
