import unittest
import warnings
import time
import docker_runner
import os
import subprocess

import warnings

warnings.simplefilter("ignore", ResourceWarning)

class initTest(unittest.TestCase):
    def setUp(self):
        self.wargame = docker_runner.WarGame()

    def tearDown(self):
        self.wargame.stop_server()

    def test_module(self):
        """
        Wargame 객체에 docker가 로드되어 있는지 확인한다.
        """
        self.assertTrue(self.wargame.check_for_init())

    def test_run_server(self):
        self.wargame.run_server()
        time.sleep(5)
        self.assertNotEqual(len(self.wargame.list_containers()), 0)        

    def test_stop_server(self):
        self.wargame.stop_server()
        time.sleep(5)
        self.assertEqual(len(self.wargame.list_containers()), 0)

class networkTest(unittest.TestCase):
    def setUp(self):
        self.wargame = docker_runner.WarGame(images=["node_echo_server","node_echo_server"])
        self.container_list = self.wargame.run_server()
        self.network_list = self.wargame.create_network()

    def tearDown(self):
        try:
            for network in self.network_list:
                for container in self.container_list:
                    network.disconnect(container)
        except Exception as e:
            print(e)

        self.wargame.remove_network()
        self.wargame.stop_server()


    def test_creation(self):
        self.assertNotEqual(len(self.network_list),0)
        self.assertNotEqual(len(self.container_list),0)

    def test_connect(self):
        network = self.network_list[0]
        self.wargame.connect_container(network, self.container_list[0])
        self.assertTrue(len(network.containers), 1)
        self.wargame.connect_container(network, self.container_list[1])
        self.assertTrue(len(network.containers), 2)
    
class connectionTest(unittest.TestCase):
    def setUp(self):
        self.wargame = docker_runner.WarGame(images=["node_echo_server","node_echo_server"])
        self.container_list = self.wargame.run_server()
        self.network_list = self.wargame.create_network()
        self.wargame.connect_container(self.network_list[0], self.container_list[0])
        self.wargame.connect_container(self.network_list[0], self.container_list[1])
    

    def tearDown(self):
        try:
            for network in self.network_list:
                for container in self.container_list:
                    network.disconnect(container)
        except Exception as e:
            print(e)

        self.wargame.remove_network()
        self.wargame.stop_server()

    def test_connected(self):
        """
        Container[0] Domainname : server0
        Container[1] Domainname : server1
        """

        result = self.container_list[0].exec_run('ping server1 -c 1')
        self.assertTrue(b"received" in result.output) # ping statisitics
        result = self.container_list[1].exec_run('ping server0 -c 1')
        self.assertTrue(b"received" in result.output)

    
    def test_message(self):
        """
        Container[0] Domainname : server0
        Container[1] Domainname : server1
        """

        result = self.container_list[0].exec_run('curl http://server1:5000/hello')
        self.assertTrue(b'"status": 200' in result.output) # status OK
        result = self.container_list[1].exec_run('curl http://server0:5000/hello')
        self.assertTrue(b'"status": 200' in result.output)

class snortTest(unittest.TestCase):
    def setUp(self):
        try:
            self.wargame = docker_runner.WarGame(images=["node_echo_server"])
            self.container_list = self.wargame.run_server()
            self.network_list = self.wargame.create_network()
            
            self.ids = self.wargame.run_snort(self.network_list[0].name)
            self.wargame.connect_container(self.network_list[0], self.container_list[0])
        except Exception as e:
            print(e)
    
    def tearDown(self):
        try:
            for network in self.network_list:
                for container in self.container_list:
                    network.disconnect(container)
        except Exception as e:
            print(e)

        self.wargame.remove_network()
        self.wargame.stop_server()

    def test_connected(self):
        print(self.ids.status)
        self.ids.logs(stream=True)
        self.assertGreaterEqual(len(self.network_list[0].containers), 2)
        result = self.container_list[0].exec_run('ping snort -c 1')
        self.assertTrue(b"received" in result.output) # ping statisitics
        print(result)
        result = self.ids.exec_run('ping server0 -c 1')
        self.assertTrue(b"received" in result.output)
        print(result)
        self.ids.attach()
    
if __name__ == '__main__':
    unittest.main()
    