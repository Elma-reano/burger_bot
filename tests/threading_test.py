import threading
import keyboard
import time


def threading_test_1():
    def process_1():
        for i in range(5):
            print(f"Process 1 - iteration {i}")
            time.sleep(1)

    def process_2():
        for j in range(6):
            print(f"Process 2 - iteration {j}")
            time.sleep(1.5)
    t1 = threading.Thread(target=process_1)
    t2 = threading.Thread(target=process_2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

def threading_test_2():

    number = 0
    stop = False

    def monitor_keyboard():
        print("Keyboard monitoring. Press 'x' to quit or 'a' to add 5 to the number.")
        nonlocal number
        nonlocal stop
        while True:
            if keyboard.is_pressed('x'):
                print("Detected 'x' key press. Exiting...")
                stop = True
                break
            elif keyboard.is_pressed('a'):
                number += 5
                print("Added 5 to the number.")
                # Debounce to avoid multiple increments
                while keyboard.is_pressed('a'):
                    time.sleep(0.15)
            time.sleep(0.1)
    
    def add_number():
        nonlocal number
        nonlocal stop
        print("Main thread is running.")
        while not stop:
            print(f"The number is: {number}")
            time.sleep(2)
            number += 1

    keyboard_thread = threading.Thread(target=monitor_keyboard)
    keyboard_thread.start()

    number_thread = threading.Thread(target=add_number)
    number_thread.start()

    keyboard_thread.join()
    #kill the number thread
    print("Main thread is exiting.")
    number_thread.join()

def threading_test_3():
    queue = []
    stop = False

    def producer():
        nonlocal queue
        nonlocal stop
        number = 1

        while not stop:
            if keyboard.is_pressed('a'):
                queue.append(number)
                number += 1
                print("Added an element to the queue")
                time.sleep(0.1)
            time.sleep(0.01)
    
    def consumer():
        nonlocal queue
        nonlocal stop

        while queue:
            item = queue.pop(0)
            print(f"Consumed item: {item}")
            time.sleep(1)
        stop = True

    queue += [1, 2, 3, 4, 5]
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()


if __name__ == "__main__":
    # threading_test_1()
    # threading_test_2()
    threading_test_3()