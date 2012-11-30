#! /usr/bin/env python


from decimal import Decimal, getcontext
import csv
import sys
from optparse import OptionParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


usage = "usage: %prog csv_file"

parser = OptionParser(usage)
parser.add_option("-g", "--user",     dest="gmail_user",     help="gmail user name to send the message")
parser.add_option("-p", "--password", dest="gmail_password", help="gmail password for the user")
parser.add_option("-t", "--to",       dest="to",             help="send email messages to specified address instead of the one in the csv file")
parser.add_option("-f", "--files",    dest="files",          help="generate files instead of messages, use supplied prefix for file names")


(options, args) = parser.parse_args()

if len(args) != 1:
    print options
    print args
    parser.error("incorrect number of arguments")

csv_file  = args[0]
subject   = 'PyCon 2013 Financial Aid Approval for %(first_name)s %(last_name)s'
body      = open('approval_letter.txt', 'rU').read()
getcontext().prec = 3


def gmail(gmail_user, gmail_password, to, subject, text):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['CC'] = 'pycon-aid@python.org'
   msg['Reply-To'] = 'pycon-aid@python.org'
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_password)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


def generate_fields(award):
    award['first_name']     = award['first name']
    award['last_name']      = award['last name']
    award['registration']   = Decimal(award['registration award'])
    award['hotel_cost']     = Decimal(award['hotel award'])
    award['travel_cost']    = Decimal(award['travel award'])
    award['total_aid']      = Decimal(int(award['registration'] + award['hotel_cost'] + award['travel_cost']))
    return award


def generate_award_messages(award, body):
    to = options.to or award['email address']
    gmail(options.gmail_user, options.gmail_password, to, subject % award, body % award)


def generate_award_files(award, body):
    award['prefix'] = options.files
    o = open('%(prefix)s%(first_name)s_%(last_name)s.txt' % award, 'w')
    o.write(subject % award)
    o.write('\n')
    o.write(body % award)
    o.close()


if __name__ == '__main__':
    print 'loading:', csv_file
    reader = csv.reader(open(csv_file, 'rU'), delimiter=',')

    header = reader.next()
    expected = set(['first name', 'last name', 'email address', 'registration award', 'hotel award', 'travel award', ])
    header_diff = expected.difference(set(header))
    if header_diff:
        print 'expected a header line of:', list(expected)
        print 'found a header line of:', header
        print 'difference of:', header_diff
        sys.exit(1)

    reader = csv.DictReader(open(csv_file, 'rU'), delimiter=',')

    for award in reader:
        award = generate_fields(award)

        #print 'generating award', 'for', award['first name'], award['last name']
        if options.files:
            print 'generating award file for', award['first name'], award['last name'], ' - total aid:', award['total_aid'], 'reg:', award['registration award'], 'hotel:', award['hotel award'], 'travel:', award['travel award']
            generate_award_files(award, body)

        elif options.gmail_user and options.gmail_password:
            print 'sending ', 'award message for', award['first name'], award['last name']
            generate_award_messages(award, body)
