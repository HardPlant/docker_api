import unittest
import warnings
import time
import docker_runner

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


if __name__ == '__main__':
    unittest.main()
    