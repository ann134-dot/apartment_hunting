from pprint import pprint

def header_conventer(file):
    dict_header = {}
    with open(file, 'r') as read:
        is_end = True
        curr_header = ''
        for line in read.readlines():
            line = line.strip()
            if line.startswith('POST') or line.startswith('GET'):
                dict_header[line] = {}
                curr_header = line
                is_end = False
            elif not line:
                is_end = True
            elif not is_end:
                x = line.split(':', 1)
                # if x[0] == 'Cookie':
                #     continue
                try:
                    dict_header[curr_header][x[0]] = x[1].strip()
                except:
                    print(x[0])
    return dict_header


# d = header_conventer('headers.txt')
# # pprint(d)

# print(d['GET /a/ajax-map-list/map/arenda/kvartiry/astana/?das[_sys.hasphoto]=1&das[live.rooms][0]=1&das[live.rooms][1]=2&das[price][to]=220000&das[who]=1&zoom=14&lat=51.11182&lon=71.41732&areas=c51.103021%2C71.396762%2C978.7&page=2']['User-Agent'])