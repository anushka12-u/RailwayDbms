import os

import requests


API_BASE_URL = os.getenv("RAILWAY_API_URL", "http://127.0.0.1:8000").rstrip("/")


class ApiError(Exception):
    pass


def request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            API_BASE_URL + path,
            timeout=10,
            **kwargs,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Cannot connect to the API: {exc}") from exc

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise ApiError(f"{response.status_code}: {detail}")

    if not response.content:
        return None
    return response.json()


def get(path, params=None):
    return request("GET", path, params=params)


def post(path, payload):
    return request("POST", path, json=payload)


def put(path, payload):
    return request("PUT", path, json=payload)


def delete(path):
    return request("DELETE", path)


def trains():
    return get("/trains/") or []


def passengers():
    return get("/passengers/") or []


def bookings():
    return get("/bookings/") or []
