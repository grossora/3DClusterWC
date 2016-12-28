

def event_processed(out_textfile, ers_string):
    lookup_log = open('Out_text/logs/log_{}.txt'.format(out_textfile),'a+')
    log_lines = lookup_log.readlines()
    # Check if the event is processed
    for l in log_lines:
        print l
        print l.split()
        if l.split()[0] ==ers_string:
            # Return right here....
            lookup_log.seek(0)
            lookup_log.close()
            return True
    # If we get here we will proceed and need to log what we are testing
    lookup_log.writelines(ers_string+'\n')
    lookup_log.seek(0)
    lookup_log.close()
    return False

