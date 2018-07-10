import unittest
import docker
import warnings
import time

warnings.simplefilter("ignore", ResourceWarning)

class TestRunDocker(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()

    def test_run(self):
        self.assertNotEqual(self.client, None)
        print(self.client.containers.run("hello-world"))
    
    def test_list_containers(self):
        self.assertEqual(self.client.containers.list(), [])
        
        container = self.client.containers.run("bfirsh/reticulate-splines", detach="True")
        time.sleep(5)
        self.assertNotEqual(self.client.containers.list(), [])

        container.stop()
        time.sleep(5)
        self.assertEqual(self.client.containers.list(), [])
    
    def test_list_images(self):
        self.assertNotEqual(self.client.images.list(), None)
    
    def test_run_background(self):
        container = self.client.containers.run("bfirsh/reticulate-splines", detach="True")
        self.assertNotEqual(container, None)
        self.assertEqual(container.attrs['Config']['Image'], "bfirsh/reticulate-splines")
        self.assertEqual(container.logs(), b'Reticulating spline 1...\n')
        container.stop()
    
    def test_log(self):
        '''Check Logs on Live:
        for line in container.logs(stream=True):
            print(line.strip())
        '''
        container = self.client.containers.run("bfirsh/reticulate-splines", detach="True")
        self.assertEqual(container.logs(),b'Reticulating spline 1...\n')
        container.stop()

class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()
        self.ubuntu1 = self.client.containers.run("ubuntu",detach="True")
        self.ubuntu2 = self.client.containers.run("ubuntu",detach="True")
    
    def test_create_network(self):
        self.network = self.client.networks.create("network1", driver="bridge")
        self.assertEqual(0, len(self.network.containers))

        self.assertNotEqual(self.network, None)
        self.network.connect(self.ubuntu1)
        self.network.connect(self.ubuntu2)
        self.assertEqual(2, len(self.network.containers))

        self.network.disconnect(self.ubuntu1)
        self.network.disconnect(self.ubuntu2)
        self.assertEqual(0, len(self.network.containers))

    def tearDown(self):
        if(self.ubuntu1 is not None):
            self.ubuntu1.stop()
        if(self.ubuntu2 is not None):
            self.ubuntu2.stop()
        if(self.network is not None):
            self.network.remove()
        time.sleep(5)
        self.assertEqual(self.ubuntu1, None)
        self.assertEqual(self.ubuntu2, None)
        self.assertEqual(self.network, None)

if __name__ == '__main__':
    unittest.main()