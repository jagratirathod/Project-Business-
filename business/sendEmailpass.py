def mymail(username, password):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    me = "jagratirathod02@gmail.com"
    you = username

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verification eauction gallery"
    msg['From'] = me
    msg['To'] = you

    html = """<html>
  					<head></head>
  					<body>
    					<h1>Welcome to E-auction side </h1>
    					<p>You have a request of forget password, please check your password</p>
    					<h2>Username : """+username+"""</h2>
    					<h2>Password : """+str(password)+"""</h2>
    					<br>
    					<a href='http://localhost:8000/verifyuser/?email="""+username+"""' >Click here to verify account</a>		
  					</body>
				</html> 
    """

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("jagratirathod02@gmail.com","rathod@12345")

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    s.sendmail(me, you, str(msg))
    s.quit()
    print("mail send successfully....")
