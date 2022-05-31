import asyncio
from socketio import client

# !!! IMPORTANT: websocket-client has to be installed -> pip install websocket-client or see requirements.txt
from VehicleActionEnum import VehicleAction

endpoint_local = "http://localhost:5000"
endpoint_productive = "https://flask-pren.herokuapp.com/"
sio = client.Client()


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    stop_timer()
    print("I'm disconnected!")


@sio.event
def status_request():
    status_update("online")


@sio.event
def change_speed_client(data):
    speed_changed_frontend(data)


def speed_changed_frontend(data):
    action = None
    if data > 95:
        action = VehicleAction.FULL_SPEED
    elif data > 85:
        action = VehicleAction.NINETY_PERCENT
    elif data > 75:
        action = VehicleAction.EIGHTY_PERCENT
    elif data > 65:
        action = VehicleAction.SEVENTY_PERCENT
    elif data > 55:
        action = VehicleAction.SIXTY_PERCENT
    elif data > 45:
        action = VehicleAction.HALF_SPEED
    elif data > 35:
        action = VehicleAction.FOURTY_PERCENT
    elif data > 25:
        action = VehicleAction.THIRTY_PERCENT
    elif data > 15:
        action = VehicleAction.TWENTY_PERCENT
    elif data > 5:
        action = VehicleAction.TEN_PERCENT
    else:
        action = VehicleAction.STOP


async def sendEvent(event_type, message):
    data = {
        "name": event_type,
        "message": message
    }
    print(f"sending event to Server: {message}")
    sio.emit(event='event', data=data)


def event_to_server(event_type, message):
    # give event_type a meaningful string, it will be displayed on frontend
    asyncio.run(sendEvent(event_type, message))


def update_sensor_data(sensor_type, message):
    # possible sensor types:
    # speed, voltage_print, coils, acceleration, voltage_motor
    # Message formats:
    # speed: float
    # voltage_print: float
    # coils:
    # [
    #   {
    #       "nr_coil": 1
    #       "value": float
    #   },
    #   {
    #       "nr_coil": 2
    #       "value": float
    #   },
    #   {
    #       "nr_coil": 3
    #       "value": float
    #   },
    #   {
    #       "nr_coil": 4
    #       "value": float
    #   },
    # ]
    # acceleration:
    # [
    #   {
    #       "axis": "x",
    #       "value": float,
    #   },{
    #       "axis": "y",
    #       "value": float,
    #   },{
    #       "axis": "z",
    #       "value": float,
    #   }
    # ]
    # voltage_motor: float
    # plant_data:
    #   {
    #     "position" : string
    #     "genus" : string
    #     "family" : string
    #     "scientificName" : string
    #     "commonNames" : [string]
    #   }

    asyncio.run(sendUpdate(sensor_type, message))
    # sendUpdate(sensor_type, message)


async def sendUpdate(sensor_type, message):
    data = {
        "name": sensor_type,
        "message": message
    }
    print(f"Updating sensor data type: {sensor_type} Data: {message}")
    sio.emit(event='sensor_update', data=data)


def status_update(status):
    asyncio.run(sendStatus(status))


async def sendStatus(status):
    data = {
        "name": "StatusInfo",
        "status": status
    }
    sio.emit('statusInfo', {"data": data})


def start_timer():
    sio.emit('start_timer')


def stop_timer():
    sio.emit('stop_timer')


def start_client_local():
    sio.connect(endpoint_local, transports=['websocket'])


def start_client_productive():
    sio.connect(endpoint_productive, transports=['websocket'])


def stop_client():
    sio.disconnect()
