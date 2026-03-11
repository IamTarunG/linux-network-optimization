use tokio::net::TcpStream;
use tokio::io::AsyncWriteExt;
use std::time::{Instant, Duration};

#[tokio::main]
async fn main() {
    let target = "8.8.8.8:80";
    let heavy_payload = vec![0u8; 128_000]; 

    for _ in 0..50 {
        let start = Instant::now();
        
        let result = tokio::time::timeout(Duration::from_secs(2), async {
            let mut stream = TcpStream::connect(target).await?;
            stream.write_all(&heavy_payload).await?;
            Ok::<(), std::io::Error>(())
        }).await;

        match result {
            Ok(Ok(_)) => {
                println!("{}", start.elapsed().as_millis());
            }
            _ => {
                println!("2000");
            }
        }
        tokio::time::sleep(Duration::from_millis(10)).await;
    }
}
