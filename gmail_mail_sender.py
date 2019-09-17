import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipients,  data):
    username = "username@email.com"
    password = "Password"
    recipients_list = recipients
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    message = MIMEMultipart('alternative')
    message['Subject'] = 'House Search Results'
    message['From'] = "House Hunter<" + username + ">"
    message['To'] = ', '.join(recipients_list)
    html = MIMEText(data, 'html')
    message.attach(html)

    server.sendmail(username, recipients_list, message.as_string())
    server.quit()


def convert_json_to_html(property_data):
    if property_data:
        beginning = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, tr, tbody, thead {{
            display: block;
            text-align: left;
            border: 1px solid black;
            width: 100%;
        }}
        </style>
        </head>
        <body>

        <table>
        <thead>
        <tr>
          <th><b>{property_data['type']}: </b>retrieved {property_data['number_of_properties']} properties with an average price: 
          {property_data['average_price']}</th>
        </tr>
        </thead>
        <tbody>
        """
        end = """
        </tbody>
        </table>

        </body>
        </html>
        """

        result = beginning

        for item in property_data['properties']:
            station_string = 'Stations: '
            for station_data in item['stations_list']:
                station_string += f"""
                {station_data['station_name']} - {station_data['distance']} 
                """
            images_string = ''
            for image in item['images']:
                images_string += f'<img src={image}> '
            result += f"""
            <tr><td>{item['key_features_text']}</td></tr>
            <tr><td>{images_string}</td></tr>
            <tr><td>{item['full_description_text']}</td></tr>                    
            <tr><td>{item['price']}</td></tr>
            <tr><td>{station_string}</td></tr>
            <tr><td><a href="{item['url']}">Link</a></td></tr>
            """
        result += end
        return result
    else:
        result = 'No new data for {property_data["type"]}'
    return result


def send_results(data, mail_list):
    html = ''
    for item in data:
        html += convert_json_to_html(item)
    recipients_list = mail_list
    send_email(recipients_list, html)


if __name__ == '__main__':
    # html = convert_json_to_html(internal=True)
    # with open('test.html', 'w') as test_html:
    #     test_html.write(html)
    #send_results()
    send_email('error@error_email.com',
               'An error has occured whilst scraping the results')
