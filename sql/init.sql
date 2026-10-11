
CREATE TABLE IF NOT EXISTS sensor_readings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message_id CHAR(36) NOT NULL UNIQUE,
    sensor_id VARCHAR(50) NOT NULL,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    device_status VARCHAR(20) NOT NULL,
    measured_at DATETIME(3) NOT NULL,
    received_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    INDEX idx_sensor_time (sensor_id, measured_at),
    INDEX idx_measured_at (measured_at)
);

CREATE TABLE IF NOT EXISTS message_processing_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    message_id CHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    processed_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    INDEX idx_message_id (message_id),
    INDEX idx_processed_at (processed_at)
);
