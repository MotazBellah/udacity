import httplib2
import json

def test():

    x = "https://catalog-api.udacity.com/v1/degrees"

    h = httplib2.Http()
    y = json.loads(h.request(x, 'GET')[1])
    # for k, v in enumerate(y['degrees']):
    #     print(k)
    #     print('================================')
    #     print(v)
    # y['degrees']
    g = []
    z = {}
    for i in y['degrees']:
        print(i['title'])
        print(i['key'])
        z[i['title']] = [i['card_image'], i['key']]
        # print(i['image'])
        print(i['card_image'])
        if i['available'] and i['open_for_enrollment']:
            g.append(i['title'])

    print('================')
    print(g)
    print(z)

    # print(y['degrees'][0]['title'])





if __name__ == '__main__':
    test()
