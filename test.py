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
        assertNotEqual(self.client.containers.list(), [])

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
        container = self.client.containers.run("bfirsh/reticulate-splines", detach="True")
        for line in container.logs(stream=True):
            print(line.strip())
        container.stop()


if __name__ == '__main__':
    unittest.main()