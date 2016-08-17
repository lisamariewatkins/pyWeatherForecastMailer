import requests
import smtplib

def convertFK(tempK):
        return int((tempK - 273.15) * 1.80 + 32)

def get_weather():
        url = 'http://api.openweathermap.org/data/2.5/weather?q=austin&main=metric&id=524901&APPID=4c85e9362b0ee61196ce179dfa223bcb'
        w_request = requests.get(url)
        w_json = w_request.json()
        description = w_json['weather'][0]['description']
        current_temp = w_json['main']['temp']
        temp_max = w_json['main']['temp_max']
        temp_min = w_json['main']['temp_min']

        forecast = 'The forecast for today is '
        forecast += str(description)
        forecast += ' with an average temperature of '
        forecast += str(convertFK(current_temp))
        forecast += '. The high for today is '
        forecast += str(convertFK(temp_max))
        forecast += ' with a low of '
        forecast += str(convertFK(temp_min))
        forecast += '.'
        

        return forecast

def send_emails(emails, schedule, forecast):
        # connect to the smtp server
        server = smtplib.SMTP('smtp.gmail.com', '587')
        #start encryption
        server.starttls()
        #login
        from_email = ''
        username = input('What is your username?')
        password = input("whats your password?")
        server.login(username, password)

        #Send to email list
        for to_email, name in emails.items():
                message = 'Subject: Today'
                message += 'Hello, ' + name + '!' + '\n\n'
                message += forecast + '\n\n'
                message += schedule + '\n\n'
                message += 'Have a great day!'
                server.sendmail(from_email, to_email, message)
                
        server.quit()
        

def get_emails():
        emails = {}


        try:
                email_file = open('emails.txt', 'r')
                for line in email_file:
                        (email, name) = line.split(',')
                        emails[email] = name.strip()
                        
        except FileNotFoundError as err:
                print(err)
	
        return emails

def get_schedule():
        try:
                schedule_file = open('schedule.txt', 'r')
                schedule = schedule_file.read()
        except FileNotFoundError as err:
                print(err)

        return schedule

def main():
        emails = get_emails()
        print (emails)
        schedule = get_schedule()
        print (schedule)
        forecast = get_weather()
        print(forecast)
        send_emails(emails, schedule, forecast)

main()
