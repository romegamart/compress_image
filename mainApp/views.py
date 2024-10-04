import pandas as pd
import pywhatkit
from django.shortcuts import render
from django.core.exceptions import ValidationError
import time  # Import time for sleep functionality

def send_auto_bulk_whatsapp_message(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        message = request.POST.get('message')

        # Check if the file is a valid CSV or Excel file
        if file:
            try:
                # Ensure the file extension is either .csv or .xlsx
                if file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)  # Read Excel file
                else:
                    return render(request, 'whatsapp-form.html', {'error': 'Only .xlsx files are supported.'})

                # Check if the phone numbers column exists
                if 'PhoneNumber' not in df.columns:
                    return render(request, 'whatsapp-form.html', {'error': 'PhoneNumber column is missing in the file.'})

                numbers = df['PhoneNumber'].tolist()  # Extract phone numbers

                for number in numbers:
                    number = "+91" + str(number).strip()  # Format phone number
                    if number:  # Check if the phone number is not empty
                        try:
                            print("Sending message to: ", number)
                            # Send WhatsApp message
                            pywhatkit.sendwhatmsg_instantly(phone_no=number, message=message, wait_time=15, tab_close=True)
                            time.sleep(30)  # Wait for a longer time before sending the next message
                        except Exception as e:
                            print(f"Error sending message to {number}: {str(e)}")
                            break  # Break out of the loop if there is an error

                return render(request, 'whatsapp-form.html', {'success': True})

            except (ValidationError, ValueError) as e:
                return render(request, 'whatsapp-form.html', {'error': f'Error processing file: {str(e)}'})
            except Exception as e:
                return render(request, 'whatsapp-form.html', {'error': f'An error occurred: {str(e)}'})

    return render(request, 'whatsapp-form.html')
