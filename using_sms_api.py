from sms_api_client import SMSAPIClient

client = SMSAPIClient("http://your_api_ip:8000")

# Send an SMS
send_response = client.send_sms("71640", "NPD028")
print(f"Send response: {send_response}")

# Poll for incoming messages for a specific plate number
messages = client.poll_for_messages(plate_number="NPD028")

for message in messages:
    plate_number = message['plate_number']
    car_brand = message['car_brand']
    color = message['color']
    model_year = message['model_year']
    taxes_paid = message['taxes_paid']
    first_day_in_traffic = message['first_day_in_traffic']
    car_owner = message['car_owner']
    car_owner_residence = message['car_owner_residence']

    print("Received message: ")
    print(f"Plate Number: {plate_number}")
    print(f"Car Brand: {car_brand}")
    print(f"Color: {color}")
    print(f"Model Year: {model_year}")
    print(f"Taxes Paid: {taxes_paid}")
    print(f"First Day in Traffic: {first_day_in_traffic}")
    print(f"Car Owner: {car_owner}")
    print(f"Car Owner Residence: {car_owner_residence}")
