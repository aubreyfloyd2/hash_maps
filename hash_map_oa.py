# Name: Aubrey Floyd
# Course: CS261 - Data Structures
# Description: Implementation of a HashMap class making use of a dynamic array to store a hash
#              table with open addressing with quadratic probing for collision resolution.
#              Class includes methods: put, get, remove, contains_key, clear, empty_buckets,
#              resize_table, table_load, get_keys_and_values, __iter__, and __next__.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

        # check if load factor is >= to 0.5, resize double if needed
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # find index for key/value pair to be put, index = hash % array_size
        index = self._hash_function(key) % self._capacity

        # initialize for quadratic probing, i = initial + p^2
        initial_index = index
        probing = 1

        # if key exists replace value, else probe to find open slot or tombstone
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                self._buckets[index] = HashEntry(key, value)
                return
            if self._buckets[index].is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            index = (initial_index + probing * probing) % self._capacity
            probing += 1

        # no existing key or tombstone, put new key value pair
        self._buckets[index] = HashEntry(key, value)
        self._size += 1


    def table_load(self) -> float:
        """
        Finds current hash table load factor. O(1) average time complexity.
        No parameters.
        :return: float value of load factor
        """

        # load factor = # of elements in table / # of buckets
        return self._size / self._capacity


    def empty_buckets(self) -> int:
        """
        Finds number of empty buckets in hash table.
        No parameters.
        :return: integer values of number of empty buckets
        """

        # initialize count of empty buckets to return
        count = 0

        # iterate over dynamic array and count empty buckets
        for bucket in range(self._capacity):
            if self._buckets[bucket] is None:
                count += 1
        return count


    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of internal hash table while maintaining key/value pairs in hash map.
        :param new_capacity: new capacity size of hash table
        :return: none
        """

        # check if new capacity is less than current number of elements
        if new_capacity <= self._size:
            return

        # make sure new capacity is prime and load factor is less than 0.5
        while not (self._is_prime(new_capacity) and (self._size / new_capacity <= 0.5)):
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
            if not self._size / new_capacity <= 0.5:
                new_capacity *= 2

        # create temporary hash map
        temp = HashMap(new_capacity, self._hash_function)

        # iterate over, find new index, and put in hash map
        for i in range(self._buckets.length()):
            element = self._buckets.get_at_index(i)
            if element is not None and not element.is_tombstone:
                index = self._hash_function(element.key) % new_capacity
                initial_index = index
                probing = 1

                while temp._buckets[index] is not None:
                    index = (initial_index + probing * probing) % new_capacity
                    probing += 1

                temp._buckets[index] = HashEntry(element.key, element.value)

        # update internal hash map
        self._buckets = temp._buckets
        self._capacity = new_capacity


    def get(self, key: str) -> object:
        """
        Gets value associated with given key, or None if key doesn't exist.
        O(1) average time complexity.
        :param key: key to get value from
        :return: value at key
        """

        # find index and set up for probing
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probing = 1

        while self._buckets[index] is not None:
            element = self._buckets.get_at_index(index)
            if not element.is_tombstone and element.key == key:
                return element.value
            index = (initial_index + probing * probing) % self._capacity
            probing += 1

        # if key not in hash map, returns None
        return None


    def contains_key(self, key: str) -> bool:
        """
        Checks if given key is in hash map. O(1) average time complexity.
        :param key: key to check for in hash map
        :return: bool value, True if exists otherwise False
        """

        # find index and set up for probing
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probing = 1

        while self._buckets.get_at_index(index) is not None:
            element = self._buckets.get_at_index(index)
            if not element.is_tombstone and element.key == key:
                return True
            index = (initial_index + probing * probing) % self._capacity
            probing += 1

        # if key not in hash map, returns False
        return False


    def remove(self, key: str) -> None:
        """
        Removes given key and value from hash map. O(1) average time complexity.
        :param key: key for key/value pair to be removed
        :return: none
        """

        # find index and set up for probing
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probing = 1

        # find slot or probe until found, set to tombstone
        while self._buckets.get_at_index(index) is not None:
            element = self._buckets.get_at_index(index)
            if not element.is_tombstone and element.key == key:
                element.is_tombstone = True
                self._size -= 1
                return
            index = (initial_index + probing * probing) % self._capacity
            probing += 1


    def clear(self) -> None:
        """
        Clears contents of the hash map without changing underlying hash table capacity.
        No parameters.
        :return: none
        """

        # clear buckets and size
        new_buckets = DynamicArray()
        for _ in range(self._capacity):
            new_buckets.append(None)

        self._buckets = new_buckets
        self._size = 0


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
            element = self._buckets.get_at_index(i)
            if element is not None and not element.is_tombstone:
                keys_values.append((element.key, element.value))
        return keys_values


    def __iter__(self):
        """
        Creates an iterator to iterate across the hash map.
        :return: none
        """

        self._curr_index = 0
        return self
    

    def __next__(self):
        """
        Obtains the next item in the hash map based on current location of the iterator.
        :return: next time in the hash map
        """
        
        while self._curr_index < self._buckets.length():
            element = self._buckets.get_at_index(self._curr_index)
            self._curr_index += 1

            # only iterates over active items
            if element is not None and not element.is_tombstone:
                return element

        raise StopIteration


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
