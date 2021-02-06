try:
    import sys
    import ovh
    import requests
    import toml
except:
    print("Install: pip3 install ovh requests toml")


class OvhDynHostUpdater:

    def __init__(self, config_filename):
        self.config_filename = config_filename

    def __read_config_file(self):
        config_file = open(self.config_filename)
        entries = toml.load(config_file)
        self.domain_name = entries["domain_name"]
        self.application_key = entries["application_key"]
        self.application_secret = entries["application_secret"]
        self.consumer_key = entries["consumer_key"]

    def update_ip(self):
        try:
            self.__read_config_file()

            client = ovh.Client(
                endpoint='ovh-eu',  # Endpoint of API OVH Europe
                application_key=self.application_key,
                application_secret=self.application_secret,
                consumer_key=self.consumer_key,
            )

            service_id = client.get('/domain/zone/' + self.domain_name + '/dynHost/record', subDomain='server')[0]

            client.put('/domain/zone/' + self.domain_name + '/dynHost/record/' + str(service_id),
                       ip=OvhDynHostUpdater.get_my_ip(),
                       subDomain='server')

            client.post('/domain/zone/' + self.domain_name + '/refresh')

            print("Ip updated")
        except:
            print("Error occured, ip not updated")

    @staticmethod
    def get_my_ip():
        """Returns my public ip"""
        response = requests.get('https://api.ipify.org?format=json').text
        ip = eval(response)['ip']
        print("Retrieved ip: " + ip)
        return ip


if __name__ == '__main__':
    try:
        OvhDynHostUpdater(sys.argv[1]).update_ip()
    except:
        print("Usage: python3 ovh_dynhost_updater.py credentials.toml")
        print("Remember to first generate token in https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*")