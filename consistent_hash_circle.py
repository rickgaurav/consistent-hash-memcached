from hashlib import md5


class ConsistentHashCircle:
    """
        This class is an implementation of consistent hash algorithm.
        All the servers(Servers and their replicas) are hashed on a circle.
        On adding a key, it checks for the server with hash value just greater than
        key. And that server is used to store the key.

        If the key is greater than all servers hashes, then server with the lowest hash
        is used to store the key.
    """
    def __init__(self, server_instances=None, no_of_instance_replicas=2):

        # This is the number of replicas of a server instance on the circle(Consistent Hash Algo circle).
        # More the replicas, smaller the divisions of the circle and hence
        # more even is the distribution of keys to servers.
        self.no_of_instance_replicas = no_of_instance_replicas

        # A dict mapping server key to server instance(A representation of consistent hash algorithm circle).
        # Eg. {12: server1, 120: server2, 234: server3}
        # For Above Eg. any object with key , say 35 will be put on server3 as
        # it is the server with the next bigger key. Also any object with 234 < key <=12 will fall in server1
        self.hash_circle = {}

        # List of sorted keys representing the servers on circle.
        self._sorted_hash_circle_keys = []

        for server_instance in server_instances:
            self.add_instance_to_hash_circle(server_instance)

    def add_instance_to_hash_circle(self, server_instance):
        for i in range(0, self.no_of_instance_replicas):

            # Key representing the server on consistent hash circle
            server_key = self.get_key('{}{}{}'.format(server_instance.ip, server_instance.port, i))

            if server_key not in self.hash_circle:
                self.hash_circle[server_key] = server_instance
                self._sorted_hash_circle_keys.append(server_key)

        self._sorted_hash_circle_keys.sort()

    def remove_instance_from_circle(self, server_instance):
        """Removes `instance` and its replicas from the hash circle
        """
        for i in range(0, self.no_of_instance_replicas):
                key = self.get_key('{}{}{}'.format(server_instance.ip, server_instance.port, i))

                if key in self.hash_circle:
                    del self.hash_circle[key]
                    self._sorted_hash_circle_keys.remove(key)

    def get_key(self, server_instance_string):
        m = md5()
        m.update(server_instance_string)
        return long(m.hexdigest(), 16)

    def get_server_instance(self, object_key_string):
        """
        Returns the server instance on which object with key ,'object_key_string' is stored.
        :param object_key_string: Key for the object to be stored/retrieved
        :return: Server instance
        """

        if not self.hash_circle:
            return None

        key = self.get_key(object_key_string)

        for hash_circle_instance_key in self._sorted_hash_circle_keys:
            if key < hash_circle_instance_key:
                return self.hash_circle[hash_circle_instance_key]

        return self.hash_circle[self._sorted_hash_circle_keys[0]]