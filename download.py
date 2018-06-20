import gdax, requests, time
from websocket import create_connection

# Get the most updated order book in .csv form
def write_csv(level):
    write_dir = "/Users/Jeff/Desktop/Novumind/ob_data_level3.csv"
    csv = open(write_dir, "w")
    csv.truncate(0)

    public_client = gdax.PublicClient()
    ob_data_level2 = public_client.get_product_order_book('BTC-USD', level=level)

    # Helper that writes either asks or bids
    def write_helper(param):
        list = ob_data_level2.get(param)

        if level == 1 or level == 2:
            label = "num_orders"
        else:
            label = "order_id"

        csv.write("price, size, " + label + "\n")

        for i in range(len(list)):
            item = list[i]
            price = item[0]
            size = item[1]
            num_orders = item[2]
            row = str(price) + "," + str(size) + "," + str(num_orders) + "," + "\n"
            csv.write(row)

    write_helper('asks')
    write_helper('bids')
    csv.close()

def download_csv(filename, num_display=200, num_files=5):
    curr_file = 0
    order_book = gdax.OrderBook(product_id='BTC-USD')
    order_book.start()
    while curr_file < num_files:
        file_dir = "/Users/Jeff/Desktop/Novumind/test_csv/" + filename + str(curr_file) + ".csv"
        csv = open(file_dir, "w")
        csv.truncate(0)

        def write_helper(side, max_time=10):
            is_asks = side is "asks"
            t = time.clock()
            while time.clock() - t < max_time:
                book = order_book.get_current_book()
                list = book[side]
                if len(list) > 0:
                    list_length = len(list)
                    curr_index = list_length - 1
                    if is_asks:
                        curr_index = 0
                    order_index = 0
                    while (curr_index >= list_length - num_display and side is "bids") or (curr_index < num_display and side is "asks"):
                        price = str(list[curr_index][0])
                        size = str(list[curr_index][1])
                        row = side + str(order_index) + "," + price + "," + size + "\n"
                        csv.write(row)
                        if is_asks:
                            curr_index += 1
                        else:
                            curr_index -=1
                        order_index += 1
                    break

        csv.write("side, price, size,\n")
        write_helper("asks")
        write_helper("bids")
        csv.close()
        curr_file += 1


def download_csv2(filename, num_display=200, num_files=10):
    curr_file = 0
    order_book = gdax.OrderBook(product_id='BTC-USD')
    order_book.start()
    while curr_file < num_files:
        file_dir = "/Users/Jeff/Desktop/Novumind/test_csv/" + filename + str(curr_file) + ".csv"
        csv = open(file_dir, "w")
        csv.truncate(0)

        def write_helper(side, max_time=10):
            is_asks = side is "asks"
            t = time.clock()
            while time.clock() - t < max_time:
                book = order_book.get_current_book()
                list = book[side]
                if len(list) > 0:
                    list_length = len(list)
                    curr_index = list_length - 1
                    if is_asks:
                        curr_index = 0
                    order_index = 0
                    while (curr_index >= list_length - num_display and side is "bids") or (curr_index < num_display and side is "asks"):
                        price = str(list[curr_index][0])
                        size = str(list[curr_index][1])
                        row = side + str(order_index) + "," + price + "," + size + "\n"
                        csv.write(row)
                        if is_asks:
                            curr_index += 1
                        else:
                            curr_index -=1
                        order_index += 1
                    break

        csv.write("side, price, size,\n")
        write_helper("asks")
        write_helper("bids")
        csv.close()
        curr_file += 1
        time.sleep(1)


def print_orders(side, max_time=10, num_display=200):
    order_book = gdax.OrderBook(product_id='BTC-USD')
    order_book.start()
    t = time.clock()
    print(side + ": ")
    while time.clock() - t < max_time:
        book = order_book.get_current_book()
        list = book[side]
        if len(list) > 0:
            list_length = len(list)
            curr_index = list_length - 1
            order_index = 0
            if side is "asks":
                curr_index = 0
            while (curr_index >= list_length - num_display and side is "bids") or (curr_index < num_display and side is "asks"):
                print(str(order_index) + ": " + str(list[curr_index][0]) + ", " + str(list[curr_index][1]))
                if side is "bids":
                    curr_index -= 1
                else:
                    curr_index += 1
                order_index += 1
            break
    order_book.close()