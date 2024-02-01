import requests
import redis
from header_converter import header_conventer

r = redis.Redis()

header = header_conventer('headers.txt')

gym_area = [
    r"zoom=14&lat=51.11182&lon=71.41732&areas=c51.103021%2C71.396762%2C978.7",
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.139866%2C71.380691%2C684.0",
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.162247%2C71.404253%2C435.4",
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.131302%2C71.423648%2C923.3",
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.117567%2C71.436238%2C560.6", 
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.112665%2C71.417162%2C827.7", 
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.088064%2C71.430474%2C760.2",
    r"zoom=15&lat=51.13953&lon=71.36965&areas=c51.086363%2C71.411509%2C1569.6"
]

with requests.Session() as session:
    text = r"_txt_=%D1%81%D0%B2%D0%B5%D0%B6%D0%B8%D0%B9%20%D1%80%D0%B5%D0%BC%D0%BE%D0%BD%D1%82%20&"
    for i in range(0,len(gym_area)):   
        page = 1
        while True:
            response = session.get(r"https://krisha.kz/a/ajax-map-list/map/arenda/kvartiry/astana/?"+text+r"das[_sys.hasphoto]=1&das[live.rooms][0]=1&das[live.rooms][1]=2&das[price][to]=220000&das[who]=1&"+gym_area[i]+"&page="+str(page),
                                headers=header[r"GET /a/ajax-map-list/map/arenda/kvartiry/astana/?das[_sys.hasphoto]=1&das[live.rooms][0]=1&das[live.rooms][1]=2&das[price][to]=220000&das[who]=1&zoom=14&lat=51.11182&lon=71.41732&areas=c51.103021%2C71.396762%2C978.7&page=2"])
            
            if response.status_code == 200:
                api_data = response.json()
                if not api_data["adverts"]:
                    print("end of the apartment list. Page: "+str(page))
                    break

                for key in api_data["adverts"]:
                    r.hset(f"areaN_{i}_{key}", mapping={
                        "price": api_data['adverts'][key]['price'],
                        "rooms": api_data['adverts'][key]['rooms'],
                        "lat": api_data['adverts'][key]['map']['lat'],
                        "lon": api_data['adverts'][key]['map']['lon']
                    })

    
                print(api_data["page"])
            else:
                print("oops at "+str(page))
                break
            page+=1
        print(f"area {gym_area[i]} done\n")
