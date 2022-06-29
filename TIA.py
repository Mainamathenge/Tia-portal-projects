from opcua import Client, ua
import requests
import time
import json


def read_input_value(node_id, client):
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    print("READ Value of : " + str(client_node) + " : " + str(client_node_value))
    return client_node_value


def write_value_bool(node_id, value, client):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))


def write_value_int(node_id, value, client):
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))


def get_firebase_state(ndp):
    endpoint = "https://tiatounity-default-rtdb.firebaseio.com/" + ndp
    resp = json.loads(requests.get(endpoint).text)
    return resp


def put_firebase_state(json_inp, ndp):
    endpoint = "https://tiatounity-default-rtdb.firebaseio.com/" + ndp
    json.loads(requests.patch(endpoint, json=json_inp).text)
    print('Inserted data successfully')



url1 = "opc.tcp://192.168.0.1:4840"
client1 = Client(url1)
client1.connect()
root1 = client1.get_root_node()
print("Object root node is: ", root1)

print('\n\nConnection Successful\n\n......WAIT FOR SERVER INITIALIZATION.......\n\n')
while True :
    # writtiing to fire-base
    start = read_input_value('ns=3;s="OPCUA TEST BLOCK"."Start"',client1)
    Green = read_input_value('ns=3;s="OPCUA TEST BLOCK"."green"',client1)
    level = read_input_value('ns=3;s="OPCUA TEST BLOCK"."tank"',client1)
    put_firebase_state({"start": "true" if start  else "false" ,
                        "green":"true" if Green else "false0",
                        "Tanklevel":level},'.json' )
    # getting data from-firebase
    data = get_firebase_state('/green.json')
    to = True if data == "true" else False
    data = get_firebase_state('/green.json')
    to = True if data == "true" else False

    print(data)
    write_value_bool('ns=3;s="OPCUA TEST BLOCK"."stop"',to,client1)

    #print(start)
    time.sleep(5)


