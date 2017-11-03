'''
Created on Jul 14, 2017

@author: admin
'''
from data.models import *

from django.core.mail import get_connection, send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

from django.core.urlresolvers import reverse
#from django.urls import reverse
from data.views import *
 
 
 



 
 

if __name__ == "__main__":
    
    messageCategoryDetail=MessageCategoryDetail.objects.get(messagecategory=MessageCategory.objects.get(pk=3))
    messageMail= MessageMail.objects.get(pk=messageCategoryDetail.message.pk)
    
        #messageMailSignup= MessageMail.objects.filter(site=Site.objects.filter(name=request.build_absolute_uri('/')))
    configurationMessage = ConfigurationMessage.objects.get(message=messageMail)
    smtpconfig= configurationMessage.account
    listuser=User.objects.filter(groups=messageCategoryDetail.group)
    for u in listuser:
        print u.username                    
                    
                    
    #mpod@cimav.edu.mx
    user = User.objects.get(pk=5)
    subject = 'Activate Your MPOD  Account'
    message="Hi n,Please click on the link below to confirm your registration: http://mpod.cimav.edu.mx/activate/Nzc=/4oq-9cac01d09e86d5e9d2d4"
    domain = 'cimav.edu.mx'
    
    ######################################################################################
    #                                 ''' con base de datos '''
    ######################################################################################
    

    smtpconfig = Configuration.objects.get(pk=1)
    messageMailSignup= MessageMail.objects.get(pk=3)
    my_use_tls = False
    if smtpconfig.email_use_tls ==1:
        my_use_tls = True
    
    fail_silently= False
    connection = get_connection(host=smtpconfig.email_host, 
                                                            port= int(smtpconfig.email_port ), 
                                                            username=smtpconfig.email_host_user, 
                                                            password=smtpconfig.email_host_password, 
                                                            use_tls=my_use_tls) 

    
    htmlmessage = messageMailSignup.email_regards +" " + user.username  +",</br> " +  messageMailSignup.email_message +"</br> " +messageMailSignup.email_message +"</br> " + "http://mpod.cimav.edu.mx/activate/Nzc=/4oq-9cac01d09e86d5e9d2d4"
    print htmlmessage
    send_mail(
                    messageMailSignup.email_subject,
                    htmlmessage,
                    smtpconfig.email_host_user,
                    [user.email],
                    connection=connection
                )
    

    
    ######################################################################################
    #                                 ''' sin  base de datos '''
    ######################################################################################
    my_host = 'smtp.gmail.com'
    my_port = 587
    a= '@'
    my_username ="mpod" 
    my_username = my_username + a
    my_username = my_username +  'cimav.edu.mx'
    my_password = 'c1m4v2017'
    my_use_tls = True
    fail_silently= False
    connection = get_connection(host=my_host, 
                                                            port=my_port, 
                                                            username=my_username, 
                                                            password=my_password, 
                                                            use_tls=my_use_tls) 
    
     
    send_mail(
                    subject,
                    message,
                    'mpod@%s' % domain,
                    [user.email],
                    connection=connection
                )
    # or
    EmailMessage(subject,
                                message,
                                'mpod@%s' % domain,
                                [user.email],
                                connection=connection).send(fail_silently=False)
                                
    
    backend = EmailBackend(   host=my_host, 
                                                        port=my_port, 
                                                        username=my_username, 
                                                        password=my_password, 
                                                        use_tls=my_use_tls,
                                                        fail_silently=fail_silently)
                                
    email = EmailMessage( subject,
                                                message,
                                                'mpod@%s' % domain,
                                                [user.email],
                                                connection=backend)
    email.send()



    
