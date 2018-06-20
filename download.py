import gdax, time, threading

# Author: Jeff Xiang

# Get the most updated order book in .csv form.
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


# Downloads the specified number of .csv files of the order book and saves as FILENAME.
def download_csv(filename, num_files=10):
    total_start_time = time.time()
    curr_file = 0
    order_book = gdax.OrderBook(product_id="BTC-USD")
    order_book.start()
    while curr_file < num_files:
        file_dir = "/Users/Jeff/Desktop/Novumind/test_csv/" + filename + str(curr_file) + ".csv"
        csv = open(file_dir, "w")
        csv.truncate(0)

        t1 = time.time()
        while True:
            book = order_book.get_current_book()
            book_timestamp = time.time()
            if len(book["asks"]) > 0 and len(book["bids"]) > 0:
                break
        if curr_file == 0:
            print("Time taken to obtain non-null order book: " + str(time.time() - t1))
        csv.write("side, price, size, timestamp of order book: " + str(book_timestamp) + "\n")
        t2 = time.time()
        write_helper("asks", book, csv)
        write_helper("bids", book, csv)
        csv.close()
        write_time = time.time() - t2
        print("Time taken to read order book & write file " + str(curr_file) + ": " + str(write_time))
        curr_file += 1
        time.sleep(float(1 - write_time))
    print("Time taken to write " + str(num_files) + " files: " + str(time.time() - total_start_time))

# Helper function that writes the top NUM_DISPLAY orders on specified SIDE to CSV based on given BOOK.
def write_helper(side, book, csv, num_display=200):
    is_asks = side is "asks"
    list = book[side]
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

def download_csv2(filename, num_display=200, num_files=10):
    total_start_time = time.time()
    curr_file = 0
    order_book = gdax.OrderBook(product_id="BTC-USD")
    order_book.start()

    threading.Timer(1, get_order_book())

def get_order_book():
    order_book = gdax.OrderBook(product_id="BTC-USD")
    while True:
        book = order_book.get_current_book()
        book_timestamp = time.time()
        if len(book["asks"]) > 0 and len(book["bids"]) > 0:
            break
    csv.write("side, price, size, timestamp of order book: " + str(book_timestamp) + "\n")
    t2 = time.time()
    write_helper("asks", book)
    write_helper("bids", book)
    csv.close()