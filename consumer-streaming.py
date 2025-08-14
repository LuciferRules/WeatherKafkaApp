from quixstreams import Application
import json

app = Application(
    broker_address="localhost:19092",
    consumer_group="consumer-streamer",
    auto_offset_reset="earliest"
)

# Define a topic
message_topic = app.topic("ipoh-weather-data")
sdf = app.dataframe(topic=message_topic)

# Print the messages before transformation
sdf= sdf.update(lambda message: print(f"Message: {message}"))

# Transform into dictionary with required fields only
def to_weather_json(message):
    data = {
        "location_name": message["location"].get("location_name"),
        "date": message.get("date"),
        "morning_forecast": message.get("morning_forecast"),
        "afternoon_forecast": message.get("afternoon_forecast"),
        "night_forecast": message.get("night_forecast")
    }
    json_str = json.dumps(data)
    print(f" --> Transformed JSON: {json_str}")
    return json_str          # now each row is a JSON string

sdf = sdf.apply(to_weather_json)

if __name__ == "__main__":
    app.run(sdf)