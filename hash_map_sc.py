# Name: Aubrey Floyd
# Course: CS261 - Data Structures
# Description: Implementation of a HashMap class making use of a dynamic array to store a hash
#              table with chaining for collision resolution using a single linked list.
#              Class includes methods: put, get, remove, contains_key, clear, empty_buckets,
#              resize_table, table_load, get_keys_and_values, and an additional separate find_mode method.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map. Resizes table if needed. O(1) average time complexity.
        :param key: key to be added
        :param value: value to be added
        :return: none
        """

        # check if load factor is >= to 1.0, resize double if needed
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # find index for key/value pair to be put, index = hash % array_size
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        # check if key exists in linked list; replace or add
        node = linked_list.contains(key)
        if node:
            node.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1


    def empty_buckets(self) -> int:
        """
        Finds number of empty buckets in hash table.
        No parameters.
        :return: integer values of number of empty buckets
        """

        # initialize count of empty buckets to return
        count = 0

        # iterate over dynamic array and count empty linked lists
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count


    def table_load(self) -> float:
        """
        Finds current hash table load factor. O(1) average time complexity.
        No parameters.
        :return: float value of load factor
        """

        # load factor = # of elements in table / # of buckets
        return self._size / self._capacity


    def clear(self) -> None:
        """
        Clears contents of the hash map without changing underlying hash table capacity.
        No parameters.
        :return: none
        """

        # clear buckets, linked list, and size
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of internal hash table while maintaining key/value pairs in hash map.
        :param new_capacity: new capacity size of hash table
        :return: none
        """

        # check that new capacity is not less than 1
        if new_capacity < 1:
            return

        # make sure new capacity is prime and load factor is less than 1
        while not (self._is_prime(new_capacity) and (self._size / new_capacity <= 1)):
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            if not self._size / new_capacity <= 1:
                new_capacity *= 2

        # create new dynamic array of linked lists with new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # rehash all key/value pairs in hash map to new buckets
        for i in range(self._capacity):
            for node in self._buckets[i]:
                new_index = self._hash_function(node.key) % new_capacity
                new_linked_list = new_buckets[new_index]
                new_linked_list.insert(node.key, node.value)

        # update capacity and buckets after resized
        self._capacity = new_capacity
        self._buckets = new_buckets


    def get(self, key: str):
        """
        Gets value associated with given key, or None if key doesn't exist.
        O(1) average time complexity.
        :param key: key to get value from
        :return: value at key
        """

        # find index for key/value pair
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)
        if node:
            return node.value

        # if key not in hash map, returns None
        return None


    def contains_key(self, key: str) -> bool:
        """
        Checks if given key is in hash map.  O(1) average time complexity.
        :param key: key to check for in hash map
        :return: bool value, True if exists otherwise False
        """

        # checks if key in is hash map, else returns False
        # empty hash map does not contain any keys
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        if not linked_list.contains(key):
            return False
        return True


    def remove(self, key: str) -> None:
        """
        Removes given key and value from hash map.  O(1) average time complexity.
        :param key: key for key/value pair to be removed
        :return: none
        """

        # find index of key/value pair and remove
        # if key not in hash map, method does nothing
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        if self.contains_key(key):
            linked_list.remove(key)
            self._size -= 1
        return


    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates a dynamic array where each index contains a tuple key/value pair stores in the
        hasp map.
        No parameters.
        :return: Dynamic Array with tuples
        """

        # initialize dynamic array, order of the keys does not matter
        keys_values = DynamicArray()

        # add each key/value tuple to array
        for i in range(self._capacity):
            for node in self._buckets[i]:
                keys_values.append((node.key, node.value))
        return keys_values


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds mode value(s) and highest frequency of given dynamic array value(s).
    O(N) average time complexity.
    :param da: dynamic array, unsorted or sorted
    :return: tuple containing dynamic array of mode value(s) and highest frequency integer for mode value(s)
    """

    # create separate chaining HashMap to store mode frequencies
    map = HashMap()

    # find frequencies and find mode frequency
    mode_freq = 0
    for i in range(da.length()):
        value = da.get_at_index(i)
        if map.contains_key(value):
            freq = map.get(value)
            freq += 1
            map.put(value, freq)
        else:
            map.put(value, 1)
            freq = 1

        if freq > mode_freq:
            mode_freq = freq

    # find mode values with the max mode frequency
    mode_values = DynamicArray()
    keys_freq = map.get_keys_and_values()
    for i in range(keys_freq.length()):
        key, freq = keys_freq.get_at_index(i)
        if freq == mode_freq:
            mode_values.append(key)

    # return tuple with dynamic array of mode value(s), highest frequency integer
    return mode_values, mode_freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
