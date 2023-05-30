---

# ud-co2s Exporter

The `ud-co2s Exporter` is a Prometheus Exporter that reads data from the ud-co2s CO2 sensor and exposes the CO2 concentration as a Prometheus metric.

## Prerequisites

Before running the Exporter, make sure you have the following prerequisites installed:

- Python 3.x
- `prometheus_client` library (`pip install prometheus_client`)
- `pyserial` library (`pip install pyserial`)
- ud-co2s CO2 sensor connected to the computer via a serial port

## Usage

1. Connect the ud-co2s CO2 sensor to your computer via a serial port.

2. Install the required Python libraries by running the following command:

    ```bash
    pip install prometheus_client pyserial
    ```

3. Start the Exporter by running the following command:

    ```bash
    python exporter.py <serial_port>
    ```

4. The Exporter will start a web server on port 8000 and begin scraping data from the ud-co2s sensor.

5. Access the Exporter's metrics at the following URL:

- [http://localhost:8000/metrics](http://localhost:8000/metrics)

6. Configure Prometheus to scrape the Exporter's metrics by adding the following job configuration to your `prometheus.yml` file:

    ```yaml
    scrape_configs:
    - job_name: ud-co2s
        static_configs:
        - targets: ['localhost:8000']
    ```

7. Restart Prometheus to start scraping metrics from the ud-co2s Exporter.
8. You can now query the following metrics in Prometheus and create visualizations or set up alerts based on the sensor readings:

- co2_ppm: Current CO2 concentration in parts per million (PPM) measured by the ud-co2s sensor.
- temperature_celsius: Current temperature in Celsius measured by the ud-co2s sensor.
- humidity_percentage: Current relative humidity in percentage measured by the ud-co2s sensor.
