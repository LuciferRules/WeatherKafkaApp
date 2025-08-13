from quixstreams import Application
import json
import time

def main():
    # Configure the Quix Streams application
    app = Application(
        broker_address="localhost:19092",
        consumer_group="ipoh-weather-consumer",
        auto_offset_reset="earliest"
    )

    message_count = 0
    timeout_seconds = 5
    last_message_time = time.time()

    # Define the topic to read from, ipoh-weather-data
    with app.get_consumer() as consumer:
        consumer.subscribe(["ipoh-weather-data"])

        while True:
            # Poll for a message with a 1-second timeout
            msg = consumer.poll(1)

            if msg is None:
                print("Waiting...")
                # Check if the timeout has been reached
                if time.time() - last_message_time > timeout_seconds:
                    print(f"No new messages for {timeout_seconds} seconds. Exiting...")
                    break
            elif msg.error() is not None:
                raise Exception(msg.error())
            else:
                last_message_time = time.time()  # Reset the timer
                message_count += 1

                key = msg.key().decode("utf8")
                value = json.loads(msg.value())
                offset = msg.offset()

                print(f"Received message {message_count}: {offset} {key} {value}")
                consumer.store_offsets(msg)

    print(f"\nPolling completed. Total messages received: {message_count}")


if __name__ == "__main__":
    print("Starting consumer. Listening for messages...")
    try:
        main()
    except KeyboardInterrupt:
        print("Application manually stopped.")