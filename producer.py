import requests
import json
import time

from quixstreams import Application

# Configure the Quix Streams application
app = Application(
    broker_address="localhost:19092",
    consumer_group="ipoh-weather-producer"
)

# Define the topic for your weather data
topic = app.topic("ipoh-weather-data")

def fetch_weather_data():
    """Fetches weather data from the API."""
    url = "https://api.data.gov.my/weather/forecast?contains=Ipoh@location__location_name"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

def main():
    """Main function to produce data to the Kafka topic."""
    with app.get_producer() as producer:
        try:
            weather_data = fetch_weather_data()
            print("Fetched new weather data for Ipoh...")
            for forecast in weather_data:
                # Use a unique key for each message, like the date
                message_key = forecast["date"].encode("utf-8")
                # Serialize the forecast object to JSON string
                message_value = json.dumps(forecast).encode("utf-8")

                # Produce the message to the topic
                producer.produce(
                    topic=topic.name,
                    key=message_key,
                    value=message_value
                )
                print(f"Produced key for message: {forecast['date']}")
                print(f"Message produced: {forecast}")

            # # Sleep for a period before fetching new data (e.g., 3600 seconds = 1 hour)
            # time.sleep(3600)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60) # Wait a minute before retrying

        except KeyboardInterrupt: # Ctrl+C to exit
            print("Exiting...")

if __name__ == "__main__":
    main()