use rdkafka::config::ClientConfig;
use rdkafka::producer::{FutureProducer, FutureRecord};
use std::time::Duration;

#[tokio::main]
async fn main() {
    let broker = "localhost:9092";
    let topic = "cities";

    let procuder = create_producer(broker);

    let payload = "New York";
    let key = "";

    match send_message(&procuder, topic, Some(key), payload).await {
        Ok(_) => println!("Successfully sent!"),
        Err(e) => eprintln!("Failed to send: {}", e),
    }
}

fn create_producer(broker: &str) -> FutureProducer {
    ClientConfig::new()
        .set("bootstrap.servers", broker)
        .set("message.timeout.ms", "5000")
        .set("debug", "all")
        .create()
        .expect("producer creation error")
}

async fn send_message(
    procuder: &FutureProducer,
    topic: &str,
    key: Option<&str>,
    payload: &str,
) -> Result<(), Box<dyn std::error::Error>> {
    let record = FutureRecord::to(topic)
        .key(key.unwrap_or(""))
        .payload(payload);

    let delivery_status = procuder.send(record, Duration::from_secs(0)).await;

    match delivery_status {
        Ok(delivery) => {
            println!("Delivered partition: {:#?}", delivery);
            Ok(())
        }
        Err((e, _)) => {
            eprintln!("Error while delivering message: {}", e);
            Err(Box::new(e))
        }
    }
}
