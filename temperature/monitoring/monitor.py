import argparse
import re

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from qibolab.instruments.bluefors import TemperatureController


def monitor_temperature(device_name: str, device_ip: str, device_port: int):
    registry = CollectorRegistry()
    flanges = [
        "_50K_flange",
        "_4K_flange",
        "_Still_flange",
        "_MXC_flange",
    ]
    temperatures = {}
    for flange in flanges:
        temperatures[flange] = Gauge(
            flange, f"Temperature of {flange}", registry=registry
        )

    tc = TemperatureController(device_name, device_ip, device_port)
    tc.connect()
    temperature_values = tc.read_data()
    for temperature_value in temperature_values:
        for key, value in temperature_value.items():
            flange = re.sub("-", "_", key)
            temperatures[f"_{flange}"].set(value["temperature"])
        push_to_gateway("pushgateway:9091", job="pushgateway", registry=registry)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="")
    parser.add_argument("--ip", type=str, default=None)
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    monitor_temperature(args.name, args.ip, args.port)


if __name__ == "__main__":
    main()
