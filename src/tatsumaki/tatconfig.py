from src import utils, config


class Tatconfig(config.Config):
    def __init__(self, path):
        super().__init__(path)

        self.replace_example()

    def populate_config(self, yaml_conf):
        """Populates a new config with user input via commandline

        :param yaml_conf: An example config to replace values of
        :return: A populated config
        """

        yaml_conf["firsttime"] = False

        print("\nNow we will set up Tatsumaki. If you would like to disable rep farming or configure it later, enter 'False' below.")
        recipient = input("However, if you would like to enable it, enter the id of the user you want to farm rep for: ")

        recipient = utils.string_to_bool(recipient)
        if not recipient:
            print("\nRep farming has been disabled.")
            yaml_conf["repfarming"] = recipient
            return yaml_conf

        recipients = []
        recipients.append(int(recipient))
        yaml_conf["recipients"] = recipients

        print("\nNow configure the interval at which rep will be farmed, called delay.")
        delay = int(input("Enter the interval in seconds: "))
        yaml_conf["delay"] = int(delay)

        print("\nFinally, configure the channel to farm rep in.")
        channel = input("Enter the id of the channel: ")
        yaml_conf["channel"] = int(channel)

        return yaml_conf
