import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
#loc1 = "Santiago, Chile"
#loc2 = "La Serena, Chile"
key = "6728ef28-aa91-4ec7-b7af-bf56bee45cb1"
def geocoding (location, key):
    while location == "":
        location = input("Escriba una ciudad : ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    #print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200 and len(json_data["hits"]) !=0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:

            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Estado de API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status,lat,lng,new_loc
    

while True:
    loc1 = input("Ciudad de Origen: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    print(orig)
    loc2 = input("Ciudad de Destino: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Viaje desde " + orig[3] + " hacia " + dest[3])
        print("=================================================")
        if paths_status == 200:
            distancia = paths_data["paths"][0]["distance"] / 1000
            print(f"Distancia de viaje: {distancia:.2f} km") #el .2f es pa los 2 decimale
            duracion_ms = paths_data["paths"][0]["time"]  # Tiempo en milisegundos
            duracion_segundos = duracion_ms / 1000 #es en 1k xq son 1k ms en 1 seg
            seg = int(duracion_segundos% 60)
            minu = int((duracion_segundos % 3600) // 60)
            hora = int(duracion_segundos // 3600)
            print(f"Duración del viaje: {hora}h {minu}m {seg}s")
            distancia_km = paths_data["paths"][0]["distance"] / 1000
            km_por_litro = 10  # 10km x 1 litro
            combustible = distancia_km / km_por_litro
            print(f"Combustible requerido: {combustible:.2f} litros")
            print("=================================================")
        for each in range(len(paths_data["paths"][0]["instructions"])):
            path = paths_data["paths"][0]["instructions"][each]["text"]
            distance = paths_data["paths"][0]["instructions"][each]["distance"]
            print("{0} ( {1:.2f} km )".format(path, distance/1000))
            print("=============================================")



