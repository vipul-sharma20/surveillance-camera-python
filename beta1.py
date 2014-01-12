"""
VIPUL SHARMA :D

---Surveillance Cam + Motion Detection----

* Captures Frames when a motion is detected
* Frames saved as .bmp (or any other format) with date and time of capture
* Sends an alert email to any person and to any number of persons 
"""
print __doc__
#------------------------------------------------surveillance----------------------------------------------------------------
import pygame                                                       # importing pygame
from pygame.locals import *
from SimpleCV import *                                              # Importing SimpleCV 
import time                               
from time import gmtime, strftime                                   # to get date and time of event
import smtplib                                                      # SMTP : Simple Mail Transfer Protocol, for email sending
import thread
def main():
    count = 0                                                       # used for naming images to be saved 
    cam = Camera()                                                  # creating camera object
    threshold = 5.0                                                 # if mean exceeds this amount do something
    #threshold = 100.0
    pygame.init()                                                   # initialising pygame
    pygame.mixer.init()                                             # initialising pygame.mixer
    pygame.mixer.music.load("beep.wav")                             # loads the sound, to be played as alert alarm ! 
    while True:
        previous = cam.getImage()                                   # grab a frame
        time.sleep(0.1)                                             # wait for 0.1 seconds
        current = cam.getImage()                                    # grab another frame
        diff = current - previous                                   # comparing two frames for any changes
        matrix = diff.getNumpy()                                    # getting numpy matrix
        mean = matrix.mean()                                        # stores mean of the numpy matrix
          
        #diff.show()
        current.show()
        #current.sideBySide(diff).show()
        if mean >= threshold:                                        # checking for the threshold limit
                try:    
                    thread.start_new_thread(send_email, ("thread-1", 0)) # starts a new thread to send email--(email sending takes about 10-15 seconds)
                except:
                    print '----------------Unable to start thread "thread-1"---------------'
                #send_email()                                        # therefore to run image capture and email sending concurrently, multithreading is                                                                     # done  
                print "Motion Detected"
		while True:
		    print 'Saving : ',
		    print "image"+str(count)+".bmp"                  # output on the output screen, shows the name of image saved
		    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())     # getting date and time of the event
		    date = dt.split(' ')[0]                          # stores date
		    time1 = dt.split(' ')[1]                         # stores time
                    #pygame.mixer.music.play(-1)                     # plays alert sound using pygame
	            current.drawText(date, 520, 430,(0, 0, 255), 24) # draws date on image frame
		    current.drawText(time1, 520, 450,(0, 0, 255), 24)# draws time on image frame :NOTE: time is GMT
		    current.save("motionp/image"+str(count)+".bmp")  # saves image fram at location home/motionp/<imagename>.bmp
		    current.show()                                   # displays image frame
   		    count += 1                                       # incrementing count for new image name which will be : image<count>.bmp
	            #time.sleep(0.1)
   	            current = cam.getImage()                         #grab another frame
#----------------------------------------------------email-------------------------------------------------------
def send_email(threadName, delay): 
    gmail_user = "vipul.sharma20@gmail.com"                          # gmail user id of sender
    gmail_pwd = "giuaqikuqbooaijq"                                   # gmail password or gmail ASP as applicable
    FROM = 'vipul.sharma20@gmail.com'                                # from name
    TO = ['vipul.sharma20@gmail.com']                                # must be a list - receivers of email
    SUBJECT = "Testing sending using gmail"                          # Subject of email (any text)
    TEXT = "Testing sending mail using gmail servers"                # text matter of email (any text)
    #----------------Prepare actual message----------------
    try:
		message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)           # Actual message 
            	#server = smtplib.SMTP(SERVER) 
            	server = smtplib.SMTP("smtp.gmail.com", 587)         # or port 465 doesn't seem to work!
            	server.ehlo()                                        # identifies the sender by sending 'helo' greeting to the receiver smtp server
            	server.starttls()                                    # TLS - Transfer layer security -- encrypts the message
            	server.login(gmail_user, gmail_pwd)                  # Logins our account
            	server.sendmail(FROM, TO, message)                   # sends email
            	#server.quit()
            	server.close()                                       # exit
                pygame.mixer.music.play(0)
            	print 'successfully sent the mail'
    except:                                                          # except when pc not connected to internet or if port doesn't responds
            	print "failed to send mail"
main()
